# Platinum Transcriber — Developer Guide

This document helps maintainers understand **structure**, **data flow**, and **safe extension points**. The main source file is a single module by design (PyInstaller one-file build); keep new features behind clear functions or small helper modules if the file grows further.

---

## 1. Runtime architecture

| Layer | Responsibility |
|--------|------------------|
| **UI (main thread)** | `PlatinumTranscriberApp`: CustomTkinter widgets, `poll_queue()` every ~100 ms |
| **Message queue** | `queue.Queue`: `log`, `progress`, `prog_mode`, `live_text`, `ui` (callable + args) |
| **Worker** | `logic(snapshot)` in a **daemon thread**: transcription, file I/O, no direct widget access |
| **Live dictation** | Separate threads: `_live_producer_thread` (PyAudio), `_live_consumer_*` (Whisper/Google) |

**Rule:** Worker threads must not call Tk `configure`/`insert` directly. Use `self.msg_queue.put(...)` or `self.ui_call(fn, *args, **kwargs)`.

---

## 2. Important algorithms & structures

- **Snapshot (`start_thread`)**  
  Copies all relevant `StringVar`/flags into a plain `dict` before starting `logic()`.  
  **Why:** Tk variables are not thread-safe; the worker reads only the snapshot.

- **Streaming segment write (Whisper path)**  
  Iterates `segments` from `model.transcribe()` once; writes SRT/VTT/TXT/etc. as segments arrive.  
  **Complexity:** O(n) in number of segments; memory does not scale with full transcript text held in RAM.

- **Queue drain (live Whisper consumer)**  
  Discards stale queued audio chunks so the consumer always processes the latest block (real-time).

- **Console log trim**  
  After insert, if line count > `CONSOLE_LOG_MAX_LINES`, delete oldest lines down to `CONSOLE_LOG_TRIM_TO`.  
  **Why:** Prevent unbounded memory growth on long sessions.

- **SQLite analytics**  
  `logs` table: append-only rows for file name, duration, engine.

---

## 3. File map (within `PlatinumTranscriber.py`)

| Section | Contents |
|---------|----------|
| Imports & env | `HF_HUB_DISABLE_XET`, optional PyAudio/numpy/recognition flags |
| `inject_ffmpeg` | Prepends `ffmpeg.exe` directory to `PATH` when bundled |
| `init_db` / `save_log` | SQLite |
| Helpers | `_wrap_lines`, `_text_to_paragraphs`, `_render_docx`, `_render_pdf`, ASS/SBV/JSON writers |
| `QueueRedirector` | Redirects `stdout`/`stderr` to UI queue |
| `PlatinumTranscriberApp` | Full UI + `logic()` + live methods |
| `if __name__ == "__main__"` | Entry point |

---

## 4. Configuration & secrets

- **User prefs:** `%USERPROFILE%\PlatinumConfig.json` (or `~/PlatinumConfig.json`) — API keys may be stored here.  
  **Do not commit** real keys; use `.gitignore` and environment-specific docs.

- **Logs DB:** `~/PlatinumLogs.db`

---

## 5. Build (`2_Build_Platinum.bat`)

- Creates `platinum_env`, installs dependencies, runs PyInstaller with `--collect-all` for heavy packages.
- Requires `ffmpeg.exe` and `logo.ico` next to the script for a full build.
- Output: `dist/PlatinumTranscriber.exe`

---

## 6. Suggested extension patterns

- **New output format:** Add a `BooleanVar`, persist in `save_prefs`/`load_prefs`, extend `snapshot`, add writer branch in `logic()` (Whisper + AssemblyAI paths if applicable).
- **New translation backend:** Add option in `trans_opt`, initialize client in `logic()`, branch in segment loop.
- **Splitting the monolith:** Extract pure helpers (e.g. `render_*`, `vad_*`) to `platinum_transcriber/` package when testability is needed; keep GUI in one file until then.

---

## 7. Testing before release

- `python -m py_compile PlatinumTranscriber.py`
- Run GUI: local file + Whisper small, one output format.
- Optional: AssemblyAI with test key; live dictation with `--no-pause` smoke test.

---

## 8. Line-by-line documentation

The codebase does **not** duplicate a comment on every physical line (that would harm readability and reviews). Instead:

- Module docstring (top of file) = global contract.
- This file = architecture and flows.
- Functions with non-obvious behavior carry short docstrings or inline comments where needed.

For GitHub, link this file from `README.md` under a **Developer** section.

---

## 9. License & CI

- **License:** Root `LICENSE` (MIT by default). Change the copyright line if needed.
- **CI:** `.github/workflows/ci.yml` runs `py_compile` on `PlatinumTranscriber.py` (and the interactive sandbox file) on pushes to `main`/`master` and on pull requests.

## 10. Publishing to GitHub

See **[`GITHUB_UPLOAD_MASTERPLAN_SOP.md`](GITHUB_UPLOAD_MASTERPLAN_SOP.md)** for step-by-step `git` commands and a checklist of what must / may / must not be committed.
