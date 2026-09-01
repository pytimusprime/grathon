"""Unit tests for the Conversation / wait_message / wait_callback fix.

Run from the repo root's parent (so ``grathon`` is importable) without a live
TDLib connection::

    PYTHONPATH=/home/devix/Desktop python3 grathon/tests/test_conversations.py

The native ``tdjson`` lib is stubbed; real TDLib schema objects are used so the
behaviour matches what happens in production.
"""
from __future__ import annotations

import asyncio
import sys
import types

# --- allow running both as a module and as a script ---
_REPO_PARENT = "/home/devix/Desktop"
if _REPO_PARENT not in sys.path:
    sys.path.insert(0, _REPO_PARENT)

# Stub the native tdjson lib so grathon imports without TDLib installed
if "tdjson" not in sys.modules:
    _tdjson_stub = types.ModuleType("tdjson")
    _tdjson_stub.set_log_verbosity_level = lambda *a, **k: None
    sys.modules["tdjson"] = _tdjson_stub

from grathon.core.TLSchema_Manager.tltypes import (  # noqa: E402
    message,
    messageText,
    formattedText,
    messageDocument,
    document,
    file as tl_file,
    remoteFile,
    messageSenderUser,
    updateNewMessage,
    updateNewCallbackQuery,
    callbackQueryPayloadData,
)
from grathon.core.contexts.NewMessageCtx import NewMessageCtx  # noqa: E402
from grathon.core.contexts.CallbackQueryCtx import CallbackQueryCtx  # noqa: E402
from grathon.high_level.conversations import (  # noqa: E402
    Conversation,
    ConversationStore,
    ConversationTimeout,
    _CANCELLED,
)


class _FakeClient:
    class session: ...
    session = None
    class api: ...


def _text_ctx(chat_id: int, user_id: int, text: str) -> NewMessageCtx:
    m = message(id=1, sender_id=messageSenderUser(user_id=user_id), chat_id=chat_id,
                content=messageText(text=formattedText(text=text, entities=[])))
    return NewMessageCtx(_FakeClient(), updateNewMessage(message=m))


def _doc_ctx(chat_id: int, user_id: int, caption: str | None = None) -> NewMessageCtx:
    f = tl_file(id=987654, size=1024, expected_size=1024, local=None,
                remote=remoteFile(id="R-FILE-ID", unique_id="u1"))
    content = messageDocument(document=document(document=f))
    if caption is not None:
        content = messageDocument(document=document(document=f),
                                  caption=formattedText(text=caption, entities=[]))
    m = message(id=2, sender_id=messageSenderUser(user_id=user_id), chat_id=chat_id, content=content)
    return NewMessageCtx(_FakeClient(), updateNewMessage(message=m))


def _cb_ctx(chat_id: int, user_id: int, data_str: str, msg_id: int = 555) -> CallbackQueryCtx:
    """Build a real CallbackQueryCtx wrapping an updateNewCallbackQuery payload."""
    upd = updateNewCallbackQuery(id=1, sender_user_id=user_id, chat_id=chat_id,
                                 message_id=msg_id, chat_instance=12345,
                                 payload=callbackQueryPayloadData(data=data_str.encode()))
    return CallbackQueryCtx(_FakeClient(), upd)


async def _ask(conv: Conversation) -> None:
    """Mirror Conversation.ask()'s future pre-registration without a real send."""
    loop = asyncio.get_running_loop()
    conv._pending_message_future = loop.create_future()
    ConversationStore.register_message(conv._chat_id, conv._user_id, conv._pending_message_future)


async def _ask_buttons(conv: Conversation) -> None:
    """Mirror ask_buttons()'s callback future pre-registration without a real send."""
    loop = asyncio.get_running_loop()
    conv._pending_callback_future = loop.create_future()
    ConversationStore.register_callback(conv._chat_id, conv._user_id, conv._pending_callback_future)


def _check(cond, msg):
    assert cond, msg


# ---------------------------------------------------------------- wait_message --

async def test_text_default_returns_str():
    ctx = _text_ctx(1, 2, "سلام")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask(conv)
        ConversationStore.resolve_message(1, 2, _text_ctx(1, 2, "سلام"))
        name = await conv.wait_message()
        _check(type(name) is str, f"expected plain str, got {type(name)}")
        _check(name == "سلام", f"expected 'سلام', got {name!r}")
        _check(f"hi {name}" == "hi سلام", "f-string coercion should work")


async def test_media_without_caption_default_str():
    ctx = _text_ctx(10, 20, "placeholder")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask(conv)
        ConversationStore.resolve_message(10, 20, _doc_ctx(10, 20))
        r = await conv.wait_message()
        _check(isinstance(r, str) and r == "", f"expected empty str, got {r!r}")


async def test_media_without_caption_only_text_false():
    """The reported bug: media w/o caption lost all context. only_text=False fixes it."""
    ctx = _text_ctx(30, 40, "placeholder")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask(conv)
        ConversationStore.resolve_message(30, 40, _doc_ctx(30, 40))
        r = await conv.wait_message(only_text=False)
        _check(r is not None and isinstance(r, NewMessageCtx), f"expected NewMessageCtx, got {type(r)}")
        _check(r.is_document, "is_document should be truthy")
        _check(r.file_id == 987654, f"file_id={r.file_id}")
        _check(r.remote_file_id == "R-FILE-ID", f"remote_file_id={r.remote_file_id}")
        _check(r.text is None, "captionless media has no text")


async def test_media_with_caption_only_text_false():
    ctx = _text_ctx(30, 41, "placeholder")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask(conv)
        ConversationStore.resolve_message(30, 41, _doc_ctx(30, 41, caption="my caption"))
        r = await conv.wait_message(only_text=False)
        assert r is not None and isinstance(r, NewMessageCtx), f"got {type(r)}"
        assert r.text == "my caption", f"text={r.text!r}"
        assert r.file_id == 987654, f"file_id={r.file_id}"
        assert r.remote_file_id == "R-FILE-ID", f"remote_file_id={r.remote_file_id}"


async def test_text_only_text_false_returns_ctx():
    ctx = _text_ctx(50, 60, "hello")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask(conv)
        ConversationStore.resolve_message(50, 60, _text_ctx(50, 60, "hello"))
        r = await conv.wait_message(only_text=False)
        _check(r is not None and r.text == "hello", f"text={getattr(r, 'text', None)!r}")


async def test_cancel_returns_none():
    ctx = _text_ctx(70, 80, "hi")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask(conv)
        ConversationStore.cancel_message(70, 80)
        r = await conv.wait_message()
        _check(r is None, f"cancel should return None, got {r!r}")


async def test_cancel_only_text_false_returns_none():
    ctx = _text_ctx(81, 82, "hi")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask(conv)
        ConversationStore.cancel_message(81, 82)
        r = await conv.wait_message(only_text=False)
        _check(r is None, f"cancel should return None, got {r!r}")


async def test_timeout_raises():
    ctx = _text_ctx(90, 91, "hi")
    try:
        async with Conversation(ctx, timeout=0.1) as conv:
            await _ask(conv)
            await conv.wait_message()
    except ConversationTimeout:
        return
    raise AssertionError("expected ConversationTimeout")


async def test_timeout_only_text_false_raises():
    ctx = _text_ctx(92, 93, "hi")
    try:
        async with Conversation(ctx, timeout=0.1) as conv:
            await _ask(conv)
            await conv.wait_message(only_text=False)
    except ConversationTimeout:
        return
    raise AssertionError("expected ConversationTimeout")


# ---------------------------------------------------------------- wait_callback --

async def test_callback_default_returns_data_str():
    """only_data=True (default) returns the decoded data string."""
    ctx = _text_ctx(200, 201, "seed")
    cb = _cb_ctx(200, 201, "btn_approve_42", msg_id=777)
    async with Conversation(ctx, timeout=10) as conv:
        await _ask_buttons(conv)
        ConversationStore.resolve_callback(200, 201, cb)
        r = await conv.wait_callback()
        _check(r == "btn_approve_42", f"expected data_str, got {r!r}")


async def test_callback_only_data_false_returns_ctx():
    """only_data=False returns the full CallbackQueryCtx with all attributes."""
    ctx = _text_ctx(210, 211, "seed")
    cb = _cb_ctx(210, 211, "btn_delete_7", msg_id=888)
    async with Conversation(ctx, timeout=10) as conv:
        await _ask_buttons(conv)
        ConversationStore.resolve_callback(210, 211, cb)
        r = await conv.wait_callback(only_data=False)
        _check(r is not None and isinstance(r, CallbackQueryCtx), f"got {type(r)}")
        _check(r.data_str == "btn_delete_7", f"data_str={r.data_str!r}")
        _check(r.message_id == 888, f"message_id={r.message_id}")
        _check(r.chat_instance == 12345, f"chat_instance={r.chat_instance}")
        _check(r.sender_user_id == 211, f"sender_user_id={r.sender_user_id}")


async def test_callback_cancel_returns_none_default():
    ctx = _text_ctx(220, 221, "seed")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask_buttons(conv)
        ConversationStore.cancel_message(220, 221)  # cancel_message only cancels msg futures
        # For callbacks we must cancel via resolving with _CANCELLED sentinel:
        fut = ConversationStore._callback_futures.get((220, 221))
        _check(fut is not None, "callback future should be registered")
        if not fut.done():
            fut.set_result(_CANCELLED)
        r = await conv.wait_callback()
        _check(r is None, f"cancelled callback should return None, got {r!r}")


async def test_callback_cancel_only_data_false_returns_none():
    ctx = _text_ctx(230, 231, "seed")
    async with Conversation(ctx, timeout=10) as conv:
        await _ask_buttons(conv)
        fut = ConversationStore._callback_futures.get((230, 231))
        if not fut.done():
            fut.set_result(_CANCELLED)
        r = await conv.wait_callback(only_data=False)
        _check(r is None, f"cancelled callback should return None, got {r!r}")


async def test_callback_timeout_raises():
    ctx = _text_ctx(240, 241, "seed")
    try:
        async with Conversation(ctx, timeout=0.1) as conv:
            await _ask_buttons(conv)
            await conv.wait_callback()
    except ConversationTimeout:
        return
    raise AssertionError("expected ConversationTimeout")


async def test_callback_timeout_only_data_false_raises():
    ctx = _text_ctx(250, 251, "seed")
    try:
        async with Conversation(ctx, timeout=0.1) as conv:
            await _ask_buttons(conv)
            await conv.wait_callback(only_data=False)
    except ConversationTimeout:
        return
    raise AssertionError("expected ConversationTimeout")


# ---------------------------------------------------------------- lifecycle ----

async def test_clear_cleanup():
    ConversationStore.clear(999, 999)
    _check((999, 999) not in ConversationStore._message_futures, "clear should remove message future")
    _check((999, 999) not in ConversationStore._callback_futures, "clear should remove callback future")


async def _main():
    await test_text_default_returns_str()
    print("PASS  only_text=True default (text) -> str")
    await test_media_without_caption_default_str()
    print("PASS  only_text=True default (media) -> empty str")
    await test_media_without_caption_only_text_false()
    print("PASS  only_text=False (media, no caption) -> NewMessageCtx w/ file_id/remote_file_id")
    await test_media_with_caption_only_text_false()
    print("PASS  only_text=False (media + caption) -> ctx.text=caption + file attrs")
    await test_text_only_text_false_returns_ctx()
    print("PASS  only_text=False (text) -> NewMessageCtx .text")
    await test_cancel_returns_none()
    print("PASS  cancel -> None (AttributeError bug fixed)")
    await test_cancel_only_text_false_returns_none()
    print("PASS  cancel only_text=False -> None")
    await test_timeout_raises()
    print("PASS  timeout -> ConversationTimeout")
    await test_timeout_only_text_false_raises()
    print("PASS  timeout only_text=False -> ConversationTimeout")
    await test_callback_default_returns_data_str()
    print("PASS  wait_callback() default -> data_str")
    await test_callback_only_data_false_returns_ctx()
    print("PASS  wait_callback(only_data=False) -> CallbackQueryCtx")
    await test_callback_cancel_returns_none_default()
    print("PASS  callback cancel (default) -> None")
    await test_callback_cancel_only_data_false_returns_none()
    print("PASS  callback cancel only_data=False -> None")
    await test_callback_timeout_raises()
    print("PASS  callback timeout -> ConversationTimeout")
    await test_callback_timeout_only_data_false_raises()
    print("PASS  callback timeout only_data=False -> ConversationTimeout")
    await test_clear_cleanup()
    print("PASS  clear lifecycle")
    print("\nALL TESTS PASSED ✅")


if __name__ == "__main__":
    asyncio.run(_main())
