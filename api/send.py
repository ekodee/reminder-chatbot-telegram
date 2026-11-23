import html
import json
import logging
import os
import random
import sys
import traceback
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
QUOTES_PATH = BASE_DIR / "quotes.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_sender")


def get_config_var(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


def load_quotes() -> dict:
    if QUOTES_PATH.exists():
        try:
            with open(QUOTES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "morning_quotes": [
            "Tidak harus langsung menguasai semuanya. Setiap hari adalah kesempatan untuk belajar sesuatu yang baru."
        ],
        "evening_quotes": [
            "Tidak semua hari berjalan sesuai rencana. Terima kasih sudah berusaha hari ini."
        ]
    }


def get_random_quote(category: str) -> str:
    quotes = load_quotes().get(category, [])
    if not quotes:
        return "Tetap semangat dan nikmati setiap prosesnya!"
    return random.choice(quotes)


def get_random_message(messages: list) -> str:
    return random.choice(messages)


def get_morning_reminder() -> tuple:
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
        f"{get_random_message(greetings)}\n\n"
        f"{get_random_message(openings)}\n\n"
        "📸 Sebelum memulai kesibukan, jangan lupa untuk mengambil "
        "dan mengirimkan <b>Foto Pagi</b> terlebih dahulu ya!\n\n"
        "💡 <i>A little reminder for today:</i>\n"
        f"<i>\"{quote}\"</i>\n\n"
        f"{get_random_message(closings)}"
    )
    return text, None


def get_attendance_reminder() -> tuple:
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
    absen_url = get_config_var("ABSEN_URL", "https://monev.maganghub.kemnaker.go.id")
    text = (
        "⏰ <b>TIME TO CHECK OUT!</b>\n\n"
        f"{get_random_message(greetings)}\n\n"
        "Tidak terasa sudah memasuki penghujung hari kerja. "
        "Sebelum bersiap pulang, pastikan kalian sudah mengisi "
        "<b>Absensi Kantor melalui portal Monev</b> ya! 📝\n\n"
        f"{get_random_message(closings)}\n\n"
        "Silakan klik tombol di bawah untuk membuka portal absensi."
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔗 Buka Portal Absensi", "url": absen_url}]
        ]
    }
    return text, keyboard


def get_evening_photo_reminder() -> tuple:
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
        "jangan lupa mengambil dan mengirimkan <b>Foto Absen Pulang</b> ya! 📸\n\n"
        "🌟 <i>A little message before you go:</i>\n"
        f"<i>\"{quote}\"</i>\n\n"
        "Setelah semuanya selesai, waktunya beristirahat dan menikmati waktu untuk diri sendiri.\n\n"
        f"{get_random_message(closings)}"
    )
    return text, None


def send_telegram_http(text: str, reply_markup=None) -> dict:
    token = get_config_var("TELEGRAM_BOT_TOKEN")
    chat_id = get_config_var("TARGET_CHAT_ID")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN belum diset di Vercel Environment Variables!")
    if not chat_id:
        raise ValueError("TARGET_CHAT_ID belum diset di Vercel Environment Variables!")

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        res_body = response.read().decode("utf-8")
        return json.loads(res_body)


def process_reminder_request(params: dict) -> tuple:
    """Mengolah parameter dan mengirim pesan, return (status_code, response_dict)"""
    # 1. Validasi secret
    configured_secret = get_config_var("CRON_SECRET", "attendance_secret_2026")
    req_secret = params.get("secret", [""])[0]

    if configured_secret and req_secret != configured_secret:
        return 401, {
            "status": "error",
            "message": "Unauthorized: secret parameter salah atau belum disertakan."
        }

    # 2. Cek tipe
    reminder_type = params.get("type", [""])[0].lower()
    if not reminder_type:
        return 200, {
            "status": "ready",
            "message": "Vercel Telegram Reminder API aktif!",
            "target_chat": get_config_var("TARGET_CHAT_ID"),
            "usage": "/api/send?type=morning&secret=..."
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
        return 400, {
            "status": "error",
            "message": f"Tipe '{reminder_type}' tidak valid. Gunakan: morning, attendance, atau evening."
        }

    # 3. Kirim via HTTP Telegram Bot API
    tg_result = send_telegram_http(text, keyboard)
    return 200, {
        "status": "success",
        "job": job_label,
        "type": reminder_type,
        "telegram_response": tg_result.get("ok", False)
    }


# ==========================================
# WSGI Application (Standar Vercel Python)
# ==========================================
def app(environ, start_response):
    try:
        query_string = environ.get("QUERY_STRING", "")
        params = urllib.parse.parse_qs(query_string)
        status_code, data = process_reminder_request(params)
    except Exception as e:
        status_code = 500
        data = {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

    status_str = f"{status_code} OK" if status_code == 200 else f"{status_code} Error"
    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Access-Control-Allow-Origin", "*")
    ]
    start_response(status_str, headers)
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    return [body]


# ==========================================
# BaseHTTPRequestHandler (Fallback Vercel)
# ==========================================
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            status_code, data = process_reminder_request(params)
        except Exception as e:
            status_code = 500
            data = {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_POST(self):
        self.do_GET()

    def log_message(self, format, *args):
        pass


application = app
