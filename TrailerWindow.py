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
LISTS = [8001, 8002, 8003, 8004, 8005, 8006, 8007]


class TrailerWindow(xbmcgui.WindowXML):

    def __init__(self, skin_file, addon_path):
        log('__init__')

    def onInit(self, startGUI=True):
        pass

    def onAction(self, action):
        action_id = action.getId()
        if action_id in ACTION_PREVIOUS_MENU:
            self.close()
        elif action_id in ACTION_SHOW_INFO:
            focusedcontrol = self.getFocusId()
            MoveProperties(focusedcontrol, focusedcontrol)
            movieid = xbmc.getInfoLabel("Container(%i).ListItem.Property(ID)" % focusedcontrol)
            builtin = "RunScript(script.extendedinfo,info=extendedinfo,id=%s,imdbid=%s)" % (movieid, xbmc.getInfoLabel("Window(home).Property(imdbid)"))
            xbmc.executebuiltin(builtin)
        # elif action_id in ACTION_LEFT:
        #     for controlnumber in LISTS:
        #         if controlnumber != focusedcontrol:
        #             xbmc.executebuiltin("Control.Move(%i,-1)" % (controlnumber))
        # elif action_id in ACTION_RIGHT:
        #     for controlnumber in LISTS:
        #         if controlnumber != focusedcontrol:
        #             xbmc.executebuiltin("Control.Move(%i,1)" % (controlnumber))

    def onClick(self, controlId):
        pass

    def onFocus(self, controlId):
        pass
