import sys
import os

# Bypass Xet protocol yang sering macet di Windows saat download model HF
os.environ["HF_HUB_DISABLE_XET"] = "1"

import pyaudio
import numpy as np
import queue
import threading
import time
import math
import io
import wave

# ==============================================================
#  SANDBOX UJI COBA LIVE DICTATION V9.1 (OPTIMIZED)
#  Arsitektur: Producer-Consumer dengan Queue Buffer
#
#  3 Mesin Tersedia:
#    [1] Faster-Whisper Lokal  (Offline, perlu download model sekali)
#    [2] AssemblyAI Real-Time  (Cloud WebSocket, butuh API Key)
#    [3] Google Speech Free    (Cloud REST, gratis, tanpa API Key)
#
#  Optimasi V9.1:
#    - Warmup dummy: eliminasi delay 27 detik pada blok pertama
#    - Queue drain: consumer loncat ke blok terbaru, buang yang basi
#    - beam_size=1: kecepatan transkripsi 3-5x lebih cepat
# ==============================================================

RATE            = 16000
CHUNK           = 1024
RECORD_SECONDS  = 3
SILENCE_THRESH  = 0.01
WHISPER_MODEL   = "tiny"


def rms_energy(audio_float32):
    if len(audio_float32) == 0:
        return 0.0
    return math.sqrt(np.mean(audio_float32 ** 2))


def audio_level_bar(energy, max_energy=0.15, bar_width=30):
    ratio = min(energy / max_energy, 1.0)
    filled = int(ratio * bar_width)
    return "[" + "#" * filled + "-" * (bar_width - filled) + "]"


def pcm_to_wav_bytes(raw_pcm, sample_rate=16000):
    """Konversi raw PCM int16 mono ke format WAV in-memory."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(raw_pcm)
    return buf.getvalue()


# ==============================================================
#  PRODUCER: Perekam Mikrofon (Shared oleh semua mesin)
# ==============================================================
def record_audio(q, stop_event, ready_event, raw_mode=False):
    """
    Merekam audio dari mikrofon, memotong per RECORD_SECONDS detik.
    raw_mode=True  -> kirim bytes mentah PCM (untuk Google Speech)
    raw_mode=False -> kirim numpy float32 array (untuk Whisper)
    """
    p = pyaudio.PyAudio()
    dev_info = p.get_default_input_device_info()
    print("[MIC] Perangkat  : " + str(dev_info["name"]))
    print("[MIC] Sample Rate: %d Hz | Chunk: %d | Blok: %d detik" % (RATE, CHUNK, RECORD_SECONDS))

    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=RATE,
        input=True, frames_per_buffer=CHUNK,
    )

    ready_event.wait()

    print("")
    print("=" * 55)
    print("  MIKROFON TERKUNCI -- SILAKAN MULAI BERBICARA...")
    print("  Tekan Ctrl+C untuk menghentikan.")
    print("=" * 55)
    print("")

    chunks_per_block = int(RATE / CHUNK * RECORD_SECONDS)
    block_number = 0

    while not stop_event.is_set():
        frames = []
        for _ in range(chunks_per_block):
            if stop_event.is_set():
                break
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except Exception:
                break

        if not frames:
            continue

        raw_bytes = b"".join(frames)
        audio_f32 = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        energy = rms_energy(audio_f32)
        block_number += 1
        level = audio_level_bar(energy)

        if energy < SILENCE_THRESH:
            sys.stdout.write("\r  Blok #%03d %s (sunyi -- dilewati)          " % (block_number, level))
            sys.stdout.flush()
            continue

        qsize = q.qsize()
        q_info = " (Q:%d)" % qsize if qsize > 0 else ""
        sys.stdout.write("\r  Blok #%03d %s >> Suara -> Antrean%s   " % (block_number, level, q_info))
        sys.stdout.flush()

        if raw_mode:
            q.put((raw_bytes, block_number))
        else:
            q.put((audio_f32, block_number))

    stream.stop_stream()
    stream.close()
    p.terminate()


# ==============================================================
#  CONSUMER A: Faster-Whisper Lokal (Offline)
# ==============================================================
def drain_queue_to_latest(q):
    """
    Buang semua blok basi di queue, kembalikan hanya blok terbaru.
    Mencegah backlog: consumer selalu memproses audio paling fresh.
    """
    latest = None
    skipped = 0
    while True:
        try:
            item = q.get_nowait()
            if latest is not None:
                skipped += 1
            latest = item
        except queue.Empty:
            break
    return latest, skipped


def consumer_whisper(q, stop_event, ready_event):
    from faster_whisper import WhisperModel

    print("")
    print("[AI] Memanaskan mesin Faster-Whisper (Model: %s)..." % WHISPER_MODEL.upper())
    print("[AI] Download pertama kali ~75MB. JANGAN Ctrl+C saat download!")
    print("")
    t0 = time.time()
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    load_time = time.time() - t0
    print("")
    print("[AI] Model dimuat (%.1f detik). Menjalankan warmup..." % load_time)

    # --- WARMUP: transkripsi audio sunyi 1 detik agar JIT compilation selesai ---
    dummy_audio = np.zeros(RATE, dtype=np.float32)
    tw = time.time()
    list(model.transcribe(dummy_audio, beam_size=1, language="id")[0])
    print("[AI] Warmup selesai (%.1f detik)." % (time.time() - tw))
    print("[AI] >>> MESIN SIAP! Total: %.1f detik <<<" % (time.time() - t0))

    ready_event.set()

    full_transcript = []

    while not stop_event.is_set():
        try:
            first_item = q.get(timeout=0.5)
        except queue.Empty:
            continue

        # Drain queue: loncat ke blok terbaru, buang yang basi
        audio_f32, block_num = first_item
        while not q.empty():
            try:
                newer = q.get_nowait()
                audio_f32, block_num = newer
            except queue.Empty:
                break

        t1 = time.time()
        segments, _ = model.transcribe(audio_f32, beam_size=1, language="id")
        text = "".join([s.text for s in segments]).strip()
        elapsed = time.time() - t1

        if text:
            full_transcript.append(text)
            print("\n")
            print("  +-- Blok #%03d (%.2fs)" % (block_num, elapsed))
            print("  |  >> " + text)
            print("  +" + "--" * 25)

    return full_transcript


# ==============================================================
#  CONSUMER B: AssemblyAI Real-Time (Cloud WebSocket)
# ==============================================================
def run_assemblyai(stop_event):
    """
    AssemblyAI Real-Time: streaming langsung via WebSocket.
    Arsitektur berbeda -- tidak pakai queue, langsung stream ke server.
    """
    try:
        import assemblyai as aai
    except ImportError:
        print("[ERROR] Package 'assemblyai' belum terinstal.")
        print("        Jalankan: pip install assemblyai")
        return []

    api_key = input("[AAI] Masukkan AssemblyAI API Key: ").strip()
    if not api_key:
        print("[ERROR] API Key kosong. Batalkan.")
        return []

    aai.settings.api_key = api_key
    full_transcript = []
    partial_text = [""]

    def on_open(session):
        print("[AAI] Koneksi WebSocket terbuka (Session: %s)" % session.session_id)

    def on_data(transcript):
        if not transcript.text:
            return
        if isinstance(transcript, aai.RealtimeFinalTranscript):
            full_transcript.append(transcript.text)
            print("\n  [FINAL] >> " + transcript.text)
        else:
            partial_text[0] = transcript.text
            sys.stdout.write("\r  [live]  >> " + transcript.text + "          ")
            sys.stdout.flush()

    def on_error(error):
        print("\n[AAI ERROR] " + str(error))

    def on_close():
        print("\n[AAI] Koneksi ditutup.")

    print("")
    print("[AAI] Menghubungkan ke AssemblyAI Real-Time Server...")

    transcriber = aai.RealtimeTranscriber(
        sample_rate=RATE,
        on_data=on_data,
        on_error=on_error,
        on_open=on_open,
        on_close=on_close,
    )
    transcriber.connect()

    p = pyaudio.PyAudio()
    dev_info = p.get_default_input_device_info()
    print("[MIC] Perangkat: " + str(dev_info["name"]))

    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=RATE,
        input=True, frames_per_buffer=CHUNK,
    )

    print("")
    print("=" * 55)
    print("  MIKROFON TERKUNCI -- SILAKAN MULAI BERBICARA...")
    print("  AssemblyAI akan mentranskripsi KATA PER KATA secara real-time!")
    print("  Tekan Ctrl+C untuk menghentikan.")
    print("=" * 55)
    print("")

    try:
        while not stop_event.is_set():
            data = stream.read(CHUNK, exception_on_overflow=False)
            transcriber.stream(data)
    except Exception as e:
        if not stop_event.is_set():
            print("\n[STREAM ERROR] " + str(e))
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        try:
            transcriber.close()
        except Exception:
            pass

    return full_transcript


# ==============================================================
#  CONSUMER C: Google Speech Recognition (Free, Cloud)
# ==============================================================
def consumer_google(q, stop_event, ready_event):
    try:
        import speech_recognition as sr
    except ImportError:
        print("[ERROR] Package 'speech_recognition' belum terinstal.")
        print("        Jalankan: pip install SpeechRecognition")
        ready_event.set()
        return []

    recognizer = sr.Recognizer()
    print("")
    print("[GOOGLE] Mesin Google Speech Recognition siap (Gratis, tanpa API Key).")
    print("[GOOGLE] Bahasa: Indonesia (id-ID)")
    ready_event.set()

    full_transcript = []

    while not stop_event.is_set():
        try:
            first_item = q.get(timeout=0.5)
        except queue.Empty:
            continue

        # Drain queue: loncat ke blok terbaru
        raw_pcm, block_num = first_item
        while not q.empty():
            try:
                newer = q.get_nowait()
                raw_pcm, block_num = newer
            except queue.Empty:
                break

        t1 = time.time()
        try:
            audio_data = sr.AudioData(raw_pcm, RATE, 2)
            text = recognizer.recognize_google(audio_data, language="id-ID")
            elapsed = time.time() - t1

            if text and text.strip():
                full_transcript.append(text.strip())
                print("\n")
                print("  +-- Blok #%03d (%.2fs)" % (block_num, elapsed))
                print("  |  >> " + text.strip())
                print("  +" + "--" * 25)

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("\n  [GOOGLE ERROR] Gagal terhubung: " + str(e))
        except Exception as e:
            print("\n  [ERROR] " + str(e))

    return full_transcript


# ==============================================================
#  MAIN: Menu + Orkestrator
# ==============================================================
def print_transcript_summary(full_transcript):
    if full_transcript:
        print("\n")
        print("=" * 55)
        print("  TRANSKRIP LENGKAP SESI INI:")
        print("=" * 55)
        print("  " + " ".join(full_transcript))
        print("=" * 55)
    else:
        print("\n[INFO] Tidak ada teks yang berhasil ditranskrip.")


def main():
    print("+======================================================+")
    print("|   SANDBOX LIVE DICTATION V9.1 -- OPTIMIZED           |")
    print("|   Arsitektur: Producer (Mic) > Queue > Consumer (AI) |")
    print("+======================================================+")
    print("")
    print("  Pilih mesin transkripsi:")
    print("")
    print("    [1] Whisper Lokal    -- 100% Offline, perlu download model 1x")
    print("    [2] AssemblyAI Live  -- Cloud real-time (kata per kata!)")
    print("    [3] Google Speech    -- Cloud gratis, tanpa API Key")
    print("")

    choice = input("  Pilihan Anda (1/2/3): ").strip()

    if choice not in ("1", "2", "3"):
        print("[ERROR] Pilihan tidak valid. Keluar.")
        return

    stop_event = threading.Event()
    audio_q = queue.Queue()

    # --- ENGINE 2: AssemblyAI (arsitektur berbeda, tidak pakai queue) ---
    if choice == "2":
        try:
            full_transcript = run_assemblyai(stop_event)
        except KeyboardInterrupt:
            print("\n\n[SYSTEM] Menerima Ctrl+C -- Menghentikan...")
            stop_event.set()
            full_transcript = []
        print_transcript_summary(full_transcript)
        return

    # --- ENGINE 1 & 3: Pakai arsitektur Producer-Consumer ---
    ready_event = threading.Event()
    raw_mode = (choice == "3")
    full_transcript_holder = [None]

    def consumer_wrapper():
        if choice == "1":
            full_transcript_holder[0] = consumer_whisper(audio_q, stop_event, ready_event)
        else:
            full_transcript_holder[0] = consumer_google(audio_q, stop_event, ready_event)

    t_consumer = threading.Thread(target=consumer_wrapper, daemon=True)
    t_producer = threading.Thread(
        target=record_audio,
        args=(audio_q, stop_event, ready_event, raw_mode),
        daemon=True,
    )

    t_consumer.start()
    t_producer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Menerima Ctrl+C -- Menghentikan semua thread...")
        stop_event.set()
        t_producer.join(timeout=5)
        t_consumer.join(timeout=5)

    print_transcript_summary(full_transcript_holder[0] or [])
    print("[SYSTEM] Operasi dihentikan dengan aman. Sampai jumpa!")


if __name__ == "__main__":
    main()
