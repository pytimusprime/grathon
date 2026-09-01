"""مثال: منوی سریال با SmartMenu — فصل، کیفیت، صدا، اپیزود"""

from grathon import GrathonBot, F
from grathon.high_level import SmartMenu

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
    await SmartMenu(ctx) \
        .text("🏠 منوی اصلی\nبه ربات سریال خوش آمدید!") \
        .item("🎬 سریال‌ها", callback="series") \
        .item("🎵 فیلم‌ها", callback="movies") \
        .item("🔍 جستجو", callback="search") \
        .send()


# ─────────────────────────────────────────────────
# لیست سریال‌ها — صفحه‌بندی ۵ تایی
# ─────────────────────────────────────────────────
@router.on(F.callback("series"))
async def series_list(ctx):
    all_series = [
        ("🔥 بریکینگ بد", "series_breakingbad"),
        ("🔫 پابی فیکس", "series_peakyblinders"),
        ("🐉 گیمز آف ترون", "series_got"),
        ("🧱 بتمن", "series_batman"),
        ("⚡ فلش", "series_flash"),
        ("🕷️ اسپایدرمن", "series_spiderman"),
        ("🦇 دارک", "series_dark"),
        ("🎭 تاونگ", "series_towntalk"),
        ("🚀 استار ترک", "series_startrek"),
        ("🐺 وایکینگ‌ها", "series_vikings"),
        ("🗡️ شانگ چی", "series_shangchi"),
        ("🎯 دارک متریال", "series_darkmatter"),
    ]

    await SmartMenu(ctx) \
        .text("🎬 سریال‌ها:\n\nکدوم سریال رو می‌خوای؟") \
        .items(all_series, per_page=5) \
        .send()
    # دکمه "← خانه" + "صفحه ۱ از ۳" + "▶️ بعدی"


# ─────────────────────────────────────────────────
# انتخاب فصل — سریال خاص
# ─────────────────────────────────────────────────
@router.on(F.callback(r"^series_(.+)$"))
async def select_season(ctx):
    series_id = ctx.match.group(1)

    await SmartMenu(ctx) \
        .text(f"📺 فصل رو انتخاب کن:") \
        .item("📺 فصل ۱", callback=f"s1_{series_id}") \
        .item("📺 فصل ۲", callback=f"s2_{series_id}") \
        .item("📺 فصل ۳", callback=f"s3_{series_id}") \
        .item("📺 فصل ۴", callback=f"s4_{series_id}") \
        .item("📺 فصل ۵", callback=f"s5_{series_id}") \
        .send()
    # دکمه "← سریال‌ها" خودکار


# ─────────────────────────────────────────────────
# انتخاب کیفیت
# ─────────────────────────────────────────────────
@router.on(F.callback(r"^s(\d+)_(.+)$"))
async def select_quality(ctx):
    season = ctx.match.group(1)
    series_id = ctx.match.group(2)

    await SmartMenu(ctx) \
        .text(f"🎞️ کیفیت رو انتخاب کن (فصل {season}):") \
        .item("🔴 1080p Full HD", callback=f"q1080_s{season}_{series_id}") \
        .item("🟠 720p HD", callback=f"q720_s{season}_{series_id}") \
        .item("🟡 480p", callback=f"q480_s{season}_{series_id}") \
        .item("🟢 360p", callback=f"q360_s{season}_{series_id}") \
        .send()
    # دکمه "← فصل انتخاب" خودکار


# ─────────────────────────────────────────────────
# انتخاب صدا (زبان)
# ─────────────────────────────────────────────────
@router.on(F.callback(r"^q(\d+)_s(\d+)_(.+)$"))
async def select_audio(ctx):
    quality = ctx.match.group(1)
    season = ctx.match.group(2)
    series_id = ctx.match.group(3)

    await SmartMenu(ctx) \
        .text(f"🔊 صدا رو انتخاب کن ({quality}p, فصل {season}):") \
        .item("🇮🇷 دوبله فارسی", callback=f"fa_q{quality}_s{season}_{series_id}") \
        .item("🇺🇸 زبان اصلی + زیرنویس", callback=f"en_q{quality}_s{season}_{series_id}") \
        .item("🇹🇷 دوبله ترکی", callback=f"tr_q{quality}_s{season}_{series_id}") \
        .item("🇮🇩 دوبله عربی", callback=f"ar_q{quality}_s{season}_{series_id}") \
        .send()
    # دکمه "← کیفیت" خودکار


# ─────────────────────────────────────────────────
# انتخاب اپیزود — صفحه‌بندی ۸ تایی
# ─────────────────────────────────────────────────
@router.on(F.callback(r"^(\w+)_q(\d+)_s(\d+)_(.+)$"))
async def select_episode(ctx):
    audio = ctx.match.group(1)
    quality = ctx.match.group(2)
    season = ctx.match.group(3)
    series_id = ctx.match.group(4)

    # ۲۰ اپیزود در هر فصل
    episodes = [(f"📺 اپیزود {i}", f"ep{i}_{audio}_q{quality}_s{season}_{series_id}") for i in range(1, 21)]

    await SmartMenu(ctx) \
        .text(f"📋 اپیزود رو انتخاب کن ({quality}p, فصل {season}, {audio}):") \
        .items(episodes, per_page=8) \
        .send()
    # دکمه "← صدا" + "صفحه ۱ از ۳" + "▶️ بعدی"


# ─────────────────────────────────────────────────
# ارسال اپیزود نهایی
# ─────────────────────────────────────────────────
@router.on(F.callback(r"^ep(\d+)_(\w+)_q(\d+)_s(\d+)_(.+)$"))
async def send_episode(ctx):
    episode = ctx.match.group(1)
    audio = ctx.match.group(2)
    quality = ctx.match.group(3)
    season = ctx.match.group(4)
    series_id = ctx.match.group(5)

    # ارسال فایل
    await SmartMenu(ctx) \
        .text(f"📺 اپیزود {episode} فصل {season}\n🎞️ کیفیت: {quality}p\n🔊 صدا: {audio}\n\n⬇️ لینک دانلود:") \
        .item("⬇️ دانلود", callback=f"dl_{episode}_{audio}_{quality}_{season}_{series_id}") \
        .item("▶️ پخش آنلاین", callback=f"stream_{episode}_{audio}_{quality}_{season}_{series_id}") \
        .item("📤 اشتراک‌گذاری", callback=f"share_{episode}_{audio}_{quality}_{season}_{series_id}") \
        .send()
    # دکمه "← اپیزود" خودکار


# ─────────────────────────────────────────────────
# شروع ربات
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    bot.run()
