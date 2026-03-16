import os
import sys
import time
import threading
import json
import subprocess
import urllib.request
import shutil
import queue
import sqlite3
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# --- 1. INJEKSI FFMPEG PORTABLE (100% PLUG AND PLAY) ---
def inject_ffmpeg():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # Path memori sementara saat jadi .exe
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")
    if os.path.exists(ffmpeg_path):
        os.environ["PATH"] += os.pathsep + base_path
        return True
    return False

HAS_FFMPEG = inject_ffmpeg()

# --- 2. PRE-FLIGHT CHECK (Pengecekan Library) ---
missing_libs = []
for lib in ['yt_dlp', 'faster_whisper', 'deep_translator', 'deepl', 'docx', 'reportlab', 'psutil', 'assemblyai', 'customtkinter']:
    try: __import__(lib)
    except: missing_libs.append(lib)

if missing_libs:
    tk.Tk().withdraw()
    err_msg = "Library belum terinstal:\n" + "\n".join(missing_libs)
    err_msg += "\n\nJalankan skrip 2_Build_Platinum.bat untuk menginstal otomatis."
    messagebox.showerror("System Diagnostics Failed", err_msg)
    sys.exit()

import yt_dlp
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
import deepl
import docx
from reportlab.pdfgen import canvas
import psutil
import assemblyai as aai
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
CONFIG_FILE = os.path.join(os.path.expanduser("~"), "PlatinumConfig.json")

# --- 3. DATABASE ANALITIK (SQLITE) ---
def init_db():
    conn = sqlite3.connect("PlatinumLogs.db")
    conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, tanggal TEXT, file_name TEXT, durasi_detik REAL, engine TEXT)")
    conn.commit()
    conn.close()

def save_log(file_name, durasi, engine):
    try:
        conn = sqlite3.connect("PlatinumLogs.db")
        tgl = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("INSERT INTO logs (tanggal, file_name, durasi_detik, engine) VALUES (?, ?, ?, ?)", (tgl, file_name, durasi, engine))
        conn.commit()
        conn.close()
    except Exception as e: print(f"[DB Error] Gagal menyimpan log: {e}")

init_db()

# --- 4. THREAD-SAFE QUEUE REDIRECTOR ---
class QueueRedirector:
    def __init__(self, q): self.q = q
    def write(self, text):
        if text.strip(): self.q.put({"type": "log", "msg": text + "\n"})
    def flush(self): pass

# --- 5. KELAS UTAMA APLIKASI ---
class PlatinumTranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Platinum Transcriber V7 (Faster-Whisper Edition)")
        self.geometry("950x800")
        self.stop_flag = False
        self.msg_queue = queue.Queue()
        
        self.setup_vars()
        self.load_prefs()
        self.setup_ui()
        
        sys.stdout = QueueRedirector(self.msg_queue)
        sys.stderr = QueueRedirector(self.msg_queue)
        self.poll_queue()

    def poll_queue(self):
        while not self.msg_queue.empty():
            msg = self.msg_queue.get()
            if msg["type"] == "log":
                self.console_log.configure(state="normal")
                self.console_log.insert("end", msg["msg"])
                self.console_log.see("end")
                self.console_log.configure(state="disabled")
            elif msg["type"] == "progress":
                self.prog_bar.set(msg["val"])
            elif msg["type"] == "prog_mode":
                self.prog_bar.configure(mode=msg["val"])
                if msg["val"] == "indeterminate": self.prog_bar.start()
                else: self.prog_bar.stop()
        self.after(100, self.poll_queue)

    def setup_vars(self):
        self.src_type = ctk.StringVar(value="local"); self.ai_eng = ctk.StringVar(value="small")
        self.out_srt = ctk.BooleanVar(value=True); self.out_vtt = ctk.BooleanVar(value=False)
        self.out_txt = ctk.BooleanVar(value=True); self.out_docx = ctk.BooleanVar(value=False); self.out_pdf = ctk.BooleanVar(value=False)
        self.trans_opt = ctk.StringVar(value="none"); self.clean_audio = ctk.BooleanVar(value=False)
        self.use_aai = ctk.BooleanVar(value=False)
        self.aai_chap = ctk.BooleanVar(value=False); self.aai_pii = ctk.BooleanVar(value=False)
        self.aai_diar = ctk.BooleanVar(value=False); self.aai_filler = ctk.BooleanVar(value=True)
        self.deepl_key = ctk.StringVar(); self.aai_key = ctk.StringVar(); self.aai_vocab = ctk.StringVar()
        self.url_input = ctk.StringVar(); self.local_files = []

    def save_prefs(self):
        prefs = {"ai_eng": self.ai_eng.get(), "out_srt": self.out_srt.get(), "out_vtt": self.out_vtt.get(), "out_txt": self.out_txt.get(), "out_docx": self.out_docx.get(), "out_pdf": self.out_pdf.get(), "trans_opt": self.trans_opt.get(), "clean_audio": self.clean_audio.get(), "deepl_key": self.deepl_key.get(), "aai_key": self.aai_key.get()}
        try: json.dump(prefs, open(CONFIG_FILE, "w"))
        except: pass

    def load_prefs(self):
        if os.path.exists(CONFIG_FILE):
            try:
                p = json.load(open(CONFIG_FILE, "r"))
                self.ai_eng.set(p.get("ai_eng", "small")); self.trans_opt.set(p.get("trans_opt", "none"))
                self.out_srt.set(p.get("out_srt", True)); self.out_txt.set(p.get("out_txt", True))
                self.out_docx.set(p.get("out_docx", False)); self.out_pdf.set(p.get("out_pdf", False))
                self.deepl_key.set(p.get("deepl_key", "")); self.aai_key.set(p.get("aai_key", ""))
            except: pass

    def setup_ui(self):
        self.current_lang = "id"
        main_frm = ctk.CTkFrame(self); main_frm.pack(fill="both", expand=True, padx=10, pady=5)
        
        # TOP BAR (Language & History)
        top_bar = ctk.CTkFrame(main_frm, fg_color="transparent"); top_bar.pack(fill="x")
        self.btn_lang = ctk.CTkButton(top_bar, text="🔄 English", command=self.toggle_lang, width=100)
        self.btn_lang.pack(side="right", padx=5)
        self.btn_hist = ctk.CTkButton(top_bar, text="📊 RIWAYAT", command=self.show_history, width=100, fg_color="gray")
        self.btn_hist.pack(side="right", padx=5)
        
        self.btn_diag = ctk.CTkButton(main_frm, text="🔍 DIAGNOSTIK SISTEM", fg_color="#ff9800", hover_color="#e68a00", command=self.run_diag)
        self.btn_diag.pack(fill="x", pady=5)

        self.tabs = ctk.CTkTabview(main_frm); self.tabs.pack(fill="both", expand=True, pady=5)
        self.t1 = self.tabs.add("1. Input & Mesin AI"); self.t2 = self.tabs.add("2. Output & Terjemahan"); self.t3 = self.tabs.add("3. AssemblyAI & Cloud")

        # TAB 1: INPUT
        ctk.CTkRadioButton(self.t1, text="Link YouTube (~30MB/jam)", variable=self.src_type, value="youtube", command=self.toggle_src).pack(anchor="w", pady=5)
        self.url_ent = ctk.CTkEntry(self.t1, textvariable=self.url_input, width=500, placeholder_text="Tempel link YouTube...")
        ctk.CTkRadioButton(self.t1, text="File Lokal (Batch - 100% Offline)", variable=self.src_type, value="local", command=self.toggle_src).pack(anchor="w", pady=5)
        self.f_frm = ctk.CTkFrame(self.t1, fg_color="transparent")
        ctk.CTkButton(self.f_frm, text="Cari File", command=self.browse).pack(side="left")
        self.f_lbl = ctk.CTkLabel(self.f_frm, text="Belum ada file", text_color="gray"); self.f_lbl.pack(side="left", padx=10)
        
        ctk.CTkLabel(self.t1, text="\nKapasitas Mesin AI (Faster-Whisper):", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10,0))
        ctk.CTkRadioButton(self.t1, text="Whisper SMALL (Sangat Cepat | RAM > 1.5GB)", variable=self.ai_eng, value="small").pack(anchor="w", pady=5)
        ctk.CTkRadioButton(self.t1, text="Whisper MEDIUM (Presisi Tinggi | RAM > 3.0GB)", variable=self.ai_eng, value="medium").pack(anchor="w", pady=5)

        # TAB 2: OUTPUT
        ctk.CTkLabel(self.t2, text="Format Output:", font=("Arial", 14, "bold")).pack(anchor="w")
        frm_out = ctk.CTkFrame(self.t2, fg_color="transparent"); frm_out.pack(anchor="w")
        for text, var in [(".srt (Video)", self.out_srt), (".vtt", self.out_vtt), (".txt (Baca)", self.out_txt), (".docx (Word)", self.out_docx), (".pdf", self.out_pdf)]:
            ctk.CTkCheckBox(frm_out, text=text, variable=var).pack(side="left", padx=5)

        ctk.CTkLabel(self.t2, text="\nOpsi Terjemahan:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10,0))
        ctk.CTkRadioButton(self.t2, text="Teks Original (100% Offline)", variable=self.trans_opt, value="none").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.t2, text="Google Translate (EN->ID | Gratis <1MB)", variable=self.trans_opt, value="google").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.t2, text="Terjemahkan ke English (Any->EN | Gratis)", variable=self.trans_opt, value="any2en").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.t2, text="DeepL AI (Presisi Tinggi EN->ID)", variable=self.trans_opt, value="deepl").pack(anchor="w", pady=2)
        ctk.CTkEntry(self.t2, textvariable=self.deepl_key, width=400, show="*", placeholder_text="DeepL API Key (Jika kosong, AI akan memakai Google)").pack(anchor="w", pady=5)

        # TAB 3: ADVANCED
        ctk.CTkLabel(self.t3, text="Audio Pre-Processing (Lokal):", font=("Arial", 14, "bold")).pack(anchor="w")
        ctk.CTkCheckBox(self.t3, text="FFmpeg Noise Reduction (Pembersih Bising)", variable=self.clean_audio).pack(anchor="w", pady=5)

        ctk.CTkLabel(self.t3, text="\nIntegrasi AssemblyAI Cloud (Akan menggantikan mesin Whisper):", font=("Arial", 14, "bold")).pack(anchor="w")
        ctk.CTkCheckBox(self.t3, text="Aktifkan AssemblyAI", variable=self.use_aai).pack(anchor="w", pady=5)
        frm_aai = ctk.CTkFrame(self.t3, fg_color="transparent"); frm_aai.pack(anchor="w")
        ctk.CTkCheckBox(frm_aai, text="Auto Chapters", variable=self.aai_chap).pack(side="left", padx=5)
        ctk.CTkCheckBox(frm_aai, text="Redaksi PII", variable=self.aai_pii).pack(side="left", padx=5)
        ctk.CTkCheckBox(frm_aai, text="Diarization", variable=self.aai_diar).pack(side="left", padx=5)
        ctk.CTkCheckBox(frm_aai, text="Hapus Kata Pengisi (um, ah)", variable=self.aai_filler).pack(side="left", padx=5)
        ctk.CTkEntry(self.t3, textvariable=self.aai_vocab, width=450, placeholder_text="Custom Vocab (Koma: safety, hazmat, toolbox meeting)").pack(anchor="w", pady=5)
        ctk.CTkEntry(self.t3, textvariable=self.aai_key, width=450, show="*", placeholder_text="AssemblyAI API Key").pack(anchor="w", pady=5)

        # DASHBOARD BAWAH
        self.prog_bar = ctk.CTkProgressBar(main_frm); self.prog_bar.pack(fill="x", pady=5); self.prog_bar.set(0)
        btn_frm = ctk.CTkFrame(main_frm, fg_color="transparent"); btn_frm.pack(fill="x")
        self.btn_start = ctk.CTkButton(btn_frm, text="▶ MULAI EKSEKUSI", fg_color="#006400", hover_color="#004d00", font=("Arial", 14, "bold"), command=self.start_thread)
        self.btn_start.pack(side="left", expand=True, fill="x", padx=(0,5))
        self.btn_stop = ctk.CTkButton(btn_frm, text="⏹ BATALKAN (E-STOP)", fg_color="#8B0000", hover_color="#660000", font=("Arial", 14, "bold"), state="disabled", command=self.trigger_stop)
        self.btn_stop.pack(side="right", expand=True, fill="x", padx=(5,0))
        self.console_log = ctk.CTkTextbox(main_frm, height=140, text_color="#00FF00", fg_color="black", font=("Consolas", 12))
        self.console_log.pack(fill="both", expand=True, pady=5); self.console_log.configure(state="disabled")
        
        self.toggle_src()
        print("[SYSTEM] V7.0 Faster-Whisper Edition Siap.")
        if HAS_FFMPEG: print("[SYSTEM] FFmpeg Portable Terdeteksi (Plug-and-Play Aktif).")

    def toggle_lang(self):
        self.current_lang = "en" if self.current_lang == "id" else "id"
        is_en = self.current_lang == "en"
        self.btn_lang.configure(text="🔄 Indonesia" if is_en else "🔄 English")
        self.btn_hist.configure(text="📊 HISTORY" if is_en else "📊 RIWAYAT")
        self.btn_diag.configure(text="🔍 SYSTEM DIAGNOSTICS" if is_en else "🔍 DIAGNOSTIK SISTEM")
        self.btn_start.configure(text="▶ START EXECUTION" if is_en else "▶ MULAI EKSEKUSI")
        self.btn_stop.configure(text="⏹ ABORT (E-STOP)" if is_en else "⏹ BATALKAN (E-STOP)")
        self.url_ent.configure(placeholder_text="Paste YouTube link..." if is_en else "Tempel link YouTube...")
        if "Belum ada" in self.f_lbl.cget("text") or "No file" in self.f_lbl.cget("text"):
            self.f_lbl.configure(text="No file selected" if is_en else "Belum ada file")

    def show_history(self):
        hist_win = ctk.CTkToplevel(self)
        hist_win.title("Dashboard Analitik" if self.current_lang=="id" else "Analytics Dashboard")
        hist_win.geometry("600x400")
        hist_win.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(hist_win, text="Riwayat Transkripsi (Log Database)", font=("Arial", 16, "bold"))
        lbl.pack(pady=10)
        textbox = ctk.CTkTextbox(hist_win, width=550, height=300)
        textbox.pack(padx=10, pady=10)
        
        try:
            conn = sqlite3.connect("PlatinumLogs.db")
            cursor = conn.execute("SELECT tanggal, file_name, durasi_detik, engine FROM logs ORDER BY id DESC")
            for row in cursor:
                mins, secs = divmod(int(row[2]), 60)
                textbox.insert("end", f"[{row[0]}] {row[1]}\nEngine: {row[3]} | Waktu Proses: {mins}m {secs}s\n{'-'*50}\n")
            conn.close()
        except: textbox.insert("end", "Belum ada riwayat / Database Error.")
        textbox.configure(state="disabled")

    def toggle_src(self):
        if self.src_type.get() == "youtube": self.f_frm.pack_forget(); self.url_ent.pack(anchor="w", pady=5)
        else: self.url_ent.pack_forget(); self.f_frm.pack(anchor="w", pady=5)

    def browse(self):
        f = filedialog.askopenfilenames()
        if f: self.local_files = list(f); self.f_lbl.configure(text=f"{len(f)} files", text_color="#00FF00")

    def run_diag(self):
        ram = psutil.virtual_memory(); fr = ram.available / (1024**3); tr = ram.total / (1024**3)
        fs = shutil.disk_usage(os.path.expanduser("~"))[2] / (1024**3)
        ff = "✅ (Portable)" if HAS_FFMPEG else ("✅ (System)" if subprocess.run(["ffmpeg", "-version"], capture_output=True).returncode == 0 else "❌")
        try: urllib.request.urlopen('http://google.com', timeout=3); inet = "✅"
        except: inet = "❌"
        messagebox.showinfo("Pre-Flight Check", f"Internet Connection: {inet}\nFFmpeg Engine: {ff}\nRAM Free: {fr:.2f}GB / {tr:.2f}GB\nStorage Free: {fs:.2f}GB")

    # FORMAT TIMESTAMP MURNI DAN PRESISI
    def format_ts(self, seconds, fmt="txt"):
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if fmt in ["srt", "vtt"]:
            delim = "," if fmt == "srt" else "."
            ms = int((seconds - int(seconds)) * 1000)
            return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}{delim}{ms:03d}"
        else:
            if hours > 0: return f"[{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}]"
            return f"[{int(minutes):02d}:{int(secs):02d}]"

    def yt_hook(self, d):
        if self.stop_flag: raise Exception("Interrupted by E-Stop!")
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try: self.msg_queue.put({"type": "progress", "val": float(p)/100})
            except: pass

    def trigger_stop(self):
        self.stop_flag = True; print("\n[E-STOP] Menerima sinyal pembatalan. Menutup operasi dengan aman...")
        self.btn_stop.configure(state="disabled", text="Membatalkan...")

    def start_thread(self):
        self.save_prefs(); self.stop_flag = False
        threading.Thread(target=self.logic, daemon=True).start()

    def logic(self):
        self.btn_start.configure(state="disabled"); self.btn_stop.configure(state="normal", text="⏹ BATALKAN (E-STOP)")
        self.msg_queue.put({"type": "progress", "val": 0})
        self.msg_queue.put({"type": "prog_mode", "val": "determinate"})
        try:
            ram_free = psutil.virtual_memory().available / (1024**3)
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            files_to_do = []
            
            if self.src_type.get() == "youtube":
                if not self.url_input.get(): raise ValueError("URL YouTube Kosong!")
                print("[YT] Mengekstrak audio jalur aman...")
                with yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': 'temp.mp3', 'progress_hooks': [self.yt_hook], 'quiet': True}) as ydl: ydl.download([self.url_input.get()])
                files_to_do.append(("temp.mp3", "YouTube_Extract"))
            else:
                if not self.local_files: raise ValueError("Belum ada file lokal yang dipilih!")
                for f in self.local_files: files_to_do.append((f, os.path.splitext(os.path.basename(f))[0]))

            # PROTEKSI TERJEMAHAN (FALLBACK LOGIC)
            engine = self.trans_opt.get()
            deepl_tr, google_tr, any_tr = None, None, None
            if engine == "deepl":
                key = self.deepl_key.get().strip()
                if not key:
                    print("[API WARNING] DeepL API Key kosong. Sistem melakukan Fallback otomatis ke Google Translate.")
                    engine = "google"
                else:
                    try: deepl_tr = deepl.Translator(key)
                    except: engine = "google"; print("[API ERROR] DeepL tidak merespon. Fallback otomatis ke Google Translate.")
            
            if engine == "google": google_tr = GoogleTranslator(source='auto', target='id')
            elif engine == "any2en": any_tr = GoogleTranslator(source='auto', target='en')

            # --- CABANG 1: ASSEMBLY AI CLOUD ---
            if self.use_aai.get():
                aai_key = self.aai_key.get().strip()
                if not aai_key: raise ValueError("AssemblyAI API Key kosong.")
                
                print("[SISTEM] Menghubungkan ke AssemblyAI Cloud...")
                aai.settings.api_key = aai_key
                vocab = [w.strip() for w in self.aai_vocab.get().split(",")] if self.aai_vocab.get() else None
                config = aai.TranscriptionConfig(auto_chapters=self.aai_chap.get(), entity_detection=self.aai_pii.get(), speaker_labels=self.aai_diar.get(), disfluencies=not self.aai_filler.get(), word_boost=vocab)
                transcriber = aai.Transcriber(config=config)
                self.msg_queue.put({"type": "prog_mode", "val": "indeterminate"})
                
                for path, name in files_to_do:
                    if self.stop_flag: break
                    print(f"[CLOUD] Memproses dokumen: {name}...")
                    try:
                        t_start = time.time()
                        transcript = transcriber.transcribe(path)
                        if transcript.error: raise ValueError(transcript.error)
                        
                        open(os.path.join(desktop, f"{name}_AAI.txt"), "w", encoding="utf-8").write(transcript.text)
                        if self.aai_chap.get() and transcript.chapters:
                            with open(os.path.join(desktop, f"{name}_Chapters.txt"), "w", encoding="utf-8") as f_chap:
                                for ch in transcript.chapters: f_chap.write(f"[{ch.start}-{ch.end}] {ch.headline}\n{ch.summary}\n\n")
                        
                        save_log(name, time.time() - t_start, "AssemblyAI Cloud")
                    except Exception as e: print(f"[AAI ERROR] Gagal memproses {name}: {e}")
                self.msg_queue.put({"type": "prog_mode", "val": "determinate"})

            # --- CABANG 2: FASTER-WHISPER LOKAL (V7.0 UPGRADE) ---
            else:
                m_type = self.ai_eng.get()
                if ram_free < 1.5: raise ValueError(f"RAM Anda terlalu kecil. Minimal 1.5GB Free RAM.")
                print(f"[AI ENGINE] Memuat arsitektur saraf FASTER-WHISPER {m_type.upper()}...")
                self.msg_queue.put({"type": "prog_mode", "val": "indeterminate"})
                
                # Inisiasi CTranslate2 Engine berbasis CPU (Agar ringan dan jalan di semua laptop)
                model = WhisperModel(m_type, device="cpu", compute_type="int8")
                
                for path, name in files_to_do:
                    if self.stop_flag: break
                    t_start = time.time()
                    proc_path = path
                    if self.clean_audio.get():
                        clean_path = f"clean_{os.path.basename(path)}.wav"
                        subprocess.run(["ffmpeg", "-y", "-i", path, "-af", "afftdn", clean_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        proc_path = clean_path

                    print(f"\n[AI] Menganalisis gelombang suara: {name}")
                    self.msg_queue.put({"type": "prog_mode", "val": "determinate"})
                    
                    # Faster-Whisper menghasilkan generator 'segments' dan 'info'
                    segments, info = model.transcribe(proc_path, beam_size=5)
                    audio_duration = info.duration
                    
                    bp = os.path.join(desktop, name)
                    doc_lines = []
                    
                    print(f"[I/O STREAM] Membuka jalur penulisan seketika ke Hardisk...")
                    f_srt = open(f"{bp}.srt", "w", encoding="utf-8") if self.out_srt.get() else None
                    f_vtt = open(f"{bp}.vtt", "w", encoding="utf-8") if self.out_vtt.get() else None
                    f_txt = open(f"{bp}.txt", "w", encoding="utf-8") if self.out_txt.get() else None
                    if f_vtt: f_vtt.write("WEBVTT\n\n")

                    # I/O STREAMING & PROGRESS TRACKING
                    for i, seg in enumerate(segments, start=1):
                        if self.stop_flag: break
                        
                        # Update Progress Bar secara presisi berdasarkan durasi segmen audio
                        if audio_duration > 0:
                            self.msg_queue.put({"type": "progress", "val": seg.end / audio_duration})
                        
                        s, e, text = seg.start, seg.end, seg.text.strip()

                        try:
                            if engine == "google": text = google_tr.translate(text)
                            elif engine == "deepl": text = deepl_tr.translate_text(text, target_lang="ID").text
                            elif engine == "any2en": text = any_tr.translate(text)
                        except: text = f"[Translate Error] {text}"

                        if f_srt: f_srt.write(f"{i}\n{self.format_ts(s, 'srt')} --> {self.format_ts(e, 'srt')}\n{text}\n\n")
                        if f_vtt: f_vtt.write(f"{self.format_ts(s, 'vtt')} --> {self.format_ts(e, 'vtt')}\n{text}\n\n")
                        
                        txt_line = f"{self.format_ts(s, 'txt')} {text}"
                        if f_txt: f_txt.write(f"{txt_line}\n")
                        
                        if self.out_docx.get() or self.out_pdf.get(): doc_lines.append(txt_line)
                        
                        # Tampilkan secercah log secara perlahan di konsol (Feedback visual)
                        if i % 10 == 0: print(f"Menulis baris ke-{i}...")

                    if f_srt: f_srt.close()
                    if f_vtt: f_vtt.close()
                    if f_txt: f_txt.close()

                    if self.stop_flag: break

                    if self.out_docx.get():
                        try:
                            doc = docx.Document()
                            for line in doc_lines: doc.add_paragraph(line)
                            doc.save(f"{bp}.docx")
                            print("[RENDER] File .docx sukses dibuat.")
                        except Exception as e: print(f"[Word Error] {e}")
                        
                    if self.out_pdf.get():
                        try:
                            c = canvas.Canvas(f"{bp}.pdf")
                            y = 800
                            for line in doc_lines:
                                if y < 40: c.showPage(); y = 800
                                c.drawString(40, y, line[:100]); y -= 15
                            c.save()
                            print("[RENDER] File .pdf sukses dibuat.")
                        except Exception as e: print(f"[PDF Error] {e}")
                    
                    if self.clean_audio.get() and os.path.exists(proc_path): os.remove(proc_path)
                    
                    # Simpan Log ke Database Lokal
                    save_log(name, time.time() - t_start, f"Faster-Whisper ({m_type.capitalize()})")

            if self.src_type.get() == "youtube" and os.path.exists("temp.mp3"): os.remove("temp.mp3")
            
            if self.stop_flag: messagebox.showwarning("Dibatalkan", "Soft E-Stop berhasil. File yang setengah jalan tetap tersimpan aman.")
            else: messagebox.showinfo("Sukses", "100% Selesai! Seluruh file telah diletakkan di Desktop.")

        except Exception as e: messagebox.showerror("System Error", str(e))
        finally:
            self.btn_start.configure(state="normal"); self.btn_stop.configure(state="disabled", text="⏹ BATALKAN (E-STOP)")
            self.msg_queue.put({"type": "progress", "val": 0})

if __name__ == "__main__":
    app = PlatinumTranscriberApp()
    app.mainloop()