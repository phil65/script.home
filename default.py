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
from ColorConfigDialog import ColorConfigDialog
from TrailerWindow import TrailerWindow
from FeaturedWindow import FeaturedWindow

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString
__addonpath__ = __addon__.getAddonInfo('path')


addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
addon_name = addon.getAddonInfo('name')

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
CANCEL_DIALOG = [9, 10, 92, 216, 247, 257, 275, 61467, 61448]


class GUI(xbmcgui.WindowXML):

    def __init__(self, skin_file, addon_path):
        log('__init__')

    def onInit(self, startGUI=True):
        log('onInit')

    def getControls(self):
        pass

    def onAction(self, action):
        action_id = action.getId()
        if action_id in ACTION_SHOW_INFO:
            if xbmc.getCondVisibility("Control.HasFocus(9000)"):
                if xbmc.getCondVisibility("IsEmpty(Window(home).Property(DisableWidgets))"):
                    xbmc.executebuiltin("SetProperty(DisableWidgets,1,home)")
                else:
                    xbmc.executebuiltin("ClearProperty(DisableWidgets,home)")
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4321),featured) + Control.HasFocus(5010)"):
                xbmc.executebuiltin("Control.Move(5001,1)")
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4321),featured) + Control.HasFocus(5011)"):
                xbmc.executebuiltin("Control.Move(5002,1)")
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4321),featured) + Control.HasFocus(5012)"):
                xbmc.executebuiltin("Control.Move(5003,1)")
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4325),featured) + Control.HasFocus(6010)"):
                xbmc.executebuiltin("Control.Move(6001,1)")
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4325),featured) + Control.HasFocus(6011)"):
                xbmc.executebuiltin("Control.Move(6002,1)")
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4325),featured) + Control.HasFocus(6012)"):
                xbmc.executebuiltin("Control.Move(6003,1)")

        elif action_id in ACTION_CONTEXT_MENU:
            if xbmc.getCondVisibility("[Substring(Control.GetLabel(4321),featured) + [Control.HasFocus(5010) | Control.HasFocus(5011) | Control.HasFocus(5012)]] | [Substring(Control.GetLabel(4325),featured) + [Control.HasFocus(6010) | Control.HasFocus(6011) | Control.HasFocus(6012)]]"):
                focusedcontrol = self.getFocusId()
                if (focusedcontrol > 6000) and (xbmc.getCondVisibility("Substring(Control.GetLabel(4325),music)")):
                    playlistpath = 'special://musicplaylists/'
                    playlisttype = "Music"
                elif (focusedcontrol < 6000) and (xbmc.getCondVisibility("Substring(Control.GetLabel(4321),music)")):
                    playlistpath = 'special://musicplaylists/'
                    playlisttype = "Music"
                elif (focusedcontrol > 6000) and (xbmc.getCondVisibility("Substring(Control.GetLabel(4325),tv)")):
                    playlistpath = 'special://videoplaylists/'
                    playlisttype = "TV"
                elif (focusedcontrol < 6000) and (xbmc.getCondVisibility("Substring(Control.GetLabel(4321),tv)")):
                    playlistpath = 'special://videoplaylists/'
                    playlisttype = "TV"
                else:
                    playlistpath = 'special://videoplaylists/'
                    playlisttype = "Movies"
                context_menu = ContextMenu(u'script-globalsearch-contextmenu.xml', addon_path, labels=["Edit Content", "Set to Default"])
                context_menu.doModal()
                log(context_menu.selection)
                log(focusedcontrol)
                if context_menu.selection == 0:
                    playlist = xbmcgui.Dialog().browse(1, "Choose Playlist", 'files', ".xsp|.m3u", False, False, playlistpath)
                    builtin = "Skin.SetString(Featured" + playlisttype + str(focusedcontrol) + "Content," + playlist + ")"
                    log(builtin)
                    xbmc.executebuiltin(builtin)
                elif context_menu.selection == 1:
                    builtin = "Skin.Reset(Featured" + playlisttype + str(focusedcontrol) + "Content)"
                    xbmc.executebuiltin(builtin)
                del context_menu
            elif xbmc.getCondVisibility("Control.HasFocus(9000)"):
                pass
            elif xbmc.getCondVisibility("[Substring(Control.GetLabel(4321),Icon) + Control.HasFocus(5010)] | [Substring(Control.GetLabel(4325),Icon) + Control.HasFocus(6010)]"):
                itemid = xbmc.getInfoLabel("Container(" + str(self.getFocusId()) + ").ListItem.Property(ID)")
                builtin = "SetProperty(MenuItem," + itemid + ",home)"
                xbmc.executebuiltin(builtin)
                for item in ["Type", "MultiFanart", "Label", "Path", "Icon"]:
                    builtin = "Skin.SetString(ItemToEdit." + item + "," + xbmc.getInfoLabel("Skin.String(" + itemid + "." + item + ")") + ")"
                    xbmc.executebuiltin(builtin)
                xbmc.executebuiltin("ActivateWindow(1135)")


    def onClick(self, controlId):
        if controlId == 9000:
            pass

    def onFocus(self, controlId):
        pass


class ContextMenu(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.labels = kwargs["labels"]

    def onInit(self):
        self._show_context_menu()

    def _show_context_menu(self):
        self._hide_buttons()
        self._setup_menu()
        self.setFocus(self.getControl(1001))

    def _hide_buttons(self):
        for button in range(1001, 1004):
            self.getControl(button).setVisible(False)

    def _setup_menu(self):
        dialog_posx, dialog_posy = self.getControl(999).getPosition()
        dialog_height = self.getControl(999).getHeight()
        button_posx, button_posy = self.getControl(1001).getPosition()
        button_height = self.getControl(1001).getHeight()
        extra_height = (len(self.labels) - 1) * button_height
        dialog_height = dialog_height + extra_height
        dialog_posy = dialog_posy - (extra_height / 2)
        button_posy = button_posy - (extra_height / 2)
        self.getControl(999).setPosition(dialog_posx, dialog_posy)
        self.getControl(999).setHeight(dialog_height)
        for button in range(len(self.labels)):
            self.getControl(button + 1001).setPosition(button_posx, button_posy + (button_height * button))
            self.getControl(button + 1001).setLabel(self.labels[button])
            self.getControl(button + 1001).setVisible(True)
            self.getControl(button + 1001).setEnabled(True)

    def _close_dialog(self, selection=None):
        self.selection = selection
        self.close()

    def onClick(self, controlId):
        self._close_dialog(controlId - 1001)

    def onFocus(self, controlId):
        pass

    def onAction(self, action):
        if (action.getId() in CANCEL_DIALOG) or (action.getId() in ACTION_CONTEXT_MENU):
            self._close_dialog()


if __name__ == '__main__':
    window = None
    for arg in sys.argv:
        param = arg.lower()
        log("param = " + param)
        if param.startswith('window='):
            window = param[7:]
        if param.startswith('container='):
            container = param[10:]
        if param.startswith('focuscontrol='):
            focuscontrol = param[13:]
    if window is not None:
        if window == "home":
            gui = GUI(u'script-%s-main.xml' % addon_name, addon_path).doModal()
            del gui
        elif window == "colorconfig":
            gui = ColorConfigDialog(u'script-%s-colorconfig.xml' % addon_name, addon_path).doModal()
            del gui
        elif window == "trailers":
            gui = TrailerWindow(u'script-%s-trailers.xml' % addon_name, addon_path).doModal()
            del gui
        elif window == "featured":
            gui = FeaturedWindow(u'script-%s-featured.xml' % addon_name, addon_path).doModal()
            del gui
    else:
        MoveProperties(container, focuscontrol)
    sys.modules.clear()
