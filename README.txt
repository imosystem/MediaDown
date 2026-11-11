MEDIADOWN 2.0 - WINDOWS

EXE OLUSTURMA
1) ZIP paketini bir klasore cikarin.
2) Python 3.10 veya ustunu kurun (kurulumda Add Python to PATH secili olsun).
3) build.bat dosyasina cift tiklayin.
4) EXE dist\MediaDown.exe konumunda olusur.

OZELLIKLER
- Turkce, English, Deutsch, Espanol, Francais arayuzu
- 50 adede kadar coklu URL ekleme ve sirali toplu indirme
- Indirme kuyrugu ve ilerleme durumu
- Kalite: En iyi, 4K/2160p, 2K/1440p, 1080p, 720p, 480p, 360p
- MP4 video ve MP3 ses secenegi
- Indirme gecmisi (uygulama kapansa da saklanir)
- Kapak fotografinin ayri kaydi ve uygun dosyalara gomulmesi
- Otomatik dosya adi sablonu
- Ayarlar: dil, kalite, format, klasor, kapak, bildirim, tekrar deneme, mevcut dosyayi atlama
- MD uygulama simgesi
- Hakkinda: Gelistirici Baran Arda Tork

AYARLAR / GECMIS
Ayarlar ve gecmis Windows'ta %APPDATA%\MediaDown altinda JSON olarak saklanir.

NOTLAR
- Uygulama yt-dlp tarafindan desteklenen kaynaklari kullanir. Platformlarin API, erisim ve URL kurallari degisebilir; her linkin calismasi garanti degildir.
- Ozel/DRM korumali iceriklerin korumalarini asmaz. Giris gerektiren bazi icerikler desteklenmeyebilir.
- 4K secenegi kaynak videoda 4K varsa kullanilir; kaynakta yoksa daha dusuk kalite secilebilir.
- MP3 ve kapak gomme islemleri FFmpeg gerektirir; build betigi imageio-ffmpeg'i EXE'ye dahil eder.
- Yalnizca indirme izniniz olan icerikleri indirin; telif ve platform kosullarina uyun.


MEDIADOWN 2.0 - WINDOWS

CREATING THE EXE
1) Extract the ZIP package into a folder.
2) Install Python 3.10 or higher (ensure "Add Python to PATH" is selected during installation).
3) Double-click the `build.bat` file.
4) The EXE will be created at `dist\MediaDown.exe`.

FEATURES
- Interface available in Turkish, English, German, Spanish, and French
- Add up to 50 URLs for sequential batch downloading
- Download queue and progress tracking
- Quality options: Best, 4K/2160p, 2K/1440p, 1080p, 720p, 480p, 360p
- MP4 video and MP3 audio formats
- Download history (persists even after the application is closed)
- Option to save cover art separately or embed it into the files
- Automatic filename templating
- Settings: language, quality, format, destination folder, cover art, notifications, retries, and skipping existing files
- Custom MD application icon
- About: Developed by Baran Arda Tork

SETTINGS / HISTORY
Settings and history are stored as JSON files under `%APPDATA%\MediaDown` on Windows.

NOTES
- The application utilizes sources supported by `yt-dlp`. Platform APIs, access requirements, and URL structures may change; therefore, functionality for every link cannot be guaranteed.
- It does not bypass protections for private or DRM-protected content. Some content requiring a login may not be supported.
- The 4K option is only available if the source video is provided in 4K resolution. If the source does not provide the desired quality, a lower quality option may be selected.
- MP3 conversion and cover art embedding require FFmpeg; the build script includes `imageio-ffmpeg` within the executable.
- Only download content you are authorized to download; ensure compliance with copyright laws and platform terms of service.