# 🏆 Platinum Standard AI Transcriber (Greatest Ultimate Edition)

*(Scroll down for Indonesian / Gulir ke bawah untuk Bahasa Indonesia)*

## 🇬🇧 ENGLISH VERSION: THE ULTIMATE LOCAL TRANSCRIPTION
Enterprise-grade software combining Data Structure Optimized 100% Offline capability (Whisper AI) with Cloud AI options (DeepL & AssemblyAI). Designed for the "Buy It For Life" philosophy.

### 💻 OS PRE-FLIGHT CHECK & INSTALLATION
Before compiling, ensure your operating system is ready:
* **Windows:** Use the provided `.bat` scripts to set up sterile virtual environments automatically.
* **macOS:** Open Terminal. Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. Then run: `brew install python ffmpeg`.
* **Linux (Ubuntu/Debian):** Open Terminal. Run: `sudo apt update && sudo apt install python3 python3-pip python3-venv ffmpeg`.

### 🚀 UNIVERSAL BUILD COMMAND (For Mac/Linux)
*(Windows users: Simply double-click `2_Build_Platinum.bat`)*
1. `python3 -m venv platinum_env`
2. `source platinum_env/bin/activate`
3. `pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter`
4. `pyinstaller --noconsole --onefile PlatinumTranscriber.py`

---

## 🇮🇩 VERSI BAHASA INDONESIA: MANUAL OPERASIONAL ENTERPRISE

### 💻 PEMERIKSAAN OS & PERSIAPAN OTOMATIS
* **Windows:** Klik ganda `1_Setup_System.bat` untuk memasukkan Python dan FFmpeg ke dalam laptop.
* **Mac/Linux:** Ikuti instruksi terminal di versi bahasa Inggris di atas.

### 🚀 INSTALASI & KOMPILASI (BUAT .EXE)
Klik ganda skrip `2_Build_Platinum.bat`. Skrip ini akan membuat "Ruang Isolasi" (Virtual Environment) agar file `.exe` yang dihasilkan sangat padat, ramping, dan bebas dari *library* sampah. 

### 🧠 FITUR & ARSITEKTUR TINGKAT TINGGI (FAQ)
* **I/O Streaming Architecture:** Aplikasi ini tidak menumpuk teks di RAM. Ia langsung menulis ke Hardisk per kalimat (O(1) Memory Footprint). Laptop Anda akan tetap dingin meski memproses video 10 jam.
* **Thread-Safe UI:** Antarmuka (Layar Monitor) dipisahkan dari otak AI menggunakan sistem Antrean (*Queue*), sehingga aplikasi 100% anti-freeze/Not Responding.
* **Soft E-Stop:** Tombol darurat yang akan menghentikan sistem dengan aman tanpa merusak *file* yang sedang diproses.
* **Proteksi API Otomatis:** Lupa memasukkan API Key DeepL/AssemblyAI? AI akan otomatis melakukan *fallback* (alih daya) ke Google Translate gratis atau mengabaikan instruksi *cloud* tanpa membuat aplikasi *crash*.
* **Output Presisi Tinggi:** Menyediakan `.srt`, `.vtt`, `.txt` dengan format waktu absolut `[02:05]`, hingga *render* otomatis ke `.docx` dan `.pdf`.