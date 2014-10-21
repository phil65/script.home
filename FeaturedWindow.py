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
homewindow = xbmcgui.Window(10000)


class FeaturedWindow(xbmcgui.WindowXML):

    def __init__(self, skin_file, addon_path):
        log('__init__')

    def onInit(self, startGUI=True):
        pass

    def getControls(self):
        pass

    def onAction(self, action):
        action_id = action.getId()
        if action_id in ACTION_PREVIOUS_MENU:
            if xbmc.getCondVisibility("Control.IsVisible(123)"):
                xbmc.executebuiltin("ClearProperty(PanelWidgetInfo,home)")
                xbmc.executebuiltin("SetFocus(40)")
            else:
                self.close()
        elif action_id in ACTION_SHOW_INFO:
            if xbmc.getCondVisibility("Control.HasFocus(5009)"):
                xbmc.executebuiltin("Control.Move(5002,1)")
            elif xbmc.getCondVisibility("Control.HasFocus(5011)"):
                xbmc.executebuiltin("Control.Move(5003,1)")
            elif xbmc.getCondVisibility("Control.HasFocus(6010)"):
                xbmc.executebuiltin("Control.Move(6002,1)")
            elif xbmc.getCondVisibility("Control.HasFocus(6011)"):
                xbmc.executebuiltin("Control.Move(6003,1)")
            elif xbmc.getCondVisibility("Control.HasFocus(7010)"):
                xbmc.executebuiltin("Control.Move(7002,1)")
            elif xbmc.getCondVisibility("Control.HasFocus(8010)"):
                xbmc.executebuiltin("Control.Move(8002,1)")
            elif xbmc.getCondVisibility("Control.HasFocus(9010)"):
                xbmc.executebuiltin("Control.Move(9002,1)")
            elif xbmc.getCondVisibility("Control.HasFocus(7003)"):
                homewindow.setProperty("PanelWidgetInfo", "true")
                homewindow.setProperty("WidgetPosition", "Widget1")
                homewindow.setProperty("WidgetType", xbmc.getInfoLabel("Control.GetLabel(4321)"))
                MoveProperties(7003, 5055)
            elif xbmc.getCondVisibility("Control.HasFocus(8003)"):
                homewindow.setProperty("PanelWidgetInfo", "true")
                homewindow.setProperty("WidgetPosition", "Widget1")
                homewindow.setProperty("WidgetType", xbmc.getInfoLabel("Control.GetLabel(4321)"))
                MoveProperties(8003, 5055)
            elif xbmc.getCondVisibility("Control.HasFocus(9003)"):
                homewindow.setProperty("PanelWidgetInfo", "true")
                homewindow.setProperty("WidgetPosition", "Widget1")
                homewindow.setProperty("WidgetType", xbmc.getInfoLabel("Control.GetLabel(4321)"))
                MoveProperties(9003, 5055)

    def onClick(self, controlId):
        if controlId == 18:
            pass

    def onFocus(self, controlId):
        pass
