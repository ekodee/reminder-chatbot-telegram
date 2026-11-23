import asyncio
import json
import logging
import os
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Tambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from telegram import Bot
from src.config import config
from src.messages import (
    get_morning_reminder,
    get_attendance_reminder,
    get_evening_photo_reminder,
)
from src.scheduler import is_workday_now

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_sender")


async def send_telegram_reminder(reminder_type: str) -> dict:
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TARGET_CHAT_ID

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN belum diset di environment variables!")
    if not chat_id:
        raise ValueError("TARGET_CHAT_ID belum diset di environment variables!")

    # Cek hari kerja jika WORK_DAYS_ONLY aktif
    if not is_workday_now():
        logger.info("Hari ini akhir pekan, reminder dilewati.")
        return {
            "status": "skipped",
            "message": "Akhir pekan, pengingat otomatis dilewati.",
            "type": reminder_type
        }

    if reminder_type == "morning":
        text, keyboard = get_morning_reminder()
        job_label = "Foto Pagi (08:40 WIB)"
    elif reminder_type == "attendance":
        text, keyboard = get_attendance_reminder()
        job_label = "Absen Kantor (17:00 WIB)"
    elif reminder_type == "evening":
        text, keyboard = get_evening_photo_reminder()
        job_label = "Foto Absen Pulang (17:30 WIB)"
    else:
        raise ValueError(f"Tipe pengingat tidak valid: {reminder_type}")

    bot = Bot(token=token)
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    logger.info("Pesan '%s' berhasil terkirim ke %s", job_label, chat_id)
    return {
        "status": "success",
        "message": f"Pengingat {job_label} berhasil dikirim!",
        "job": job_label,
        "type": reminder_type,
        "chat_id": chat_id
    }


class handler(BaseHTTPRequestHandler):
    """Serverless HTTP Handler untuk Vercel"""

    def _send_json_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        # 1. Validasi secret
        req_secret = params.get("secret", [""])[0]
        configured_secret = config.CRON_SECRET

        if configured_secret and req_secret != configured_secret:
            self._send_json_response(401, {
                "status": "error",
                "message": "Unauthorized: secret parameter tidak valid atau tidak disertakan."
            })
            return

        # 2. Cek tipe reminder
        reminder_type = params.get("type", [""])[0].lower()
        if not reminder_type:
            # Jika hanya tes ping tanpa parameter type
            self._send_json_response(200, {
                "status": "ready",
                "message": "Vercel Telegram Reminder API is running!",
                "usage": "/api/send?type=morning&secret=..."
            })
            return

        if reminder_type not in ("morning", "attendance", "evening"):
            self._send_json_response(400, {
                "status": "error",
                "message": f"Tipe '{reminder_type}' tidak valid. Gunakan: morning, attendance, atau evening."
            })
            return

        # 3. Eksekusi pengiriman
        try:
            result = asyncio.run(send_telegram_reminder(reminder_type))
            self._send_json_response(200, result)
        except Exception as e:
            logger.error("Error executing reminder: %s", e)
            self._send_json_response(500, {
                "status": "error",
                "message": str(e)
            })

    def do_POST(self):
        # Handle POST identically to GET for flexiblity
        self.do_GET()

    def log_message(self, format, *args):
        # Mute default noisy stdout logging
        pass
