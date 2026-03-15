@echo off
title Platinum Transcriber - Auto Setup System
color 0B

:LANG_SELECT
cls
echo ===================================================
echo  [1] English (Install Python & FFmpeg)
echo  [2] Bahasa Indonesia (Instal Python & FFmpeg)
echo ===================================================
set /p lang="Select / Pilih (1/2): "
if "%lang%"=="1" goto EN
if "%lang%"=="2" goto ID
goto LANG_SELECT

:EN
cls
echo Installing Core Engines (Python & FFmpeg)...
winget install Python.Python.3.12 --accept-package-agreements
winget install Gyan.FFmpeg --accept-package-agreements
echo SETUP COMPLETE! CRITICAL: Restart your PC now.
pause
exit

:ID
cls
echo Menginstal Mesin Utama (Python & FFmpeg)...
echo Anda menyetujui proses ini untuk memasukkan "Otak" dan "Telinga" ke sistem.
winget install Python.Python.3.12 --accept-package-agreements
winget install Gyan.FFmpeg --accept-package-agreements
echo INSTALASI SELESAI! KRITIKAL: Restart Laptop Anda sekarang.
pause
exit