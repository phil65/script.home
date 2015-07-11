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
__addonicon__ = __addon__.getAddonInfo('icon')
__language__ = __addon__.getLocalizedString


Addon_Data_Path = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % __addonid__).decode("utf-8"))


def MoveProperties(container_number, focuscontrol):
    focusedcontrol = "todo"
    if container_number == "focused":
        container_number = focusedcontrol
    if focuscontrol == "focused":
        focuscontrol = focusedcontrol
    InfoLabels = ["Label", "Label2", "icon", "thumb", "Path", "Season", "Year", "Plot", "OriginalTitle", "TVShowTitle",
                  "Director", "Rating", "Votes", "Studio", "StarRating", "Country", "PercentPlayed", "AudioChannels", "AudioCodec", "VideoCodec", "VideoAspect",
                  "mpaa", "Genre", "Premiered", "duration", "Folder", "Episode", "DBID", "Writer", "Watched", "VideoResolution"]
    Properties = ["Album_Type", "Type", "imdb_id", "Album_Genre", "Artist_Genre", "Id", "Description", "Artist_Description", "Album_Description", "Album_Label",
                  "DBID", "Artist_Mood", "Album_Mood", "duration_formatted", "Path", "Album_Style", "Artist_Style", "Album_Theme", "Artist_Instrument", "Artist_Born",
                  "Artist_Died", "Artist_Formed", "Artist_Disbanded", "Artist_YearsActive", "Addon.Description", "Addon.Summary", "Addon.Version", "Addon.Creator"]
    Art = ["fanart", "tvshow.fanart", "poster", "tvshow.poster", "clearlogo", "tvshow.clearlogo", "clearart", "tvshow.clearart", "landscape", "tvshow.landscape",
           "banner", "characterart", "tvshow.banner", "tvshow.characterart"]
    for prop in InfoLabels:
        InfoLabel = xbmc.getInfoLabel("Container(%s).ListItem.%s" % (str(container_number), prop))
        xbmcgui.Window(10000).setProperty(prop, InfoLabel.strip())
    for prop in Properties:
        InfoLabel = xbmc.getInfoLabel("Container(%s).ListItem.Property(%s)" % (str(container_number), prop))
        if (InfoLabel.strip() == "") and (prop in InfoLabels):
            InfoLabel = xbmc.getInfoLabel("Container(%s).ListItem.%s" % (str(container_number), prop))
        xbmcgui.Window(10000).setProperty(prop, InfoLabel.strip())
    for prop in Art:
        InfoLabel = xbmc.getInfoLabel("Container(%s).ListItem.Art(%s)" % (str(container_number), prop))
        xbmcgui.Window(10000).setProperty(prop, InfoLabel.strip())
    xbmc.executebuiltin("SetFocus(%s)" % (str(focuscontrol)))


def Main_Menu_Move():
    xbmcgui.Window(10000).setProperty("scrolling", "true")
    xbmc.sleep(150)
    for i in range(0, 7):
        xbmcgui.Window(10000).setProperty("Widget%iType" % i, xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget%iType)" % i))
        xbmcgui.Window(10000).setProperty("Widget%iTitle" % i, xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget%iTitle)" % i))
        xbmcgui.Window(10000).setProperty("Widget%iContent" % i, xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget%iContent)" % i))
    xbmcgui.Window(10000).clearProperty("scrolling")


def create_light_movielist():
    json_query = xbmc.executeJSONRPC(
        '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["file", "genre", "thumbnail", "art"], "sort": { "method": "random" } }, "id": 1}')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    json_query = simplejson.loads(json_query)
    return json_query


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


def CreateListItems(data):
    InfoLabels = ["genre", "year", "episode", "season", "top250", "tracknumber", "year", "plot", "tagline", "originaltitle", "tvshowtitle",
                  "director", "rating", "studio", "starrating", "country", "percentplayed", "audiochannels", "audiocodec", "videocodec", "videoaspect",
                  "mpaa", "genre", "premiered", "duration", "folder", "episode", "dbid", "plotoutline", "trailer", "top250", "writer", "watched", "videoresolution"]    # log(str(xbmcgui.getCurrentWindowId()))
    # log(str(xbmcgui.getCurrentWindowDialogId()))
    # log(str(controlwindow))
    itemlist = []
    if data is not None:
        for (count, result) in enumerate(data):
            listitem = xbmcgui.ListItem('%s' % (str(count)))
            itempath = ""
            for (key, value) in result.iteritems():
           #     log("key: " + unicode(key) + "  value: " + unicode(value))
                if str(key).lower() in ["name", "label", "title"]:
                    listitem.setLabel(unicode(value))
                if str(key).lower() in ["thumb"]:
                    listitem.setThumbnailImage(unicode(value))
                if str(key).lower() in ["icon"]:
                    listitem.setIconImage(unicode(value))
                if str(key).lower() in ["thumb", "poster", "banner", "fanart", "clearart", "clearlogo", "landscape", "discart", "characterart", "tvshow.fanart", "tvshow.poster", "tvshow.banner", "tvshow.clearart", "tvshow.characterart"]:
                    listitem.setArt({str(key).lower(): unicode(value)})
                if str(key).lower() in ["path"]:
                    itempath = unicode(value)
                # if str(key).lower() in InfoLabels:
                #     listitem.setInfo('video', {str(key).lower(): unicode(value)})
       #             Notify(value)
                listitem.setProperty('%s' % (str(key)), unicode(value))
           # itempath = "SetFocus(" + str((controlnumber + 1)) + ")"
            listitem.setPath(path=itempath)
            listitem.setProperty("target_url", itempath)
            listitem.setProperty("node:target_url", itempath)
            listitem.setProperty("node.target_url", itempath)
            itemlist.append(listitem)
    return itemlist


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
        if key in ["thumb", "poster", "banner", "icon", "discart", "clearlogo", "characterart", "landscape", "tvshow.clearlogo", "tvshow.characterart", "tvshow.clearlogo"]:
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


def Notify(header="", message="", icon=__addonicon__, time=5000, sound=True):
    dialog = xbmcgui.Dialog()
    dialog.notification(heading=header, message=message, icon=icon, time=time, sound=sound)


def prettyprint(string):
    log(simplejson.dumps(string, sort_keys=True, indent=4, separators=(',', ': ')))
