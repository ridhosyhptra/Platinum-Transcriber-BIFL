# 🏆 Platinum Standard AI Transcriber (Ultimate Masterplan Edition)

*(Scroll down for Indonesian / Gulir ke bawah untuk Bahasa Indonesia)*

## 🇬🇧 ENGLISH VERSION
The Ultimate Local Transcription tool. 100% Offline capability (Whisper AI) combined with Cloud AI options (DeepL & AssemblyAI) for Enterprise-grade processing.

### 💻 SYSTEM REQUIREMENTS & OS CHECK
Before running, ensure your OS is ready:
* **Windows:** Use the provided `.bat` scripts to install Python 3.12 and FFmpeg automatically.
* **macOS:** Open Terminal. Install Homebrew if you haven't: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. Then run: `brew install python ffmpeg`.
* **Linux (Ubuntu/Debian):** Open Terminal. Run: `sudo apt update && sudo apt install python3 python3-pip ffmpeg`.

### 🚀 INSTALLATION & BUILD (Universal Terminal)
Run this command to install all necessary engines:
`python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai`

To build the standalone `.exe` (Windows) or executable (Mac/Linux) with an icon:
`pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py`

### 🧠 FEATURES FAQ
* **Offline AI (Whisper):** SMALL (~460MB, >2GB RAM) for speed. MEDIUM (~1.5GB, >5GB RAM) for high precision.
* **Translations:** Original (Offline), Google Translate (Free, Light), DeepL (Needs API Key), Any-to-English.
* **AssemblyAI:** Advanced cloud features (Auto-Chapters, PII Redaction, Diarization). Needs an API Key.

---

## 🇮🇩 VERSI BAHASA INDONESIA
Alat Transkripsi Lokal Definitif. Kemampuan 100% Offline (Whisper AI) dipadukan dengan opsi Cloud AI (DeepL & AssemblyAI).

### 💻 PEMERIKSAAN OS & PERSIAPAN
* **Windows:** Gunakan skrip `.bat` yang disediakan untuk instalasi otomatis.
* **macOS:** Buka Terminal. Instal Homebrew, lalu jalankan: `brew install python ffmpeg`.
* **Linux:** Buka Terminal. Jalankan: `sudo apt update && sudo apt install python3 python3-pip ffmpeg`.

### 🚀 INSTALASI & BUILD KOMPILASI
Instal semua pustaka mesin melalui terminal:
`python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai`

Buat aplikasi mandiri berlogo (pastikan Anda punya gambar `logo.ico` di folder yang sama):
`pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py`

### 🧠 FITUR & KEMAMPUAN
* **Output Super Lengkap:** .srt, .vtt, .txt, .docx (Word), dan .pdf.
* **Sistem Diagnostik:** Mengecek RAM, Storage, dan koneksi sebelum AI bekerja untuk mencegah *Crash*.
* **Proteksi DeepL & AssemblyAI:** Jika Anda memilih opsi ini tapi lupa memasukkan API Key, sistem tidak akan *error*. Ia akan otomatis mengalihkan terjemahan ke Google Translate atau mematikan fitur AssemblyAI dengan aman.