# Masterplan SOP — Upload folder *Platinum Transcriber* ke GitHub

Dokumen ini adalah panduan **langkah demi langkah** untuk menerbitkan isi proyek ke repositori GitHub dengan aman: apa yang **wajib**, **opsional**, dan **tidak boleh** di-upload.

---

## Prasyarat

| # | Item | Catatan |
|---|------|---------|
| 1 | Akun **GitHub** | Gratis cukup untuk repo publik |
| 2 | **Git** terpasang di Windows (`git --version`) | [git-scm.com](https://git-scm.com/) |
| 3 | Folder proyek: `Platinum Transcriber` | Path Anda bisa berbeda |

---

## Fase A — Siapkan repositori di GitHub (web)

| Langkah | Aksi |
|---------|------|
| **A1** | Login [github.com](https://github.com) → **New repository** |
| **A2** | Nama repo: contoh `platinum-transcriber` atau `PlatinumTranscriber` |
| **A3** | **Public** (disarankan untuk proyek open-source) atau **Private** |
| **A4** | Jangan centang *Add a README* jika Anda sudah punya README lokal (hindari konflik pertama kali) — atau centang lalu nanti digabung |
| **A5** | Catat URL: `https://github.com/<username>/<repo>.git` |

---

## Fase B — Klasifikasi file & folder (WAJIB / OPSIONAL / DILARANG)

### B.1 WAJIB di-commit (sumber kode & dokumentasi)

| Path | Alasan |
|------|--------|
| `PlatinumTranscriber.py` | Aplikasi utama |
| `README.md` | Dokumentasi pengguna |
| `LICENSE` | Lisensi legal |
| `2_Build_Platinum.bat` | Skrip build Windows |
| `.gitignore` | Mencegah file sensitif/berat ter-commit |
| `docs/DEVELOPER.md` | Panduan developer |
| `docs/GITHUB_UPLOAD_MASTERPLAN_SOP.md` | SOP ini (opsional tapi disarankan) |
| `RELEASE_NOTES_V8.0.md` | Catatan rilis |
| `.github/workflows/ci.yml` | CI pemeriksaan sintaks |

**Opsional namun disarankan**

| Path | Alasan |
|------|--------|
| `Test_Interactive_Text.py` | Sandbox eksperimental; transparansi untuk kontributor |
| `logo.ico` | **Hanya jika** Anda punya hak pakai ikon dan ukuran wajar |

---

### B.2 OPSIONAL (boleh tidak di-push)

| Path | Catatan |
|------|---------|
| `Test_Interactive_Text.py` | Jika tidak ingin repo “berisi eksperimen”, bisa hapus dari commit atau pindah ke branch `experimental` |
| `assets/` | Gambar tambahan untuk README; buat folder jika perlu |
| `CHANGELOG.md` | Jika Anda ingin riwayat versi terpisah dari release notes |

---

### B.3 TIDAK BOLEH / JANGAN di-commit

| Path / pola | Alasan |
|-------------|--------|
| `platinum_env/` | Virtual environment — besar, bisa dibuat ulang dengan `2_Build_Platinum.bat` |
| `dist/` | Output PyInstaller — artefak build, bukan sumber |
| `build/` | Cache PyInstaller |
| `*.spec` | File spec PyInstaller (di-ignore `.gitignore`; bisa dibuat ulang) |
| `__pycache__/`, `*.pyc` | Cache Python |
| `ffmpeg.exe` | **Biasanya JANGAN** — binari besar (~80–100MB+), lisensi FFmpeg: dokumentasikan “unduh sendiri” di README (sudah ada). |
| `PlatinumConfig.json` | **JANGAN** — bisa berisi **API key** (DeepL, AssemblyAI) di mesin Anda |
| `PlatinumLogs.db` | Data pribadi pengguna; **disarankan tidak** (uncomment di `.gitignore` jika perlu) |
| `*.env`, `.env` | Rahasia |
| File `*_key*.txt` | Rahasia |
| File `.p12`, `.pem` kunci | Rahasia |
| **Isi folder OneDrive sync** yang bukan proyek | Hanya commit folder proyek yang bersih |

> **ffmpeg.exe / logo.ico:** Untuk **kolaborasi publik**, standar yang aman adalah: README menjelaskan “letakkan `ffmpeg.exe` di sini” tanpa commit binari. Untuk **rilis internal**, Anda bisa menyimpan binari di **GitHub Releases** (bukan di repo Git).

---

## Fase C — Perintah Git (lokal, step-by-step)

Jalankan di **PowerShell** atau **CMD**.

### C0 — Identitas Git (WAJIB — tanpa ini `commit` gagal: *Author identity unknown*)

Sekali per komputer, ganti nama dan email Anda:

```bat
git config --global user.name "Nama Anda"
git config --global user.email "email-anda@example.com"
```

Cek: `git config --global --list` (harus ada `user.name` dan `user.email`).

---

### C0b — Pastikan Anda di **folder proyek**, bukan folder user Windows

**Gejala salah:** `git status` menampilkan file aneh seperti `Videos\`, `ntuser.ini`, `Untitled.ipynb`, `UTM-Settings.ini`, dll. — itu berarti `git init` dijalankan di **`C:\Users\Hp\`** (folder user), **bukan** di folder *Platinum Transcriber*.

**Perbaikan:**

1. **Jangan** commit dari folder user. Masuk ke folder proyek:

```bat
cd "C:\Users\Hp\OneDrive\Desktop\Platinum Transcriber"
dir
```

Anda harus melihat `PlatinumTranscriber.py`, `README.md`, folder `docs`, `2_Build_Platinum.bat`, dll.

2. Jika Anda **sudah** membuat repo Git di folder user (`C:\Users\Hp\.git`), hapus **hanya** folder tersembunyi tersebut agar tidak mengotori seluruh profil:

   - Tutup semua jendela CMD yang sedang di `C:\Users\Hp`.
   - Di **File Explorer**: `C:\Users\Hp` → **View** → tampilkan **Hidden items** → hapus folder **`.git`** (jika ada).
   - Atau CMD (hati-hati, hanya jika yakin tidak ada proyek Git lain di profil user):

```bat
cd /d %USERPROFILE%
if exist .git rmdir /s /q .git
```

3. Setelah itu, buka lagi CMD, `cd` ke folder **Platinum Transcriber** (lihat C1), lalu `git init` **di sana** (C2).

---

### C1 — Masuk folder proyek

```bat
cd "C:\Users\Hp\OneDrive\Desktop\Platinum Transcriber"
```

*(Sesuaikan path jika folder Anda berbeda.)*

### C2 — Inisialisasi (jika belum ada `.git`)

```bat
git init
```

### C3 — Pastikan `.gitignore` sudah benar

Buka `.gitignore` — pastikan `platinum_env/`, `dist/`, `PlatinumConfig.json` ada.

### C4 — Tambahkan file (aman)

```bat
git add .
git status
```

**Periksa `git status`:** tidak boleh muncul `platinum_env`, `dist`, `ffmpeg.exe` (jika besar). Jika muncul, perbaiki `.gitignore` lalu `git reset` dan ulang `git add`.

### C5 — Commit pertama

```bat
git commit -m "Initial commit: Platinum Transcriber v8.0"
```

### C6 — Branch utama (GitHub modern memakai `main`)

```bat
git branch -M main
```

### C7 — Remote & push

```bat
git remote add origin https://github.com/<USERNAME>/<REPO>.git
git push -u origin main
```

> Jika diminta login: gunakan **Personal Access Token** (GitHub → Settings → Developer settings) sebagai password, atau **GitHub CLI** (`gh auth login`).

---

## Fase D — Verifikasi di GitHub

| Langkah | Aksi |
|---------|------|
| D1 | Buka repo di browser — pastikan file utama terlihat |
| D2 | Tab **Actions** — workflow CI harus hijau (setelah push) |
| D3 | Pastikan **tidak ada** file `PlatinumConfig.json` atau `ffmpeg.exe` jika Anda tidak sengaja mengunggah |

---

## Fase E — Rilis (GitHub Releases)

| Langkah | Aksi |
|---------|------|
| E1 | **Releases** → **Draft a new release** |
| E2 | Tag: `v8.0.0` atau `8.0.0` |
| E3 | Judul: `Platinum Transcriber v8.0` |
| E4 | Isi deskripsi: salin ringkasan dari `RELEASE_NOTES_V8.0.md` |
| E5 | **Binary:** unggah `PlatinumTranscriber_V8.zip` (berisi `dist/PlatinumTranscriber.exe` + README singkat) — **bukan** wajib menyertakan `ffmpeg.exe` di dalam zip jika Anda menginstruksikan pengguna mengunduh FFmpeg terpisah |

---

## Checklist keamanan sebelum `push`

- [ ] Tidak ada API key di file yang di-commit (grep: `api_key`, `sk-`, `deepl`, `assemblyai` di file teks).
- [ ] `PlatinumConfig.json` tidak ter-track (`git check-ignore -v PlatinumConfig.json`).
- [ ] `ffmpeg.exe` tidak ter-commit kecuali Anda sengaja dan memakai **Git LFS** + kepatuhan lisensi.
- [ ] `README.md` sudah menjelaskan cara build untuk developer.

---

## Ringkasan satu halaman

| Kategori | Contoh |
|----------|--------|
| **WAJIB** | `.py` utama, `README`, `LICENSE`, `docs/`, `.gitignore`, `.github/workflows/`, `bat` build, `RELEASE_NOTES` |
| **OPSIONAL** | `Test_Interactive_Text.py`, `logo.ico`, gambar README |
| **JANGAN** | `platinum_env/`, `dist/`, `build/`, `PlatinumConfig.json`, kunci API, `ffmpeg.exe` (default) |

---

*Versi dokumen: 1.1 — menambah C0 (identitas Git) & C0b (folder proyek vs folder user).*
