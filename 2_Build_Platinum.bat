@echo off
title Platinum Transcriber - VENV Build Engine
color 0A

:LANG_SELECT
cls
echo ===================================================
echo  [1] English (Build with Virtual Environment)
echo  [2] Bahasa Indonesia (Build dengan Lingkungan Isolasi)
echo ===================================================
set /p lang="Select / Pilih (1/2): "
if "%lang%"=="1" goto EN
if "%lang%"=="2" goto ID
goto LANG_SELECT

:EN
echo [1/5] Creating Sterile Virtual Environment (venv)...
python -m venv platinum_env
echo [2/5] Activating venv and downloading required libraries ONLY...
call platinum_env\Scripts\activate
python -m pip install --upgrade pip
python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter
echo [3/5] Moving to Desktop...
cd /d "%USERPROFILE%\Desktop"
echo [4/5] Testing Script and Compiling to .EXE safely...
python PlatinumTranscriber.py
pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py
echo [5/5] Cleaning up and opening 'dist' folder...
call deactivate
cd dist
start PlatinumTranscriber.exe
exit

:ID
echo [1/5] Membangun Ruang Isolasi Virtual (venv)...
python -m venv platinum_env
echo [2/5] Mengaktifkan ruang isolasi dan mengunduh pustaka murni...
call platinum_env\Scripts\activate
python -m pip install --upgrade pip
python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter
echo [3/5] Berpindah ke Desktop...
cd /d "%USERPROFILE%\Desktop"
echo [4/5] Uji coba script dan Mengkompilasi menjadi .EXE secara aman...
python PlatinumTranscriber.py
pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py
echo [5/5] Membersihkan sistem dan membuka folder 'dist'...
call deactivate
cd dist
start PlatinumTranscriber.exe
exit