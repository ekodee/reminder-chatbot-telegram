import logging
from datetime import time, datetime
import pytz
from telegram.ext import Application, ContextTypes

from src.config import config
from src.messages import (
    get_morning_reminder,
    get_attendance_reminder,
    get_evening_photo_reminder
)

logger = logging.getLogger(__name__)


def is_workday_now() -> bool:
    """Mengecek apakah hari ini adalah hari kerja (Senin=0 s/d Jumat=4) pada zona waktu yang ditentukan."""
    if not config.WORK_DAYS_ONLY:
        return True
    tz = pytz.timezone(config.TIMEZONE)
    current_time = datetime.now(tz)
    return current_time.weekday() < 5


async def send_morning_reminder_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Job pengingat 08:40 WIB: Foto Pagi & Motivasi"""
    if not is_workday_now():
        logger.info("Hari ini akhir pekan, reminder pagi dilewati.")
        return

    chat_id = config.TARGET_CHAT_ID
    if not chat_id:
        logger.warning("TARGET_CHAT_ID belum diatur. Gunakan /set_chat di grup tujuan.")
        return

    text, keyboard = get_morning_reminder()
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        logger.info("Reminder pagi berhasil dikirim ke %s", chat_id)
    except Exception as e:
        logger.error("Gagal mengirim reminder pagi ke %s: %s", chat_id, e)


async def send_attendance_reminder_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Job pengingat 17:00 WIB: Absen Kantor + Link Tombol"""
    if not is_workday_now():
        logger.info("Hari ini akhir pekan, reminder absen kantor dilewati.")
        return

    chat_id = config.TARGET_CHAT_ID
    if not chat_id:
        logger.warning("TARGET_CHAT_ID belum diatur. Gunakan /set_chat di grup tujuan.")
        return

    text, keyboard = get_attendance_reminder()
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        logger.info("Reminder absen kantor berhasil dikirim ke %s", chat_id)
    except Exception as e:
        logger.error("Gagal mengirim reminder absen kantor ke %s: %s", chat_id, e)


async def send_evening_reminder_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Job pengingat 17:30 WIB: Foto Absen Pulang & Ucapan Istirahat"""
    if not is_workday_now():
        logger.info("Hari ini akhir pekan, reminder foto pulang dilewati.")
        return

    chat_id = config.TARGET_CHAT_ID
    if not chat_id:
        logger.warning("TARGET_CHAT_ID belum diatur. Gunakan /set_chat di grup tujuan.")
        return

    text, keyboard = get_evening_photo_reminder()
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        logger.info("Reminder foto pulang berhasil dikirim ke %s", chat_id)
    except Exception as e:
        logger.error("Gagal mengirim reminder foto pulang ke %s: %s", chat_id, e)


def setup_scheduler(application: Application) -> None:
    """Mendaftarkan jadwal otomatis pada JobQueue."""
    job_queue = application.job_queue
    if not job_queue:
        logger.error("JobQueue tidak tersedia. Pastikan 'python-telegram-bot[job-queue]' terpasang.")
        return

    tz = pytz.timezone(config.TIMEZONE)
    # (0, 1, 2, 3, 4) merepresentasikan Senin s/d Jumat di PTB
    active_days = (0, 1, 2, 3, 4) if config.WORK_DAYS_ONLY else tuple(range(7))

    # 1. 08:40 WIB
    job_queue.run_daily(
        callback=send_morning_reminder_job,
        time=time(hour=8, minute=40, tzinfo=tz),
        days=active_days,
        name="reminder_foto_pagi_0840"
    )

    # 2. 17:00 WIB
    job_queue.run_daily(
        callback=send_attendance_reminder_job,
        time=time(hour=17, minute=0, tzinfo=tz),
        days=active_days,
        name="reminder_absen_kantor_1700"
    )

    # 3. 17:30 WIB
    job_queue.run_daily(
        callback=send_evening_reminder_job,
        time=time(hour=17, minute=30, tzinfo=tz),
        days=active_days,
        name="reminder_foto_pulang_1730"
    )

    logger.info(
        "Scheduler berhasil dikonfigurasi pada zona waktu %s (Hari: %s)",
        config.TIMEZONE,
        "Senin-Jumat" if config.WORK_DAYS_ONLY else "Setiap Hari"
    )
