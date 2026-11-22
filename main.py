import asyncio
import logging
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

from telegram.ext import ApplicationBuilder

from src.config import config
from src.bot import register_handlers
from src.scheduler import setup_scheduler

# Konfigurasi logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Handler ringan untuk layanan web free tier (Render/Koyeb) agar port binding berhasil."""
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Attendance Reminder Bot is running!")

    def log_message(self, format, *args):
        # Mute logging akses health-check agar tidak memenuhi log
        pass


def start_dummy_health_server(port: int) -> None:
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    logger.info("Health-check server aktif di port %s (siap untuk Render/Koyeb/Cloud)", port)
    server.serve_forever()


def main() -> None:
    token = config.TELEGRAM_BOT_TOKEN
    if not token or token == "your_bot_token_here":
        logger.error("TELEGRAM_BOT_TOKEN belum diatur di file .env!")
        sys.exit(1)

    # Selalu jalankan dummy health server ringan pada port 7860 (default Hugging Face Spaces) atau PORT
    port_env = os.getenv("PORT", "7860")
    try:
        port = int(port_env)
        thread = threading.Thread(target=start_dummy_health_server, args=(port,), daemon=True)
        thread.start()
    except Exception as e:
        logger.warning("Gagal memulai health server: %s", e)

    logger.info("Menginisialisasi Attendance Reminder Bot...")
    application = ApplicationBuilder().token(token).build()

    # Daftarkan command handlers
    register_handlers(application)

    # Daftarkan scheduler jobs (08:40, 17:00, 17:30)
    setup_scheduler(application)

    logger.info("Bot siap berjalan. Tekan Ctrl+C untuk menghentikan.")
    application.run_polling()


if __name__ == "__main__":
    main()
