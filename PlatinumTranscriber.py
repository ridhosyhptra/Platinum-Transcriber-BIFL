import os
import sys
import threading
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import subprocess
import urllib.request
import shutil

# --- 1. PERLINDUNGAN IMPOR (PRE-FLIGHT CHECK LIBRARIES) ---
missing_libs = []
try: import yt_dlp
except: missing_libs.append("yt-dlp")
try: import whisper
except: missing_libs.append("openai-whisper")
try: from deep_translator import GoogleTranslator
except: missing_libs.append("deep-translator")
try: import deepl
except: missing_libs.append("deepl")
try: import docx
except: missing_libs.append("python-docx")
try: from reportlab.pdfgen import canvas
except: missing_libs.append("reportlab")
try: import psutil
except: missing_libs.append("psutil")
try: import assemblyai as aai
except: missing_libs.append("assemblyai")

# --- KELAS TELEMETRI (REDIRECT TERMINAL) ---
class TextRedirector(object):
    def __init__(self, widget): self.widget = widget
    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str)
        self.widget.see("end")
        self.widget.configure(state="disabled")
        self.widget.update_idletasks()
    def flush(self): pass

# --- KELAS UTAMA APLIKASI ---
class PlatinumTranscriberApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "id"
        
        # Jika ada library hilang, munculkan Pop-Up Error lalu hentikan aplikasi
        if missing_libs:
            err_msg = "Library belum terinstal / Missing Libraries:\n" + "\n".join(missing_libs)
            err_msg += "\n\nJalankan / Run:\npython -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai"
            messagebox.showerror("Fatal Error", err_msg)
            self.root.destroy()
            return

        self.setup_variables()
        self.setup_ui()
        self.update_texts()
        
        sys.stdout = TextRedirector(self.console_log)
        sys.stderr = TextRedirector(self.console_log)

    def setup_variables(self):
        self.source_type = tk.StringVar(value="local")
        self.ai_engine = tk.StringVar(value="small")
        self.out_srt = tk.BooleanVar(value=True)
        self.out_vtt = tk.BooleanVar(value=False)
        self.out_txt = tk.BooleanVar(value=False)
        self.out_docx = tk.BooleanVar(value=False)
        self.out_pdf = tk.BooleanVar(value=False)
        self.trans_opt = tk.StringVar(value="none")
        
        # AssemblyAI Options
        self.use_aai = tk.BooleanVar(value=False)
        self.aai_chapters = tk.BooleanVar(value=False)
        self.aai_pii = tk.BooleanVar(value=False)
        self.aai_diarization = tk.BooleanVar(value=False)
        
        self.deepl_key = tk.StringVar()
        self.aai_key = tk.StringVar()
        self.url_input = tk.StringVar()
        self.local_files = []
        self.file_lbl_txt = tk.StringVar()

    def toggle_lang(self):
        self.current_lang = "id" if self.current_lang == "en" else "en"
        self.update_texts()

    def update_texts(self):
        # Kamus Dwibahasa Real-Time
        t_id = {
            "title": "Platinum Transcriber (Masterplan Edition)", "btn_lang": "🔄 English", "btn_diag": "🔍 DIAGNOSTIK SISTEM",
            "l1": "1. Sumber Media:", "rb_yt": "YouTube (~30MB/jam)", "rb_loc": "File Lokal (Batch 100% Offline)", "btn_br": "Browse",
            "l2": "2. Mesin AI (Cek RAM):", "rb_sm": "Whisper SMALL (~460MB | >2GB RAM)", "rb_md": "Whisper MEDIUM (~1.5GB | >5GB RAM)",
            "l3": "3. Format Output:", "l4": "4. Terjemahan:", "rb_ori": "Teks Asli (Offline)", "rb_gt": "Google Translate (EN->ID)",
            "rb_dp": "DeepL (Presisi EN->ID)", "rb_any": "Terjemahkan ke English (Any->EN)",
            "l5": "5. Integrasi AssemblyAI (Opsional, Butuh Internet & API):",
            "cb_aai": "Gunakan AssemblyAI (Mengabaikan Whisper)", "cb_ch": "Auto Chapters", "cb_pii": "Sensor Info Pribadi (PII)", "cb_dia": "Deteksi Pembicara (Diarization)",
            "btn_start": "MULAI PROSES", "lbl_mon": "Layar Telemetri Real-Time:"
        }
        t_en = {
            "title": "Platinum Transcriber (Masterplan Edition)", "btn_lang": "🔄 Bahasa Indonesia", "btn_diag": "🔍 SYSTEM DIAGNOSTICS",
            "l1": "1. Media Source:", "rb_yt": "YouTube (~30MB/hr)", "rb_loc": "Local File (Batch 100% Offline)", "btn_br": "Browse",
            "l2": "2. AI Engine (Check RAM):", "rb_sm": "Whisper SMALL (~460MB | >2GB RAM)", "rb_md": "Whisper MEDIUM (~1.5GB | >5GB RAM)",
            "l3": "3. Output Formats:", "l4": "4. Translation:", "rb_ori": "Original Text (Offline)", "rb_gt": "Google Translate (EN->ID)",
            "rb_dp": "DeepL (High Precision EN->ID)", "rb_any": "Translate to English (Any->EN)",
            "l5": "5. AssemblyAI Integration (Optional, Needs API):",
            "cb_aai": "Use AssemblyAI (Overrides Whisper)", "cb_ch": "Auto Chapters", "cb_pii": "Redact PII", "cb_dia": "Speaker Diarization",
            "btn_start": "START PROCESSING", "lbl_mon": "Real-Time Telemetry:"
        }
        c = t_id if self.current_lang == "id" else t_en
        self.root.title(c["title"])
        self.btn_lang.config(text=c["btn_lang"]); self.btn_diag.config(text=c["btn_diag"])
        self.lbl_1.config(text=c["l1"]); self.r_yt.config(text=c["rb_yt"]); self.r_loc.config(text=c["rb_loc"]); self.btn_br.config(text=c["btn_br"])
        self.lbl_2.config(text=c["l2"]); self.r_sm.config(text=c["rb_sm"]); self.r_md.config(text=c["rb_md"])
        self.lbl_3.config(text=c["l3"]); self.lbl_4.config(text=c["l4"])
        self.r_ori.config(text=c["rb_ori"]); self.r_gt.config(text=c["rb_gt"]); self.r_dp.config(text=c["rb_dp"]); self.r_any.config(text=c["rb_any"])
        self.lbl_5.config(text=c["l5"]); self.c_aai.config(text=c["cb_aai"]); self.c_ch.config(text=c["cb_ch"]); self.c_pii.config(text=c["cb_pii"]); self.c_dia.config(text=c["cb_dia"])
        self.btn_start.config(text=c["btn_start"]); self.lbl_mon.config(text=c["lbl_mon"])

    def setup_ui(self):
        # Menggunakan Frame dan Grid untuk UI yang bersih dan rapi
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        top_bar = tk.Frame(main_frame); top_bar.pack(fill="x")
        self.btn_lang = tk.Button(top_bar, command=self.toggle_lang); self.btn_lang.pack(side="right")
        self.btn_diag = tk.Button(main_frame, bg="#ff9800", font=("Arial", 10, "bold"), command=self.run_diagnostics)
        self.btn_diag.pack(fill="x", pady=5)

        # Container Kiri & Kanan
        left_col = tk.Frame(main_frame); left_col.pack(side="left", fill="both", expand=True)
        right_col = tk.Frame(main_frame); right_col.pack(side="right", fill="both", expand=True, padx=10)

        # --- KOLOM KIRI ---
        self.lbl_1 = tk.Label(left_col, font=("Arial", 10, "bold")); self.lbl_1.pack(anchor="w")
        self.r_yt = tk.Radiobutton(left_col, variable=self.source_type, value="youtube", command=self.toggle_source); self.r_yt.pack(anchor="w")
        self.r_loc = tk.Radiobutton(left_col, variable=self.source_type, value="local", command=self.toggle_source); self.r_loc.pack(anchor="w")
        
        self.src_frame = tk.Frame(left_col); self.src_frame.pack(fill="x", pady=5)
        self.url_ent = tk.Entry(self.src_frame, textvariable=self.url_input, width=40)
        self.file_frm = tk.Frame(self.src_frame)
        self.btn_br = tk.Button(self.file_frm, command=self.browse_files); self.btn_br.pack(side="left")
        tk.Label(self.file_frm, textvariable=self.file_lbl_txt, fg="blue").pack(side="left", padx=5)

        self.lbl_2 = tk.Label(left_col, font=("Arial", 10, "bold")); self.lbl_2.pack(anchor="w", pady=(10,0))
        self.r_sm = tk.Radiobutton(left_col, variable=self.ai_engine, value="small"); self.r_sm.pack(anchor="w")
        self.r_md = tk.Radiobutton(left_col, variable=self.ai_engine, value="medium"); self.r_md.pack(anchor="w")

        self.lbl_4 = tk.Label(left_col, font=("Arial", 10, "bold")); self.lbl_4.pack(anchor="w", pady=(10,0))
        self.r_ori = tk.Radiobutton(left_col, variable=self.trans_opt, value="none"); self.r_ori.pack(anchor="w")
        self.r_gt = tk.Radiobutton(left_col, variable=self.trans_opt, value="google"); self.r_gt.pack(anchor="w")
        self.r_dp = tk.Radiobutton(left_col, variable=self.trans_opt, value="deepl"); self.r_dp.pack(anchor="w")
        self.r_any = tk.Radiobutton(left_col, variable=self.trans_opt, value="any2en"); self.r_any.pack(anchor="w")
        
        tk.Label(left_col, text="DeepL API Key:").pack(anchor="w")
        tk.Entry(left_col, textvariable=self.deepl_key, width=40, show="*").pack(anchor="w")

        # --- KOLOM KANAN ---
        self.lbl_3 = tk.Label(right_col, font=("Arial", 10, "bold")); self.lbl_3.pack(anchor="w")
        tk.Checkbutton(right_col, text=".srt", variable=self.out_srt).pack(anchor="w")
        tk.Checkbutton(right_col, text=".vtt", variable=self.out_vtt).pack(anchor="w")
        tk.Checkbutton(right_col, text=".txt", variable=self.out_txt).pack(anchor="w")
        tk.Checkbutton(right_col, text=".docx", variable=self.out_docx).pack(anchor="w")
        tk.Checkbutton(right_col, text=".pdf", variable=self.out_pdf).pack(anchor="w")

        self.lbl_5 = tk.Label(right_col, font=("Arial", 10, "bold")); self.lbl_5.pack(anchor="w", pady=(10,0))
        self.c_aai = tk.Checkbutton(right_col, variable=self.use_aai); self.c_aai.pack(anchor="w")
        self.c_ch = tk.Checkbutton(right_col, variable=self.aai_chapters); self.c_ch.pack(anchor="w", padx=15)
        self.c_pii = tk.Checkbutton(right_col, variable=self.aai_pii); self.c_pii.pack(anchor="w", padx=15)
        self.c_dia = tk.Checkbutton(right_col, variable=self.aai_diarization); self.c_dia.pack(anchor="w", padx=15)
        tk.Label(right_col, text="AssemblyAI Key:").pack(anchor="w")
        tk.Entry(right_col, textvariable=self.aai_key, width=40, show="*").pack(anchor="w")

        # --- BAWAH (TELEMETRI & TOMBOL) ---
        bottom_frame = tk.Frame(self.root); bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.btn_start = tk.Button(bottom_frame, bg="#002147", fg="white", font=("Arial", 12, "bold"), command=self.start_thread)
        self.btn_start.pack(fill="x", pady=10)
        
        self.lbl_mon = tk.Label(bottom_frame, font=("Arial", 10, "bold"), fg="#002147"); self.lbl_mon.pack(anchor="w")
        self.console_log = ScrolledText(bottom_frame, height=12, bg="black", fg="lime", font=("Consolas", 9))
        self.console_log.pack(fill="both", expand=True)
        self.toggle_source()

    def toggle_source(self):
        if self.source_type.get() == "youtube":
            self.file_frm.pack_forget(); self.url_ent.pack(anchor="w")
        else:
            self.url_ent.pack_forget(); self.file_frm.pack(anchor="w")

    def browse_files(self):
        f = filedialog.askopenfilenames()
        if f:
            self.local_files = list(f)
            self.file_lbl_txt.set(f"{len(f)} files")

    # --- FUNGSI DIAGNOSTIK PRE-FLIGHT ---
    def run_diagnostics(self):
        import psutil
        ram = psutil.virtual_memory()
        free_ram_gb = ram.available / (1024**3)
        total_ram_gb = ram.total / (1024**3)
        
        total_st, used_st, free_st = shutil.disk_usage(os.path.expanduser("~"))
        free_storage_gb = free_st / (1024**3)
        
        ffmpeg_ok = "✅" if subprocess.run(["ffmpeg", "-version"], capture_output=True).returncode == 0 else "❌"
        try: urllib.request.urlopen('http://google.com', timeout=3); net_ok = "✅"
        except: net_ok = "❌"

        msg = f"--- PRE-FLIGHT CHECK ---\nInternet: {net_ok}\nFFmpeg: {ffmpeg_ok}\nRAM Free: {free_ram_gb:.2f} GB / {total_ram_gb:.2f} GB\nStorage Free: {free_storage_gb:.2f} GB"
        print(msg)
        messagebox.showinfo("Diagnostik Sistem", msg)

    # --- FORMAT TIMESTAMP MURNI ---
    def format_timestamp(self, seconds, fmt="txt"):
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if fmt in ["srt", "vtt"]:
            delim = "," if fmt == "srt" else "."
            millisecs = int((seconds - int(seconds)) * 1000)
            return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}{delim}{millisecs:03d}"
        else:
            # Sesuai permintaan: Detik murni misal [02:05]
            if hours > 0: return f"[{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}]"
            return f"[{int(minutes):02d}:{int(secs):02d}]"

    def yt_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            print(f"[YT-DLP] Mengunduh: {p}", end='\r')

    # --- THREADING AGAR GUI TIDAK FREEZE ---
    def start_thread(self):
        threading.Thread(target=self.process_logic, daemon=True).start()

    def process_logic(self):
        self.btn_start.config(state="disabled")
        try:
            print("\n[SYSTEM] Menginisiasi The Platinum Engine...")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            # Cek Output Terpilih
            if not any([self.out_srt.get(), self.out_vtt.get(), self.out_txt.get(), self.out_docx.get(), self.out_pdf.get()]):
                raise ValueError("Pilih minimal 1 Format Output!")

            # 1. Kumpulkan File
            files_to_process = []
            if self.source_type.get() == "youtube":
                url = self.url_input.get().strip()
                if not url: raise ValueError("URL Kosong!")
                print("[YT] Menarik audio dari YouTube...")
                with yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': 'temp_audio.mp3', 'progress_hooks': [self.yt_hook], 'quiet': True}) as ydl:
                    ydl.download([url])
                files_to_process.append(("temp_audio.mp3", "YouTube_Extract"))
            else:
                if not self.local_files: raise ValueError("Pilih file lokal!")
                for f in self.local_files: files_to_process.append((f, os.path.splitext(os.path.basename(f))[0]))

            # 2. Persiapan Translasi & Fallback Proteksi
            engine = self.trans_opt.get()
            deepl_trans = None
            if engine == "deepl":
                key = self.deepl_key.get().strip()
                if not key:
                    print("\n[WARNING] DeepL API Key kosong! Mengalihkan ke Google Translate agar tidak error.")
                    engine = "google"
                else:
                    try: deepl_trans = deepl.Translator(key)
                    except Exception as e:
                        print(f"\n[WARNING] Error DeepL: {e}. Mengalihkan ke Google Translate.")
                        engine = "google"
            
            google_trans = GoogleTranslator(source='auto', target='id') if engine == "google" else None
            google_any2en = GoogleTranslator(source='auto', target='en') if engine == "any2en" else None

            # 3. Eksekusi AssemblyAI vs Whisper
            if self.use_aai.get():
                aai_key = self.aai_key.get().strip()
                if not aai_key:
                    raise ValueError("AssemblyAI dipilih tapi API Key kosong! Masukkan key atau hapus centang AssemblyAI.")
                
                import assemblyai as aai
                aai.settings.api_key = aai_key
                config = aai.TranscriptionConfig(
                    auto_chapters=self.aai_chapters.get(),
                    entity_detection=self.aai_pii.get(),
                    speaker_labels=self.aai_diarization.get()
                )
                print("[API] Mengirim data ke AssemblyAI Cloud...")
                transcriber = aai.Transcriber(config=config)
                
                for path, name in files_to_process:
                    print(f"[AAI] Memproses {name}...")
                    transcript = transcriber.transcribe(path)
                    if transcript.error: raise ValueError(f"AAI Error: {transcript.error}")
                    
                    final_text = transcript.text
                    # Membuat TXT standar
                    if self.out_txt.get():
                        with open(os.path.join(desktop, f"{name}.txt"), "w", encoding="utf-8") as f:
                            f.write(final_text)
                    
                    # Ekstraksi Chapters
                    if self.aai_chapters.get() and transcript.chapters:
                        with open(os.path.join(desktop, f"{name}_Chapters.txt"), "w", encoding="utf-8") as f:
                            for ch in transcript.chapters:
                                f.write(f"[{ch.start}-{ch.end}] {ch.headline}\n{ch.summary}\n\n")
                    print(f"[OK] Selesai AssemblyAI untuk {name}")

            else:
                # LOCAL WHISPER PROCESSING
                m_type = self.ai_engine.get()
                import psutil
                if psutil.virtual_memory().available / (1024**3) < (4.5 if m_type == "medium" else 2.0):
                    raise ValueError("RAM tidak cukup! Pilih model SMALL.")
                
                print(f"\n[AI] Memuat mesin Whisper {m_type.upper()}...")
                print(f"[INFO] Jika file .pt belum ada, AI akan mengunduhnya sekarang (Small 460MB / Medium 1.5GB).")
                model = whisper.load_model(m_type)
                
                for path, name in files_to_process:
                    print(f"\n[AI] Mentranskripsi: {name}")
                    res = model.transcribe(path, verbose=False)
                    
                    srt_content, vtt_content, txt_content = "", "WEBVTT\n\n", ""
                    total_segs = len(res["segments"])
                    print(f"[AI] Memproses {total_segs} baris...")

                    # BLOK LOOP SESUAI PERMINTAAN USER (Merapikan waktu di depan baris)
                    for i, segment in enumerate(res["segments"], start=1):
                        print(f"Memformat baris {i}/{total_segs}...", end='\r')
                        s_start = segment["start"]; s_end = segment["end"]
                        text = segment["text"].strip()

                        # Blok Try-Except Berlapis untuk Jaringan Translasi
                        try:
                            if engine == "google": text = google_trans.translate(text)
                            elif engine == "deepl": text = deepl_trans.translate_text(text, target_lang="ID").text
                            elif engine == "any2en": text = google_any2en.translate(text)
                        except Exception as e:
                            text = f"[Trans Error] {text}"

                        # Format SRT
                        if self.out_srt.get():
                            srt_content += f"{i}\n{self.format_timestamp(s_start, 'srt')} --> {self.format_timestamp(s_end, 'srt')}\n{text}\n\n"
                        # Format VTT
                        if self.out_vtt.get():
                            vtt_content += f"{self.format_timestamp(s_start, 'vtt')} --> {self.format_timestamp(s_end, 'vtt')}\n{text}\n\n"
                        # Format TXT (Menit & Detik presisi)
                        txt_content += f"{self.format_timestamp(s_start, 'txt')} {text}\n"

                    # 4. PENYIMPANAN MULTI-FORMAT
                    print(f"\n[SISTEM] Menyimpan file ke Desktop...")
                    base_path = os.path.join(desktop, name)
                    
                    if self.out_srt.get(): open(f"{base_path}.srt", "w", encoding="utf-8").write(srt_content)
                    if self.out_vtt.get(): open(f"{base_path}.vtt", "w", encoding="utf-8").write(vtt_content)
                    if self.out_txt.get(): open(f"{base_path}.txt", "w", encoding="utf-8").write(txt_content)
                    
                    if self.out_docx.get():
                        import docx
                        doc = docx.Document()
                        for line in txt_content.split('\n'): doc.add_paragraph(line)
                        doc.save(f"{base_path}.docx")
                    
                    if self.out_pdf.get():
                        from reportlab.pdfgen import canvas
                        c = canvas.Canvas(f"{base_path}.pdf")
                        y = 800
                        for line in txt_content.split('\n'):
                            if y < 40: c.showPage(); y = 800
                            c.drawString(40, y, line[:100]) # Batasan margin sederhana
                            y -= 15
                        c.save()

            if self.source_type.get() == "youtube" and os.path.exists("temp_audio.mp3"):
                os.remove("temp_audio.mp3")
                
            print("\n✅ OPERASI SELESAI 100%!")
            messagebox.showinfo("Sukses", "Semua file berhasil diproses dan disimpan di Desktop.")

        except Exception as e:
            print(f"\n[ERROR FATAL] {str(e)}")
            messagebox.showerror("System Error", str(e))
        finally:
            self.btn_start.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlatinumTranscriberApp(root)
    root.mainloop()