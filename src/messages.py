
import html
import json
import random
from typing import Tuple, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.config import config, BASE_DIR


QUOTES_PATH = BASE_DIR / "quotes.json"


def load_quotes() -> dict:
    """Load quotes from JSON file."""
    if QUOTES_PATH.exists():
        try:
            with open(QUOTES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "morning_quotes": [
            "Tidak harus langsung menguasai semuanya. Setiap hari adalah kesempatan untuk belajar sesuatu yang baru."
        ],
        "evening_quotes": [
            "Tidak semua hari berjalan sesuai rencana. Terima kasih sudah berusaha, sekecil apa pun kemajuanmu."
        ]
    }


def get_random_quote(category: str) -> str:
    """Get a random quote from a category."""
    quotes = load_quotes().get(category, [])

    if not quotes:
        return "Tetap semangat dan nikmati setiap prosesnya!"

    return random.choice(quotes)


def get_random_message(messages: list) -> str:
    """Get a random message variation."""
    return random.choice(messages)


def get_morning_reminder() -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    """Generate morning photo reminder."""

    greetings = [
        "Selamat pagi, teman-teman!",
        "Good morning, everyone!",
        "Pagi semuanya! Semoga hari ini menyenangkan.",
        "Halo, teman-teman! Selamat memulai aktivitas hari ini.",
        "Selamat pagi! Semoga semuanya dalam keadaan baik."
    ]

    openings = [
        "Semoga pagi ini semuanya dalam keadaan baik dan siap menjalani aktivitas hari ini.",
        "Semoga hari ini membawa banyak hal baik dan pengalaman baru untuk kita semua.",
        "Sudah siap menjalani hari? Jangan lupa awali dengan semangat dan pikiran positif!",
        "Hari baru, kesempatan baru untuk belajar dan berkembang. Semoga semuanya berjalan lancar!"
    ]

    closings = [
        "Semangat menjalani hari ini! Semoga pekerjaan lancar, ilmunya bertambah, dan ada pengalaman baru yang bisa dibawa pulang nanti. 🚀",
        "Selamat beraktivitas! Jangan takut mencoba hal baru dan jangan malu untuk bertanya. Kita sama-sama masih belajar. 😊",
        "Have a great day! Semoga hari ini produktif, menyenangkan, dan penuh hal baik. ✨",
        "Nikmati prosesnya, kerjakan satu per satu, dan jangan lupa jaga kesehatan. Semangat! 💪"
    ]

    quote = html.escape(get_random_quote("morning_quotes"))

    text = (
        "☀️ <b>GOOD MORNING, EVERYONE!</b>\n\n"
        f"{get_random_message(greetings)}\n"
        f"{get_random_message(openings)}\n\n"
        "📸 Sebelum memulai kesibukan, jangan lupa untuk mengambil "
        "dan mengirimkan <b>Foto Pagi</b> terlebih dahulu ya!\n\n"
        "💡 <i>A little reminder for today:</i>\n"
        f"<i>\"{quote}\"</i>\n\n"
        f"{get_random_message(closings)}"
    )

    return text, None


def get_attendance_reminder() -> Tuple[str, InlineKeyboardMarkup]:
    """Generate office attendance reminder."""

    greetings = [
        "Halo, teman-teman!",
        "Hai semuanya!",
        "Halo! Semoga aktivitas hari ini berjalan lancar.",
        "Hi, everyone!"
    ]

    closings = [
        "Jangan sampai sudah siap pulang, ternyata absensinya belum diisi. Hehe. 😄",
        "Yuk, pastikan semuanya sudah tercatat sebelum meninggalkan kantor!",
        "Sedikit lagi selesai! Jangan lupa selesaikan absensinya terlebih dahulu ya. 😉",
        "Pastikan absensi berhasil tercatat sebelum bersiap pulang. Jangan sampai terlewat!"
    ]

    text = (
        "⏰ <b>TIME TO CHECK OUT!</b>\n\n"
        f"{get_random_message(greetings)}\n\n"
        "Tidak terasa sudah memasuki penghujung hari kerja. "
        "Sebelum bersiap pulang, pastikan kalian sudah mengisi "
        "<b>Absensi Kantor melalui portal Monev</b> ya! 📝\n\n"
        f"{get_random_message(closings)}\n\n"
        "Silakan klik tombol di bawah untuk membuka portal absensi."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔗 Buka Portal Absensi",
                url=config.ABSEN_URL
            )
        ]
    ])

    return text, keyboard


def get_evening_photo_reminder() -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    """Generate evening photo reminder."""

    greetings = [
        "Halo, teman-teman!",
        "Hai semuanya! Tidak terasa hari ini sudah sampai di penghujung.",
        "Good evening, everyone!",
        "Selamat sore! Semoga hari ini memberikan banyak pengalaman baik.",
        "Halo! Bagaimana hari kalian hari ini?"
    ]

    closings = [
        "Hati-hati di perjalanan pulang, teman-teman! Sampai bertemu besok. 👋",
        "Sekarang waktunya menikmati waktu pribadi. Jangan lupa istirahat yang cukup dan hati-hati di jalan! 🏠",
        "Terima kasih sudah menjalani hari ini. Sampai bertemu di hari berikutnya. Stay safe! ❤️",
        "Waktunya recharge energi! Semoga perjalanan pulang lancar dan malam ini menyenangkan. 🌙",
        "Sampai jumpa besok! Jangan lupa jaga kesehatan dan berikan waktu untuk diri sendiri. 😊"
    ]

    quote = html.escape(get_random_quote("evening_quotes"))

    text = (
        "🌇 <b>THAT'S A WRAP FOR TODAY!</b>\n\n"
        f"{get_random_message(greetings)}\n\n"
        "Sebelum benar-benar mengakhiri aktivitas hari ini, "
        "jangan lupa mengambil dan mengirimkan "
        "<b>Foto Absen Pulang</b> ya! 📸\n\n"
        "🌟 <i>A little message before you go:</i>\n"
        f"<i>\"{quote}\"</i>\n\n"
        "Setelah semuanya selesai, waktunya beristirahat dan "
        "menikmati waktu untuk diri sendiri.\n\n"
        f"{get_random_message(closings)}"
    )

    return text, None
