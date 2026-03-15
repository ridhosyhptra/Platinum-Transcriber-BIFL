import os
import threading
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import urllib.request
import sys
import shutil
import ctypes

try:
    import yt_dlp
    import whisper
    from deep_translator import GoogleTranslator
    import deepl
    LIBRARIES_OK = True
except ImportError as e:
    LIBRARIES_OK = False
    MISSING_LIB = str(e)

# Sistem Sensor RAM
class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

def get_ram_info():
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    free_ram_gb = stat.ullAvailPhys / (1024**3)
    total_ram_gb = stat.ullTotalPhys / (1024**3)
    return free_ram_gb, total_ram_gb

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.see("end")
        self.widget.configure(state="disabled")
        self.widget.update_idletasks()
    def flush(self):
        pass

class PlatinumTranscriberApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "en" # Default Language
        
        # Kamus Terjemahan UI
        self.lang_dict = {
            "en": {
                "title": "Platinum Transcriber (Ultimate Dashboard)",
                "btn_lang": "🔄 Ganti ke Bahasa Indonesia",
                "btn_diag": "🔍 SYSTEM DIAGNOSTICS (Check RAM & Storage)",
                "lbl_step1": "1. Select Media Source:",
                "rb_yt": "YouTube Link (Needs Internet ~30MB/hr)",
                "rb_local": "Local File (BATCH - 100% Offline, No Data)",
                "btn_browse": "Browse File(s)",
                "lbl_nofile": "No file selected",
                "lbl_step2": "\n2. Select AI Engine Power (Check Laptop Specs):",
                "rb_small": "Whisper SMALL (~460 MB) | Fast & Light | Needs: Free RAM > 2 GB",
                "rb_medium": "Whisper MEDIUM (~1.5 GB) | High Precision | Needs: Free RAM > 5 GB",
                "lbl_step3": "\n3. Select Output Format:",
                "rb_srt": "Subtitles (.srt) - For Video Players",
                "rb_txt": "Transcript (.txt) - For Reading",
                "lbl_step4": "\n4. Translation Options:",
                "rb_none": "Original Text (No Translation - 100% Offline)",
                "rb_google": "Google Translate (Light Internet < 1 MB)",
                "rb_deepl": "DeepL AI (High Precision)",
                "lbl_api": "DeepL API Key:",
                "btn_start": "START TRANSCRIPTION",
                "lbl_monitor": "Data & Progress Monitor:",
                "status_ready": "Status: Ready",
                "msg_sys_safe": "System Safe",
                "msg_sys_warn": "System Warning",
                "err_lib": "Missing Libraries! Run in CMD:\npip install yt-dlp openai-whisper deep-translator deepl",
                "err_nofile": "No local file selected!",
                "err_url": "YouTube link is empty!",
                "err_api": "DeepL API Key is empty!",
                "err_storage": "Not enough storage! Free up at least 2 GB.",
                "err_ram": "Not enough free RAM for the selected model! Close apps or select SMALL.",
                "msg_success": "All files transcribed successfully!"
            },
            "id": {
                "title": "Platinum Transcriber (Dashboard Ultimate)",
                "btn_lang": "🔄 Switch to English",
                "btn_diag": "🔍 DIAGNOSTIK SISTEM (Cek RAM & Storage)",
                "lbl_step1": "1. Pilih Sumber Media:",
                "rb_yt": "YouTube Link (Butuh Internet ~30MB/jam)",
                "rb_local": "File Lokal (BATCH - 100% Offline, Tanpa Kuota)",
                "btn_browse": "Browse File(s)",
                "lbl_nofile": "Belum ada file terpilih",
                "lbl_step2": "\n2. Pilih Kekuatan Mesin AI (Perhatikan Spek Laptop):",
                "rb_small": "Whisper SMALL (~460 MB) | Cepat & Ringan | Syarat: Sisa RAM > 2 GB",
                "rb_medium": "Whisper MEDIUM (~1.5 GB) | Presisi Tinggi | Syarat: Sisa RAM > 5 GB",
                "lbl_step3": "\n3. Pilih Format Output:",
                "rb_srt": "Subtitles (.srt) - Untuk Video Player",
                "rb_txt": "Transcript (.txt) - Untuk bacaan dokumen",
                "lbl_step4": "\n4. Opsi Terjemahan:",
                "rb_none": "Teks Asli (Tanpa Terjemahan - 100% Offline)",
                "rb_google": "Google Translate (Internet Ringan < 1 MB)",
                "rb_deepl": "DeepL AI (Presisi Tinggi)",
                "lbl_api": "API Key DeepL:",
                "btn_start": "MULAI TRANSKRIPSI",
                "lbl_monitor": "Layar Monitor Data & Progres:",
                "status_ready": "Status: Ready",
                "msg_sys_safe": "Sistem Aman",
                "msg_sys_warn": "Peringatan Sistem",
                "err_lib": "Library belum lengkap! Jalankan di CMD:\npip install yt-dlp openai-whisper deep-translator deepl",
                "err_nofile": "Belum ada file lokal yang dipilih!",
                "err_url": "Link YouTube kosong!",
                "err_api": "DeepL API Key kosong!",
                "err_storage": "Ruang penyimpanan tidak cukup! Kosongkan minimal 2 GB.",
                "err_ram": "RAM kosong tidak cukup! Tutup aplikasi berat atau pilih Whisper SMALL.",
                "msg_success": "Seluruh file berhasil ditranskripsi!"
            }
        }

        self.root.geometry("750x950")
        self.root.configure(padx=20, pady=20)

        if not LIBRARIES_OK:
            messagebox.showerror("Fatal Error", self.lang_dict["en"]["err_lib"])
            self.root.destroy()
            return

        self.source_type = tk.StringVar(value="youtube")
        self.output_format = tk.StringVar(value="srt")
        self.trans_engine = tk.StringVar(value="none")
        self.ai_model = tk.StringVar(value="small")
        self.local_files = [] 
        self.file_label_text = tk.StringVar(value="")
        self.url_input = tk.StringVar()
        self.deepl_api_key = tk.StringVar()

        self.setup_ui()
        self.update_ui_texts() # Terapkan bahasa default
        
        sys.stdout = TextRedirector(self.console_log, "stdout")
        sys.stderr = TextRedirector(self.console_log, "stderr")

    def toggle_language(self):
        self.current_lang = "id" if self.current_lang == "en" else "en"
        self.update_ui_texts()

    def update_ui_texts(self):
        t = self.lang_dict[self.current_lang]
        self.root.title(t["title"])
        self.btn_lang.config(text=t["btn_lang"])
        self.diag_btn.config(text=t["btn_diag"])
        self.lbl_step1.config(text=t["lbl_step1"])
        self.rb_yt.config(text=t["rb_yt"])
        self.rb_local.config(text=t["rb_local"])
        self.file_btn.config(text=t["btn_browse"])
        if not self.local_files:
            self.file_label_text.set(t["lbl_nofile"])
        self.lbl_step2.config(text=t["lbl_step2"])
        self.rb_small.config(text=t["rb_small"])
        self.rb_medium.config(text=t["rb_medium"])
        self.lbl_step3.config(text=t["lbl_step3"])
        self.rb_srt.config(text=t["rb_srt"])
        self.rb_txt.config(text=t["rb_txt"])
        self.lbl_step4.config(text=t["lbl_step4"])
        self.rb_none.config(text=t["rb_none"])
        self.rb_google.config(text=t["rb_google"])
        self.rb_deepl.config(text=t["rb_deepl"])
        self.lbl_api.config(text=t["lbl_api"])
        self.process_btn.config(text=t["btn_start"])
        self.lbl_monitor.config(text=t["lbl_monitor"])
        
        if "Ready" in self.status_label.cget("text"):
            self.status_label.config(text=t["status_ready"])

    def setup_ui(self):
        # Tombol Bahasa
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=(0, 10))
        self.btn_lang = tk.Button(top_frame, bg="#f0f0f0", font=("Arial", 9), command=self.toggle_language)
        self.btn_lang.pack(side="right")

        self.diag_btn = tk.Button(self.root, bg="#ff9800", font=("Arial", 10, "bold"), command=self.run_diagnostics)
        self.diag_btn.pack(fill="x", pady=(0, 10))

        self.lbl_step1 = tk.Label(self.root, font=("Arial", 11, "bold"))
        self.lbl_step1.pack(anchor="w")
        self.rb_yt = tk.Radiobutton(self.root, variable=self.source_type, value="youtube", command=self.toggle_inputs)
        self.rb_yt.pack(anchor="w")
        self.rb_local = tk.Radiobutton(self.root, variable=self.source_type, value="local", command=self.toggle_inputs)
        self.rb_local.pack(anchor="w")

        self.url_entry = tk.Entry(self.root, textvariable=self.url_input, width=70)
        
        self.file_frame = tk.Frame(self.root)
        self.file_btn = tk.Button(self.file_frame, command=self.browse_files)
        self.file_btn.pack(side="left", padx=5)
        self.file_label = tk.Label(self.file_frame, textvariable=self.file_label_text, fg="blue", wraplength=450)
        self.file_label.pack(side="left")

        self.lbl_step2 = tk.Label(self.root, font=("Arial", 11, "bold"))
        self.lbl_step2.pack(anchor="w", pady=(5,0))
        self.rb_small = tk.Radiobutton(self.root, variable=self.ai_model, value="small")
        self.rb_small.pack(anchor="w")
        self.rb_medium = tk.Radiobutton(self.root, variable=self.ai_model, value="medium")
        self.rb_medium.pack(anchor="w")

        self.lbl_step3 = tk.Label(self.root, font=("Arial", 11, "bold"))
        self.lbl_step3.pack(anchor="w", pady=(5,0))
        self.rb_srt = tk.Radiobutton(self.root, variable=self.output_format, value="srt")
        self.rb_srt.pack(anchor="w")
        self.rb_txt = tk.Radiobutton(self.root, variable=self.output_format, value="txt")
        self.rb_txt.pack(anchor="w")

        self.lbl_step4 = tk.Label(self.root, font=("Arial", 11, "bold"))
        self.lbl_step4.pack(anchor="w", pady=(5,0))
        self.rb_none = tk.Radiobutton(self.root, variable=self.trans_engine, value="none", command=self.toggle_api_input)
        self.rb_none.pack(anchor="w")
        self.rb_google = tk.Radiobutton(self.root, variable=self.trans_engine, value="google", command=self.toggle_api_input)
        self.rb_google.pack(anchor="w")
        self.rb_deepl = tk.Radiobutton(self.root, variable=self.trans_engine, value="deepl", command=self.toggle_api_input)
        self.rb_deepl.pack(anchor="w")

        self.api_frame = tk.Frame(self.root)
        self.lbl_api = tk.Label(self.api_frame)
        self.lbl_api.pack(side="left")
        tk.Entry(self.api_frame, textvariable=self.deepl_api_key, width=45, show="*").pack(side="left", padx=5)

        self.process_btn = tk.Button(self.root, bg="#002147", fg="white", font=("Arial", 12, "bold"), command=self.start_processing)
        self.process_btn.pack(pady=15, fill="x")

        self.lbl_monitor = tk.Label(self.root, font=("Arial", 10, "bold"), fg="#002147")
        self.lbl_monitor.pack(anchor="w")
        self.status_label = tk.Label(self.root, fg="blue", font=("Arial", 10, "bold"))
        self.status_label.pack(anchor="w")
        
        self.console_log = ScrolledText(self.root, height=10, bg="black", fg="lime", font=("Consolas", 9))
        self.console_log.pack(fill="both", expand=True, pady=5)
        self.console_log.configure(state="disabled")

        self.toggle_inputs()
        self.toggle_api_input()

    def toggle_inputs(self):
        if self.source_type.get() == "youtube":
            self.file_frame.pack_forget()
            self.url_entry.pack(pady=5, anchor="w")
        else:
            self.url_entry.pack_forget()
            self.file_frame.pack(pady=5, anchor="w", fill="x")

    def toggle_api_input(self):
        if self.trans_engine.get() == "deepl":
            self.api_frame.pack(pady=5, anchor="w")
        else:
            self.api_frame.pack_forget()

    def browse_files(self):
        filepaths = filedialog.askopenfilenames(title="Media", filetypes=[("Media Files", "*.mp4 *.mkv *.mp3 *.wav *.m4a")])
        if filepaths:
            self.local_files = list(filepaths)
            self.file_label_text.set(f"{len(self.local_files)} files.")

    def run_diagnostics(self):
        threading.Thread(target=self._diagnostics_logic).start()

    def _diagnostics_logic(self):
        report, is_clear = [], True
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            report.append("✅ FFmpeg: OK")
        except:
            report.append("❌ FFmpeg: ERROR"); is_clear = False
        try:
            urllib.request.urlopen('http://google.com', timeout=3)
            report.append("✅ Internet: OK")
        except:
            report.append("⚠️ Internet: Offline")
        
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        total, used, free = shutil.disk_usage(desktop_path)
        free_storage_gb = free / (1024 ** 3)
        if free_storage_gb < 2.0:
            report.append(f"❌ Storage: {free_storage_gb:.2f} GB")
            is_clear = False
        else:
            report.append(f"✅ Storage: {free_storage_gb:.2f} GB")

        free_ram_gb, total_ram_gb = get_ram_info()
        if free_ram_gb < 2.0:
            report.append(f"❌ Free RAM: {free_ram_gb:.2f} GB")
            is_clear = False
        else:
            report.append(f"✅ Free RAM: {free_ram_gb:.2f} GB")

        msg = "\n".join(report)
        print(f"--- DIAGNOSTICS ---\n{msg}\n-------------------")
        t = self.lang_dict[self.current_lang]
        if is_clear: messagebox.showinfo(t["msg_sys_safe"], msg)
        else: messagebox.showwarning(t["msg_sys_warn"], msg)

    def format_time(self, seconds, is_srt):
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if is_srt:
            millisecs = int((seconds - int(seconds)) * 1000)
            return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d},{millisecs:03d}"
        else:
            return f"[{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}]" if hours > 0 else f"[{int(minutes):02d}:{int(secs):02d}]"

    def yt_progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.status_label.config(text=f"YT Progress: {percent} | Speed: {speed}")
            self.root.update_idletasks()

    def process_logic(self):
        self.process_btn.config(state="disabled")
        t = self.lang_dict[self.current_lang]
        try:
            print("\n[SYSTEM] Starting...")
            
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            total_st, used_st, free_st = shutil.disk_usage(desktop_path)
            free_storage_gb = free_st / (1024 ** 3)
            if free_storage_gb < 2.0:
                raise ValueError(t["err_storage"])

            selected_model = self.ai_model.get()
            required_ram = 4.5 if selected_model == "medium" else 2.0
            free_ram_gb, total_ram_gb = get_ram_info()
            if free_ram_gb < required_ram:
                raise ValueError(t["err_ram"])

            files_to_process = []
            is_temp = False

            if self.source_type.get() == "youtube":
                url = self.url_input.get().strip()
                if not url: raise ValueError(t["err_url"])
                target_file = "temp_audio.mp3"
                ydl_opts = {'format': 'bestaudio/best', 'outtmpl': target_file, 'quiet': True, 'progress_hooks': [self.yt_progress_hook]}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
                files_to_process.append((target_file, "YouTube_Audio"))
                is_temp = True
            else:
                if not self.local_files: raise ValueError(t["err_nofile"])
                for f in self.local_files:
                    title = os.path.splitext(os.path.basename(f))[0]
                    files_to_process.append((f, title))

            self.status_label.config(text=f"Loading AI Model: {selected_model.upper()}...")
            print(f"\n[AI] Loading Whisper {selected_model.upper()} (May download if first time)...")
            model = whisper.load_model(selected_model)
            print("[AI] Ready!")
            
            engine = self.trans_engine.get()
            google_trans = None
            deepl_trans = None
            if engine == "google": google_trans = GoogleTranslator(source='auto', target='id')
            elif engine == "deepl":
                api_key = self.deepl_api_key.get().strip()
                if not api_key: raise ValueError(t["err_api"])
                deepl_trans = deepl.Translator(api_key)

            is_srt = self.output_format.get() == "srt"
            lang_tag = "_ID" if engine != "none" else "_EN"

            total_files = len(files_to_process)
            for current_idx, (file_path, title_prefix) in enumerate(files_to_process, 1):
                self.status_label.config(text=f"Processing [{current_idx}/{total_files}]...")
                print(f"\n[AI] Transcribing: {title_prefix}")
                
                result = model.transcribe(file_path)
                final_content = ""
                total_segments = len(result["segments"])

                for index, segment in enumerate(result["segments"], start=1):
                    self.status_label.config(text=f"Line {index} / {total_segments}...")
                    self.root.update_idletasks()

                    start_t = self.format_time(segment["start"], is_srt)
                    end_t = self.format_time(segment["end"], is_srt)
                    text = segment["text"].strip()

                    if engine == "google":
                        try: text = google_trans.translate(text)
                        except: text = f"[Error] {text}"
                    elif engine == "deepl":
                        try: text = deepl_trans.translate_text(text, target_lang="ID").text
                        except: text = f"[Error] {text}"

                    if is_srt: final_content += f"{index}\n{start_t} --> {end_t}\n{text}\n\n"
                    else: final_content += f"{start_t} {text}\n"

                timestamp = datetime.now().strftime('%H%M%S')
                save_name = f"{title_prefix[:20]}{lang_tag}_{timestamp}{'.srt' if is_srt else '.txt'}"
                save_path = os.path.join(desktop_path, save_name)

                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(final_content)
                print(f"[OUTPUT] Saved: {save_name}")

            if is_temp and os.path.exists("temp_audio.mp3"): os.remove("temp_audio.mp3")

            self.status_label.config(text=t["msg_success"], fg="green")
            messagebox.showinfo("Success", t["msg_success"])

        except Exception as e:
            self.status_label.config(text="ERROR!", fg="red")
            print(f"\n[ERROR] {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.process_btn.config(state="normal")
            print("[SYSTEM] Standby.")

    def start_processing(self):
        threading.Thread(target=self.process_logic).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlatinumTranscriberApp(root)
    root.mainloop()