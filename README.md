# 🏆 Platinum Standard AI Transcriber (BIFL Edition)

*(Scroll down for the comprehensive Indonesian version / Gulir ke bawah untuk versi Bahasa Indonesia yang sangat detail)*

## 🇬🇧 ENGLISH VERSION

This is an Enterprise-grade, *Buy It For Life* (BIFL) software designed to transcribe audio/video to text and translate it with high precision. It operates **100% offline** on Windows, features a real-time Telemetry Dashboard, automatic Storage & RAM sensors, and guarantees absolute data privacy.

### 🛠️ PHASE 1: Automated Setup (For Beginners)
1. Download `Setup_Sistem.bat` from this repository.
2. Double-click it. Choose your language, read the prompt, and type 'Y' to install Python and FFmpeg automatically.
3. **CRITICAL:** Restart your PC once the terminal closes.

### 🚀 PHASE 2: Running the App
1. Download `PlatinumTranscriber.py` to your Desktop.
2. Open **Command Prompt (CMD)** and type:
   `pip install yt-dlp openai-whisper pyinstaller deep-translator deepl`
3. Navigate to Desktop: `cd Desktop`
4. Run the app: `python PlatinumTranscriber.py` *(Note: Click the language toggle at the top right to switch between English and Indonesian).*

### 🧠 COMPREHENSIVE FAQ & TROUBLESHOOTING
**1. Internet Usage: When exactly does it need data?**
* **First Run (Needs Data):** The first time you run a specific AI model, it downloads the "Brain" (Small: ~460MB, Medium: ~1.5GB). This happens only once.
* **100% Offline Mode (0 MB):** If you use "Local File" and "Original Text", you can turn off your Wi-Fi. It processes everything locally.
* **YouTube Links:** Uses ~30-50 MB/hour just to extract the audio track.
* **Translation:** Uses barely a few Kilobytes to send text lines to translation servers.

**2. Memory Errors: "enforce fail: not enough memory"**
* This means your laptop is out of **RAM (Working Memory)**, not Storage.
* **Solution:** Switch the AI Engine from MEDIUM to SMALL in the app, or close heavy applications like Chrome.

**3. Small vs Medium Models: Which one to choose?**
* **SMALL (~460 MB):** Like a "City Car". Fast, agile, needs only 2GB of free RAM. Excellent for clear English audio.
* **MEDIUM (~1.5 GB):** Like a "Heavy Duty Truck". Slower, needs 5GB of free RAM. Perfect for noisy backgrounds, heavy accents, or mixed languages.

**4. Batch Processing Large Files**
* You can select dozens of long videos at once. The AI processes them sequentially (one by one) to prevent laptop crashes. The outputs (`.txt` or `.srt`) will be saved separately matching the original video names.

**5. Cybersecurity & Privacy**
* **100% Secure.** In offline mode, not a single byte of your audio is uploaded. It is processed directly by your laptop's CPU.

---
---

## 🇮🇩 VERSI BAHASA INDONESIA (MANUAL OPERASIONAL LENGKAP)

Aplikasi ini adalah perangkat lunak tingkat *Enterprise* untuk mengubah suara menjadi teks (Transkripsi) dan menerjemahkannya. Dirancang beroperasi **100% offline**, dilengkapi Dasbor Telemetri, Sensor Keselamatan Sistem (RAM & Storage), dan menjaga privasi data secara absolut.

### 🛠️ FASE 1: Persiapan Sistem Otomatis (Untuk Pemula Total)
Jika Anda sama sekali tidak mengerti *coding*, ikuti langkah ini:
1. Unduh file `Setup_Sistem.bat` dari repositori ini ke laptop Anda.
2. Klik ganda (*double-click*) file tersebut.
3. Pilih bahasa, baca penjelasannya, dan ketik 'Y' (Enter) untuk menginstal Python (Mesin Utama) dan FFmpeg (Pengekstrak Audio) secara otomatis.
4. **SANGAT KRUSIAL:** Setelah terminal tertutup, Anda **WAJIB me-restart (hidupkan ulang)** laptop Anda agar mesin baru tersebut dikenali oleh Windows.

### 🚀 FASE 2: Instalasi Otak AI & Menjalankan Aplikasi
1. Unduh file `PlatinumTranscriber.py` dan letakkan di **Desktop** Anda.
2. Buka **Command Prompt (CMD)** dari menu Start Windows, ketik perintah ini lalu tekan Enter (Pastikan internet stabil):
   `pip install yt-dlp openai-whisper pyinstaller deep-translator deepl`
3. Arahkan CMD ke Desktop dengan mengetik: `cd Desktop`
4. Jalankan aplikasinya dengan mengetik: `python PlatinumTranscriber.py` 
*(Aplikasi akan terbuka. Anda bisa mengklik tombol di pojok kanan atas untuk mengubah bahasa antarmuka ke Bahasa Indonesia kapan saja).*

---

### 🧠 FASE 3: FAQ & PEMECAHAN MASALAH (WAJIB BACA)
Bagian ini merangkum seluruh potensi kendala di lapangan. Membaca ini akan mengubah Anda dari pengguna awam menjadi pengguna mahir (*proficient*).

#### 1. KONSUMSI INTERNET & KUOTA
**Q: Kapan persisnya aplikasi ini menyedot kuota internet saya?**
* **Pemakaian Pertama (Wajib Internet):** Saat Anda pertama kali menekan "MULAI", aplikasi akan mengunduh file "Otak AI". Ukurannya tergantung pilihan Anda (Model Small: ~460 MB, Model Medium: ~1.5 GB). Ini hanya terjadi **satu kali seumur hidup**.
* **Skenario 100% Offline (0 MB):** Jika Anda memproses "File Lokal" (video yang sudah ada di laptop) dan memilih "Teks Asli (Tanpa Terjemahan)", Anda bisa **mencabut Wi-Fi**. Mesin bekerja murni menggunakan tenaga prosesor (CPU) laptop Anda.
* **Skenario YouTube Link:** Aplikasi ini tidak mendownload gambar videonya, melainkan hanya mengekstrak suaranya. Sangat hemat, memakan sekitar **30-50 MB per jam durasi video**.
* **Skenario Terjemahan:** Hanya memakan kuota dalam ukuran **Kilobyte** (nyaris tidak terasa), karena ia hanya mengirim teks murni baris demi baris ke server Google/DeepL.

#### 2. KENDALA MEMORI (RAM VS STORAGE)
**Q: Muncul peringatan merah di terminal: "enforce fail... not enough memory: you tried to allocate...". Apa yang terjadi?**
* Ini **Bukan** karena Hardisk Anda penuh. Ini karena laptop Anda kehabisan **RAM (Memori Kerja)**. 
* Model Whisper (terutama ukuran Medium) saat bekerja akan membengkak di dalam sistem dan butuh ruang RAM Kosong yang sangat besar. Jika memori penuh, aplikasi akan membatalkan operasi agar laptop Anda tidak *Blue Screen* (Hang total).
* **Solusinya:** Tutup aplikasi berat lain (Chrome, Word, dll), ATAU ganti pilihan AI Engine Anda di aplikasi dari MEDIUM ke **SMALL**.

**Q: Apa bedanya memilih model Whisper SMALL dan MEDIUM?**
* **Whisper SMALL (~460 MB):** Ibarat **"Mobil Gesit / City Car"**. Sangat cepat, ringan, dan hanya butuh Sisa RAM Kosong 2 GB. Akurasi bahasa Inggrisnya sangat tajam (Cocok untuk rekaman bahasa Inggris yang jernih, podcast, materi IELTS).
* **Whisper MEDIUM (~1.5 GB):** Ibarat **"Truk Alat Berat"**. Lebih lambat dan butuh Sisa RAM Kosong minimal 5 GB. Namun, akurasinya absolut. Sangat tangguh untuk membedah audio dengan *background noise* (bising), logat asing yang kental, atau percakapan campur bahasa.

**Q: Bagaimana jika Hardisk (Storage) laptop saya penuh di tengah jalan?**
* Aplikasi ini dilengkapi **Pre-Flight Storage Sensor**. Sebelum mesin menyala, ia akan menginspeksi *hardisk* Anda. Jika sisa ruang kurang dari 2 GB, aplikasi menolak perintah dan meminta Anda mengosongkan ruang terlebih dahulu. File Anda dijamin tidak akan korup.

#### 3. PEMROSESAN FILE RAKSASA & MOBILITAS
**Q: Saya punya banyak video berjam-jam (ratusan MB). Apakah bisa dimasukkan sekaligus?**
* **Bisa.** Anda bisa memblok (sorot) puluhan video sekaligus (Batch Processing). Mesin akan memprosesnya **satu per satu secara berurutan**, bukan sekaligus. Jika Video 1 selesai, ia lanjut ke Video 2. Sangat aman ditinggal tidur. Pastikan laptop dicolok ke *charger*.
* **Q: Apakah hasil teksnya akan tercampur?**
* **Tidak.** Output (`.srt` atau `.txt`) akan dipisah dan dinamai persis sesuai nama video aslinya.

**Q: Bagaimana cara menggunakan hasilnya untuk belajar di HP?**
* Proses video di laptop dan pilih format **Subtitles (.srt)**. Pastikan nama video dan nama file `.srt` tersebut sama persis (misal: `Materi.mp4` dan `Materi.srt`). Pindahkan keduanya ke dalam satu folder di HP Anda. Gunakan aplikasi **VLC Player** di HP untuk memutarnya. Teks akan muncul otomatis.

#### 4. CYBERSECURITY & COMPILER WARNINGS
**Q: Amankah untuk merekam dan mentranskripsi data rahasia proyek/perusahaan?**
* **100% Aman.** Saat Anda menggunakan mode File Lokal (Offline), mesin Whisper AI membedah gelombang suara di dalam laptop Anda sendiri. Tidak ada satu pun data yang diunggah ke *server* pihak ketiga.

**Q: Jika saya ingin mengubah script Python ini menjadi aplikasi .exe, saya melihat tulisan kuning "WARNING" di terminal (seperti 'nvcuda.dll' atau 'module named js'). Apakah itu error?**
* **Bukan Error.** Itu sangat aman. PyInstaller sering mencari pustaka ekstra yang didesain untuk sistem operasi Linux atau kartu grafis (GPU) tingkat tinggi. Karena Anda menggunakan Windows standar, PyInstaller sekadar "melaporkan" bahwa ia mengabaikan file tersebut. Selama tulisan akhirnya adalah "Successfully", aplikasi `.exe` Anda siap digunakan.

**Q: Jika saya meng-compile ulang aplikasinya (atau menghapus folder 'build' dan 'dist'), apakah otak AI berukuran 1.5 GB yang sudah saya download akan terhapus?**
* **Tidak Akan Terhapus.** Folder `build` dan `dist` hanyalah sampah sisa konstruksi. File "Otak AI" Anda disimpan secara permanen di brankas tersembunyi sistem Windows (`C://Users/NamaUser/.cache/whisper`). Anda bisa meng-compile kode ratusan kali dan file AI raksasa tersebut akan tetap aman.