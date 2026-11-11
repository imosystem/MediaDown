@echo off
setlocal
cd /d "%~dp0"
title MediaDown - EXE Builder
echo =====================================
echo          MEDIADOWN BUILD TOOL
echo =====================================
echo.
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3.10+ bulunamadi. Python kurun ve Add Python to PATH secin.
  pause
  exit /b 1
)
echo Gerekli kutuphaneler kuruluyor...
py -m pip install --upgrade pip
py -m pip install yt-dlp pyinstaller pillow imageio-ffmpeg
if errorlevel 1 goto fail
echo.
echo MediaDown.exe olusturuluyor...
py -m PyInstaller --noconfirm --clean --onefile --windowed --name MediaDown --icon MediaDown.ico --add-data "MediaDown.ico;." --collect-all yt_dlp --collect-all imageio_ffmpeg --hidden-import PIL._tkinter_finder app.py
if errorlevel 1 goto fail
echo.
echo BASARILI: dist\MediaDown.exe
echo Uygulama ayarlari ve gecmisi %%APPDATA%%\MediaDown klasorunde saklanir.
pause
exit /b 0
:fail
echo.
echo Derleme basarisiz. Hata mesajlarini kontrol edin.
pause
exit /b 1
