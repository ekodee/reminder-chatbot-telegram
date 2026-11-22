import unittest
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import config
from src.messages import (
    load_quotes,
    get_random_quote,
    get_morning_reminder,
    get_attendance_reminder,
    get_evening_photo_reminder,
)
from src.scheduler import is_workday_now


class TestAttendanceReminderBot(unittest.TestCase):
    def test_config_loaded(self):
        self.assertTrue(len(config.TELEGRAM_BOT_TOKEN) > 0)
        self.assertEqual(config.ABSEN_URL, "https://monev.maganghub.kemnaker.go.id")
        self.assertEqual(config.TIMEZONE, "Asia/Jakarta")
        self.assertTrue(config.WORK_DAYS_ONLY)

    def test_quotes_file_loaded(self):
        quotes = load_quotes()
        self.assertIn("morning_quotes", quotes)
        self.assertIn("evening_quotes", quotes)
        self.assertGreater(len(quotes["morning_quotes"]), 0)
        self.assertGreater(len(quotes["evening_quotes"]), 0)

    def test_random_quotes(self):
        mq = get_random_quote("morning_quotes")
        eq = get_random_quote("evening_quotes")
        self.assertIsInstance(mq, str)
        self.assertIsInstance(eq, str)
        self.assertGreater(len(mq), 5)
        self.assertGreater(len(eq), 5)

    def test_morning_reminder(self):
        text, markup = get_morning_reminder()
        self.assertIn("GOOD MORNING", text)
        self.assertIn("Foto Pagi", text)
        self.assertIsNone(markup)

    def test_attendance_reminder(self):
        text, markup = get_attendance_reminder()
        self.assertIn("TIME TO CHECK OUT", text)
        self.assertIn("Absensi Kantor", text)
        self.assertIsNotNone(markup)
        # Verify inline keyboard has the attendance link button
        button = markup.inline_keyboard[0][0]
        self.assertEqual(button.url, "https://monev.maganghub.kemnaker.go.id")
        self.assertIn("Portal Absensi", button.text)

    def test_evening_photo_reminder(self):
        text, markup = get_evening_photo_reminder()
        self.assertIn("THAT'S A WRAP", text)
        self.assertIn("Foto Absen Pulang", text)
        self.assertIsNone(markup)

    def test_is_workday(self):
        # Should return a boolean without throwing an error
        result = is_workday_now()
        self.assertIsInstance(result, bool)

    def test_scheduler_jobs_registration(self):
        from telegram.ext import ApplicationBuilder
        from src.scheduler import setup_scheduler

        app = ApplicationBuilder().token("123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ").build()
        setup_scheduler(app)
        jobs = app.job_queue.jobs()
        job_names = [j.name for j in jobs]

        self.assertIn("reminder_foto_pagi_0840", job_names)
        self.assertIn("reminder_absen_kantor_1700", job_names)
        self.assertIn("reminder_foto_pulang_1730", job_names)
        self.assertEqual(len(job_names), 3)



if __name__ == "__main__":
    unittest.main()
