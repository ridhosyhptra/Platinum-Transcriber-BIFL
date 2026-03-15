@echo off
title Platinum Transcriber - Auto Setup
color 0B

:LANG_SELECT
cls
echo ===================================================
echo  [1] English
echo  [2] Bahasa Indonesia
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
echo.
echo SETUP COMPLETE! CRITICAL: Restart your PC now.
pause
exit

:ID
cls
echo Menginstal Mesin Utama (Python & FFmpeg)...
winget install Python.Python.3.12 --accept-package-agreements
winget install Gyan.FFmpeg --accept-package-agreements
echo.
echo INSTALASI SELESAI! KRITIKAL: Restart Laptop Anda sekarang.
pause
exit