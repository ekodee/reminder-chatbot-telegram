import json
import random
from pathlib import Path
from typing import Tuple, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.config import config, BASE_DIR

QUOTES_PATH = BASE_DIR / "quotes.json"


def load_quotes() -> dict:
    if QUOTES_PATH.exists():
        try:
            with open(QUOTES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "morning_quotes": ["Awali hari ini dengan senyuman dan niat terbaik! Semangat!"],
        "evening_quotes": ["Terima kasih atas kerja keras hari ini. Selamat beristirahat!"]
    }


def get_random_quote(category: str) -> str:
    quotes = load_quotes().get(category, [])
    if not quotes:
        return "Tetap semangat dan berikan yang terbaik!"
    return random.choice(quotes)


def get_morning_reminder() -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    quote = get_random_quote("morning_quotes")
    text = (
        "☀️ <b>REMINDER FOTO PAGI (08:40 WIB)</b> ☀️\n\n"
        "Halo Rekan-rekan! Selamat pagi.\n"
        "Jangan lupa untuk mengambil dan mengirimkan <b>Foto Pagi</b> Anda sekarang ya! 📸\n\n"
        f"💡 <i>Kata Motivasi Hari Ini:</i>\n"
        f"<i>\"{quote}\"</i>\n\n"
        "Semoga hari ini penuh berkah, produktif, dan menyenangkan! 💪✨"
    )
    return text, None


def get_attendance_reminder() -> Tuple[str, InlineKeyboardMarkup]:
    text = (
        "⏰ <b>REMINDER ABSEN KANTOR (17:00 WIB)</b> ⏰\n\n"
        "Halo Rekan-rekan!\n"
        "Waktu menunjukkan pukul 17:00 WIB.\n"
        "Jangan lupa untuk mengisi <b>Absensi Kantor</b> sekarang sebelum pulang ya! 📝\n\n"
        "Silakan klik tombol di bawah untuk langsung menuju portal absensi:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Buka Link Absensi", url=config.ABSEN_URL)]
    ])
    return text, keyboard


def get_evening_photo_reminder() -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    quote = get_random_quote("evening_quotes")
    text = (
        "📸 <b>REMINDER FOTO ABSEN PULANG (17:30 WIB)</b> 📸\n\n"
        "Halo Rekan-rekan!\n"
        "Sudah pukul 17:30 WIB, waktunya untuk mengambil dan mengirimkan <b>Foto Absen Pulang</b>. 🏁\n\n"
        f"🌟 <i>Pesan Penutup:</i>\n"
        f"<i>\"{quote}\"</i>\n\n"
        "Hati-hati di perjalanan pulang dan selamat menikmati waktu istirahat yang berkualitas! 🏠💤"
    )
    return text, None
