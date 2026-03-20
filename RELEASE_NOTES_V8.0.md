# Release Notes — Platinum Transcriber **V8.0**

**Release type:** Major (Enterprise Edition)  
**Codename suggestion:** *Enterprise + Live + Extended Formats*

> Tanggal rilis: isi manual saat Anda publish (contoh: `2026-03-20`).

---

## Ringkasan eksekutif

V8.0 menambahkan **dikte live dari mikrofon**, **filter VAD (Silero)**, **timestamp per kata**, **format ekspor tambahan**, perluasan **format input media**, peringatan **file besar**, dokumentasi **developer**, **CI** GitHub, dan perbaikan **thread-safety / preferensi / build**.

---

## Fitur baru

| Area | Deskripsi |
|------|-----------|
| **Live dictation** | Tombol rekaman live; mesin Google Speech (online) atau Whisper *tiny* (offline); antrean producer–consumer; auto-save transkrip ke Desktop. |
| **VAD filter** | Opsional pada transkripsi lokal (Faster-Whisper + Silero VAD); preset sensitivitas Rendah / Sedang / Tinggi. |
| **Word-level timestamps** | Opsional; SRT/VTT (dan ekspor terkait) bisa per kata; lebih cocok untuk subtitle rapat; ~30% waktu proses tambahan. |
| **Format ekspor** | `.json`, `.tsv`, `.sbv`, `.md`, `.ass` selain `.srt`, `.vtt`, `.txt`, `.docx`, `.pdf`. |
| **Input media** | Filter & dukungan ekstensi audio/video diperluas; ringkasan total ukuran & format di konsol; peringatan file **> 2 GB**. |
| **Preferensi** | `clean_audio` dan format baru tersimpan di `PlatinumConfig.json`. |
| **Build** | Skrip build memasang `pyaudio`, `SpeechRecognition`, `numpy`, `onnxruntime`; PyInstaller mengumpulkan data `speech_recognition` dan `onnxruntime`. |

## Perbaikan & kualitas

- Penanganan tutup jendela (`WM_DELETE_WINDOW`), mutex UI untuk live vs batch, kunci thread untuk `live_transcript`.
- Fallback & pesan error pada thread live; reset UI konsisten.
- i18n untuk string baru (ID / EN).
- Bugfix potensi `temp_mp3` tidak terdefinisi pada alur YouTube gagal awal.
- Antrean UI: konsumen memakai `get_nowait()` untuk pola antrean yang lebih aman.
- Konstanta terpusat untuk log konsol dan ambang RAM / file besar.

## Dokumentasi & repositori

- `README.md` diperbarui untuk V8.0.
- `docs/DEVELOPER.md` — arsitektur, threading, ekstensi.
- `LICENSE` (MIT).
- `.gitignore` — venv, build, rahasia.
- `.github/workflows/ci.yml` — `py_compile` otomatis.

## Sandbox (non-wajib untuk pengguna akhir)

- `Test_Interactive_Text.py` — percobaan editor teks sinkron + pemutar; pengembangan terpisah dari alur `.exe` utama.

---

## Dependensi runtime (ringkas)

- **Inti:** `customtkinter`, `faster-whisper`, `yt-dlp`, `psutil`, dll. (lihat `2_Build_Platinum.bat`).
- **Live + VAD:** `pyaudio`, `SpeechRecognition`, `numpy`, `onnxruntime`.

## Catatan upgrade dari V7.x

- Pertama kali build V8.0: jalankan ulang `2_Build_Platinum.bat` agar dependensi baru terpasang di venv.
- Model Whisper lokal tetap di-cache Hugging Face seperti sebelumnya (`HF_HUB_DISABLE_XET` tetap disetel untuk Windows).

## Known limitations

- **Musik / vokal campur instrumen:** akurasi Whisper tetap bergantung pada kualitas audio; VAD dapat memotong jeda napas tidak teratur jika sensitivitas terlalu agresif.
- **AssemblyAI / kunci API:** fitur cloud memerlukan kunci valid; kuota mengikuti penyedia.
- **Live Google:** membutuhkan koneksi internet; **Live Whisper:** unduhan model *tiny* pertama kali.

---

## Checksum / artefak (opsional)

> Isi saat rilis: SHA256 dari `PlatinumTranscriber.exe` atau `PlatinumTranscriber_V8.zip`.

---

*Dokumen ini diselaraskan dengan branch/tag `v8.0` atau `8.0.0` di Git.*
