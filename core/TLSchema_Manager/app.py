import re
from typing import List, Dict, Any, Set

TDLIB_VERSION = "1.8.63"
OFFICIAL_URL = "https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/td_api.tl"

import os
SCHEMA_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = os.path.join(SCHEMA_DIR, "td_api.tl.txt")

# Python reserved builtins that cannot be used as class names
PYTHON_BUILTINS_RESERVED = {
    "bytes", "dict", "list", "tuple", "set", "frozenset", "str", "int", "float",
    "bool", "object", "type", "property", "classmethod", "staticmethod",
    "super", "Exception", "BaseException", "ValueError", "TypeError", "KeyError",
    "IndexError", "AttributeError", "NameError", "RuntimeError", "NotImplementedError"
}

# ===================== Utils =====================
def to_snake_case(name: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def map_type(td_type: str) -> str:
    base = {
        "string": "str",
        "int32": "int",
        "int53": "int",
        "int64": "int",
        "double": "float",
        "bytes": "bytes",
        "Bool": "bool",
    }

    if td_type.startswith("vector<"):
        inner = td_type[7:-1]
        return f"List[{map_type(inner)}]"

    return base.get(td_type, td_type)


# ===================== Schema =====================

def read_schema() -> str:
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        return f.read()


def parse_functions(tl_text: str) -> List[Dict[str, Any]]:
    # جدا کردن بخش توابع
    if "---functions---" in tl_text:
        tl_text = tl_text.split("---functions---")[1]

    lines = tl_text.strip().split('\n')
    blocks: List[List[str]] = []
    current_block: List[str] = []

    for line in lines:
        if line.strip():
            current_block.append(line.strip())
        elif current_block:
            blocks.append(current_block)
            current_block = []
    if current_block: blocks.append(current_block)

    parsed_data: List[Dict[str, Any]] = []

    for block in blocks:
        # خط آخر کد است، بقیه توضیحات هستند
        code_line = block[-1]
        description_lines = [l for l in block[:-1] if l.startswith("//@")]

        try:
            func_body, func_return = code_line.split("=")
            func_return = func_return.strip().replace(";", "")

            parts = func_body.strip().split(" ")
            func_name = parts[0]
            params_raw = parts[1:] if len(parts) > 1 else []

            params: List[Dict[str, Any]] = []
            for p in params_raw:
                p_name, p_type = p.split(":")
                params.append({"name": p_name, "type": p_type})

            parsed_data.append({
                "name": func_name,
                "params": params,
                "return": func_return,
                "docs": description_lines
            })
        except Exception as e:
            print(f"Exception parse function: {e} On: {block}")
            continue

    return parsed_data


def generate_python_file(parsed_functions: List[Dict[str, Any]], file_name: str = "tlmethods.py"):
    file_path = os.path.join(SCHEMA_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        _ = f.write("from typing import Any, List, Optional, Union\n")
        _ = f.write("from grathon.core.TLSchema_Manager.tltypes import *\n\n")
        _ = f.write("class GeneratedMethods:\n")
        _ = f.write("    def __init__(self, client):\n")
        _ = f.write("        self._client = client\n\n")

        for func in parsed_functions:
            method_name = func['name']
            py_name = to_snake_case(method_name)
            params = func['params']
            ret_type = func['return']

            # ساخت ورودی‌های تابع
            arg_list = ["self"]
            dict_entries = [f"'@type': '{method_name}'"]

            for p in params:
                p_name = p['name']
                p_type = map_type(p['type'])
                arg_list.append(f"{p_name}: {p_type} = None")
                dict_entries.append(f"'{p_name}': {p_name}")

            # نوشتن بدنه متد
            _=f.write(f"    async def {py_name}({', '.join(arg_list)}) -> {ret_type}:\n")
            _=f.write('        """\n')
            for doc in func['docs']:
                _=f.write(f"        {doc.replace('//@', '').strip()}\n")
            _=f.write('        """\n')
            _=f.write(
                f"        return await self._client.call_method('{method_name}', {{{', '.join(dict_entries)}}})\n\n")
    print(f"✅ {file_name} generated successfully.")


def parse_tl_types(tl_content: str) -> tuple[list[Any], list[str]]:
    types_section = tl_content.split("---functions---")[0]
    lines = types_section.splitlines()

    parsed: List[Dict[str, Any]] = []
    abstract_parents: Set[str] = set()
    current_docs: List[str] = []

    for line in lines:
        line = line.strip()

        # ۱. اگر خط خالی بود، نادیده بگیر
        if not line:
            continue

        # ۲. اگر خط توضیحات بود، آن را در بافر نگه دار
        if line.startswith("//@"):
            current_docs.append(line)
            continue

        # ۳. اگر خط کد بود (یعنی علامت = دارد)
        if "=" in line:
            code_line = line.split("//")[0].strip()

            try:
                left, parent = code_line.split("=")
                parent = parent.strip().replace(";", "")

                parts = left.strip().split()
                if not parts: continue

                name = parts[0]
                params_raw = parts[1:]

                # حذف موارد خاص
                if name in ("vector", "Vector", "t") or (len(params_raw) == 1 and params_raw[0] == "t"):
                    current_docs = []  # بافر را خالی کن برای بلاک بعد
                    continue

                if name != parent:
                    abstract_parents.add(parent)

                params: List[Dict[str, Any]] = []
                for p in params_raw:
                    if ":" in p:
                        n, t = p.split(":")
                        params.append({"name": n, "type": t})

                parsed.append({
                    "name": name,
                    "parent": parent,
                    "params": params,
                    "docs": current_docs,  # توضیحات جمع شده را اینجا بذار
                })

                # مهم: بعد از اتمام هر بلاک، بافر توضیحات را خالی کن
                current_docs = []

            except Exception as e:
                print(f"Exception generate type: {e} On: {line}")
                current_docs = []
                continue
        else:
            # اگر خطی بود که نه توضیحات بود و نه کد اصلی (مثلاً کامنت معمولی //)
            # بافر توضیحات را خالی نکن، چون شاید توضیحات هنوز ادامه داشته باشند
            pass

    return parsed, sorted(abstract_parents)


# ===================== Codegen =====================

def write_types_file(parsed_types:List[Dict[str, Any]],
                     abstract_parents:List[str],
                     file_name:str="tltypes.py"):
    file_path = os.path.join(SCHEMA_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:

        _ = f.write((
            "from dataclasses import dataclass, field, fields\n"
            "from typing import Any, List, Optional, Dict\n\n"
        ))

        # ---------- Base TdObject ----------
        _ = f.write((
            "class TdObject:\n"
            "    __td_type__: str\n\n"
            "    def to_dict(self) -> Dict[str, Any]:\n"
            "        data = {'@type': self.__td_type__}\n"
            "        for f_ in fields(self):\n"
            "            # Skip __td_type__ field (already set above)\n"
            "            if f_.name == '__td_type__':\n"
            "                continue\n"
            "            val = getattr(self, f_.name)\n"
            "            if val is None:\n"
            "                continue\n"
            "            if isinstance(val, TdObject):\n"
            "                data[f_.name] = val.to_dict()\n"
            "            elif isinstance(val, list):\n"
            "                data[f_.name] = [\n"
            "                    v.to_dict() if isinstance(v, TdObject) else v\n"
            "                    for v in val\n"
            "                ]\n"
            "            else:\n"
            "                data[f_.name] = val\n"
            "        return data\n\n"
        ))

        # ---------- Abstract base classes ----------
        for base in abstract_parents:
            _ = f.write(f"class {base}(TdObject):\n    pass\n\n")

        # ---------- Concrete types ----------
        for t in parsed_types:
            name = t["name"]
            parent = t["parent"]

            # Skip reserved Python builtin names (Bug 5)
            if name in PYTHON_BUILTINS_RESERVED:
                print(f"⚠️  Skipping reserved builtin name: {name}")
                continue

            _= f.write("@dataclass\n")
            _= f.write(f"class {name}({parent}):\n")
            _= f.write(f"    __td_type__: str = field(default='{name}', init=False)\n")

            # Generate comprehensive docstring
            if t["docs"] or t["params"]:
                _= f.write("    \"\"\"\n")
                if t["docs"]:
                    for d in t["docs"]:
                        _= f.write(f"    {d.replace('//@', '').strip()}\n")
                    if t["params"]:
                        _= f.write("\n    Parameters:\n")
                if t["params"]:
                    for p in t["params"]:
                        _= f.write(f"        {p['name']}: {p['type']}\n")
                _ = f.write("    \"\"\"\n")

            if not t["params"]:
                _ = f.write("    pass\n\n")
                continue

            for p in t["params"]:
                py_type = map_type(p["type"])
                _ = f.write(f"    {p['name']}: Optional[{py_type}] = None\n")

            # Generate __repr__ method
            param_names = ", ".join([f"{p['name']}={{self.{p['name']}}}" for p in t["params"]])
            _= f.write(f"\n    def __repr__(self) -> str:\n")
            _= f.write(f"        return f\"{name}({param_names})\"\n")

            _ = f.write("\n")
        _ = f.write("\n\n# ────────────────────────────────────────────────\n")
        _ = f.write("# Auto-generated type registry for safe deserialization\n")
        _ = f.write("# Do NOT edit this section manually\n\n")

        _ = f.write("from typing import Dict, Type, Any\n\n")
        _ = f.write("TYPE_REGISTRY: Dict[str, Type[Any]] = {\n")

        for t in parsed_types:
            name = t["name"]
            # Skip reserved names (Bug 5)
            if name not in PYTHON_BUILTINS_RESERVED:
                _ = f.write(f"    '{name}': {name},\n")

        _ = f.write("}\n\n")

        _ = f.write("def get_td_type(type_name: str) -> Type[Any] | None:\n")
        _ = f.write("    \"\"\"Safe lookup for TDLib types by @type string\"\"\"\n")
        _ = f.write("    return TYPE_REGISTRY.get(type_name)\n")

    print(f"✅ tltypes.py generated with registry ({len(parsed_types)} types)")


# ===================== Run =====================

if __name__ == "__main__":
    schema = read_schema()
    parsed_types, abstract_parents = parse_tl_types(schema)
    write_types_file(parsed_types, abstract_parents)
    functions = parse_functions(schema)
    generate_python_file(functions)
