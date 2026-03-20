# 🏆 PLATINUM TRANSCRIBER AI 🏆
*(Scroll down for the Indonesian Version / Gulir ke bawah untuk versi Bahasa Indonesia)*

**Edition:** V8.0 Enterprise  
**Document Nature:** README & Essential Operational Guide

| Topic | Link / note |
|--------|----------------|
| **Developer architecture** | [`docs/DEVELOPER.md`](docs/DEVELOPER.md) — threading, queues, extension points |
| **License** | [MIT](LICENSE) — update the copyright line if you publish under a company name |
| **CI (GitHub)** | [`.github/workflows/ci.yml`](.github/workflows/ci.yml) — `py_compile` on push/PR |
| **Sandbox (optional)** | `Test_Interactive_Text.py` — experimental karaoke-style sync (not bundled in main `.exe` workflow) |
| **Release notes (V8.0)** | [`RELEASE_NOTES_V8.0.md`](RELEASE_NOTES_V8.0.md) |
| **GitHub upload SOP** | [`docs/GITHUB_UPLOAD_MASTERPLAN_SOP.md`](docs/GITHUB_UPLOAD_MASTERPLAN_SOP.md) — wajib / opsional / dilarang upload |

Repository hygiene: [`.gitignore`](.gitignore) excludes `platinum_env/`, `dist/`, build artifacts, and local config patterns — safe defaults before `git push`.

---

## 🇬🇧 PART 1: PROJECT OVERVIEW & FEATURES (V8.0)

Enterprise-grade desktop app: **local Faster-Whisper** plus optional **cloud** (AssemblyAI, DeepL, Google). Batch files or YouTube audio; outputs go to **Desktop → `PlatinumTranscriber_Output`**.

### 🧠 V8.0 highlights (latest)
* **Live dictation:** Microphone → real-time transcription (Google Speech or local Whisper *tiny*), producer–consumer queue, thread-safe UI.
* **VAD (Voice Activity Detection):** Silero VAD via faster-whisper — skips long silence; adjustable sensitivity (low / med / high).
* **Word-level timestamps:** Optional per-word timing for SRT/VTT (and related exports); ~30% more processing when enabled.
* **Extended export formats:** `.json`, `.tsv`, `.sbv`, `.md`, `.ass` in addition to `.srt`, `.vtt`, `.txt`, `.docx`, `.pdf`.
* **Broad audio/video input:** Many extensions (MP3, WAV, M4A, FLAC, MP4, MKV, …) via bundled **FFmpeg**; warning logged for files **> 2 GB**.
* **Preferences:** UI choices persisted to `%USERPROFILE%\PlatinumConfig.json` (do not commit real API keys).

### 🧠 Core architecture (carried forward)
* **Faster-Whisper (CTranslate2):** Fast local inference; first run downloads models (then offline).
* **Portable FFmpeg:** `ffmpeg.exe` next to the app (or in PyInstaller bundle) prepended to `PATH` — no system install for end users.
* **SQLite analytics:** History of jobs (file, duration, engine) — **📊 HISTORY**.
* **Streaming I/O:** Transcript segments written incrementally — bounded memory vs. holding full text in RAM.
* **Thread-safe UI:** Worker thread talks to the UI only through `queue.Queue` (log, progress, UI callbacks).
* **API fallbacks:** DeepL / cloud issues can fall back to Google Translate where implemented.

---

## 🇬🇧 PART 2: INSTALLATION & BUILD

### 👤 For end users
You do **not** need Python or FFmpeg on PATH if you use the release **`.exe`**.
1. Download the release archive from **GitHub Releases** (or your distribution channel).  
   *Suggested asset name when you publish:* **`PlatinumTranscriber_V8.zip`** (contains `dist/PlatinumTranscriber.exe` or a single portable `.exe`, depending on how you package).
2. Extract anywhere (e.g. Desktop).
3. Open **`dist/PlatinumTranscriber.exe`** (or the single portable exe you ship).

*Windows “SmartScreen” may show “Unknown publisher” — see Part 4.*

### 🛠️ For developers (build `.exe` from source)
1. Place **`ffmpeg.exe`** and **`logo.ico`** in the same folder as `PlatinumTranscriber.py`.
2. Run **`2_Build_Platinum.bat`** (choose language in the menu).
3. The script creates **`platinum_env`**, installs dependencies (including `faster-whisper`, `customtkinter`, `pyaudio`, `SpeechRecognition`, `numpy`, `onnxruntime`, …), and runs **PyInstaller** with data collection for CustomTkinter / speech_recognition / onnxruntime.
4. Output: **`dist/PlatinumTranscriber.exe`**.

To run from source without building: create a venv, `pip install` the same packages as in the batch file, then `python PlatinumTranscriber.py`.

---

## 🇬🇧 PART 3: OPERATIONAL GUIDE

### PHASE 1: Diagnostics
Open the app → **🔍 SYSTEM DIAGNOSTICS** — check Internet, FFmpeg, RAM, storage.

### PHASE 2: Input (Tab 1)
* **YouTube:** paste URL (needs network for download only).
* **Local files:** batch selection; many audio/video extensions supported.

### PHASE 3: Local AI model (Tab 1)
First run of a model downloads weights; then works offline.
* **Whisper SMALL:** fast, ~**> 1.5 GB** free RAM recommended.
* **Whisper MEDIUM:** heavier, ~**> 3.0 GB** free RAM for difficult audio.

### PHASE 4: Output & translation (Tab 2)
* **Formats:** `.srt`, `.vtt`, `.txt`, `.docx`, `.pdf`, `.json`, `.tsv`, `.sbv`, `.md`, `.ass`.
* **Word-level timestamps:** checkbox (local Whisper, translation off) — finer subtitles, more CPU time.
* **Translation:** Original / Google / Any→EN / DeepL (key required).

### PHASE 5: Audio & cloud (Tab 3)
* **FFmpeg noise reduction** (local, requires FFmpeg).
* **VAD filter** + sensitivity — helps long recordings with silence.
* **AssemblyAI:** cloud path (key required); disables local Whisper for that run; optional chapters, PII, diarization, etc.

### PHASE 6: Live dictation (main window)
* **🎙️ RECORD & TRANSCRIBE (LIVE)** — choose engine; mutual exclusion with batch transcription while running.

### PHASE 7: Execution & history
* **▶ START EXECUTION** — batch job.
* **⏹ ABORT** — soft stop.
* **📊 HISTORY** — SQLite log.

---

## 🇬🇧 PART 4: SECURITY & TROUBLESHOOTING

### 🛡️ Windows “Protected your PC”
Unsigned / PyInstaller builds often trigger SmartScreen. Use **More info → Run anyway** if you trust the binary.

### 💰 API billing
DeepL / AssemblyAI use account limits; over-quota usually returns errors, not surprise charges. App may fall back to Google Translate where coded.

### 🔐 GitHub / source
Do **not** commit **`PlatinumConfig.json`** with real keys — see `.gitignore`.

---
<br><br>
---

## 🇮🇩 BAGIAN 1: RINGKASAN PROYEK & FITUR V8.0

Aplikasi desktop **enterprise**: transkripsi **lokal (Faster-Whisper)** dan opsi **cloud** (AssemblyAI, DeepL, Google). Input file lokal atau YouTube; hasil ke **Desktop → `PlatinumTranscriber_Output`**.

### 🧠 Fitur utama V8.0 (pembaruan terbaru)
* **Dikte live:** Mikrofon → teks real-time (Google Speech atau Whisper lokal *tiny*), antrean producer–consumer, UI aman thread.
* **Filter VAD:** Pendeteksi aktivitas suara (Silero) — melewati diam panjang; sensitivitas bisa diatur.
* **Timestamp per kata:** Opsional untuk SRT/VTT; proses lebih lama ~30% bila aktif.
* **Format ekspor tambahan:** `.json`, `.tsv`, `.sbv`, `.md`, `.ass` selain `.srt`, `.vtt`, `.txt`, `.docx`, `.pdf`.
* **Input audio/video luas:** Banyak ekstensi lewat **FFmpeg**; peringatan untuk file **> 2 GB**.
* **Preferensi tersimpan:** `PlatinumConfig.json` di folder user (jangan commit API key asli).

### 🧠 Arsitektur inti (tetap)
* **Faster-Whisper** — inferensi cepat; unduhan model sekali lalu offline.
* **FFmpeg portable** — `ffmpeg.exe` disuntik ke `PATH` aplikasi.
* **SQLite** — riwayat lewat tombol **📊 RIWAYAT**.
* **Streaming ke disk** — memori terkendali.
* **UI thread-safe** — komunikasi lewat antrean.
* **Fallback API** — jika layanan bermasalah, bisa dialihkan ke Google (di bagian yang relevan).

---

## 🇮🇩 BAGIAN 2: INSTALASI & BUILD

### 👤 Pengguna akhir
Tidak perlu instal Python/FFmpeg sistem jika memakai **`.exe`** rilis.
1. Unduh arsip dari **GitHub Releases** (atau saluran distribusi Anda).  
   *Nama aset yang disarankan saat rilis:* **`PlatinumTranscriber_V8.zip`** (berisi `dist/PlatinumTranscriber.exe` atau satu file `.exe` portable, sesuai cara Anda mengemas).
2. Ekstrak (misalnya di Desktop).
3. Jalankan **`PlatinumTranscriber.exe`** di folder `dist` (atau satu file portable).

### 🛠️ Pengembang (kompilasi `.exe`)
1. Letakkan **`ffmpeg.exe`** dan **`logo.ico`** sejajar dengan `PlatinumTranscriber.py`.
2. Jalankan **`2_Build_Platinum.bat`** (pilih bahasa di menu).
3. Skrip membuat **`platinum_env`**, menginstal dependensi (termasuk `onnxruntime` untuk VAD, `pyaudio` untuk live, dll.), lalu **PyInstaller**.
4. Hasil: **`dist/PlatinumTranscriber.exe`**.

Untuk menjalankan dari source: buat venv, `pip install` sesuai baris di batch file, lalu `python PlatinumTranscriber.py`.

---

## 🇮🇩 BAGIAN 3: PANDUAN OPERASIONAL

### FASE 1: Diagnostik
Buka aplikasi → **🔍 DIAGNOSTIK SISTEM**.

### FASE 2: Input (Tab 1)
* **YouTube** — tempel URL.
* **File lokal** — batch, banyak format.

### FASE 3: Model AI (Tab 1)
Unduhan pertama kali untuk model; setelah itu offline.
* **SMALL** — cepat, RAM bebas ~**> 1,5 GB**.
* **MEDIUM** — lebih berat, ~**> 3 GB** untuk audio sulit.

### FASE 4: Output & terjemahan (Tab 2)
* **Format:** `.srt`, `.vtt`, `.txt`, `.docx`, `.pdf`, `.json`, `.tsv`, `.sbv`, `.md`, `.ass`.
* **Timestamp per kata:** centang jika perlu (Whisper lokal, tanpa terjemahan otomatis pada mode tertentu).
* **Terjemahan:** Asli / Google / Any→EN / DeepL.

### FASE 5: Audio & cloud (Tab 3)
* **Noise reduction** FFmpeg.
* **VAD** + tingkat sensitivitas.
* **AssemblyAI** — butuh API key; fitur cloud (chapter, PII, diarization, dll.).

### FASE 6: Dikte live
Tombol **🎙️ REKAM & TRANSKIP (LIVE)** — tidak bersamaan dengan eksekusi batch.

### FASE 7: Eksekusi & riwayat
* **▶ MULAI EKSEKUSI**
* **⏹ BATALKAN**
* **📊 RIWAYAT**

---

## 🇮🇩 BAGIAN 4: KEAMANAN & MASALAH UMUM

### 🛡️ Peringatan Windows / antivirus
Proyek tanpa sertifikat code-signing dapat memicu SmartScreen — **Info lebih lanjut → Tetap jalankan** jika Anda percaya sumbernya.

### 💰 Biaya API
Kuota habis biasanya menolak permintaan, bukan tagihan diam-diam. Mitigasi ke Google Translate di beberapa jalur.

### 🔐 Git & GitHub
Jangan commit **`PlatinumConfig.json`** berisi kunci asli — gunakan `.gitignore`.

---

## 🇬🇧🇮🇩 Quick links (English / Indonesia)

| Item | Location |
|------|----------|
| Developer guide | [`docs/DEVELOPER.md`](docs/DEVELOPER.md) |
| License | [`LICENSE`](LICENSE) |
| CI workflow | [`.github/workflows/ci.yml`](.github/workflows/ci.yml) |
