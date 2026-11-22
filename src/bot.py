import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from src.config import config
from src.messages import (
    get_morning_reminder,
    get_attendance_reminder,
    get_evening_photo_reminder
)

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    text = (
        "👋 <b>Halo! Saya Attendance Reminder Bot.</b>\n\n"
        "Saya bertugas untuk mengirimkan pengingat absensi dan foto secara otomatis:\n"
        "• <b>08:40 WIB</b>: Foto Pagi & Kata Motivasi ☀️\n"
        "• <b>17:00 WIB</b>: Absen Kantor + Tombol Link Absen ⏰\n"
        "• <b>17:30 WIB</b>: Foto Absen Pulang & Kata Penutup 📸\n\n"
        "<b>Cara Memasang di Grup:</b>\n"
        "1. Tambahkan bot ini ke grup Anda (@SeroAttendanceBot).\n"
        "2. Di dalam grup, ketik perintah <code>/set_chat</code> untuk menjadikan grup tersebut sebagai target pengingat.\n"
        "3. Selesai! Bot akan otomatis mengirimkan pengingat setiap hari kerja (Senin - Jumat).\n\n"
        "Ketik <code>/help</code> untuk melihat daftar perintah yang tersedia."
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📋 <b>Daftar Perintah Bot:</b>\n\n"
        "• <code>/start</code> - Memulai bot & melihat panduan\n"
        "• <code>/get_id</code> - Melihat Chat ID saat ini\n"
        "• <code>/set_chat</code> - Menjadikan chat/grup ini sebagai target reminder otomatis\n"
        "• <code>/status</code> - Melihat konfigurasi dan status bot saat ini\n"
        "• <code>/test_morning</code> - Tes langsung pesan reminder pagi (08:40)\n"
        "• <code>/test_absen</code> - Tes langsung pesan reminder absen (17:00)\n"
        "• <code>/test_evening</code> - Tes langsung pesan reminder pulang (17:30)\n"
        "• <code>/help</code> - Menampilkan bantuan ini"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def get_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    chat_type = chat.type
    chat_title = chat.title if chat.title else "Personal Chat"
    text = (
        f"ℹ️ <b>Informasi Chat:</b>\n"
        f"• <b>Chat ID:</b> <code>{chat.id}</code>\n"
        f"• <b>Tipe:</b> {chat_type}\n"
        f"• <b>Nama/Judul:</b> {chat_title}\n\n"
        "💡 <i>Tip: Ketik <code>/set_chat</code> di grup ini untuk langsung menyimpannya sebagai target pengingat.</i>"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def set_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    config.set_target_chat_id(str(chat.id))
    chat_name = chat.title if chat.title else "Personal Chat"
    text = (
        f"✅ <b>Berhasil!</b>\n\n"
        f"Chat <b>{chat_name}</b> (ID: <code>{chat.id}</code>) telah ditetapkan sebagai target pengingat otomatis.\n"
        f"Pengingat akan dikirimkan pada jam 08:40, 17:00, dan 17:30 WIB (Senin - Jumat)."
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    target = config.TARGET_CHAT_ID if config.TARGET_CHAT_ID else "<i>Belum diatur (gunakan /set_chat)</i>"
    days_info = "Senin s/d Jumat (Hari Kerja)" if config.WORK_DAYS_ONLY else "Setiap Hari"
    text = (
        "⚙️ <b>Status & Konfigurasi Bot:</b>\n\n"
        f"• <b>Target Chat ID:</b> <code>{target}</code>\n"
        f"• <b>Zona Waktu:</b> {config.TIMEZONE}\n"
        f"• <b>Jadwal Hari:</b> {days_info}\n"
        f"• <b>Link Absen:</b> {config.ABSEN_URL}\n\n"
        "<b>Jadwal Aktif:</b>\n"
        "1. 08:40 WIB - Foto Pagi & Motivasi\n"
        "2. 17:00 WIB - Absen Kantor & Tombol Link\n"
        "3. 17:30 WIB - Foto Absen Pulang & Apresiasi"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def test_morning_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, keyboard = get_morning_reminder()
    await update.message.reply_text(
        f"[TEST PREVIEW]\n\n{text}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


async def test_absen_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, keyboard = get_attendance_reminder()
    await update.message.reply_text(
        f"[TEST PREVIEW]\n\n{text}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


async def test_evening_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text, keyboard = get_evening_photo_reminder()
    await update.message.reply_text(
        f"[TEST PREVIEW]\n\n{text}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


def register_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("get_id", get_id_handler))
    application.add_handler(CommandHandler("set_chat", set_chat_handler))
    application.add_handler(CommandHandler("status", status_handler))
    application.add_handler(CommandHandler("test_morning", test_morning_handler))
    application.add_handler(CommandHandler("test_absen", test_absen_handler))
    application.add_handler(CommandHandler("test_evening", test_evening_handler))
