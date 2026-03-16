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
python -m pip install --upgrade yt-dlp faster-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter
echo [3/5] Locking to current directory...
cd /d "%~dp0"
echo [4/5] Compiling to .EXE safely...
pyinstaller --noconsole --onefile --add-binary "ffmpeg.exe;." --icon=logo.ico PlatinumTranscriber.py
echo [5/5] Cleaning up and opening 'dist' folder...
call deactivate
if exist dist (
    explorer dist
) else (
    echo Build failed. Check the logs above.
    pause
)
exit

:ID
echo [1/5] Membangun Ruang Isolasi Virtual (venv)...
python -m venv platinum_env
echo [2/5] Mengaktifkan ruang isolasi dan mengunduh pustaka murni...
call platinum_env\Scripts\activate
python -m pip install --upgrade pip
python -m pip install --upgrade yt-dlp faster-whisper pyinstaller deep-translator deepl python-docx reportlab psutil assemblyai customtkinter
echo [3/5] Mengunci direktori kerja...
cd /d "%~dp0"
echo [4/5] Mengkompilasi menjadi .EXE secara aman...
pyinstaller --noconsole --onefile --add-binary "ffmpeg.exe;." --icon=logo.ico PlatinumTranscriber.py
echo [5/5] Membersihkan sistem dan membuka folder 'dist'...
call deactivate
if exist dist (
    explorer dist
) else (
    echo Gagal membuat aplikasi. Silakan cek log di atas.
    pause
)
exit