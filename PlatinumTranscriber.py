import os
import sys
import threading
import json
import subprocess
import urllib.request
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# --- PRE-FLIGHT LIBRARIES CHECK ---
missing_libs = []
for lib in ['yt_dlp', 'whisper', 'deep_translator', 'deepl', 'docx', 'reportlab', 'psutil', 'assemblyai', 'customtkinter']:
    try: __import__(lib)
    except: missing_libs.append(lib)

if missing_libs:
    tk.Tk().withdraw()
    err_msg = "Library belum terinstal / Missing Libraries:\n" + "\n".join(missing_libs)
    err_msg += "\n\nJalankan / Run:\npython -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter"
    messagebox.showerror("System Diagnostics Failed", err_msg)
    sys.exit()

import yt_dlp
import whisper
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

class TextRedirector:
    def __init__(self, widget): self.widget = widget
    def write(self, text):
        self.widget.configure(state="normal"); self.widget.insert("end", text)
        self.widget.see("end"); self.widget.configure(state="disabled"); self.widget.update_idletasks()
    def flush(self): pass

class PlatinumTranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Platinum Transcriber (Greatest Ultimate V5)")
        self.geometry("900x750")
        self.stop_flag = False
        
        self.setup_vars()
        self.load_prefs()
        self.setup_ui()
        
        sys.stdout = TextRedirector(self.console_log)
        sys.stderr = TextRedirector(self.console_log)

    def setup_vars(self):
        self.src_type = ctk.StringVar(value="local")
        self.ai_eng = ctk.StringVar(value="small")
        self.out_srt = ctk.BooleanVar(value=True); self.out_vtt = ctk.BooleanVar(value=False)
        self.out_txt = ctk.BooleanVar(value=True); self.out_docx = ctk.BooleanVar(value=False); self.out_pdf = ctk.BooleanVar(value=False)
        self.trans_opt = ctk.StringVar(value="none")
        self.clean_audio = ctk.BooleanVar(value=False)
        
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

        top_bar = ctk.CTkFrame(main_frm, fg_color="transparent"); top_bar.pack(fill="x")
        self.btn_lang = ctk.CTkButton(top_bar, text="🔄 English", command=self.toggle_lang, width=100)
        self.btn_lang.pack(side="right")
        self.btn_diag = ctk.CTkButton(main_frm, text="🔍 DIAGNOSTIK SISTEM", fg_color="#ff9800", hover_color="#e68a00", command=self.run_diag)
        self.btn_diag.pack(fill="x", pady=5)

        self.tabs = ctk.CTkTabview(main_frm)
        self.tabs.pack(fill="both", expand=True, pady=5)
        self.t1 = self.tabs.add("1. Input & Mesin AI")
        self.t2 = self.tabs.add("2. Output & Terjemahan")
        self.t3 = self.tabs.add("3. AssemblyAI & Cloud")

        # TAB 1
        ctk.CTkRadioButton(self.t1, text="Link YouTube (~30MB/jam)", variable=self.src_type, value="youtube", command=self.toggle_src).pack(anchor="w", pady=5)
        self.url_ent = ctk.CTkEntry(self.t1, textvariable=self.url_input, width=500, placeholder_text="Tempel link YouTube...")
        ctk.CTkRadioButton(self.t1, text="File Lokal (Batch - 100% Offline)", variable=self.src_type, value="local", command=self.toggle_src).pack(anchor="w", pady=5)
        self.f_frm = ctk.CTkFrame(self.t1, fg_color="transparent")
        ctk.CTkButton(self.f_frm, text="Cari File", command=self.browse).pack(side="left")
        self.f_lbl = ctk.CTkLabel(self.f_frm, text="Belum ada file", text_color="gray"); self.f_lbl.pack(side="left", padx=10)
        
        ctk.CTkLabel(self.t1, text="\nKapasitas Mesin AI (Periksa Spek Laptop):", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10,0))
        ctk.CTkRadioButton(self.t1, text="Whisper SMALL (~460MB | Cepat & Ringan | RAM > 2GB)", variable=self.ai_eng, value="small").pack(anchor="w", pady=5)
        ctk.CTkRadioButton(self.t1, text="Whisper MEDIUM (~1.5GB | Presisi Tinggi | RAM > 5GB)", variable=self.ai_eng, value="medium").pack(anchor="w", pady=5)

        # TAB 2
        ctk.CTkLabel(self.t2, text="Format Output:", font=("Arial", 14, "bold")).pack(anchor="w")
        frm_out = ctk.CTkFrame(self.t2, fg_color="transparent"); frm_out.pack(anchor="w")
        for text, var in [(".srt (Video)", self.out_srt), (".vtt", self.out_vtt), (".txt (Baca)", self.out_txt), (".docx (Word)", self.out_docx), (".pdf", self.out_pdf)]:
            ctk.CTkCheckBox(frm_out, text=text, variable=var).pack(side="left", padx=5)

        ctk.CTkLabel(self.t2, text="\nOpsi Terjemahan:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10,0))
        ctk.CTkRadioButton(self.t2, text="Teks Original (100% Offline)", variable=self.trans_opt, value="none").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.t2, text="Google Translate (EN->ID | Ringan <1MB)", variable=self.trans_opt, value="google").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.t2, text="Terjemahkan ke English (Any->EN)", variable=self.trans_opt, value="any2en").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.t2, text="DeepL AI (Presisi Tinggi EN->ID)", variable=self.trans_opt, value="deepl").pack(anchor="w", pady=2)
        ctk.CTkEntry(self.t2, textvariable=self.deepl_key, width=400, show="*", placeholder_text="DeepL API Key (Opsional)").pack(anchor="w", pady=5)

        # TAB 3
        ctk.CTkLabel(self.t3, text="Audio Pre-Processing (Lokal):", font=("Arial", 14, "bold")).pack(anchor="w")
        ctk.CTkCheckBox(self.t3, text="FFmpeg Noise Reduction (Pembersih Bising)", variable=self.clean_audio).pack(anchor="w", pady=5)

        ctk.CTkLabel(self.t3, text="\nIntegrasi AssemblyAI Cloud (Mengabaikan Whisper):", font=("Arial", 14, "bold")).pack(anchor="w")
        ctk.CTkCheckBox(self.t3, text="Gunakan AssemblyAI", variable=self.use_aai).pack(anchor="w", pady=5)
        frm_aai = ctk.CTkFrame(self.t3, fg_color="transparent"); frm_aai.pack(anchor="w")
        ctk.CTkCheckBox(frm_aai, text="Auto Chapters", variable=self.aai_chap).pack(side="left", padx=5)
        ctk.CTkCheckBox(frm_aai, text="Redaksi PII", variable=self.aai_pii).pack(side="left", padx=5)
        ctk.CTkCheckBox(frm_aai, text="Diarization", variable=self.aai_diar).pack(side="left", padx=5)
        ctk.CTkCheckBox(frm_aai, text="Hapus Kata Pengisi (um, ah)", variable=self.aai_filler).pack(side="left", padx=5)
        
        ctk.CTkEntry(self.t3, textvariable=self.aai_vocab, width=400, placeholder_text="Custom Vocab (Pisahkan dengan koma: safety, hazmat, JSA)").pack(anchor="w", pady=5)
        ctk.CTkEntry(self.t3, textvariable=self.aai_key, width=400, show="*", placeholder_text="AssemblyAI API Key").pack(anchor="w", pady=5)

        # DASHBOARD
        self.prog_bar = ctk.CTkProgressBar(main_frm); self.prog_bar.pack(fill="x", pady=5); self.prog_bar.set(0)
        btn_frm = ctk.CTkFrame(main_frm, fg_color="transparent"); btn_frm.pack(fill="x")
        self.btn_start = ctk.CTkButton(btn_frm, text="▶ MULAI EKSEKUSI", fg_color="#006400", hover_color="#004d00", font=("Arial", 14, "bold"), command=self.start_thread)
        self.btn_start.pack(side="left", expand=True, fill="x", padx=(0,5))
        self.btn_stop = ctk.CTkButton(btn_frm, text="⏹ BATALKAN (E-STOP)", fg_color="#8B0000", hover_color="#660000", font=("Arial", 14, "bold"), state="disabled", command=self.trigger_stop)
        self.btn_stop.pack(side="right", expand=True, fill="x", padx=(5,0))
        self.console_log = ctk.CTkTextbox(main_frm, height=120, text_color="#00FF00", fg_color="black", font=("Consolas", 12))
        self.console_log.pack(fill="both", expand=True, pady=5); self.console_log.configure(state="disabled")
        self.toggle_src()

    def toggle_lang(self):
        self.current_lang = "id" if self.current_lang == "en" else "en"
        self.btn_lang.configure(text="🔄 English" if self.current_lang == "id" else "🔄 Indonesia")

    def toggle_src(self):
        if self.src_type.get() == "youtube": self.f_frm.pack_forget(); self.url_ent.pack(anchor="w", pady=5)
        else: self.url_ent.pack_forget(); self.f_frm.pack(anchor="w", pady=5)

    def browse(self):
        f = filedialog.askopenfilenames()
        if f: self.local_files = list(f); self.f_lbl.configure(text=f"{len(f)} files", text_color="#00FF00")

    def run_diag(self):
        ram = psutil.virtual_memory()
        fr = ram.available / (1024**3); tr = ram.total / (1024**3)
        fs = shutil.disk_usage(os.path.expanduser("~"))[2] / (1024**3)
        ff = "✅" if subprocess.run(["ffmpeg", "-version"], capture_output=True).returncode == 0 else "❌"
        try: urllib.request.urlopen('http://google.com', timeout=3); inet = "✅"
        except: inet = "❌"
        messagebox.showinfo("Pre-Flight Check", f"Internet: {inet}\nFFmpeg: {ff}\nRAM Free: {fr:.2f}GB / {tr:.2f}GB\nStorage Free: {fs:.2f}GB")

    # FORMAT TIMESTAMP MURNI [02:05]
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
        if self.stop_flag: raise Exception("Dibatalkan!")
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try: self.prog_bar.set(float(p)/100)
            except: pass
            print(f"[YT] Downloading: {p}%", end='\r')

    def trigger_stop(self):
        self.stop_flag = True; print("\n[E-STOP] Menunggu proses membatalkan...")
        self.btn_stop.configure(state="disabled", text="Membatalkan...")

    def start_thread(self):
        self.save_prefs(); self.stop_flag = False
        threading.Thread(target=self.logic, daemon=True).start()

    def logic(self):
        self.btn_start.configure(state="disabled"); self.btn_stop.configure(state="normal", text="⏹ BATALKAN")
        self.prog_bar.set(0); self.prog_bar.configure(mode="determinate")
        try:
            ram_free = psutil.virtual_memory().available / (1024**3)
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            files_to_do = []
            
            if self.src_type.get() == "youtube":
                if not self.url_input.get(): raise ValueError("URL Kosong!")
                print("[YT] Mengekstrak audio...")
                with yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': 'temp.mp3', 'progress_hooks': [self.yt_hook], 'quiet': True}) as ydl: ydl.download([self.url_input.get()])
                files_to_do.append(("temp.mp3", "YouTube_Extract"))
            else:
                if not self.local_files: raise ValueError("Pilih file lokal!")
                for f in self.local_files: files_to_do.append((f, os.path.splitext(os.path.basename(f))[0]))

            # Fallback DeepL & Opsi Terjemahan Terbaik
            engine = self.trans_opt.get()
            deepl_tr, google_tr, any_tr = None, None, None
            if engine == "deepl":
                key = self.deepl_key.get().strip()
                if not key:
                    if messagebox.askyesno("API Key Kosong", "DeepL butuh API Key. Ingin otomatis alihkan ke Google Translate (Gratis)?"): engine = "google"
                    else: raise ValueError("DeepL dibatalkan.")
                else:
                    try: deepl_tr = deepl.Translator(key)
                    except: engine = "google"; print("[API LIMIT] DeepL error. Fallback ke Google.")
            
            if engine == "google": google_tr = GoogleTranslator(source='auto', target='id')
            elif engine == "any2en": any_tr = GoogleTranslator(source='auto', target='en')

            # BLOK ASSEMBLYAI
            if self.use_aai.get():
                aai_key = self.aai_key.get().strip()
                if not aai_key: raise ValueError("AssemblyAI butuh API Key!")
                aai.settings.api_key = aai_key
                vocab = [w.strip() for w in self.aai_vocab.get().split(",")] if self.aai_vocab.get() else None
                config = aai.TranscriptionConfig(auto_chapters=self.aai_chap.get(), entity_detection=self.aai_pii.get(), speaker_labels=self.aai_diar.get(), disfluencies=not self.aai_filler.get(), word_boost=vocab)
                
                transcriber = aai.Transcriber(config=config)
                self.prog_bar.configure(mode="indeterminate"); self.prog_bar.start()
                for path, name in files_to_do:
                    if self.stop_flag: break
                    print(f"[AAI CLOUD] Mengunggah {name}...")
                    try:
                        transcript = transcriber.transcribe(path)
                        if transcript.error: raise ValueError(transcript.error)
                        open(os.path.join(desktop, f"{name}_AAI.txt"), "w", encoding="utf-8").write(transcript.text)
                    except Exception as e: print(f"[AAI ERROR] Gagal memproses {name}: {e}")
                self.prog_bar.stop()

            # BLOK WHISPER LOKAL
            else:
                m_type = self.ai_eng.get()
                if ram_free < (4.5 if m_type == "medium" else 2.0): raise ValueError(f"RAM {ram_free:.2f}GB tidak cukup!")
                print(f"[AI] Memuat Whisper {m_type.upper()}... (Pertama kali: Small ~460MB, Medium ~1.5GB)")
                model = whisper.load_model(m_type)
                
                for path, name in files_to_do:
                    if self.stop_flag: break
                    proc_path = path
                    if self.clean_audio.get():
                        clean_path = f"clean_{os.path.basename(path)}.wav"
                        subprocess.run(["ffmpeg", "-y", "-i", path, "-af", "afftdn", clean_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        proc_path = clean_path

                    print(f"\n[AI] Menganalisis: {name}")
                    self.prog_bar.configure(mode="indeterminate"); self.prog_bar.start()
                    res = model.transcribe(proc_path, verbose=False)
                    self.prog_bar.stop(); self.prog_bar.configure(mode="determinate")
                    
                    segments = res["segments"]
                    total_segs = len(segments)
                    srt_c, vtt_c, txt_c = "", "WEBVTT\n\n", ""

                    for i, seg in enumerate(segments, start=1):
                        if self.stop_flag: break
                        self.prog_bar.set(i / total_segs)
                        s, e, text = seg["start"], seg["end"], seg["text"].strip()

                        # Perlindungan Terjemahan Berlapis
                        try:
                            if engine == "google": text = google_tr.translate(text)
                            elif engine == "deepl": text = deepl_tr.translate_text(text, target_lang="ID").text
                            elif engine == "any2en": text = any_tr.translate(text)
                        except: text = f"[Error] {text}"

                        if self.out_srt.get(): srt_c += f"{i}\n{self.format_ts(s, 'srt')} --> {self.format_ts(e, 'srt')}\n{text}\n\n"
                        if self.out_vtt.get(): vtt_c += f"{self.format_ts(s, 'vtt')} --> {self.format_ts(e, 'vtt')}\n{text}\n\n"
                        # Penumpukan baris dengan Format Waktu Murni yang presisi
                        txt_c += f"{self.format_ts(s, 'txt')} {text}\n"

                    if self.stop_flag: break
                    print(f"\n[SISTEM] Menyimpan ke Desktop...")
                    bp = os.path.join(desktop, name)
                    if self.out_srt.get(): open(f"{bp}.srt", "w", encoding="utf-8").write(srt_c)
                    if self.out_vtt.get(): open(f"{bp}.vtt", "w", encoding="utf-8").write(vtt_c)
                    if self.out_txt.get(): open(f"{bp}.txt", "w", encoding="utf-8").write(txt_c)
                    if self.out_docx.get():
                        try:
                            doc = docx.Document()
                            for line in txt_c.split('\n'): doc.add_paragraph(line)
                            doc.save(f"{bp}.docx")
                        except Exception as e: print(f"[DOCX Error] {e}")
                    if self.out_pdf.get():
                        try:
                            c = canvas.Canvas(f"{bp}.pdf")
                            y = 800
                            for line in txt_c.split('\n'):
                                if y < 40: c.showPage(); y = 800
                                c.drawString(40, y, line[:100]); y -= 15
                            c.save()
                        except Exception as e: print(f"[PDF Error] {e}")
                    
                    if self.clean_audio.get() and os.path.exists(proc_path): os.remove(proc_path)

            if self.src_type.get() == "youtube" and os.path.exists("temp.mp3"): os.remove("temp.mp3")
            
            if self.stop_flag: messagebox.showwarning("Dibatalkan", "Operasi dibatalkan dengan aman.")
            else: messagebox.showinfo("Sukses", "Selesai 100%! Cek Desktop Anda.")

        except Exception as e: messagebox.showerror("System Error", str(e))
        finally:
            self.btn_start.configure(state="normal"); self.btn_stop.configure(state="disabled", text="⏹ BATALKAN")
            self.prog_bar.set(0)

if __name__ == "__main__":
    app = PlatinumTranscriberApp()
    app.mainloop()