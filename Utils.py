import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import urllib2
import os
import sys
import time
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString


Addon_Data_Path = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % __addonid__).decode("utf-8"))


def MoveProperties(container_number, focuscontrol):
    Properties = ["Label", "Label2", "icon", "thumb", "fanart", "Path", "RootPath", "LibraryPath", "Poster", "clearlogo", "clearart", "landscape", "Season",
                  "banner", "characterart", "discart", "Year", "Plot", "Tagline", "OriginalTitle", "Album_Type", "Type", "TVShowTitle",
                  "Director", "Rating", "StatusID", "Status", "NextTitle", "LatestTitle", "LatestDate", "Studio", "Budget",
                  "Country", "Network", "PercentPlayed", "AudioChannels", "AudioCodec", "VideoCodec", "VideoAspect",, "Album_Genre", "Artist_Genre",
                  "mpaa", "Id", "Channel", "Publisher", "Description", "Artist_Description", "Album_Description", "Genre", "Album_Label", "Premiered", "Duration",
                  "Folder", "EpisodeNumber", "Version", "DBID", "Artist_Mood", "Album_Mood", "Album_Style", "Artist_Style", "Album_Theme", "Artist_Instrument", "Artist_Born", "PlotOutline",
                  "Artist_Died", "Artist_Formed", "Artist_Disbanded", "Artist_YearsActive", "Trailer", "Top250", "Writer", "Watched", "VideoResolution"]
    for prop in Properties:
        InfoLabel = xbmc.getInfoLabel("$ESCINFO[Container(%s).ListItem.Property(%s)]" % (str(container_number), prop))
        if InfoLabel.strip() is "":
            InfoLabel = xbmc.getInfoLabel("$ESCINFO[Container(%s).ListItem.%s]" % (str(container_number), prop))
        if InfoLabel.strip() is "":
            InfoLabel = xbmc.getInfoLabel("$ESCINFO[Container(%s).ListItem.Art(%s)]" % (str(container_number), prop))
        builtin = "SetProperty(%s,%s,home)" % (prop, InfoLabel.strip())
        xbmc.executebuiltin(builtin)
    xbmc.executebuiltin("SetFocus(%s)" % (str(focuscontrol)))


def GetStringFromUrl(encurl):
    succeed = 0
    while succeed < 5:
        try:
            request = urllib2.Request(encurl)
            request.add_header('User-agent', 'XBMC/13.2 ( ptemming@gmx.net )')
           # request.add_header('Accept-encoding', 'gzip')
            response = urllib2.urlopen(request)
           # if response.info().get('Content-Encoding') == 'gzip':
           #     buf = StringIO(response.read())
           #     compr = gzip.GzipFile(fileobj=buf)
           #     data = compr.read()
           # else:
            data = response.read()
            return data
        except:
            log("GetStringFromURL: could not get data from %s" % encurl)
            xbmc.sleep(1000)
            succeed += 1
    return ""


def Get_JSON_response(base_url="", custom_url="", cache_days=0.5):
    from base64 import b64encode
    filename = b64encode(custom_url).replace("/", "XXXX")
    path = Addon_Data_Path + "\\&" + filename + ".txt"
    cache_seconds = int(cache_days * 86400.0)
    if xbmcvfs.exists(path) and ((time.time() - os.path.getmtime(path)) < cache_seconds):
        return read_from_file(path)
    else:
        url = base_url + custom_url
        response = GetStringFromUrl(url)
        results = simplejson.loads(response)
        save_to_file(results, filename, Addon_Data_Path)
        return results


def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)


def CreateListItem(json_array):
    item = xbmcgui.ListItem("Undefined")
    for key, value in json_array.iteritems():
        item.setProperty(key, value)
        if key in ["thumb", "poster", "banner", "icon"]:
            item.setArt({key: value})
        elif key == "label":
            item.setLabel(value)
        elif key == "label2":
            item.setLabel2(value)
    item.setProperty("item_info", simplejson.dumps(json_array))
    return item


def save_to_file(content, filename, path=""):
    if path == "":
        text_file_path = get_browse_dialog() + filename + ".txt"
    else:
        if not xbmcvfs.exists(path):
            xbmcvfs.mkdir(path)
        text_file_path = os.path.join(path, filename + ".txt")
    log("save to textfile:")
    log(text_file_path)
    text_file = xbmcvfs.File(text_file_path, "w")
    simplejson.dump(content, text_file)
    text_file.close()
    return True


def read_from_file(path=""):
    log("trying to load " + path)
    # Set path
    if path == "":
        path = get_browse_dialog(dlg_type=1)
    # Check to see if file exists
    if xbmcvfs.exists(path):
        f = open(path)
        fc = simplejson.load(f)
        log("loaded textfile " + path)
        try:
            return fc
        except:
            log("error when loading file")
            log(fc)
            return []
    else:
        return False


def cleanText(text):
    import re
    if text is not None:
        text = re.sub('<br \/>', '[CR]', text)
        text = re.sub('<br\/>', '[CR]', text)
        text = re.sub('<(.|\n|\r)*?>', '', text)
        text = re.sub('&quot;', '"', text)
        text = re.sub('&amp;', '&', text)
        text = re.sub('&gt;', '>', text)
        text = re.sub('&lt;', '<', text)
        text = re.sub('&#;', "'", text)
        text = re.sub('&#39;', "'", text)
        text = re.sub('<i>', '[I]', text)
        text = re.sub('<\/i>', '[/I]', text)
        text = re.sub('<strong>', '[B]', text)
        text = re.sub('<\/strong>', '[/B]', text)
        text = re.sub('User-contributed text is available under the Creative Commons By-SA License and may also be available under the GNU FDL.', '', text)
        return text.strip()
    else:
        return ""


def Notify(header, line='', line2='', line3=''):
    xbmc.executebuiltin('Notification(%s,%s,%s,%s)' % (header, line, line2, line3))


def prettyprint(string):
    log(simplejson.dumps(string, sort_keys=True, indent=4, separators=(',', ': ')))
