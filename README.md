# reminder-chatbot-telegram

Bot Telegram pengingat absensi kantor dan foto harian otomatis.

## Jadwal Pengingat (Senin - Jumat WIB)
1. **08:40 WIB**: Reminder Foto Pagi & Kata Motivasi Semangat Kerja.
2. **17:00 WIB**: Reminder Absensi Kantor + Tombol Link Absen ([monev.maganghub.kemnaker.go.id](https://monev.maganghub.kemnaker.go.id)).
3. **17:30 WIB**: Reminder Foto Absen Pulang & Kata Penutup / Istirahat.

## Fitur
- Pengiriman otomatis berbasis zona waktu `Asia/Jakarta` (WIB).
- Hanya aktif pada hari kerja (Senin s/d Jumat).
- Tombol Inline Keyboard untuk membuka link absen langsung.
- Kata-kata motivasi dan penutup bervariasi setiap hari (dari `quotes.json`).
- Perintah interaktif untuk testing dan diagnosa: `/start`, `/get_id`, `/status`, `/test_morning`, `/test_absen`, `/test_evening`.
