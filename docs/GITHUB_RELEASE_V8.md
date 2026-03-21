# Menerbitkan rilis **V8.0.0** di GitHub Releases

Repo: [`ridhosyhptra/Platinum-Transcriber-BIFL`](https://github.com/ridhosyhptra/Platinum-Transcriber-BIFL)

Ringkasan: buat **tag** `v8.0.0` pada `main`, unggah **`PlatinumTranscriber_V8.zip`** (dan opsional `.exe` tunggal), isi catatan dari **`RELEASE_NOTES_V8.0.md`**.

---

## 0. Prasyarat

| Item | Catatan |
|------|---------|
| **`dist\PlatinumTranscriber.exe`** | Hasil **`2_Build_Platinum.bat`** (butuh **`ffmpeg.exe`** + **`logo.ico`** di folder proyek — tidak di-repo). |
| **Push `main` terbaru** | Kode yang Anda rilis sejajar dengan commit di GitHub. |

---

## 1. Build & paket ZIP (lokal)

Dari folder proyek (mis. `Desktop\Platinum Transcriber`):

1. Jalankan **`2_Build_Platinum.bat`** → pastikan **`dist\PlatinumTranscriber.exe`** ada.
2. Paket ZIP sesuai README (**folder `dist`** di dalam arsip):

```powershell
cd "C:\Users\Hp\Desktop\Platinum Transcriber"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\package_v8_release.ps1"
```

Keluaran:

- **`PlatinumTranscriber_V8.zip`** di root proyek  
- **`PlatinumTranscriber_V8.zip.sha256`** — hash untuk dicatat di catatan rilis (opsional)

*(Opsional)* Salin juga **`dist\PlatinumTranscriber.exe`** ke folder lain jika ingin mengunggah **dua aset**: ZIP + EXE tunggal.

---

## 2. Buat rilis di GitHub (antarmuka web)

1. Buka: **https://github.com/ridhosyhptra/Platinum-Transcriber-BIFL/releases**
2. **Draft a new release**
3. **Choose a tag** → ketik **`v8.0.0`** → **Create new tag on: `main`**
4. **Release title:** mis. `Platinum Transcriber V8.0.0`
5. **Describe:** salin isi dari [`RELEASE_NOTES_V8.0.md`](../RELEASE_NOTES_V8.0.md) (sesuaikan tanggal di bagian atas dokumen).
6. **Attach binaries** — tarik atau **select files**:
   - Wajib disarankan: **`PlatinumTranscriber_V8.zip`**
   - Opsional: **`PlatinumTranscriber.exe`** (satu file dari `dist\`, untuk pengguna yang tidak ingin ekstrak ZIP)
7. Centang **Set as the latest release** jika ini rilis utama terbaru.
8. **Publish release**

---

## 3. Setelah publish

- Di README, pengguna mengunduh dari **Releases** — pastikan judul/tag jelas (**V8**).
- Jika rilis lama masih bertanda **Latest** (mis. V7), edit rilis V8 dan set sebagai **latest** atau nonaktifkan centang di rilis lama sesuai kebijakan Anda.

---

## 4. (Opsional) GitHub CLI `gh`

Jika **`gh`** terpasang dan sudah `gh auth login`:

```bat
gh release create v8.0.0 --repo ridhosyhptra/Platinum-Transcriber-BIFL --title "Platinum Transcriber V8.0.0" --notes-file RELEASE_NOTES_V8.0.md PlatinumTranscriber_V8.zip dist\PlatinumTranscriber.exe
```

Jalankan dari **root proyek** setelah ZIP dan build ada. Tanpa `gh`, cukup langkah **§2**.

---

## 5. Checklist singkat

- [ ] `dist\PlatinumTranscriber.exe` ada (ukuran besar — normal)
- [ ] `PlatinumTranscriber_V8.zip` dibuat (skrip §1)
- [ ] Tag **`v8.0.0`** mengarah ke commit **`main`** yang benar
- [ ] Catatan rilis mengacu V8.0 (bukan V7)
- [ ] Opsional: isi baris checksum di `RELEASE_NOTES_V8.0.md` dari file `.sha256`
