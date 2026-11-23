import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

# Load .env file
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    TARGET_CHAT_ID: str = os.getenv("TARGET_CHAT_ID", "").strip()
    ABSEN_URL: str = os.getenv("ABSEN_URL", "https://monev.maganghub.kemnaker.go.id").strip()
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Jakarta").strip()
    WORK_DAYS_ONLY: bool = os.getenv("WORK_DAYS_ONLY", "true").lower() in ("true", "1", "yes")
    CRON_SECRET: str = os.getenv("CRON_SECRET", "attendance_secret_2026").strip()

    @classmethod
    def set_target_chat_id(cls, chat_id: str) -> None:
        """Update TARGET_CHAT_ID di memori dan simpan ke file .env"""
        cls.TARGET_CHAT_ID = str(chat_id)
        if ENV_PATH.exists():
            content = ENV_PATH.read_text(encoding="utf-8")
            lines = content.splitlines()
            found = False
            new_lines = []
            for line in lines:
                if line.startswith("TARGET_CHAT_ID="):
                    new_lines.append(f"TARGET_CHAT_ID={chat_id}")
                    found = True
                else:
                    new_lines.append(line)
            if not found:
                new_lines.append(f"TARGET_CHAT_ID={chat_id}")
            ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        else:
            ENV_PATH.write_text(f"TARGET_CHAT_ID={chat_id}\n", encoding="utf-8")


config = Config()
