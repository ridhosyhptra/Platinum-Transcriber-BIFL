# ==============================================================
#  SANDBOX: Editor Teks Interaktif Sinkron (Gaya Descript)
#  Prototipe V9.0 - Karaoke Highlight + Click-to-Seek
#
#  Alur:
#    1. Pilih file audio (WAV/MP3) -> Transkripsi word-level
#    2. Teks tampil dengan tag per kata
#    3. Play -> highlight mengikuti pemutaran
#    4. Klik kata -> audio loncat ke timestamp kata tersebut
#
#  Dependency: pygame (pip install pygame)
#  Format audio: WAV, MP3, OGG (pygame native)
# ==============================================================

import os
import sys
import tempfile
import subprocess

os.environ["HF_HUB_DISABLE_XET"] = "1"

# Pre-flight: check libs
missing = []
for lib in ["customtkinter", "faster_whisper", "pygame"]:
    try:
        __import__(lib)
    except ImportError:
        missing.append(lib)

if missing:
    print("[ERROR] Library belum terinstal:", ", ".join(missing))
    print("Jalankan: pip install pygame")
    sys.exit(1)

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from faster_whisper import WhisperModel
import pygame

# --- Konfigurasi ---
WHISPER_MODEL = "small"
POLL_MS = 80
HIGHLIGHT_TAG = "active"
HIGHLIGHT_BG = "#2d5016"
HIGHLIGHT_FG = "#ffffff"


def _fmt_time(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m}:{s:02d}"


def transcribe_with_words(audio_path):
    """Transkripsi dengan word-level timestamps. Return list of (word, start_sec, end_sec)."""
    print("[WHISPER] Memuat model...")
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    print("[WHISPER] Mentranskripsi (word_timestamps=True)...")
    segments, _ = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True,
        condition_on_previous_text=False,
        compression_ratio_threshold=2.4,
        no_speech_threshold=0.5,
    )
    words = []
    for seg in segments:
        if getattr(seg, "words", None):
            for w in seg.words:
                wt = w.word.strip()
                if wt:
                    words.append((wt, w.start, w.end))
        else:
            text = seg.text.strip()
            if text:
                words.append((text, seg.start, seg.end))
    return words


def _get_ffmpeg_path():
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "ffmpeg.exe")


def _get_ffprobe_path():
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ("ffprobe.exe", "ffprobe"):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    return "ffprobe"


def get_audio_duration(path):
    """Durasi audio dalam detik. Fallback: max dari transcript."""
    ffprobe = _get_ffprobe_path()
    try:
        r = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            return float(r.stdout.strip())
    except Exception:
        pass
    return None


def ensure_playable_audio(src_path):
    """Gunakan file asli untuk playback. Konversi ke WAV hanya jika format tidak didukung pygame."""
    ext = os.path.splitext(src_path)[1].lower()
    if ext in (".wav", ".mp3", ".ogg"):
        return src_path
    ffmpeg = _get_ffmpeg_path()
    if not os.path.exists(ffmpeg):
        return None
    fd, tmp = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        r = subprocess.run(
            [ffmpeg, "-y", "-i", src_path, "-acodec", "pcm_s16le", "-ar", "44100", tmp],
            capture_output=True,
            timeout=120,
        )
        if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
            return tmp
    except Exception:
        pass
    if os.path.exists(tmp):
        try:
            os.remove(tmp)
        except Exception:
            pass
    return None


class InteractiveEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Test: Editor Teks Interaktif Sinkron")
        self.geometry("800x500")
        ctk.set_appearance_mode("dark")

        self.audio_path = None
        self.play_path = None
        self.words = []
        self.word_ranges = []
        self.audio_duration = 0.0
        self._poll_id = None
        self._last_active = -1
        self._slider_updating = False
        self._user_dragging = False

        # UI
        frm_top = ctk.CTkFrame(self, fg_color="transparent")
        frm_top.pack(fill="x", padx=10, pady=10)

        self.btn_load = ctk.CTkButton(frm_top, text="Pilih File Audio", command=self._on_load)
        self.btn_load.pack(side="left", padx=5)

        self.btn_play = ctk.CTkButton(frm_top, text="Play", command=self._on_play, state="disabled")
        self.btn_play.pack(side="left", padx=5)

        self.btn_pause = ctk.CTkButton(frm_top, text="Pause", command=self._on_pause, state="disabled")
        self.btn_pause.pack(side="left", padx=5)

        self.lbl_status = ctk.CTkLabel(frm_top, text="Pilih file audio (WAV/MP3) untuk memulai.")
        self.lbl_status.pack(side="left", padx=15)

        # Mini player: seek bar + time labels
        frm_player = ctk.CTkFrame(self, fg_color="transparent")
        frm_player.pack(fill="x", padx=10, pady=(0, 5))

        self.lbl_time_current = ctk.CTkLabel(frm_player, text="0:00", width=45, anchor="w")
        self.lbl_time_current.pack(side="left", padx=(0, 5))

        self.slider_seek = tk.Scale(
            frm_player, from_=0, to=1, orient=tk.HORIZONTAL, showvalue=0,
            bg="#2b2b2b", fg="#d4d4d4", troughcolor="#1a1a1a",
            highlightthickness=0, length=400, resolution=0.1,
            command=lambda v: self._on_slider_drag(v),
        )
        self.slider_seek.pack(side="left", fill="x", expand=True, padx=5)
        self.slider_seek.bind("<ButtonPress-1>", self._on_slider_press)
        self.slider_seek.bind("<ButtonRelease-1>", self._on_slider_release)

        self.lbl_time_total = ctk.CTkLabel(frm_player, text="0:00", width=45, anchor="e")
        self.lbl_time_total.pack(side="left", padx=(5, 0))

        # Text area: tk.Text inside CTkFrame for tag support
        frm_text = ctk.CTkFrame(self, fg_color=("#2b2b2b", "#1a1a1a"))
        frm_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.text = tk.Text(
            frm_text,
            wrap="word",
            font=("Consolas", 12),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            selectbackground="#264f78",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.text.pack(fill="both", expand=True)
        self.text.tag_config(HIGHLIGHT_TAG, background=HIGHLIGHT_BG, foreground=HIGHLIGHT_FG)
        self.text.bind("<Button-1>", self._on_click)
        self.text.bind("<KeyRelease>", self._on_text_edit)
        self._rebuild_after_id = None

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        except Exception:
            pygame.mixer.init()

    def _on_load(self):
        path = filedialog.askopenfilename(
            title="Pilih File Audio",
            filetypes=[("Audio", "*.wav *.mp3 *.ogg"), ("WAV", "*.wav"), ("MP3", "*.mp3"), ("All", "*.*")],
        )
        if not path:
            return
        self.audio_path = path
        self.lbl_status.configure(text="Memproses...")
        self.update()

        play_path = ensure_playable_audio(path)
        if not play_path:
            self.lbl_status.configure(text="Format tidak didukung. Gunakan WAV/MP3/OGG atau pasang ffmpeg.exe.")
            return

        self.play_path = play_path
        try:
            self.words = transcribe_with_words(path)
        except Exception as e:
            self.lbl_status.configure(text=f"Transkripsi gagal: {e}")
            return

        dur = get_audio_duration(play_path)
        self.audio_duration = dur if dur and dur > 0 else (max((w[2] for w in self.words), default=0) + 5)
        self.slider_seek.configure(from_=0, to=max(self.audio_duration, 1))
        self.slider_seek.set(0)
        self.lbl_time_total.configure(text=_fmt_time(self.audio_duration))
        self.lbl_time_current.configure(text="0:00")

        self._build_text()
        self.btn_play.configure(state="normal")
        self.btn_pause.configure(state="normal")
        self.lbl_status.configure(text=f"Loaded: {len(self.words)} kata | {os.path.basename(path)}")

    def _build_text(self):
        self.text.delete("1.0", "end")
        self.word_ranges.clear()
        for i, (word, _, _) in enumerate(self.words):
            tag = f"w{i}"
            self.text.tag_config(tag, background="", foreground="")
            if i > 0:
                self.text.insert("end", " ")
            start = self.text.index("end")
            self.text.insert("end", word, tag)
            end = self.text.index("end")
            self.word_ranges.append((start, end, tag))

    def _on_text_edit(self, event=None):
        """Debounce: rebuild tags 300ms setelah pengguna selesai mengedit."""
        if self._rebuild_after_id:
            self.after_cancel(self._rebuild_after_id)
        self._rebuild_after_id = self.after(300, self._rebuild_tags_from_text)

    def _rebuild_tags_from_text(self):
        """Re-sync tag dengan teks saat ini setelah pengguna mengedit."""
        self._rebuild_after_id = None
        if not self.words:
            return
        content = self.text.get("1.0", "end-1c")
        tokens = content.split()
        for i in range(len(self.words)):
            self.text.tag_remove(f"w{i}", "1.0", "end")
        self.word_ranges.clear()
        pos = 0
        for i, token in enumerate(tokens):
            if i >= len(self.words):
                break
            idx_in_content = content.find(token, pos)
            if idx_in_content == -1:
                break
            tag = f"w{i}"
            start_idx = self.text.index(f"1.0+{idx_in_content}c")
            end_idx = self.text.index(f"1.0+{idx_in_content + len(token)}c")
            self.text.tag_add(tag, start_idx, end_idx)
            self.text.tag_config(tag, background="", foreground="")
            self.word_ranges.append((start_idx, end_idx, tag))
            pos = idx_in_content + len(token)

    def _on_slider_drag(self, value):
        if self._slider_updating:
            return
        sec = float(value)
        self.lbl_time_current.configure(text=_fmt_time(sec))
        if self._user_dragging:
            return
        self._do_seek(sec)

    def _on_slider_press(self, event=None):
        self._user_dragging = True
        self._stop_poll()

    def _on_slider_release(self, event=None):
        self._user_dragging = False
        if self.play_path:
            try:
                sec = float(self.slider_seek.get())
                self._do_seek(sec)
            except (ValueError, TypeError):
                pass

    def _do_seek(self, seek_sec):
        if not self.play_path:
            return
        try:
            pygame.mixer.music.load(self.play_path)
            pygame.mixer.music.play(start=seek_sec)
            self._last_active = -1
            self.lbl_time_current.configure(text=_fmt_time(seek_sec))
            if pygame.mixer.music.get_busy():
                self._start_poll()
        except Exception:
            pass

    def _on_play(self):
        if not self.play_path or not self.words:
            return
        if not os.path.exists(self.play_path):
            self.lbl_status.configure(text=f"File tidak ditemukan: {self.play_path[:50]}...")
            return
        try:
            pygame.mixer.music.load(self.play_path)
            pygame.mixer.music.play()
            self.after(100, self._check_play_started)
        except Exception as e:
            self.lbl_status.configure(text=f"Play error: {e}")
            print(f"[PLAY ERROR] {e}")

    def _check_play_started(self):
        if pygame.mixer.music.get_busy():
            self._start_poll()
            return
        if self.play_path and self.play_path.lower().endswith(".mp3"):
            wav_path = self._try_convert_to_wav()
            if wav_path:
                self.play_path = wav_path
                try:
                    pygame.mixer.music.load(wav_path)
                    pygame.mixer.music.play()
                    self.after(100, self._check_play_started)
                except Exception:
                    self.lbl_status.configure(text="Play gagal setelah konversi WAV.")
                return
        self.lbl_status.configure(
            text="Play gagal. Pasang ffmpeg.exe untuk konversi WAV, atau gunakan file WAV."
        )

    def _try_convert_to_wav(self):
        ffmpeg = _get_ffmpeg_path()
        if not os.path.exists(ffmpeg):
            return None
        fd, tmp = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        try:
            r = subprocess.run(
                [ffmpeg, "-y", "-i", self.audio_path, "-acodec", "pcm_s16le", "-ar", "44100", tmp],
                capture_output=True, timeout=120,
            )
            if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
                return tmp
        except Exception:
            pass
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass
        return None

    def _on_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self._stop_poll()
        else:
            pygame.mixer.music.unpause()
            self._start_poll()

    def _start_poll(self):
        self._stop_poll()
        self._poll_position()

    def _stop_poll(self):
        if self._poll_id:
            self.after_cancel(self._poll_id)
            self._poll_id = None

    def _poll_position(self):
        if not pygame.mixer.music.get_busy():
            self._stop_poll()
            return
        pos_ms = pygame.mixer.music.get_pos()
        pos_sec = pos_ms / 1000.0
        self._slider_updating = True
        try:
            self.slider_seek.set(min(pos_sec, self.audio_duration))
            self.lbl_time_current.configure(text=_fmt_time(pos_sec))
        finally:
            self._slider_updating = False
        active = -1
        for i, (_, start, end) in enumerate(self.words):
            if start <= pos_sec <= end:
                active = i
                break
        if active != self._last_active:
            self._last_active = active
            self._update_highlight(active)
        self._poll_id = self.after(POLL_MS, self._poll_position)

    def _update_highlight(self, active_idx):
        for i, (start, end, tag) in enumerate(self.word_ranges):
            if i == active_idx:
                self.text.tag_config(tag, background=HIGHLIGHT_BG, foreground=HIGHLIGHT_FG)
                try:
                    self.text.see(start)
                except Exception:
                    pass
            else:
                self.text.tag_config(tag, background="", foreground="")

    def _on_click(self, event):
        if not self.words or not self.play_path:
            return
        idx = self.text.index(f"@{event.x},{event.y}")
        for i, (start, end, _) in enumerate(self.word_ranges):
            if self._index_in_range(idx, start, end):
                _, seek_sec, _ = self.words[i]
                try:
                    pygame.mixer.music.load(self.play_path)
                    pygame.mixer.music.play(start=seek_sec)
                    self._last_active = -1
                    self._slider_updating = True
                    self.slider_seek.set(seek_sec)
                    self.lbl_time_current.configure(text=_fmt_time(seek_sec))
                    self._slider_updating = False
                    self._start_poll()
                except Exception as e:
                    self.lbl_status.configure(text=f"Seek error: {e}")
                break

    def _index_in_range(self, idx, start, end):
        def key(s):
            r = self.text.index(s)
            a, b = r.split(".")
            return (int(a), int(b))
        return key(start) <= key(idx) <= key(end)

    def destroy(self):
        self._stop_poll()
        if self._rebuild_after_id:
            self.after_cancel(self._rebuild_after_id)
        pygame.mixer.quit()
        if self.play_path and self.play_path != self.audio_path and os.path.exists(self.play_path):
            try:
                os.remove(self.play_path)
            except Exception:
                pass
        super().destroy()


if __name__ == "__main__":
    app = InteractiveEditor()
    app.mainloop()
