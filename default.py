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


addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
addon_name = addon.getAddonInfo('name')


class GUI(xbmcgui.WindowXML):

    CONTROL_SEARCH = 101
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

    def __init__(self, skin_file, addon_path):
        log('__init__')

    def onInit(self, startGUI=True):
        log('onInit')

    def init_vars(self):
        self.NavMode_active = False
        self.street_view = False

    def getControls(self):
        pass

    def onAction(self, action):
        action_id = action.getId()
        if action_id in self.ACTION_SHOW_INFO:
            if xbmc.getCondVisibility("IsEmpty(Window(home).Property(DisableWidgets))"):
                xbmc.executebuiltin("SetProperty(DisableWidgets,1,home)")
            else:
                xbmc.executebuiltin("ClearProperty(DisableWidgets,home)")

    def onClick(self, controlId):
        if controlId == 100:
            pass

    def onFocus(self, controlId):
        pass
        
if __name__ == '__main__':
    startGUI = True
    for arg in sys.argv:
        param = arg.lower()
        log("param = " + param)
        if param.startswith('container='):
            startGUI = False
            container = param[10:]
        if param.startswith('focuscontrol='):
            startGUI = False
            focuscontrol = param[13:]
    if startGUI:
        gui = GUI(u'script-%s-main.xml' % addon_name, addon_path).doModal()
        del gui
    else:
        MoveProperties(container, focuscontrol)
    sys.modules.clear()
