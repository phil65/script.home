import os
import re
import fnmatch
import zipfile
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import shutil

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')
__cwd__ = __addon__.getAddonInfo('path').decode("utf-8")
__language__ = __addon__.getLocalizedString

SKIN_PATH = os.path.join(xbmc.translatePath("special://home/addons"), xbmc.getSkinDir())
ADDON_DATA_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % __addonid__).decode("utf-8"))


class Downloader():

    def show_download_dialog(self):
        modeselect = []
        if xbmc.getSkinDir() != "skin.aeon.nox":
            xbmcgui.Dialog().ok(__addonid__, "Skin not supported")
            return
        modeselect.append(__language__(34008))
        modeselect.append(__language__(34009))
        modeselect.append(__language__(34013))
        modeselect.append(__language__(34019))
        self.checkDir(os.path.join(ADDON_DATA_PATH))
        dialogSelection = xbmcgui.Dialog()
        self.download_mode = dialogSelection.select(__language__(34010), modeselect)
        if self.download_mode == -1:
            return
        # Download more themes...
        elif self.download_mode == 0:
            url_folder = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/backgrounds/"
            self.zip_path = os.path.join(ADDON_DATA_PATH, "backgroundpacks")
            self.install_path = os.path.join(SKIN_PATH, "backgrounds")
            download_button = __language__(34001)
            # Install local theme...
        elif self.download_mode == 1:
            url_folder = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/themes/"
            self.install_path = os.path.join(SKIN_PATH, "media")
            self.zip_path = os.path.join(ADDON_DATA_PATH, "themes")
            download_button = __language__(34011)
        elif self.download_mode == 2:
            url_folder = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/genreart/icons/"
            self.install_path = os.path.join(SKIN_PATH, "extras", "genre", "video", "icons")
            self.zip_path = os.path.join(ADDON_DATA_PATH, "videogenreicons")
            download_button = __language__(34012)
        elif self.download_mode == 3:
            url_folder = "http://aeon-nox-background-packs.googlecode.com/svn/trunk/Music/icons/"
            self.install_path = os.path.join(SKIN_PATH, "extras", "genre", "music", "icons")
            self.zip_path = os.path.join(ADDON_DATA_PATH, "musicgenreicons")
            download_button = __language__(34020)
        themes = self.get_download_list(self.zip_path)
        themes.append(download_button)
        self.checkDir(self.zip_path)
     #   if len(sys.argv) == 2 and sys.argv[ 1 ].startswith("http://") :
     #       url_folder = sys.argv[ 1 ]
        # Dialog to select local theme or download more...
        dialogThemes = xbmcgui.Dialog()
        index = dialogThemes.select(__language__(34002), themes)
        # Cancel / Back...
        if index == -1:
            return
        # Download more themes...
        elif index == len(themes) - 1:
            self.show_remote_themes(url_folder)
        # Install local theme...
        else:
            theme = themes[index]
            self.install_local_zip(theme)

    def log(self, txt):
        if isinstance(txt, str):
            txt = txt.decode("utf-8")
        message = u'%s: %s' % (__addonid__, txt)
        xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

    def checkDir(self, path):
        if not xbmcvfs.exists(path):
            xbmcvfs.mkdir(path)

    def get_download_list(self, path):
        # Get a list of extra themes (local)
        themes = []
        if os.path.isdir(self.zip_path):
            for entry in os.listdir(self.zip_path):
                if fnmatch.fnmatch(entry, "*.zip"):
                    (name, ext) = os.path.splitext(entry)
                    themes.append(name)
        return themes

    def show_remote_themes(self, url_folder):
        file = urllib.urlopen(url_folder)
        html = file.read()
        # Parse HTML...
        regexp = re.compile("<li><a href=\"(.*?)\">(.*?)</a></li>", re.DOTALL)
        items = regexp.findall(html)
        # Build a list of remote themes...
        themes = []
        for item in items:
            if item[1] != "..":
                (name, ext) = os.path.splitext(item[1])
                themes.append(name)
        # No remote themes found...
        if len(themes) == 0:
            xbmcgui.Dialog().ok(__addonid__, __language__(34007))
        # User to choose a remote theme...
        else:
            dialogThemes = xbmcgui.Dialog()
            index = dialogThemes.select(__language__(34006), themes)
            # Cancel...
            if index == -1:
                return
            #  User chose remote theme...
            theme = themes[index]
            # Show progress dialog...
            dp = xbmcgui.DialogProgress()
            dp.create(__addonid__, __language__(34005), theme)
            # Download theme...
            remote_theme = os.path.join(url_folder, "%s.zip" % theme)
            local_theme = os.path.join(self.zip_path, "%s.zip" % theme)
            urllib.urlretrieve(remote_theme, local_theme, lambda nb, bs, fs, url=remote_theme: self.download_progress_hook(nb, bs, fs, local_theme, dp))
            # Close progress dialog...
            dp.close()
            # Install local zip...
            self.install_local_zip(theme)

    def download_progress_hook(self, numblocks, blocksize, filesize, url=None, dp=None, ratio=1.0):
        downloadedsize = numblocks * blocksize
        percent = int(downloadedsize * 100 / filesize)
        dp.update(percent)

    def install_local_zip(self, theme):
        try:
            # Init
         #   shutil.rmtree(self.install_path)
            if self.download_mode == 0:
                contents = [os.path.join(self.install_path, i) for i in os.listdir(self.install_path)]
                [shutil.rmtree(i) if os.path.isdir(i) else os.unlink(i) for i in contents]
            DownloadedZip = os.path.join(self.zip_path, "%s.zip" % theme)
            # Extract theme zip...
            zip = zipfile.ZipFile(DownloadedZip, "r")
            zip.extractall(self.install_path, filter(lambda f: not f.endswith('/'), zip.namelist()))
            zip.close()
            xbmcgui.Dialog().ok(__addonid__, __language__(34003))
            self.show_download_dialog()
        except:
            # Message...
            xbmcgui.Dialog().ok(__addonid__, __language__(34004))
            self.show_download_dialog()
