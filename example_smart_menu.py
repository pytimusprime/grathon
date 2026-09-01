"""مثال کامل SmartMenu — نشون میده چطوری همه ویژگی‌ها کار می‌کنن"""

from grathon import GrathonBot, F
from grathon.high_level import SmartMenu
from grathon.core.router import Router

bot = GrathonBot(
    api_id=12345,
    api_hash="your_api_hash",
    bot_token="your_bot_token",
)
router = bot.router


# ─────────────────────────────────────────────────
# منوی اصلی
# ─────────────────────────────────────────────────
@router.on(F.command("start"))
async def main_menu(ctx):
    await SmartMenu(ctx).text("🏠 منوی اصلی\nبه ربات فروشگاه خوش آمدید!").item(
        "🛒 محصولات", callback="products"
    ).item("📦 سفارشات", callback="orders").item(
        "⚙️ تنظیمات", callback="settings"
    ).item(
        "📞 پشتیبانی", callback="support"
    ).send()


# ─────────────────────────────────────────────────
# منوی محصولات → لیست با صفحه‌بندی
# ─────────────────────────────────────────────────
@router.on(F.callback("products"))
async def products_menu(ctx):
    # ۱۲ محصول → خودش صفحه‌بندی می‌کنه (۵ تایی)
    all_products = [
        ("📱 آیفون ۱۶", "prod_iphone16"),
        ("📱 آیفون ۱۵", "prod_iphone15"),
        ("📱 گلکسی S25", "prod_galaxy25"),
        ("📱 گلکسی S24", "prod_galaxy24"),
        ("📱 شیائومی ۱۵", "prod_xiaomi15"),
        ("📱 هواوی P70", "prod_huaweip70"),
        ("📱 وان پلاس ۱۳", "prod_oneplus13"),
        ("📱 گوگل پیکسل ۹", "prod_pixel9"),
        ("📱 سونی Xperia", "prod_xperia"),
        ("📱 موتورولا Edge", "prod_moto"),
        ("📱 نوکیا G60", "prod_nokia"),
        ("📱 ایسوس ROG", "prod_rog"),
    ]

    # خودش صفحه‌بندی می‌کنه: ۵ تایی، دکمه بعدی/قبلی
    await SmartMenu(ctx).text(
        "🛒 محصولات ما:\n\nهر کدوم رو بزن جزئیات ببین:"
    ).items(all_products, per_page=5).send()
    # دکمه "← خانه" + "صفحه ۱ از ۳" + "▶️ بعدی"


# ─────────────────────────────────────────────────
# جزئیات محصول (با breadcrumb)
# ─────────────────────────────────────────────────
@router.on(F.callback(r"^prod_(.+)$"))
async def product_detail(ctx):
    product_id = ctx.match.group(1)

    # نمایش مسیر حرکت
    await SmartMenu(ctx).text(
        f"📱 جزئیات محصول: {product_id}\n⭐ امتیاز: 4.5\n💰 قیمت: ۵۰,۰۰۰,۰۰۰ تومان"
    ).item("🛒 اضافه به سبد", callback=f"add_cart_{product_id}").item(
        "❤️ علاقه‌مندی", callback=f"add_fav_{product_id}"
    ).item(
        "📤 اشتراک‌گذاری", callback=f"share_{product_id}"
    ).show_path(True).send()
    # breadcrumb: 🏠 خانه > 🛒 محصولات > 📱 آیفون ۱۶
    # دکمه "← محصولات" خودکار اضافه می‌شود


# ─────────────────────────────────────────────────
# منوی سفارشات (با دکمه خانه)
# ─────────────────────────────────────────────────
@router.on(F.callback("orders"))
async def orders_menu(ctx):
    orders = [
        ("📦 سفارش #1001", "order_1001"),
        ("📦 سفارش #1002", "order_1002"),
        ("📦 سفارش #1003", "order_1003"),
        ("📦 سفارش #1004", "order_1004"),
        ("📦 سفارش #1005", "order_1005"),
        ("📦 سفارش #1006", "order_1006"),
        ("📦 سفارش #1007", "order_1007"),
        ("📦 سفارش #1008", "order_1008"),
    ]

    # دکمه خانه همیشه قابل دسترس
    await SmartMenu(ctx).text("📦 سفارشات شما:").items(
        orders, per_page=4
    ).show_home(True, label="🏠 خانه").send()


# ─────────────────────────────────────────────────
# جزئیات سفارش
# ─────────────────────────────────────────────────
@router.on(F.callback(r"^order_(\d+)$"))
async def order_detail(ctx):
    order_id = ctx.match.group(1)

    await SmartMenu(ctx).text(
        f"📦 سفارش #{order_id}\n\nوضعیت: ✅ تحویل شده\nمبلغ: ۵۰,۰۰۰,۰۰۰ تومان\nتاریخ: ۱۴۰۵/۰۶/۰۱"
    ).item("📋 فاکتور", callback=f"invoice_{order_id}").item(
        "⭐ امتیازدهی", callback=f"rate_{order_id}"
    ).send()
    # دکمه "← سفارشات" خودکار


# ─────────────────────────────────────────────────
# منوی تنظیمات (با دکمه بازگشت سفارشی)
# ─────────────────────────────────────────────────
@router.on(F.callback("settings"))
async def settings_menu(ctx):
    # دکمه بازگشت سفارشی (بجای "← خانه")
    await SmartMenu(ctx).text("⚙️ تنظیمات").item(
        "🔔 اعلان‌ها", callback="settings_notif"
    ).item("🌐 زبان", callback="settings_lang").item(
        "👤 پروفایل", callback="settings_profile"
    ).item(
        "🔒 حریم خصوصی", callback="settings_privacy"
    ).back_button("🔙 برگردیم").send()


# ─────────────────────────────────────────────────
# زیرمنوی تنظیمات → اعلان‌ها
# ─────────────────────────────────────────────────
@router.on(F.callback("settings_notif"))
async def settings_notif(ctx):
    await SmartMenu(ctx).text("🔔 تنظیمات اعلان‌ها").item(
        "✅ روشن", callback="notif_on"
    ).item("❌ خاموش", callback="notif_off").send()
    # دکمه "🔙 برگردیم" خودکار (چون منوی قبلی همین رو ست کرده)


# ─────────────────────────────────────────────────
# منوی پشتیبانی (با محدودیت عمق)
# ─────────────────────────────────────────────────
@router.on(F.callback("support"))
async def support_menu(ctx):
    # فقط ۲ مرحله برگشت می‌شه
    await SmartMenu(ctx).text("📞 پشتیبانی").item(
        "❓ سؤالات متداول", callback="support_faq"
    ).item("💬 چت با پشتیبان", callback="support_chat").item(
        "🐞 گزارش مشکل", callback="support_bug"
    ).max_depth(2).send()


# ─────────────────────────────────────────────────
# سؤالات متداول → لیست بلند با صفحه‌بندی
# ─────────────────────────────────────────────────
@router.on(F.callback("support_faq"))
async def support_faq(ctx):
    faqs = [
        ("❓ ارسال چقدر طول می‌کشه؟", "faq_delivery"),
        ("❓ نحوه پرداخت چطوره؟", "faq_payment"),
        ("❓ امکان بازگشت کالا هست؟", "faq_return"),
        ("❓ بهترین محصول چیه؟", "faq_best"),
        ("❓ تخفیف دارید؟", "faq_discount"),
        ("❓ اگه خراب بود؟", "faq_broken"),
        ("❓ گارانتی دارید؟", "faq_warranty"),
        ("❓ نحوه استفاده چطوره؟", "faq_howto"),
    ]

    await SmartMenu(ctx).text("❓ سؤالات متداول:").items(
        faqs, per_page=3
    ).send()


# ─────────────────────────────────────────────────
# شروع ربات
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    bot.run()
