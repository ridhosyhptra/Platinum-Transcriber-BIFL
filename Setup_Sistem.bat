@echo off
title Platinum Transcriber - Auto Setup
color 0A

:LANG_SELECT
cls
echo ===================================================
echo  Please select your language / Pilih bahasa Anda:
echo  [1] English
echo  [2] Bahasa Indonesia
echo ===================================================
set /p lang="Enter 1 or 2: "
if "%lang%"=="1" goto EN_START
if "%lang%"=="2" goto ID_START
goto LANG_SELECT

:EN_START
cls
echo ==================================================================
echo           PLATINUM TRANSCRIBER - THE AUTOMATED SETUP
echo ==================================================================
echo.
echo Welcome! This script will prepare your laptop to run the AI.
echo To do this, we need to install two core components from the internet:
echo.
echo 1. PYTHON : The "Brain" that will read and run the AI code.
echo 2. FFMPEG : The "Ear" that will extract audio from your videos.
echo.
echo Please ensure your internet connection is stable.
echo.
set /p agree="Do you agree to install these components now? (Y/N): "
if /i "%agree%" NEQ "Y" exit

echo.
echo [1/2] Downloading and Installing Python...
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements

echo.
echo [2/2] Downloading and Installing FFmpeg...
winget install Gyan.FFmpeg --accept-package-agreements --accept-source-agreements

echo.
echo ==================================================================
echo                      SETUP COMPLETE!
echo ==================================================================
echo.
echo CRITICAL ACTION: 
echo You MUST restart your computer NOW to apply the changes.
echo After restarting, read Phase 2 in the README file on GitHub.
echo.
pause
exit

:ID_START
cls
echo ==================================================================
echo           PLATINUM TRANSCRIBER - SETUP SISTEM OTOMATIS
echo ==================================================================
echo.
echo Selamat datang! Skrip ini akan menyiapkan laptop Anda untuk AI.
echo Kita perlu menginstal dua komponen utama dari internet:
echo.
echo 1. PYTHON : "Otak" yang akan membaca dan menjalankan kode AI.
echo 2. FFMPEG : "Telinga" yang akan mengekstrak suara dari video Anda.
echo.
echo Pastikan koneksi internet Anda stabil.
echo.
set /p agree="Apakah Anda setuju untuk menginstalnya sekarang? (Y/N): "
if /i "%agree%" NEQ "Y" exit

echo.
echo [1/2] Mengunduh dan Menginstal Python...
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements

echo.
echo [2/2] Mengunduh dan Menginstal FFmpeg...
winget install Gyan.FFmpeg --accept-package-agreements --accept-source-agreements

echo.
echo ==================================================================
echo                      INSTALASI SELESAI!
echo ==================================================================
echo.
echo TINDAKAN KRITIS: 
echo Anda WAJIB me-restart (hidupkan ulang) laptop Anda SEKARANG.
echo Setelah menyala, baca Fase 2 di file README pada GitHub.
echo.
pause
exit