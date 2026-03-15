# 🏆 Platinum Standard AI Transcriber (Ultimate Masterplan)

*(Scroll down for Indonesian / Gulir ke bawah untuk Bahasa Indonesia)*

## 🇬🇧 ENGLISH VERSION: THE ULTIMATE LOCAL TRANSCRIPTION
Enterprise-grade software combining 100% Offline capability (Whisper AI) with Cloud AI options (DeepL & AssemblyAI).

### 💻 OS PRE-FLIGHT CHECK & INSTALLATION
Before running, ensure your OS is ready:
* **Windows:** Use the provided `.bat` scripts to install Python 3.12 and FFmpeg automatically.
* **macOS:** Open Terminal. Install Homebrew if needed: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. Then run: `brew install python ffmpeg`.
* **Linux (Ubuntu/Debian):** Open Terminal. Run: `sudo apt update && sudo apt install python3 python3-pip ffmpeg`.

### 🚀 UNIVERSAL BUILD COMMAND
Run this in your terminal to install all engines:
`python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter`

To compile into a standalone app with a logo (Ensure `logo.ico` is in the same folder):
`pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py`

---

## 🇮🇩 VERSI BAHASA INDONESIA: MANUAL OPERASIONAL ENTERPRISE
Alat Transkripsi Definitif. Kemampuan 100% Offline dipadukan dengan opsi Cloud AI.

### 💻 PEMERIKSAAN OS & PERSIAPAN
* **Windows:** Gunakan skrip `1_Setup_System.bat` untuk otomatisasi.
* **macOS:** Buka Terminal, instal Homebrew, lalu: `brew install python ffmpeg`.
* **Linux:** Buka Terminal, lalu: `sudo apt update && sudo apt install python3 python3-pip ffmpeg`.

### 🚀 INSTALASI & BUILD KOMPILASI
Terminal Universal untuk mengunduh pustaka:
`python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter`

Untuk membuat file `.exe` berlogo (Siapkan gambar bernama `logo.ico` di desktop):
`pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py`

### 🧠 FITUR & FAQ
* **Sumber Media:** YouTube Link (~30MB/jam) atau File Lokal BATCH (100% Offline).
* **AI Engine (Whisper):** SMALL (~460MB, Cepat, Sisa RAM >2GB). MEDIUM (~1.5GB, Presisi Tinggi, Sisa RAM >5GB). *Peringatan ukuran akan muncul saat pertama kali diunduh.*
* **Output:** `.srt`, `.vtt`, `.txt` (Format `[02:05]`), `.docx`, dan `.pdf`.
* **Proteksi API (DeepL/AssemblyAI):** Jika Anda memilih fitur berbayar tapi API Key kosong atau limit habis, sistem akan otomatis melakukan *fallback* (alih daya) ke opsi gratis (Google Translate) agar aplikasi tidak *crash*.
* **AssemblyAI Fitur Penuh:** Mendukung Auto-Chapters, Sensor PII (Data Pribadi), Diarization (Pendeteksi Pembicara), Custom Vocab, dan Filter Kata Pengisi (Filler words).