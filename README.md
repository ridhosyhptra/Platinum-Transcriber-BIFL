# 🏆 PLATINUM TRANSCRIBER AI 🏆
*(Scroll down for the Indonesian Version / Gulir ke bawah untuk versi Bahasa Indonesia)*

**Edition:** V7.0 (Faster-Whisper, SQLite Analytics & Portable FFmpeg)  
**Document Nature:** README & Essential Operational Guide

---

## 🇬🇧 PART 1: PROJECT OVERVIEW & FEATURES
Enterprise-grade software combining Data Structure Optimized 100% Offline capability with Cloud AI options (DeepL & AssemblyAI). Designed for the "Buy It For Life" philosophy.

### 🧠 High-Level Architecture & V7.0 Upgrades
* **Faster-Whisper Engine (New in V7):** Replaced standard Whisper with CTranslate2 (C++ based engine). Transcription is now 3x to 4x faster with a significantly cooler RAM footprint.
* **100% Plug-and-Play (Portable FFmpeg):** FFmpeg is now injected directly into the `.exe` memory. End-users no longer need to install any system dependencies. Just click and run.
* **Analytics Dashboard (SQLite):** Built-in lightweight database tracking transcription history, processing duration, and engine used. Accessible via the "📊 HISTORY" button.
* **I/O Streaming Architecture:** The application does not stack text in RAM. It writes directly to the Hard Drive per sentence (O(1) Memory Footprint). 
* **Thread-Safe UI & Auto-Theme:** The interface is separated from the AI brain using a Queue system. It responds instantly to Windows Dark/Light mode changes without freezing.
* **Automatic API Protection:** Fallback logic ensures that if DeepL/AssemblyAI quotas run out, the app silently switches to Google Translate without crashing.
* **High-Precision Output:** Provides `.srt`, `.vtt`, `.txt` with absolute time formatting `[02:05]`, and auto-renders to `.docx` and `.pdf`.

---

## 🇬🇧 PART 2: INSTALLATION & BUILD GUIDE

### 👤 For End-Users (Colleagues / Clients)
You **DO NOT** need to install Python, FFmpeg, or run any setup scripts.
1. Download the `PlatinumTranscriber_V7.zip` file from the Releases page.
2. Extract the `.zip` file to your Desktop.
3. Open the `dist` folder and double-click **`PlatinumTranscriber.exe`**.
*(Note: See the Troubleshooting section below if Windows displays a blue "Protected your PC" warning).*

### 🛠️ For Developers (Building the .EXE from Source)
If you want to compile this code yourself:
1. Download the raw `ffmpeg.exe` (~100MB) and place it next to `PlatinumTranscriber.py`.
2. Double-click the `2_Build_Platinum.bat` script.
3. The script will create a Sterile Virtual Environment, download `faster-whisper`, inject the portable `ffmpeg.exe`, and compile everything into a single, standalone `.exe` inside the `dist` folder.

---

## 🇬🇧 PART 3: MASTERPLAN SOP (OPERATIONAL GUIDE)

### PHASE 1: System Safety Inspection (*Pre-Flight Check*)
1. Open the application and click the orange **🔍 SYSTEM DIAGNOSTICS** button.
2. Check the pop-up window:
   * **Internet:** Must be "✅" for initial AI model downloads, YouTube extraction, or Cloud APIs.
   * **FFmpeg Engine:** Will display "✅ (Portable)" indicating Plug-and-Play is active.
   * **RAM & Storage:** Ensure sufficient space based on your selected engine.

### PHASE 2: Input Parameter Selection (Tab 1)
* **Option A: YouTube Link:** Paste the URL. Requires light internet (~30MB/hour) just to extract audio.
* **Option B: Local File (Batch / 100% Offline):** Select multiple `.mp4` or `.mp3` files to process simultaneously.

### PHASE 3: AI Engine Load Assignment (Tab 1)
⚠️ **FIRST-RUN DOWNLOAD WARNING:** When selecting an engine for the **first time**, the app must download the "AI Brain". The green progress bar will move as it downloads. **Once complete, the engine is 100% Offline forever**.
* **Whisper SMALL:** Extremely fast, needs > 1.5GB RAM. Sharp accuracy for clear English. 
* **Whisper MEDIUM:** Slower, needs > 3.0GB RAM. Use ONLY for noisy audio or thick accents. 

### PHASE 4: Output & Translation Configuration (Tab 2)
1. **File Format:** Choose from `.srt`, `.vtt`, `.txt`, `.docx`, or `.pdf`.
2. **Translation:** Original Text (Offline), Google Translate (Free), DeepL AI (High precision, requires API Key).

### PHASE 5: Advanced Audio Processing & Cloud (Tab 3)
* **FFmpeg Noise Reduction:** Cleans background noise locally before AI processing.
* **Use AssemblyAI (Cloud Option):** Shifts workload to Cloud (*Auto Chapters, PII Redaction, Diarization*). Disables local Whisper. Requires an AssemblyAI API Key.

### PHASE 6: Execution, Telemetry & Analytics
1. Click the green **▶ START EXECUTION** button.
2. **Emergency (Soft E-Stop):** Click the red **⏹ ABORT (E-STOP)** button to safely cut data and halt the process.
3. **Analytics:** After completion, click **📊 HISTORY** at the top right to view the log of your processed files and their execution times.

---

## 🇬🇧 PART 4: SECURITY & TROUBLESHOOTING

### 🛡️ False Positive Antivirus (Windows Protected Your PC)
When opening the `.exe` for the first time, Windows Defender might show a blue warning screen. **This is not a virus.** Because this is an independent project without a paid corporate "Digital Certificate," Windows flags it as an "Unknown Publisher." The PyInstaller packaging method also triggers overly sensitive antivirus heuristics. 
* **How to Bypass:** Click **"More Info"** -> click **"Run Anyway"**.

### 💰 API Key Cost Facts (Will it suddenly charge fees?)
**NO.** Both DeepL and AssemblyAI enforce a *Hard Limit*. If your free quota runs out, the service will not bill you; it will simply refuse to translate. 
*Fail-Safe:* If your DeepL quota is exhausted, Platinum Transcriber will **automatically divert to the free Google Translate engine** without crashing.

---
<br><br>
---

## 🇮🇩 BAGIAN 1: RINGKASAN PROYEK & FITUR V7.0
Perangkat lunak tingkat *Enterprise* yang menggabungkan kemampuan 100% Offline dengan efisiensi Struktur Data, dipadukan opsi Cloud AI (DeepL & AssemblyAI).

### 🧠 Arsitektur Tingkat Tinggi & Peningkatan V7.0
* **Mesin Faster-Whisper (Baru di V7):** Mengganti Whisper standar dengan mesin berbasis C++ (CTranslate2). Transkripsi kini 3x hingga 4x lebih cepat dengan penggunaan RAM yang jauh lebih dingin.
* **100% Plug-and-Play (Portable FFmpeg):** `ffmpeg.exe` kini disuntikkan langsung ke dalam memori aplikasi. Pengguna akhir tidak perlu lagi repot menginstal *dependency* sistem. Tinggal klik dan jalan.
* **Dashboard Analitik (SQLite):** Database internal super ringan untuk melacak riwayat transkripsi, durasi pemrosesan, dan mesin yang digunakan. Dapat diakses melalui tombol "📊 RIWAYAT".
* **I/O Streaming Architecture:** Aplikasi ini tidak menumpuk teks di RAM. Ia langsung menulis ke Hardisk per kalimat (O(1) Memory Footprint).
* **Thread-Safe UI & Auto-Theme:** Antarmuka dipisahkan dari otak AI menggunakan sistem Antrean (*Queue*). UI akan merespons seketika jika Anda mengubah tema Windows (Gelap/Terang) tanpa membuat aplikasi *freeze*.
* **Proteksi API Otomatis:** Jika limit API DeepL/AssemblyAI habis, AI akan otomatis melakukan *fallback* ke Google Translate gratis tanpa membuat aplikasi *crash*.

---

## 🇮🇩 BAGIAN 2: PANDUAN INSTALASI & KOMPILASI

### 👤 Untuk Pengguna Akhir (Rekan / Klien)
Anda **TIDAK PERLU** menginstal Python, FFmpeg, atau menjalankan skrip *setup* apa pun.
1. Unduh file `PlatinumTranscriber_V7.zip` dari halaman rilis (*Releases*).
2. Ekstrak folder zip tersebut (misalnya di Desktop).
3. Buka folder `dist`, lalu klik ganda file **`PlatinumTranscriber.exe`**.
*(Catatan: Lihat bagian Keamanan di bawah jika Windows memunculkan layar biru peringatan).*

### 🛠️ Untuk Pengembang (Kompilasi dari Source Code)
Jika Anda ingin membungkus ulang kode ini:
1. Unduh file `ffmpeg.exe` mentah (~80MB) dan letakkan sejajar dengan `PlatinumTranscriber.py`.
2. Klik ganda skrip `2_Build_Platinum.bat`.
3. Skrip akan membuat Ruang Isolasi, mengunduh pustaka `faster-whisper`, menyuntikkan `ffmpeg.exe`, dan mengkompilasinya menjadi satu file `.exe` yang utuh di dalam folder `dist`.

---

## 🇮🇩 BAGIAN 3: MASTERPLAN SOP (PANDUAN OPERASIONAL)

### FASE 1: Inspeksi Keselamatan Sistem (*Pre-Flight Check*)
1. Buka aplikasi dan klik tombol oranye **🔍 DIAGNOSTIK SISTEM**.
2. Periksa jendela *pop-up*:
   * **Internet:** Harus "✅" untuk unduhan mesin AI pertama kali atau penggunaan API Cloud.
   * **FFmpeg Engine:** Akan menampilkan "✅ (Portable)" yang menandakan fitur Plug-and-Play aktif.
   * **RAM & Storage:** Pastikan sisa ruang memadai sesuai mesin AI yang dipilih.

### FASE 2: Pemilihan Parameter Input (Tab 1)
* **Opsi A: Link YouTube:** Membutuhkan internet ringan (~30MB/jam video) hanya untuk ekstrak audio.
* **Opsi B: File Lokal (Batch / 100% Offline):** Pilih beberapa file `.mp4` atau `.mp3` sekaligus untuk diproses berurutan.

### FASE 3: Penetapan Beban Mesin AI (Tab 1)
⚠️ **PERINGATAN INISIASI PERTAMA (FIRST-RUN DOWNLOAD):** Saat menjalankan mesin AI untuk **pertama kali**, aplikasi wajib mengunduh *file* "Otak AI". Bilah progres hijau akan bergerak menandakan unduhan. **Setelah selesai, mesin 100% Offline seumur hidup**.
* **Whisper SMALL:** Sangat cepat, butuh RAM > 1.5GB. Akurasi sangat tajam untuk bahasa Inggris.
* **Whisper MEDIUM:** Lebih lambat, butuh RAM > 3.0GB. Gunakan HANYA jika audio bising atau logat kental.

### FASE 4: Konfigurasi Output & Terjemahan (Tab 2)
1. **Format File:** Pilih antara `.srt`, `.vtt`, `.txt`, `.docx`, atau `.pdf`.
2. **Opsi Terjemahan:** Teks Original (Offline), Google Translate (Gratis), DeepL AI (Presisi tinggi, butuh API Key).

### FASE 5: Pemrosesan Audio Lanjutan & Cloud (Tab 3)
* **FFmpeg Noise Reduction:** Membersihkan audio bising secara lokal sebelum diproses AI.
* **Gunakan AssemblyAI (Cloud):** Mematikan mesin lokal. Memindahkan beban ke server *Cloud* (*Auto Chapters, Redaksi PII, Diarization*). Wajib memasukkan API Key.

### FASE 6: Eksekusi, Telemetri & Analitik
1. Klik tombol hijau **▶ MULAI EKSEKUSI**.
2. **Keadaan Darurat (Soft E-Stop):** Klik tombol merah **⏹ BATALKAN (E-STOP)** untuk memotong data dengan rapi dan berhenti dengan aman.
3. **Analitik:** Setelah selesai, klik tombol **📊 RIWAYAT** di pojok kanan atas untuk melihat catatan log durasi pemrosesan setiap file Anda.

---

## 🇮🇩 BAGIAN 4: KEAMANAN & PEMECAHAN MASALAH

### 🛡️ Peringatan Antivirus (Windows Protected Your PC)
Saat membuka file `.exe` untuk pertama kalinya, Windows Defender mungkin akan memunculkan layar biru peringatan. **Ini bukanlah virus.**
Karena ini adalah proyek independen dan tidak memiliki "Sertifikat Digital" berbayar dari Microsoft, Windows melabelinya sebagai "Penerbit Tidak Dikenal" (*Unknown Publisher*). Selain itu, metode pembungkusan `PyInstaller` sering memicu kecurigaan sistem keamanan.
* **Cara Melewati (Safety Bypass):** Klik tulisan **"More Info"** (Info lebih lanjut) -> lalu klik tombol **"Run Anyway"** (Tetap jalankan).

### 💰 Fakta Biaya API Key (Apakah akan tiba-tiba berbayar?)
**TIDAK.** Layanan DeepL dan AssemblyAI menerapkan sistem *Hard Limit*. Jika kuota gratis Anda habis, layanan **tidak akan menagih biaya** ke kartu/akun Anda, melainkan hanya akan menolak permintaan terjemahan.
*Sistem Mitigasi:* Jika kuota DeepL habis, aplikasi Platinum Transcriber **tidak akan crash**, melainkan **otomatis mengambil alih tugas tersebut menggunakan Google Translate**.