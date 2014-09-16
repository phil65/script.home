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


class ColorConfigDialog(xbmcgui.WindowXMLDialog):

    def __init__(self, skin_file, addon_path):
        log('__init__')

    def onInit(self, startGUI=True):
        self.getControl(18).setPercent(100)
        xbmc.sleep(100)
        if xbmc.getCondVisibility("Window.IsActive(skinsettings)"):
            self.color = xbmc.getInfoLabel("Skin.String(diffuse_color)")
        else:
            self.color = xbmc.getInfoLabel("Skin.String(BackgroundDarkness)")            
        self.alpha = int(self.color[:2],16)
        log(self.color)
        self.basecolor = self.color[2:]
        log(self.basecolor)
        self.getControl(18).setPercent(self.alpha)

    def getControls(self):
        pass

    def onAction(self, action):
        action_id = action.getId()
        if action_id in ACTION_PREVIOUS_MENU:
            self.close()

    def onClick(self, controlId):
        if controlId == 18:
            percent = self.getControl(18).getPercent()
            normed = 155 + int(percent)
            self.alpha = hex(normed)[2:]
            self.color = self.alpha + self.basecolor
            log(str(normed))
            log(self.basecolor)
            log(self.alpha)
            if xbmc.getCondVisibility("Window.IsActive(skinsettings)"):
                xbmc.executebuiltin("Skin.SetString(diffuse_color,%s)" % (self.color))
            else:
                xbmc.executebuiltin("Skin.SetString(BackgroundDarkness,%s)" % (self.color))

    def onFocus(self, controlId):
        pass
