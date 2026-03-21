# Git — pemecahan masalah umum (Platinum Transcriber)

## 1. `git check-ignore` kosong untuk `platinum_env`

| Penyebab | Cek & perbaikan |
|----------|-----------------|
| **Folder `platinum_env` sudah pernah di-commit** | Git **tetap melacak** file yang sudah di-index; `.gitignore` tidak mengabaikan yang sudah ter-track. Jalankan: `git rm -r --cached platinum_env` lalu commit. |
| **Bukan di root repo** | Prompt harus `...\Platinum Transcriber>`, bukan `...\Platinum Transcriber\.git>`. |
| **Perintah dari folder `.git`** | Akan error `fatal: this operation must be run in a work tree`. |

Verifikasi setelah `git rm --cached` (jika folder tidak ada, cukup pastikan tidak muncul di `git ls-files`):

```bat
git ls-files platinum_env
```

Harus kosong.

---

## 2. `__pycache__` / `*.pyc` ikut ter-staged (salah)

`.gitignore` hanya mencegah file **baru**; kalau `__pycache__` sudah pernah `git add`, ia tetap ter-track.

**Perbaiki index (aman — tidak menghapus file di disk):**

```bat
cd "C:\Users\Hp\OneDrive\Desktop\Platinum Transcriber"
git rm -r --cached .
git add .
git status
```

Ini **memuat ulang** staging dari working tree dan mematuhi `.gitignore` saat ini. Pastikan `.gitignore` sudah disimpan sebelum `git add .`

### Error: `git rm -r --cached .` → `staged content different from both the file and the HEAD`

Sering terjadi saat **rebase interaktif** sedang berjalan: index tidak sama dengan HEAD maupun working tree untuk beberapa file (mis. `.gitignore`, `README.md`).

**Pilihan (pilih satu):**

1. **Disarankan — selesaikan rebase dulu, baru bersihkan index**  
   ```bat
   git rebase --abort
   git rm -r --cached .
   git add .
   git status
   ```

2. **Lanjut rebase — paksa lepas index dari staging**  
   ```bat
   git rm -r --cached -f .
   git add .
   git status
   ```
   `-f` = **force** (sesuai saran Git). Setelah staging bersih, lanjutkan rebase:  
   `git rebase --continue` (atau `git commit` + `git rebase --continue` jika Git meminta).

Jika masih membingungkan, **Opsi 1** (`rebase --abort`) biasanya paling bersih untuk pemula.

---

## 3. Rebase macet: `interactive rebase in progress`

Anda sedang di tengah **rebase**; staging berantakan + commit ganda di todo bisa membingungkan.

### Opsi A — Batalkan rebase (kembali ke keadaan sebelum `git pull --rebase` / `rebase`)

```bat
git rebase --abort
git status
```

Lalu rapikan dengan langkah normal: pastikan `.gitignore` benar → perintah di **§2** → `git add .` → `git commit` → `git push`.

### Opsi B — Lanjutkan rebase setelah index bersih

1. Simpan semua edit (`.gitignore`, `docs/`, dll.).
2. Jalankan **§2** agar tidak ada `__pycache__` di staging.
3. `git add .`
4. Jika rebase meminta commit:  
   `git commit --amend --no-edit` **atau** buat commit dengan pesan yang diminta.
5. Lanjutkan:  
   `git rebase --continue`

Jika Git mengeluh konflik, selesaikan file bertanda konflik → `git add` file itu → `git rebase --continue`.

---

## 4. Ringkas: urutan “bersih” sebelum push

1. Root repo: `...\Platinum Transcriber>`
2. **Jika ada rebase:** `git rebase --abort` (kecuali Anda yakin ingin melanjutkan)
3. `.gitignore` lengkap & **disimpan**
4. `git rm -r --cached .` lalu `git add .` — jika error, pakai **§2** (`-f` atau abort rebase dulu)
5. `git status` — tidak ada `__pycache__`, tidak ada `ffmpeg.exe` kecuali sengaja
6. `git commit` → `git push`

---

## 5. File `.md` “hilang” dari folder

| Penyebab umum | Yang terjadi |
|----------------|--------------|
| **`git checkout` / `reset` ke commit lama** | Commit itu tidak berisi file docs → hilang dari working tree. |
| **`git pull` dari remote** | Remote tidak punya file tersebut → tertimpa / tidak pernah ada. |
| **Rebase / merge salah** | Konflik diselesaikan dengan menghapus file. |
| **OneDrive / sync** | Versi lama dipulihkan atau konflik salinan. |
| **Buka folder proyek lain** | Salinan berbeda tanpa `docs/`. |

**Pencegahan:** commit & push docs ke `main`; backup zip periodik; hindari `git reset --hard` tanpa yakin.

---

## 6. `git rebase --abort` → `Unlink of file ... failed` (`.dll` di `platinum_env/`)

Windows mem-lock file **DLL** jika Python/editor masih berjalan, antivirus memindai, atau **OneDrive** sedang sync.

1. Tutup Cursor/terminal yang memakai venv; di Task Manager hentikan `python.exe` jika perlu.  
2. **Pause** OneDrive untuk sementara.  
3. Hapus manual folder **`platinum_env`** (`rmdir /s /q platinum_env` dari root proyek).  
4. Jalankan lagi: `git rebase --abort`  
5. Jika masih macet: `git rebase --quit` (Git 2.33+), lalu `git rm -r --cached platinum_env` dan pastikan `platinum_env` di `.gitignore` — **venv tidak boleh** masuk repo.

---

## 7. `fatal: unable to read files to diff` + `.docx` / `unsupported filetype`

| Penyebab | Penjelasan |
|----------|------------|
| **`git diff` memproses blob biner** | Staging besar (mis. menghapus `platinum_env` dari repo) menyertakan file dari paket Python — ada **`default.docx`** atau biner lain. Alat diff eksternal / konversi teks di mesin Anda bisa gagal dan memutus `git diff` dengan `fatal: unable to read files to diff`. |
| **Diff eksternal global** | `diff.external` atau filter `textconv` di **config global** Git memaksa pemrosesan jenis file tertentu. |

**Cek cepat tanpa diff penuh (aman untuk lanjut kerja):**

```bat
git diff --cached --stat
git status
```

**Pindaian string sensitif** tanpa memaksa diff isi setiap biner — batasi ke file teks proyek:

```bat
git diff --cached --no-ext-diff -- "*.py" "*.md" "*.bat" "*.yml" ".github/*" | findstr /i "api_key ghp_ sk-"
```

Atau pakai pencarian di index:

```bat
git grep -i --cached -E "api_key|ghp_|sk-" -- "*.py" "*.md"
```

*(Baris yang ketemu di **`docs/*.md`** karena contoh perintah mengandung `api_key` / `ghp_` itu **bukan** kebocoran rahasia — itu teks dokumentasi.)*

---

## 8. `remote rejected` — PAT tidak boleh mengubah `.github/workflows/`

**Pesan:** `refusing to allow a Personal Access Token to create or update workflow '.github/workflows/ci.yml' without 'workflow' scope`

| Penyebab | Perbaikan |
|----------|-----------|
| Token **classic** / **fine-grained** tidak punya izin **workflow** | Buat token **baru** di GitHub → **Settings → Developer settings → Personal access tokens** — centang scope **`workflow`** (classic) atau untuk fine-grained: izin **Actions / Workflows** sesuai dokumentasi GitHub. |
| Tidak ingin memberi scope itu | Sementara **hapus** atau **jangan commit** `.github/workflows/ci.yml`, push, lalu tambahkan lagi lewat UI GitHub / komputer lain dengan token yang punya scope. *(Kurang praktis.)* |

Setelah token baru disimpan di **Windows Credential Manager** (atau ganti URL remote dengan token baru), ulangi: `git push -u origin main`.

---

## 9. Peringatan `ffmpeg.exe` (>50 MB) saat push

GitHub menolak file **>100 MB**; di atas **~50 MB** biasanya muncul peringatan.

| Situasi | Tindakan |
|---------|----------|
| **`ffmpeg.exe` tidak boleh di repo** | Pastikan ada di **`.gitignore`** (sudah ada pola `ffmpeg.exe`). Jika pernah ter-commit: `git rm --cached ffmpeg.exe` lalu commit; jika sudah di history, perlu **hapus dari history** (`git filter-repo` / BFG) atau repo baru. |
| **Memang ingin menyimpan biner besar** | Pakai **Git LFS** (dan konfigurasi `.gitattributes`) — tetap perlu perbaikan token **`workflow`** jika push menyertakan workflow. |

---

*Lihat juga: [`GITHUB_UPLOAD_MASTERPLAN_SOP.md`](GITHUB_UPLOAD_MASTERPLAN_SOP.md)*
