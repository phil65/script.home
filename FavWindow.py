#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2014 Philipp Temminghoff (philipptemminghoff@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import xbmcaddon
import xbmcgui
import simplejson
from Utils import *

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString
__addonpath__ = __addon__.getAddonInfo('path')

CONTROL_SLIDER = 101
ACTION_CONTEXT_MENU = [117]
ACTION_OSD = [122]
ACTION_PREVIOUS_MENU = [9, 92, 10]
ACTION_SHOW_INFO = [11]
ACTION_EXIT_SCRIPT = [13]
ACTION_DOWN = [4]
ACTION_UP = [3]
ACTION_LEFT = [1]
ACTION_RIGHT = [2]
ACTION_0 = [58, 18]
ACTION_PLAY = [79]
ACTION_SELECT_ITEM = [7]
homewindow = xbmcgui.Window(10000)


class FavWindow(xbmcgui.WindowXML):

    def __init__(self, skin_file, addon_path):
        log('__init__')

    def onInit(self, startGUI=True):
        self.favitems = self.GetFavouriteswithType("media")
        db_movielist = create_light_movielist()
        favmovies = []
        for db_movie in db_movielist["result"]["movies"]:
            for fav in self.favitems:
                if db_movie["file"] in fav["Builtin"]:
                    favmovies.append(db_movie)
        listitems = CreateListItems(favmovies)
        self.getControl(110).setLabel("Movies")
        self.getControl(111).addItems(listitems)
     #   self.setFocus(110)
        Notify("here")

    def getControls(self):
        pass

    def onAction(self, action):
        action_id = action.getId()
        if action_id in ACTION_PREVIOUS_MENU:
            self.close()
        elif action_id in ACTION_SHOW_INFO:
            if xbmc.getCondVisibility("Control.HasFocus(5009)"):
                xbmc.executebuiltin("Control.Move(5002,1)")

    def onClick(self, controlId):
        if controlId == 18:
            pass

    def onFocus(self, controlId):
        pass

    def GetFavouriteswithType(self, favtype):
        favs = self.GetFavourites()
        favlist = []
        for fav in favs:
            if fav["Type"] == favtype:
                favlist.append(fav)
        return favlist

    def GetFavPath(self, fav):
        if fav["type"] == "media":
            path = "PlayMedia(%s)" % (fav["path"])
        elif fav["type"] == "script":
            path = "RunScript(%s)" % (fav["path"])
        else:
            path = "ActivateWindow(%s,%s)" % (fav["window"], fav["windowparameter"])
        return path

    def GetFavourites(self):
        items = []
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Favourites.GetFavourites", "params": {"type": null, "properties": ["path", "thumbnail", "window", "windowparameter"]}, "id": 1}')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_query = simplejson.loads(json_query)
        if json_query["result"]["limits"]["total"] > 0:
            for fav in json_query["result"]["favourites"]:
                path = self.GetFavPath(fav)
                newitem = {'Label': fav["title"],
                           'Thumb': fav["thumbnail"],
                           'Type': fav["type"],
                           'Builtin': path,
                           'Path': "plugin://script.extendedinfo/?info=action&&id=" + path}
                items.append(newitem)
        return items
