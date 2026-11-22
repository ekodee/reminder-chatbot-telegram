import argparse
import asyncio
import logging
import sys

from telegram import Bot

from src.config import config
from src.messages import (
    get_morning_reminder,
    get_attendance_reminder,
    get_evening_photo_reminder,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Send scheduled Telegram reminder")
    parser.add_argument(
        "--type",
        choices=["morning", "attendance", "evening"],
        required=True,
        help="Jenis pengingat yang akan dikirim: morning (08:40), attendance (17:00), evening (17:30)"
    )
    args = parser.parse_args()

    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TARGET_CHAT_ID

    if not token:
        logger.error("Error: TELEGRAM_BOT_TOKEN belum diset!")
        sys.exit(1)
    if not chat_id:
        logger.error("Error: TARGET_CHAT_ID belum diset!")
        sys.exit(1)

    if args.type == "morning":
        text, keyboard = get_morning_reminder()
        job_label = "Foto Pagi (08:40 WIB)"
    elif args.type == "attendance":
        text, keyboard = get_attendance_reminder()
        job_label = "Absen Kantor (17:00 WIB)"
    elif args.type == "evening":
        text, keyboard = get_evening_photo_reminder()
        job_label = "Foto Absen Pulang (17:30 WIB)"
    else:
        logger.error("Tipe pengingat tidak valid: %s", args.type)
        sys.exit(1)

    bot = Bot(token=token)
    logger.info("Mengirim reminder '%s' ke chat ID: %s...", job_label, chat_id)

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        logger.info("Pengingat '%s' berhasil terkirim ke Telegram!", job_label)
    except Exception as e:
        logger.error("Gagal mengirim pengingat ke Telegram: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
