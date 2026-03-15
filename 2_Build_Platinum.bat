@echo off
title Platinum Transcriber - Build & Compile Engine
color 0A

:LANG_SELECT
cls
echo  [1] English Build Process
echo  [2] Proses Build Bahasa Indonesia
set /p lang="Select / Pilih (1/2): "
if "%lang%"=="1" goto EN
if "%lang%"=="2" goto ID
goto LANG_SELECT

:EN
echo [1/4] Upgrading PIP and downloading AI Libraries...
python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter
echo [2/4] Moving to Desktop...
cd /d "%USERPROFILE%\Desktop"
echo [3/4] Compiling to .EXE (Needs logo.ico on Desktop)...
pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py
echo [4/4] Opening 'dist' folder and running the App...
cd dist
start PlatinumTranscriber.exe
exit

:ID
echo [1/4] Memperbarui PIP dan mengunduh Pustaka AI...
python -m pip install --upgrade yt-dlp openai-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter
echo [2/4] Berpindah ke Desktop...
cd /d "%USERPROFILE%\Desktop"
echo [3/4] Uji coba script dan Mengkompilasi menjadi .EXE berlogo...
python PlatinumTranscriber.py
pyinstaller --noconsole --onefile --icon=logo.ico PlatinumTranscriber.py
echo [4/4] Memasuki folder 'dist' dan mengeksekusi Aplikasi...
cd dist
start PlatinumTranscriber.exe
exit