# 🏆 PLATINUM STANDARD AI TRANSCRIBER (Greatest Ultimate Edition) 🏆
*(Scroll down for the Indonesian Version / Gulir ke bawah untuk versi Bahasa Indonesia)*

**Edition:** Ultimate V6 (Data Structure & I/O Streaming Optimized)  
**Document Nature:** README & Essential Operational Guide

---

## 🇬🇧 PART 1: PROJECT OVERVIEW & FEATURES
Enterprise-grade software combining Data Structure Optimized 100% Offline capability (Whisper AI) with Cloud AI options (DeepL & AssemblyAI). Designed for the "Buy It For Life" philosophy.

### 🧠 High-Level Architecture & Features
* **I/O Streaming Architecture:** The application does not stack text in RAM. It writes directly to the Hard Drive per sentence (O(1) Memory Footprint). Your laptop remains cool even when processing a 10-hour video.
* **Thread-Safe UI:** The interface (Monitor Screen) is separated from the AI brain using a Queue system, making the app 100% anti-freeze/Not Responding.
* **Soft E-Stop:** An emergency button that safely halts the system without corrupting the files currently being processed.
* **Automatic API Protection:** Forgot to input your DeepL/AssemblyAI API Key? The AI will automatically fallback to the free Google Translate or safely ignore cloud instructions without crashing.
* **High-Precision Output:** Provides `.srt`, `.vtt`, `.txt` with absolute time formatting `[02:05]`, and auto-renders to `.docx` and `.pdf`.

---

## 🇬🇧 PART 2: INSTALLATION & BUILD GUIDE (README)

### 💻 OS Pre-Flight Check & Setup
Before compiling, ensure your operating system is ready:
* **Windows:** Simply double-click the provided `1_Setup_System.bat` script to install Python and FFmpeg automatically. **Restart your PC afterward.**
* **macOS:** Open Terminal. Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. Then run: `brew install python ffmpeg`.
* **Linux (Ubuntu/Debian):** Open Terminal. Run: `sudo apt update && sudo apt install python3 python3-pip python3-venv ffmpeg`.

### 🚀 Compilation (Building the .EXE / App)
* **For Windows:** Double-click the `2_Build_Platinum.bat` script. This creates a "Sterile Virtual Environment" so the resulting `.exe` is compact and free of junk libraries. The final app will appear in the `dist` folder.
* **For Mac/Linux (Run these in Terminal):**
  1. `python3 -m venv platinum_env`
  2. `source platinum_env/bin/activate`
  3. `pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter`
  4. `pyinstaller --noconsole --onefile PlatinumTranscriber.py`

---

## 🇬🇧 PART 3: MASTERPLAN SOP (OPERATIONAL GUIDE)

### PHASE 1: System Safety Inspection (*Pre-Flight Check*)
1. Open the **PlatinumTranscriber.exe** application.
2. Click the orange **🔍 SYSTEM DIAGNOSTICS** button at the top.
3. Check the pop-up window:
   * **Internet:** Must be "✅" if this is the first use, or to use YouTube, DeepL, or AssemblyAI.
   * **FFmpeg:** Must be "✅" to process audio.
   * **RAM Free:** Match with the AI engine you will select (Minimum > 2GB).
   * **Storage Free:** Ensure at least 5 GB of free space.

### PHASE 2: Input Parameter Selection (Tab 1)
* **Option A: YouTube Link:** Paste the URL. Requires light internet (~30MB/hour) just to extract audio.
* **Option B: Local File (100% Offline):** Select `.mp4` or `.mp3` files. Supports Batch Processing.

### PHASE 3: AI Engine Load Assignment (Tab 1)
⚠️ **FIRST-RUN DOWNLOAD WARNING:** When selecting an engine for the **first time**, the app must download the "AI Brain". Ensure a stable connection. **Once complete, the engine is 100% Offline forever**.
* **Whisper SMALL (~460MB):** Extremely fast, needs > 2GB RAM. Sharp accuracy for clear English. *(Initial download: ~2-5 mins).*
* **Whisper MEDIUM (~1.5GB):** Slower, needs > 5GB RAM. Use ONLY for noisy audio or thick accents. *(Initial download: ~10-20 mins).*

### PHASE 4: Output & Translation Configuration (Tab 2)
1. **File Format:** `.srt`/`.vtt` (Video), `.txt` (Reading), `.docx`/`.pdf` (Auto-rendered documents).
2. **Translation:** Original Text (Offline), Google Translate (Free/Light), DeepL AI (High precision, requires API Key).

### PHASE 5: Advanced Audio Processing & Cloud (Tab 3)
* **FFmpeg Noise Reduction:** Cleans background noise locally before AI processing.
* **Use AssemblyAI (Cloud Option):** Shifts workload to Cloud (*Auto Chapters, PII Redaction, Diarization*). Disables local Whisper. Requires AssemblyAI API Key.

### PHASE 6: Execution, Telemetry & E-Stop
1. Click the green **▶ START EXECUTION** button.
2. **Monitor Telemetry:** If this is the **First Use**, the console will appear idle during the 460MB/1.5GB background download. **This is not an error.**
3. **Emergency (Soft E-Stop):** Click the red **⏹ ABORT (E-STOP)** button to safely cut data and halt the process.

### PHASE 7: Harvesting
* Final files will automatically be placed on your **Desktop** with the exact original filename.

---

## 🇬🇧 PART 4: API KEY PROCUREMENT & TROUBLESHOOTING

### A. Cost Facts & Financial Security
**WILL IT SUDDENLY CHARGE FEES? NO.** Both API services enforce a *Hard Limit*. If your free quota runs out, the service will not bill you; it will simply refuse to translate. 
*Fail-Safe:* If your DeepL quota is exhausted, Platinum Transcriber will **automatically divert to the free Google Translate engine** without crashing.

### B. How to Get a DeepL API Key (Free 500k chars/month)
1. Visit: **www.deepl.com/pro-api**
2. Click **"Sign up for free"** on the **DeepL API Free** plan.
3. *Security Verification:* DeepL asks for Card data ONLY as an anti-bot measure. **You will not be charged.**
4. Once logged in, go to **"Account"** > **"API Keys"**.
5. Click **"Create a new API Key"**, copy the code, and paste it into **Tab 2** of the app.

### C. How to Get an AssemblyAI API Key (Large free quota)
1. Visit: **www.assemblyai.com**
2. Click **"Start for Free"**. Create an account using Google/Gmail.
3. On the **Dashboard**, find the **"Your API Key"** box on the right.
4. Copy the code and paste it into **Tab 3** of the app.

### 🚨 Troubleshooting Guide
| Indication | Root Cause | Solution |
| :--- | :--- | :--- |
| **App sits idle long when started** | Downloading the "AI Brain" (First use). | Wait patiently. Ensure internet is stable. |
| **"Not enough RAM"** | Free RAM is below safe limits. | Close Chrome/Word, or downgrade AI to SMALL. |
| **API Limit Error** | DeepL quota exhausted. | Ignore. System auto-fallbacks to Google Translate. |
| **Screen responds slowly** | CPU is working at 100%. | Do not click repeatedly. The *Queue* prevents freezing. |

<br><br>

---
---

## 🇮🇩 BAGIAN 1: RINGKASAN PROYEK & FITUR
Perangkat lunak tingkat *Enterprise* yang menggabungkan kemampuan 100% Offline (Whisper AI) dengan efisiensi Struktur Data, dipadukan opsi Cloud AI (DeepL & AssemblyAI).

### 🧠 Arsitektur Tingkat Tinggi & Fitur
* **I/O Streaming Architecture:** Aplikasi ini tidak menumpuk teks di RAM. Ia langsung menulis ke Hardisk per kalimat (O(1) Memory Footprint). Laptop Anda akan tetap dingin meski memproses video 10 jam.
* **Thread-Safe UI:** Antarmuka (Layar Monitor) dipisahkan dari otak AI menggunakan sistem Antrean (*Queue*), sehingga aplikasi 100% anti-freeze/Not Responding.
* **Soft E-Stop:** Tombol darurat yang akan menghentikan sistem dengan aman tanpa merusak *file* yang sedang diproses.
* **Proteksi API Otomatis:** Lupa memasukkan API Key DeepL/AssemblyAI? AI akan otomatis melakukan *fallback* (alih daya) ke Google Translate gratis atau mengabaikan instruksi *cloud* tanpa membuat aplikasi *crash*.
* **Output Presisi Tinggi:** Menyediakan `.srt`, `.vtt`, `.txt` dengan format waktu absolut `[02:05]`, hingga *render* otomatis ke `.docx` dan `.pdf`.

---

## 🇮🇩 BAGIAN 2: PANDUAN INSTALASI & KOMPILASI (README)

### 💻 Pemeriksaan OS & Persiapan Otomatis
Sebelum kompilasi, pastikan sistem Anda siap:
* **Windows:** Klik ganda skrip `1_Setup_System.bat` untuk menginstal Python dan FFmpeg secara otomatis. **Wajib Restart Laptop setelah selesai.**
* **Mac/Linux:** Ikuti instruksi terminal di versi bahasa Inggris di atas (menggunakan Homebrew atau apt).

### 🚀 Instalasi & Kompilasi (Membuat .EXE)
* **Untuk Windows:** Klik ganda skrip `2_Build_Platinum.bat`. Skrip ini akan membuat "Ruang Isolasi" (Virtual Environment) agar file `.exe` yang dihasilkan sangat padat, ramping, dan bebas dari *library* sampah. Aplikasi final ada di dalam folder `dist`.
* **Untuk Mac/Linux:** Jalankan 4 baris perintah terminal yang ada di panduan bahasa Inggris di atas.

---

## 🇮🇩 BAGIAN 3: MASTERPLAN SOP (PANDUAN OPERASIONAL)

### FASE 1: Inspeksi Keselamatan Sistem (*Pre-Flight Check*)
1. Buka aplikasi **PlatinumTranscriber.exe**.
2. Klik tombol oranye **🔍 DIAGNOSTIK SISTEM** di bagian atas.
3. Periksa jendela *pop-up*:
   * **Internet:** Harus "✅" jika ini penggunaan pertama, atau ingin menggunakan YouTube, DeepL, AssemblyAI.
   * **FFmpeg:** Harus "✅" untuk memproses audio.
   * **RAM Free:** Pastikan sisa RAM sesuai mesin AI yang dipilih (> 2GB).
   * **Storage Free:** Pastikan sisa ruang Hardisk minimal 5 GB.

### FASE 2: Pemilihan Parameter Input (Tab 1)
* **Opsi A: Link YouTube:** Membutuhkan internet ringan (~30MB/jam video) hanya untuk ekstrak audio.
* **Opsi B: File Lokal (100% Offline):** Pilih file `.mp4` atau `.mp3`. Mendukung *Batch Processing*.

### FASE 3: Penetapan Beban Mesin AI (Tab 1)
⚠️ **PERINGATAN INISIASI PERTAMA (FIRST-RUN DOWNLOAD):** Saat menjalankan mesin AI untuk **pertama kali**, aplikasi wajib mengunduh *file* "Otak AI" ke brankas sistem. **Setelah unduhan pertama selesai, mesin 100% Offline seumur hidup**.
* **Whisper SMALL (~460MB):** Sangat cepat, butuh RAM > 2GB. Akurasi tajam untuk bahasa Inggris jelas. *(Lama unduhan: ~2-5 menit).*
* **Whisper MEDIUM (~1.5GB):** Lebih lambat, butuh RAM > 5GB. Gunakan HANYA jika audio bising atau logat kental. *(Lama unduhan: ~10-20 menit).*

### FASE 4: Konfigurasi Output & Terjemahan (Tab 2)
1. **Format File:** `.srt`/`.vtt` (Video), `.txt` (Waktu Murni), `.docx`/`.pdf` (*Render* otomatis).
2. **Opsi Terjemahan:** Teks Original (Offline), Google Translate (Gratis), DeepL AI (Presisi tinggi, butuh API Key).

### FASE 5: Pemrosesan Audio Lanjutan & Cloud (Tab 3)
* **FFmpeg Noise Reduction:** Membersihkan audio bising secara lokal.
* **Gunakan AssemblyAI (Cloud):** Mematikan mesin lokal. Memindahkan beban ke server *Cloud* (*Auto Chapters, Redaksi PII, Diarization*). Wajib memasukkan API Key.

### FASE 6: Eksekusi, Telemetri & E-Stop
1. Klik tombol hijau **▶ MULAI EKSEKUSI**.
2. **Layar Telemetri:** Jika ini **Penggunaan Pertama**, konsol akan terlihat diam setelah tulisan *"Memuat Whisper..."*. **INI BUKAN ERROR.** Mesin sedang mengunduh *file* di latar belakang.
3. **Keadaan Darurat (Soft E-Stop):** Klik tombol merah **⏹ BATALKAN (E-STOP)** untuk memotong data dengan rapi dan berhenti aman.

### FASE 7: Pengambilan Hasil (*Harvesting*)
* Seluruh *file* hasil akan otomatis diletakkan di **Desktop** Anda dengan nama yang sama dengan *file* aslinya.

---

## 🇮🇩 BAGIAN 4: PENGADAAN API KEY & PEMECAHAN MASALAH

### A. Fakta Biaya (Apakah Akan Tiba-tiba Berbayar?)
**TIDAK.** Kedua layanan API di bawah ini menerapkan sistem *Hard Limit*. Jika kuota gratis habis, layanan **tidak akan menagih biaya**. Layanan hanya akan menolak permintaan.
*Sistem Mitigasi:* Jika DeepL mati karena kehabisan kuota, aplikasi **tidak akan crash**, melainkan **otomatis mengalihkan tugas ke Google Translate**.

### B. Cara Mendapatkan DeepL API Key (Gratis 500.000 karakter/bulan)
1. Kunjungi: **www.deepl.com/pro-api**
2. Klik **"Sign up for free"** pada paket **DeepL API Free**.
3. *Verifikasi Keamanan:* DeepL meminta data Kartu Kredit HANYA sebagai anti-bot. **Saldo Anda tidak akan dipotong sepeser pun.**
4. Setelah *login*, masuk ke **"Account"** > **"API Keys"**.
5. Klik **"Create a new API Key"**, salin (*Copy*) kodenya, dan tempel (*Paste*) di **Tab 2** aplikasi Anda.

### C. Cara Mendapatkan AssemblyAI API Key (Gratis kuota besar)
1. Kunjungi: **www.assemblyai.com**
2. Klik **"Start for Free"**. Buat akun menggunakan Gmail.
3. Di halaman **Dashboard**, lihat kotak **"Your API Key"** di sebelah kanan.
4. Salin kodenya dan tempel di **Tab 3** aplikasi Anda.

### 🚨 Panduan Mitigasi Kendala (Troubleshooting)
| Indikasi Kendala | Akar Masalah | Tindakan Perbaikan (Solusi) |
| :--- | :--- | :--- |
| **Aplikasi diam lama saat distart** | Sedang mengunduh "Otak AI" (Penggunaan pertama). | Tunggu dengan sabar. Pastikan internet stabil. |
| **"RAM tidak cukup"** | Sisa RAM di bawah batas aman. | Tutup Chrome/Word, atau turunkan AI ke SMALL. |
| **API Limit Error** | Kuota DeepL habis. | Abaikan. Sistem otomatis melompat ke Google Translate. |
| **Layar sedikit lambat merespon** | CPU bekerja 100% memproses AI. | Jangan klik berulang kali. Sistem *Queue* mencegah *freeze*. |