import os, sys, json, threading, queue, re, urllib.request, io, subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

try:
    import yt_dlp
except Exception:
    yt_dlp = None
try:
    from PIL import Image, ImageTk, ImageDraw
except Exception:
    Image = ImageTk = ImageDraw = None

APP='MediaDown'
VERSION='2.0.0'
BG='#0b1020'; PANEL='#121a2b'; PANEL2='#1a263b'; LINE='#24324a'
TEXT='#edf3ff'; MUTED='#91a0b8'; BLUE='#3985ff'; BLUE2='#2469e8'; GREEN='#39c98a'; RED='#ff657a'
HOME=Path(os.environ.get('APPDATA', str(Path.home()))) / 'MediaDown'
HOME.mkdir(parents=True, exist_ok=True)
CONFIG=HOME/'settings.json'; HISTORY=HOME/'history.json'; THUMBS=HOME/'thumbnails'
THUMBS.mkdir(exist_ok=True)

LANG={
 'tr': {'home':'Ana Sayfa','history':'İndirme Geçmişi','settings':'Ayarlar','about':'Hakkında','tagline':'Tüm platformlardan videoları kolayca indirin','subtitle':'YouTube, TikTok, Instagram, X ve daha fazlası','links':'VİDEO BAĞLANTILARI','paste':'Bağlantıları alt alta yapıştırın (her satıra bir link)','add':'Listeye Ekle','download':'Sırayı İndir','format':'FORMAT','quality':'KALİTE','filename':'DOSYA İSİMLENDİRME','queue':'İNDİRME KUYRUĞU','clear':'Kuyruğu Temizle','status':'Durum','title':'Video','platform':'Platform','progress':'İlerleme','ready':'Hazır','waiting':'Bekliyor','working':'İndiriliyor','done':'Tamamlandı','failed':'Hata','cancelled':'İptal edildi','choose':'Klasör Seç','location':'İNDİRME KONUMU','general':'Genel','download_settings':'İndirme','appearance':'Görünüm','notifications':'Bildirimler','advanced':'Gelişmiş','language':'Uygulama Dili','default_quality':'Varsayılan Kalite','default_format':'Varsayılan Format','save':'Ayarları Kaydet','reset':'Varsayılanlara Dön','embed':'Kapak fotoğrafını dosyaya ekle (uygunsa)','save_thumb':'Kapak fotoğrafını ayrıca kaydet','notify':'İndirme tamamlanınca bildirim göster','skip':'İndirilmiş dosyaları atla','retries':'Bağlantı tekrar deneme sayısı','template':'Dosya adı şablonu','template_help':'Örn: %(title)s [%(id)s]','open_folder':'İndirme Klasörünü Aç','empty_history':'Henüz indirme geçmişi yok.','clear_history':'Geçmişi Temizle','about_title':'MediaDown Hakkında','developer':'Geliştirici','credits':'Emeği Geçenler','version':'Sürüm','about_text':'Video bağlantılarını tek bir sade arayüzden yönetmek ve indirmek için geliştirildi.','legal':'Yalnızca indirme hakkınız olan içerikleri kaydedin. Platform kurallarına ve telif haklarına uyun.','added':'bağlantı kuyruğa eklendi.','invalid':'Geçerli bir http/https bağlantısı girin.','no_links':'Önce en az bir bağlantı ekleyin.','complete':'İndirme kuyruğu tamamlandı.','error':'İndirme hatası','confirm_clear':'İndirme geçmişi kalıcı olarak temizlensin mi?','saved':'Ayarlar kaydedildi.','mp4':'MP4 · Video','mp3':'MP3 · Ses','best':'En iyi','theme':'Koyu tema','max_items':'Tek seferde en fazla 50 bağlantı eklenebilir.','thumb':'Kapak','date':'Tarih','file':'Dosya','size':'Boyut','browse':'Gözat','paused':'Durduruldu','start':'Başlat','cancel':'İptal','remove':'Seçileni Sil','all':'Tümü','quality_note':'4K seçeneği, kaynak videoda mevcutsa kullanılır.'},
 'en': {'home':'Home','history':'Download History','settings':'Settings','about':'About','tagline':'Download videos from your favorite platforms','subtitle':'YouTube, TikTok, Instagram, X and more','links':'VIDEO LINKS','paste':'Paste links on separate lines (one URL per line)','add':'Add to Queue','download':'Download Queue','format':'FORMAT','quality':'QUALITY','filename':'FILE NAMING','queue':'DOWNLOAD QUEUE','clear':'Clear Queue','status':'Status','title':'Video','platform':'Platform','progress':'Progress','ready':'Ready','waiting':'Waiting','working':'Downloading','done':'Completed','failed':'Failed','cancelled':'Cancelled','choose':'Choose Folder','location':'DOWNLOAD LOCATION','general':'General','download_settings':'Downloads','appearance':'Appearance','notifications':'Notifications','advanced':'Advanced','language':'App Language','default_quality':'Default Quality','default_format':'Default Format','save':'Save Settings','reset':'Restore Defaults','embed':'Embed thumbnail in media file (if supported)','save_thumb':'Save thumbnail as a separate file','notify':'Show notification when downloads finish','skip':'Skip already downloaded files','retries':'Connection retry count','template':'Filename template','template_help':'Example: %(title)s [%(id)s]','open_folder':'Open Download Folder','empty_history':'No downloads in history yet.','clear_history':'Clear History','about_title':'About MediaDown','developer':'Developer','credits':'Credits','version':'Version','about_text':'Built to manage and download video links through one clean interface.','legal':'Only save content you have permission to download. Follow platform terms and copyright rules.','added':'link(s) added to the queue.','invalid':'Please enter a valid http/https URL.','no_links':'Add at least one link first.','complete':'Download queue completed.','error':'Download error','confirm_clear':'Permanently clear download history?','saved':'Settings saved.','mp4':'MP4 · Video','mp3':'MP3 · Audio','best':'Best','theme':'Dark theme','max_items':'You can add up to 50 links at a time.','quality_note':'4K is available when the source video provides it.','thumb':'Thumbnail','date':'Date','file':'File','size':'Size','browse':'Browse','paused':'Paused','start':'Start','cancel':'Cancel','remove':'Remove Selected','all':'All','quality_note':'4K is used when available in the source.'},
 'de': {'home':'Startseite','history':'Download-Verlauf','settings':'Einstellungen','about':'Über','tagline':'Videos von deinen Plattformen herunterladen','subtitle':'YouTube, TikTok, Instagram, X und mehr','links':'VIDEO-LINKS','paste':'Links in separaten Zeilen einfügen','add':'Zur Warteschlange','download':'Warteschlange starten','format':'FORMAT','quality':'QUALITÄT','filename':'DATEINAME','queue':'DOWNLOAD-WARTESCHLANGE','clear':'Warteschlange leeren','status':'Status','title':'Video','platform':'Plattform','progress':'Fortschritt','ready':'Bereit','waiting':'Wartet','working':'Wird geladen','done':'Fertig','failed':'Fehler','cancelled':'Abgebrochen','choose':'Ordner wählen','location':'SPEICHERORT','general':'Allgemein','download_settings':'Downloads','appearance':'Darstellung','notifications':'Benachrichtigungen','advanced':'Erweitert','language':'App-Sprache','default_quality':'Standardqualität','default_format':'Standardformat','save':'Einstellungen speichern','reset':'Zurücksetzen','embed':'Vorschaubild einbetten (falls unterstützt)','save_thumb':'Vorschaubild separat speichern','notify':'Bei Abschluss benachrichtigen','skip':'Bereits geladene Dateien überspringen','retries':'Wiederholungsversuche','template':'Dateinamenvorlage','template_help':'Beispiel: %(title)s [%(id)s]','open_folder':'Download-Ordner öffnen','empty_history':'Noch kein Download-Verlauf.','clear_history':'Verlauf löschen','about_title':'Über MediaDown','developer':'Entwickler','credits':'Mitwirkende','version':'Version','about_text':'Eine einfache Oberfläche zum Verwalten und Herunterladen von Videolinks.','legal':'Nur Inhalte herunterladen, für die du eine Erlaubnis hast.','added':'Link(s) hinzugefügt.','invalid':'Bitte eine gültige URL eingeben.','no_links':'Füge zuerst einen Link hinzu.','complete':'Warteschlange abgeschlossen.','error':'Download-Fehler','confirm_clear':'Download-Verlauf dauerhaft löschen?','saved':'Einstellungen gespeichert.','mp4':'MP4 · Video','mp3':'MP3 · Audio','best':'Beste','choose':'Ordner wählen','theme':'Dunkles Design','thumb':'Vorschaubild','date':'Datum','file':'Datei','size':'Größe','browse':'Durchsuchen','start':'Start','cancel':'Abbrechen','remove':'Auswahl entfernen','quality_note':'4K wird verwendet, wenn die Quelle es anbietet.'},
 'es': {'home':'Inicio','history':'Historial','settings':'Ajustes','about':'Acerca de','tagline':'Descarga vídeos de tus plataformas favoritas','subtitle':'YouTube, TikTok, Instagram, X y más','links':'ENLACES DE VÍDEO','paste':'Pega enlaces en líneas separadas','add':'Añadir a la cola','download':'Iniciar descargas','format':'FORMATO','quality':'CALIDAD','filename':'NOMBRE DE ARCHIVO','queue':'COLA DE DESCARGAS','clear':'Vaciar cola','status':'Estado','title':'Vídeo','platform':'Plataforma','progress':'Progreso','ready':'Listo','waiting':'En espera','working':'Descargando','done':'Completado','failed':'Error','cancelled':'Cancelado','choose':'Elegir carpeta','location':'UBICACIÓN','general':'General','download_settings':'Descargas','appearance':'Apariencia','notifications':'Notificaciones','advanced':'Avanzado','language':'Idioma de la aplicación','default_quality':'Calidad predeterminada','default_format':'Formato predeterminado','save':'Guardar ajustes','reset':'Restablecer','embed':'Incrustar miniatura si es compatible','save_thumb':'Guardar miniatura por separado','notify':'Avisar al terminar','skip':'Omitir archivos ya descargados','retries':'Reintentos de conexión','template':'Plantilla de nombre','template_help':'Ejemplo: %(title)s [%(id)s]','open_folder':'Abrir carpeta','empty_history':'Aún no hay descargas.','clear_history':'Borrar historial','about_title':'Acerca de MediaDown','developer':'Desarrollador','credits':'Créditos','version':'Versión','about_text':'Creado para gestionar y descargar enlaces de vídeo fácilmente.','legal':'Descarga solo contenido que tengas permiso para guardar.','added':'enlace(s) añadidos.','invalid':'Introduce una URL http/https válida.','no_links':'Añade al menos un enlace.','complete':'Cola completada.','error':'Error de descarga','confirm_clear':'¿Borrar el historial permanentemente?','saved':'Ajustes guardados.','mp4':'MP4 · Vídeo','mp3':'MP3 · Audio','best':'Mejor','thumb':'Miniatura','date':'Fecha','file':'Archivo','size':'Tamaño','browse':'Examinar','start':'Iniciar','cancel':'Cancelar','remove':'Eliminar selección','quality_note':'4K disponible si el vídeo original lo permite.'},
 'fr': {'home':'Accueil','history':'Historique','settings':'Paramètres','about':'À propos','tagline':'Téléchargez des vidéos depuis vos plateformes','subtitle':'YouTube, TikTok, Instagram, X et plus','links':'LIENS VIDÉO','paste':'Collez les liens sur des lignes séparées','add':'Ajouter à la file','download':'Lancer les téléchargements','format':'FORMAT','quality':'QUALITÉ','filename':'NOM DU FICHIER','queue':'FILE DE TÉLÉCHARGEMENT','clear':'Vider la file','status':'État','title':'Vidéo','platform':'Plateforme','progress':'Progression','ready':'Prêt','waiting':'En attente','working':'Téléchargement','done':'Terminé','failed':'Erreur','cancelled':'Annulé','choose':'Choisir un dossier','location':'EMPLACEMENT','general':'Général','download_settings':'Téléchargements','appearance':'Apparence','notifications':'Notifications','advanced':'Avancé','language':'Langue de l’application','default_quality':'Qualité par défaut','default_format':'Format par défaut','save':'Enregistrer','reset':'Réinitialiser','embed':'Intégrer la miniature si possible','save_thumb':'Enregistrer la miniature séparément','notify':'Notifier à la fin','skip':'Ignorer les fichiers déjà téléchargés','retries':'Nombre de tentatives','template':'Modèle de nom','template_help':'Exemple : %(title)s [%(id)s]','open_folder':'Ouvrir le dossier','empty_history':'Aucun téléchargement.','clear_history':'Effacer l’historique','about_title':'À propos de MediaDown','developer':'Développeur','credits':'Crédits','version':'Version','about_text':'Conçu pour gérer et télécharger facilement des liens vidéo.','legal':'Téléchargez uniquement les contenus autorisés.','added':'lien(s) ajouté(s).','invalid':'Veuillez saisir une URL valide.','no_links':'Ajoutez d’abord un lien.','complete':'File terminée.','error':'Erreur de téléchargement','confirm_clear':'Effacer définitivement l’historique ?','saved':'Paramètres enregistrés.','mp4':'MP4 · Vidéo','mp3':'MP3 · Audio','best':'Meilleur','thumb':'Miniature','date':'Date','file':'Fichier','size':'Taille','browse':'Parcourir','start':'Démarrer','cancel':'Annuler','remove':'Supprimer la sélection','quality_note':'La 4K dépend de la vidéo source.'}
}
DEFAULT={'language':'tr','quality':'1080p','format':'MP4 · Video','folder':str(Path.home()/'Downloads'/'MediaDown'),'filename':'%(title).180B [%(id)s]','embed_thumbnail':True,'save_thumbnail':True,'notify':True,'skip_existing':True,'retries':3,'theme':'dark'}

def load_json(path, default):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception: return default.copy() if isinstance(default,dict) else default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def fmt_size(n):
    if not n: return '—'
    units=['B','KB','MB','GB']
    n=float(n)
    for u in units:
        if n<1024 or u=='GB': return f'{n:.1f} {u}'
        n/=1024

def platform_name(url):
    u=url.lower()
    for key,name in [('youtube','YouTube'),('youtu.be','YouTube'),('tiktok','TikTok'),('instagram','Instagram'),('twitter','X'),('x.com','X'),('facebook','Facebook'),('fb.watch','Facebook'),('reddit','Reddit'),('vimeo','Vimeo'),('twitch','Twitch')]:
        if key in u: return name
    return 'Web'

class MediaDown:
 def __init__(self, root):
    self.root=root; self.cfg=load_json(CONFIG,DEFAULT); self.cfg={**DEFAULT,**self.cfg}
    self.history=load_json(HISTORY,[]); self.items=[]; self.events=queue.Queue(); self.cancel_event=threading.Event(); self.worker=None; self.current_index=None; self.thumb_refs={}
    Path(self.cfg['folder']).mkdir(parents=True,exist_ok=True)
    root.title('MediaDown'); root.geometry('1120x780'); root.minsize(900,660); root.configure(bg=BG)
    try:
        root.iconbitmap(resource_path('MediaDown.ico'))
    except Exception: pass
    self.style=ttk.Style(); self.style.theme_use('clam')
    self.style.configure('Treeview',background=PANEL,foreground=TEXT,fieldbackground=PANEL,rowheight=32,borderwidth=0,font=('Segoe UI',9))
    self.style.configure('Treeview.Heading',background=PANEL2,foreground='#b9c9e3',relief='flat',font=('Segoe UI',9,'bold'))
    self.style.map('Treeview',background=[('selected','#244b80')],foreground=[('selected','white')])
    self.style.configure('TCombobox',fieldbackground=PANEL2,background=PANEL2,foreground=TEXT,arrowcolor=TEXT,bordercolor=PANEL2)
    self.style.map('TCombobox',fieldbackground=[('readonly',PANEL2)],foreground=[('readonly',TEXT)])
    self.style.configure('Horizontal.TProgressbar',troughcolor=PANEL2,background=BLUE,bordercolor=PANEL2,lightcolor=BLUE,darkcolor=BLUE)
    self._build(); self.show_page('home'); self.root.after(100,self._poll)

 def t(self,key): return LANG.get(self.cfg.get('language','tr'),LANG['tr']).get(key,LANG['tr'].get(key,key))
 def frame(self,parent,bg=PANEL,**kw): return tk.Frame(parent,bg=bg,**kw)
 def label(self,parent,text='',color=TEXT,size=10,bold=False,**kw): return tk.Label(parent,text=text,bg=parent.cget('bg'),fg=color,font=('Segoe UI',size,'bold' if bold else 'normal'),**kw)
 def button(self,parent,text,cmd,primary=False,**kw):
    return tk.Button(parent,text=text,command=cmd,bg=BLUE if primary else PANEL2,fg='white' if primary else TEXT,activebackground=BLUE2 if primary else '#263750',activeforeground='white',relief='flat',bd=0,cursor='hand2',font=('Segoe UI',9,'bold'),padx=15,pady=9,**kw)
 def _build(self):
    self.sidebar=self.frame(self.root,'#0e1627',width=218); self.sidebar.pack(side='left',fill='y'); self.sidebar.pack_propagate(False)
    logo=self.frame(self.sidebar,'#0e1627'); logo.pack(fill='x',padx=20,pady=(24,26))
    tk.Label(logo,text='MD',bg='#0e1627',fg='#64a7ff',font=('Segoe UI',31,'bold')).pack(anchor='w')
    self.label(logo,'MediaDown',TEXT,17,True).pack(anchor='w'); self.label(logo,'DOWNLOAD. ENJOY.',MUTED,8,True).pack(anchor='w',pady=(2,0))
    self.nav={}
    for key,ico in [('home','⌂'),('history','◷'),('settings','⚙'),('about','ⓘ')]:
        b=tk.Button(self.sidebar,text=f'  {ico}   {self.t(key)}',anchor='w',command=lambda k=key:self.show_page(k),bg='#0e1627',fg='#b8c6dc',activebackground='#1a3156',activeforeground='white',relief='flat',bd=0,font=('Segoe UI',10),padx=17,pady=13,cursor='hand2')
        b.pack(fill='x',padx=12,pady=3); self.nav[key]=b
    self.label(self.sidebar,'v'+VERSION,MUTED,8).pack(side='bottom',anchor='w',padx=22,pady=16)
    self.main=self.frame(self.root,BG); self.main.pack(side='left',fill='both',expand=True)
    self.top=self.frame(self.main,BG); self.top.pack(fill='x',padx=30,pady=(20,6))
    self.lang_var=tk.StringVar(value=self.cfg['language'])
    ttk.Combobox(self.top,textvariable=self.lang_var,values=['tr','en','de','es','fr'],state='readonly',width=6).pack(side='right')
    self.lang_var.trace_add('write',self._language_changed)
    self.page=self.frame(self.main,BG); self.page.pack(fill='both',expand=True,padx=30,pady=(5,24))

 def _language_changed(self,*_):
    self.cfg['language']=self.lang_var.get(); save_json(CONFIG,self.cfg); self._build_refresh()
 def _build_refresh(self):
    for w in self.sidebar.winfo_children():
        if isinstance(w,tk.Button): w.configure(text=f"  { {'home':'⌂','history':'◷','settings':'⚙','about':'ⓘ'}[next((k for k,v in self.nav.items() if v==w),'home')] }   {self.t(next((k for k,v in self.nav.items() if v==w),'home'))}")
    self.show_page(self.current_page)
 def show_page(self,name):
    self.current_page=name
    for w in self.page.winfo_children(): w.destroy()
    for k,b in self.nav.items(): b.configure(bg='#17345f' if k==name else '#0e1627',fg='white' if k==name else '#b8c6dc')
    if name=='home': self._home()
    elif name=='history': self._history_page()
    elif name=='settings': self._settings_page()
    else: self._about_page()

 def _home(self):
    self.label(self.page,self.t('tagline'),TEXT,23,True).pack(anchor='w')
    self.label(self.page,self.t('subtitle'),MUTED,10).pack(anchor='w',pady=(3,18))
    card=self.frame(self.page,PANEL,highlightthickness=1,highlightbackground=LINE); card.pack(fill='x')
    pad=self.frame(card,PANEL); pad.pack(fill='x',padx=18,pady=16)
    self.label(pad,self.t('links'),TEXT,9,True).pack(anchor='w',pady=(0,8))
    self.link_text=tk.Text(pad,height=3,bg=PANEL2,fg=TEXT,insertbackground=TEXT,relief='flat',font=('Segoe UI',10),wrap='word',padx=10,pady=9,highlightthickness=1,highlightbackground=LINE)
    self.link_text.pack(fill='x')
    self.link_text.insert('1.0',self.t('paste'))
    self.link_text.bind('<FocusIn>',lambda e:self.link_text.delete('1.0','end') if self.link_text.get('1.0','end-1c')==self.t('paste') else None)
    row=self.frame(pad,PANEL); row.pack(fill='x',pady=(12,0))
    self.format_var=tk.StringVar(value=self.cfg['format']); self.quality_var=tk.StringVar(value=self.cfg['quality'])
    ttk.Combobox(row,textvariable=self.format_var,values=[self.t('mp4'),self.t('mp3'),'MP4 · Video','MP3 · Audio'],state='readonly',width=17).pack(side='left',ipady=5,padx=(0,8))
    ttk.Combobox(row,textvariable=self.quality_var,values=['En iyi','2160p (4K)','1440p (2K)','1080p','720p','480p','360p','Best','2160p (4K)','1440p (2K)'],state='readonly',width=17).pack(side='left',ipady=5,padx=(0,8))
    ttk.Combobox(row,values=['Otomatik isimlendirme','Automatic naming'],state='readonly',width=23).pack(side='left',ipady=5)
    self.button(row,self.t('add'),self.add_links).pack(side='right')
    self.button(row,self.t('download'),self.start_queue,True).pack(side='right',padx=(0,8))
    self.label(pad,self.t('quality_note'),MUTED,8).pack(anchor='w',pady=(8,0))
    lower=self.frame(self.page,BG); lower.pack(fill='both',expand=True,pady=(16,0))
    qcard=self.frame(lower,PANEL,highlightthickness=1,highlightbackground=LINE); qcard.pack(side='left',fill='both',expand=True,padx=(0,8))
    hcard=self.frame(lower,PANEL,highlightthickness=1,highlightbackground=LINE,width=265); hcard.pack(side='left',fill='both',padx=(8,0)); hcard.pack_propagate(False)
    qhead=self.frame(qcard,PANEL); qhead.pack(fill='x',padx=15,pady=12)
    self.label(qhead,self.t('queue'),TEXT,11,True).pack(side='left')
    self.button(qhead,self.t('clear'),self.clear_queue).pack(side='right')
    self.button(qhead,self.t('cancel'),self.cancel_queue).pack(side='right',padx=(0,6))
    self.button(qhead,self.t('remove'),self.remove_selected).pack(side='right',padx=(0,6))
    cols=('title','platform','status','progress')
    self.queue_tree=ttk.Treeview(qcard,columns=cols,show='headings',height=8)
    for col,w in [('title',330),('platform',95),('status',115),('progress',90)]:
        self.queue_tree.heading(col,text=self.t(col if col!='title' else 'title')); self.queue_tree.column(col,width=w,anchor='w')
    self.queue_tree.pack(fill='both',expand=True,padx=12,pady=(0,12))
    self.label(hcard,self.t('history'),TEXT,11,True).pack(anchor='w',padx=15,pady=13)
    self.recent_box=self.frame(hcard,PANEL); self.recent_box.pack(fill='both',expand=True,padx=12,pady=(0,10)); self._refresh_recent()
    self._refresh_queue()

 def add_links(self):
    raw=self.link_text.get('1.0','end-1c').strip()
    urls=[]
    for line in raw.splitlines():
        u=line.strip().strip('"\'<>')
        if u.startswith(('http://','https://')) and u not in urls: urls.append(u)
    if not urls: messagebox.showwarning(APP,self.t('invalid')); return
    if len(urls)>50: messagebox.showwarning(APP,self.t('max_items')); urls=urls[:50]
    existing={x['url'] for x in self.items}
    count=0
    for url in urls:
        if url in existing: continue
        self.items.append({'url':url,'title':url,'platform':platform_name(url),'status':'waiting','progress':0,'thumbnail':None,'file':None,'error':None})
        count+=1
    self.link_text.delete('1.0','end'); self._refresh_queue()
    self.label # keep UI callback safe
    if count: self.root.title(f'MediaDown · {count} {self.t("added")}')

 def _refresh_queue(self):
    if not hasattr(self,'queue_tree') or not self.queue_tree.winfo_exists(): return
    for iid in self.queue_tree.get_children(): self.queue_tree.delete(iid)
    for i,item in enumerate(self.items):
        status=self.t(item['status']) if item['status'] in ['waiting','working','done','failed','cancelled'] else item['status']
        self.queue_tree.insert('','end',iid=str(i),values=(item['title'][:65],item['platform'],status,f"{item['progress']:.0f}%"))
 def clear_queue(self):
    if self.worker and self.worker.is_alive(): return
    self.items=[]; self._refresh_queue()
 def remove_selected(self):
    if self.worker and self.worker.is_alive(): return
    ids=self.queue_tree.selection()
    for iid in sorted([int(x) for x in ids],reverse=True): self.items.pop(iid)
    self._refresh_queue()

 def start_queue(self):
    if yt_dlp is None: messagebox.showerror(APP,'yt-dlp is not installed. Run build.bat.'); return
    if not self.items: messagebox.showinfo(APP,self.t('no_links')); return
    if self.worker and self.worker.is_alive(): return
    self.cancel_event.clear(); self.worker=threading.Thread(target=self._run_queue,daemon=True); self.worker.start()
 def _run_queue(self):
    for i,item in enumerate(self.items):
        if self.cancel_event.is_set(): break
        if item['status']=='done': continue
        self.current_index=i; item['status']='working'; self.events.put(('refresh',))
        try:
            self._download_one(i,item)
        except Exception as e:
            item['status']='cancelled' if self.cancel_event.is_set() else 'failed'; item['error']=str(e)[:350]
            self.events.put(('refresh',))
        if self.cancel_event.is_set(): break
    self.events.put(('queue_done',))
 def _download_one(self,index,item):
    audio=self.format_var.get().lower().startswith('mp3')
    q=self.quality_var.get() if hasattr(self,'quality_var') else self.cfg['quality']
    if '2160' in q or '4k' in q.lower(): h=2160
    elif '1440' in q or '2k' in q.lower(): h=1440
    elif '1080' in q: h=1080
    elif '720' in q: h=720
    elif '480' in q: h=480
    elif '360' in q: h=360
    else: h=None
    if audio: fmt='bestaudio/best'
    elif h: fmt=f'bestvideo[height<={h}]+bestaudio/best[height<={h}]/best'
    else: fmt='bestvideo*+bestaudio/best'
    folder=Path(self.cfg['folder']); folder.mkdir(parents=True,exist_ok=True)
    template=self.cfg.get('filename') or DEFAULT['filename']
    outtmpl=str(folder/(template+'.%(ext)s'))
    def hook(d):
        if self.cancel_event.is_set(): raise Exception('Cancelled')
        if d.get('status')=='downloading':
            total=d.get('total_bytes') or d.get('total_bytes_estimate') or 0; done=d.get('downloaded_bytes',0)
            pct=done*100/total if total else 0
            item['progress']=pct; item['title']=d.get('info_dict',{}).get('title') or item['title']
            self.events.put(('progress',index,pct,item['title']))
        elif d.get('status')=='finished': item['progress']=100; self.events.put(('progress',index,100,item['title']))
    opts={'outtmpl':outtmpl,'format':fmt,'noplaylist':True,'progress_hooks':[hook],'quiet':True,'no_warnings':True,'windowsfilenames':True,'retries':int(self.cfg.get('retries',3)),'continuedl':True,'overwrites':not self.cfg.get('skip_existing',True),'writethumbnail':bool(self.cfg.get('save_thumbnail',True))}
    if audio: opts['postprocessors']=[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192'}]
    if self.cfg.get('embed_thumbnail',True):
        opts.setdefault('postprocessors',[]).append({'key':'EmbedThumbnail'})
    try:
        import imageio_ffmpeg
        opts['ffmpeg_location']=imageio_ffmpeg.get_ffmpeg_exe()
    except Exception: pass
    with yt_dlp.YoutubeDL(opts) as ydl:
        info=ydl.extract_info(item['url'],download=True)
        item['title']=info.get('title') or item['title']; item['thumbnail']=info.get('thumbnail')
        item['file']=ydl.prepare_filename(info)
        item['status']='done'; item['progress']=100
        record={'title':item['title'],'platform':item['platform'],'url':item['url'],'file':item['file'],'thumbnail':item.get('thumbnail'),'date':datetime.now().strftime('%Y-%m-%d %H:%M'),'status':'done','size':os.path.getsize(item['file']) if item.get('file') and os.path.exists(item['file']) else 0}
        self.history.insert(0,record); self.history=self.history[:500]; save_json(HISTORY,self.history)
    self.events.put(('refresh',))
 def cancel_queue(self): self.cancel_event.set()
 def _poll(self):
    try:
        while True:
            e=self.events.get_nowait(); kind=e[0]
            if kind=='refresh': self._refresh_queue()
            elif kind=='progress':
                _,i,pct,title=e
                if i<len(self.items): self.items[i]['title']=title; self.items[i]['progress']=pct; self._refresh_queue()
            elif kind=='queue_done':
                self._refresh_queue(); self._refresh_recent()
                if self.cfg.get('notify',True): self.root.bell()
                self.root.title('MediaDown')
                if not self.cancel_event.is_set(): self.root.after(100,lambda:messagebox.showinfo(APP,self.t('complete')))
    except queue.Empty: pass
    self.root.after(150,self._poll)

 def _refresh_recent(self):
    if not hasattr(self,'recent_box') or not self.recent_box.winfo_exists(): return
    for w in self.recent_box.winfo_children(): w.destroy()
    if not self.history:
        self.label(self.recent_box,self.t('empty_history'),MUTED,9).pack(anchor='w',pady=10); return
    for rec in self.history[:5]:
        f=self.frame(self.recent_box,PANEL2); f.pack(fill='x',pady=4)
        self.label(f,rec.get('title','Video')[:32],TEXT,9,True).pack(anchor='w',padx=9,pady=(7,1))
        self.label(f,rec.get('date',''),MUTED,8).pack(anchor='w',padx=9,pady=(0,7))

 def _history_page(self):
    self.label(self.page,self.t('history'),TEXT,22,True).pack(anchor='w')
    self.label(self.page,self.t('subtitle'),MUTED,9).pack(anchor='w',pady=(3,15))
    card=self.frame(self.page,PANEL,highlightthickness=1,highlightbackground=LINE); card.pack(fill='both',expand=True)
    head=self.frame(card,PANEL); head.pack(fill='x',padx=16,pady=12)
    self.button(head,self.t('clear_history'),self.clear_history).pack(side='right')
    cols=('title','platform','date','size','file'); tree=ttk.Treeview(card,columns=cols,show='headings')
    for c,w in [('title',270),('platform',100),('date',135),('size',80),('file',300)]: tree.heading(c,text=self.t(c)); tree.column(c,width=w,anchor='w')
    tree.pack(fill='both',expand=True,padx=12,pady=(0,12))
    for rec in self.history: tree.insert('','end',values=(rec.get('title',''),rec.get('platform',''),rec.get('date',''),fmt_size(rec.get('size')),rec.get('file','')))
    foot=self.frame(self.page,BG); foot.pack(fill='x',pady=(10,0)); self.button(foot,self.t('open_folder'),self.open_folder).pack(side='left')
 def clear_history(self):
    if messagebox.askyesno(APP,self.t('confirm_clear')): self.history=[]; save_json(HISTORY,[]); self.show_page('history')
 def _settings_page(self):
    self.label(self.page,self.t('settings'),TEXT,22,True).pack(anchor='w')
    self.label(self.page,'MediaDown · '+VERSION,MUTED,9).pack(anchor='w',pady=(3,15))
    card=self.frame(self.page,PANEL,highlightthickness=1,highlightbackground=LINE); card.pack(fill='both',expand=True)
    body=self.frame(card,PANEL); body.pack(fill='both',expand=True,padx=22,pady=18)
    self.label(body,self.t('general'),TEXT,12,True).pack(anchor='w',pady=(0,10))
    self.settings_vars={}
    def combo(label,key,values):
        r=self.frame(body,PANEL); r.pack(fill='x',pady=5); self.label(r,label,TEXT,9).pack(side='left'); v=tk.StringVar(value=str(self.cfg.get(key,''))); ttk.Combobox(r,textvariable=v,values=values,state='readonly',width=22).pack(side='right',ipady=4); self.settings_vars[key]=v
    combo(self.t('language'),'language',['tr','en','de','es','fr'])
    combo(self.t('default_quality'),'quality',['best','2160p (4K)','1440p (2K)','1080p','720p','480p','360p'])
    combo(self.t('default_format'),'format',['MP4 · Video','MP3 · Audio'])
    self.label(body,self.t('location'),TEXT,9,True).pack(anchor='w',pady=(15,6))
    fr=self.frame(body,PANEL); fr.pack(fill='x')
    self.folder_var=tk.StringVar(value=self.cfg['folder']); tk.Entry(fr,textvariable=self.folder_var,bg=PANEL2,fg=TEXT,insertbackground=TEXT,relief='flat').pack(side='left',fill='x',expand=True,ipady=8)
    self.button(fr,self.t('choose'),self.choose_folder).pack(side='right',padx=(8,0))
    self.label(body,self.t('download_settings'),TEXT,12,True).pack(anchor='w',pady=(17,8))
    for key,labelkey in [('embed_thumbnail','embed'),('save_thumbnail','save_thumb'),('notify','notify'),('skip_existing','skip')]:
        v=tk.BooleanVar(value=bool(self.cfg.get(key,True))); self.settings_vars[key]=v
        tk.Checkbutton(body,text=self.t(labelkey),variable=v,bg=PANEL,fg=TEXT,activebackground=PANEL,activeforeground=TEXT,selectcolor=PANEL2,font=('Segoe UI',9)).pack(anchor='w',pady=3)
    r=self.frame(body,PANEL); r.pack(fill='x',pady=(10,4)); self.label(r,self.t('retries'),TEXT,9).pack(side='left')
    self.retries_var=tk.StringVar(value=str(self.cfg.get('retries',3))); ttk.Combobox(r,textvariable=self.retries_var,values=['1','2','3','5','10'],state='readonly',width=8).pack(side='right')
    self.label(body,self.t('filename'),TEXT,9,True).pack(anchor='w',pady=(12,5))
    self.filename_var=tk.StringVar(value=self.cfg.get('filename',DEFAULT['filename'])); tk.Entry(body,textvariable=self.filename_var,bg=PANEL2,fg=TEXT,insertbackground=TEXT,relief='flat').pack(fill='x',ipady=8)
    self.label(body,self.t('template_help'),MUTED,8).pack(anchor='w',pady=(4,0))
    foot=self.frame(body,PANEL); foot.pack(fill='x',pady=(17,0)); self.button(foot,self.t('reset'),self.reset_settings).pack(side='left'); self.button(foot,self.t('save'),self.save_settings,True).pack(side='right')
 def choose_folder(self):
    d=filedialog.askdirectory(initialdir=self.cfg['folder']);
    if d: self.folder_var.set(d)
 def save_settings(self):
    for k,v in self.settings_vars.items(): self.cfg[k]=v.get()
    self.cfg['folder']=self.folder_var.get().strip() or DEFAULT['folder']; self.cfg['retries']=int(self.retries_var.get() or 3); self.cfg['filename']=self.filename_var.get().strip() or DEFAULT['filename']
    Path(self.cfg['folder']).mkdir(parents=True,exist_ok=True); save_json(CONFIG,self.cfg); messagebox.showinfo(APP,self.t('saved')); self.show_page('settings')
 def reset_settings(self):
    self.cfg=DEFAULT.copy(); save_json(CONFIG,self.cfg); self.show_page('settings')
 def open_folder(self):
    os.startfile(self.cfg['folder']) if os.name=='nt' else subprocess.Popen(['xdg-open',self.cfg['folder']])
 def _about_page(self):
    card=self.frame(self.page,PANEL,highlightthickness=1,highlightbackground=LINE); card.pack(fill='both',expand=True)
    center=self.frame(card,PANEL); center.pack(expand=True,padx=30,pady=30)
    tk.Label(center,text='MD',bg=PANEL,fg='#64a7ff',font=('Segoe UI',55,'bold')).pack()
    self.label(center,'MediaDown',TEXT,25,True).pack(pady=(0,2)); self.label(center,'Download. Enjoy.',MUTED,9).pack()
    self.label(center,'v'+VERSION,MUTED,9).pack(pady=(12,20))
    self.label(center,self.t('about_text'),TEXT,10).pack(pady=(0,24))
    self.label(center,self.t('credits'),MUTED,9,True).pack(); self.label(center,'Baran Arda Törk',TEXT,16,True).pack(pady=(5,2)); self.label(center,self.t('developer'),MUTED,9).pack()
    self.label(center,self.t('legal'),MUTED,8,wraplength=550,justify='center').pack(pady=(30,0))

 def _language_changed(self,*_):
    # Refresh the visible page using the selected language. Persist immediately.
    self.cfg['language']=self.lang_var.get(); save_json(CONFIG,self.cfg)
    self._build_refresh()
 def _build_refresh(self):
    icons={'home':'⌂','history':'◷','settings':'⚙','about':'ⓘ'}
    for k,b in self.nav.items(): b.configure(text=f"  {icons[k]}   {self.t(k)}")
    self.show_page(self.current_page)

def resource_path(name):
    base=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base,name)

if __name__=='__main__':
    root=tk.Tk(); app=MediaDown(root); root.mainloop()
