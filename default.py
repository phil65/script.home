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
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4321),image) + Control.HasFocus(5010)"):
                xbmc.executebuiltin("SetProperty(WidgetPosition,Widget1,home)")
                xbmc.executebuiltin("SetFocus(22222)")
            elif xbmc.getCondVisibility("Substring(Control.GetLabel(4325),image) + Control.HasFocus(6010)"):
                xbmc.executebuiltin("SetProperty(WidgetPosition,Widget2,home)")
                xbmc.executebuiltin("SetFocus(22222)")
            elif xbmc.getCondVisibility("Control.HasFocus(5010)"):
                xbmc.executebuiltin("SetFocus(5014)")
            elif xbmc.getCondVisibility("Control.HasFocus(6010)"):
                xbmc.executebuiltin("SetFocus(6014)")

        elif action_id in ACTION_CONTEXT_MENU:
            if xbmc.getCondVisibility("[Substring(Control.GetLabel(4321),featured) + [Control.HasFocus(5010) | Control.HasFocus(5011) | Control.HasFocus(5012)]] | [Substring(Control.GetLabel(4325),featured) + [Control.HasFocus(6010) | Control.HasFocus(6011) | Control.HasFocus(6012)]]"):
                self.FeaturedContextMenu()
            elif xbmc.getCondVisibility("Control.HasFocus(9000)"):
                self.HomeContextMenu()
            elif xbmc.getCondVisibility("[Substring(Control.GetLabel(4321),Icon) + Control.HasFocus(5010)] | [Substring(Control.GetLabel(4325),Icon) + Control.HasFocus(6010)]"):
                itemid = xbmc.getInfoLabel("Container(" + str(self.getFocusId()) + ").ListItem.Property(ID)")
                builtin = "SetProperty(MenuItem," + itemid + ",home)"
                xbmc.executebuiltin(builtin)
                for item in ["Type", "MultiFanart", "Label", "Path", "Icon"]:
                    builtin = "Skin.SetString(ItemToEdit." + item + "," + xbmc.getInfoLabel("Skin.String(" + itemid + "." + item + ")") + ")"
                    xbmc.executebuiltin(builtin)
                xbmc.executebuiltin("ActivateWindow(1135)")

    def HomeContextMenu(self):
        xbmc.executebuiltin("SetProperty(" + xbmc.getInfoLabel("Window(home).Property(MenuName)") + "," + xbmc.getInfoLabel("Container(9000).ListItem.Property(ID)") + ",home)")
        xbmc.executebuiltin("SetProperty(MenuItem," + xbmc.getInfoLabel("Container(9000).ListItem.Property(ID)") + ",home)")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Label," + xbmc.getInfoLabel("Container(9000).ListItem.Label") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.MultiFanart," + xbmc.getInfoLabel("Container(9000).ListItem.Icon") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Icon," + xbmc.getInfoLabel("Container(9000).ListItem.Property(BigIcon)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Widget," + xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Widget2," + xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget2)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.WidgetTitle," + xbmc.getInfoLabel("Container(9000).ListItem.Property(WidgetTitle)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Widget2Title," + xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget2Title)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.InfoLine," + xbmc.getInfoLabel("Container(9000).ListItem.Property(InfoLine)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.SubMenu," + xbmc.getInfoLabel("Container(9000).ListItem.Property(submenuVisibility)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Disable," + xbmc.getInfoLabel("Container(9000).ListItem.Property(DisableIcon)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Type," + xbmc.getInfoLabel("Container(9000).ListItem.Property(Type)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Path," + xbmc.getInfoLabel("Container(9000).ListItem.Property(Path)") + ")")
        context_menu = ContextMenu(u'script-globalsearch-contextmenu.xml', addon_path, labels=["Edit Main Menu Item", "Color Settings", "Furniture Settings", "Smart Playlist Manager", "Hide / Unhide All Items", "NowPlaying Widget Options"])
        context_menu.doModal()
        if context_menu.selection == 0:
            Notify("Experimental")
            xbmc.executebuiltin("ActivateWindow(1122)")
        elif context_menu.selection == 1:
            xbmc.executebuiltin("ActivateWindow(1128)")
        elif context_menu.selection == 2:
            xbmc.executebuiltin("ActivateWindow(1131)")
        elif context_menu.selection == 3:
            xbmc.executebuiltin("ActivateWindow(1148)")
        elif context_menu.selection == 4:
            if xbmc.getCondVisibility("IsEmpty(Window(home).Property(EditMode))"):
                xbmc.executebuiltin("SetProperty(EditMode,True,home)")
            else:
                xbmc.executebuiltin("ClearProperty(EditMode,home)")
        elif context_menu.selection == 5:
            xbmc.executebuiltin("ActivateWindow(1158)")

    def FeaturedContextMenu(self):
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
        context_menu = ContextMenu(u'script-globalsearch-contextmenu.xml', addon_path, labels=["Set to Smart Playlist", "Set to Library Node", "Set to Default"])
        context_menu.doModal()
        if context_menu.selection == 0:
            playlist = xbmcgui.Dialog().browse(1, "Choose Playlist", 'files', ".xsp|.m3u", False, False, playlistpath)
            builtin = "Skin.SetString(Featured" + playlisttype + str(focusedcontrol) + "Content," + playlist + ")"
            log(builtin)
            xbmc.executebuiltin(builtin)
        elif context_menu.selection == 1:
            playlist = xbmcgui.Dialog().browse(0, "Choose Path", 'files', "", True, False, "library://video/")
            builtin = "Skin.SetString(Featured" + playlisttype + str(focusedcontrol) + "Content," + playlist + ")"
            log(builtin)
            xbmc.executebuiltin(builtin)
        elif context_menu.selection == 2:
            builtin = "Skin.Reset(Featured" + playlisttype + str(focusedcontrol) + "Content)"
            xbmc.executebuiltin(builtin)
        del context_menu

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
        for button in range(1001, 1008):
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
            from ColorConfigDialog import ColorConfigDialog
            gui = ColorConfigDialog(u'script-%s-colorconfig.xml' % addon_name, addon_path).doModal()
            del gui
        elif window == "trailers":
            from TrailerWindow import TrailerWindow
            gui = TrailerWindow(u'script-%s-trailers.xml' % addon_name, addon_path).doModal()
            del gui
        elif window == "featured":
            from FeaturedWindow import FeaturedWindow
            gui = FeaturedWindow(u'script-%s-featured.xml' % addon_name, addon_path).doModal()
            del gui
        elif window == "dialogalbuminfo":
            from DialogAlbumInfo import DialogAlbumInfo
            gui = DialogAlbumInfo(u'script-%s-dialogalbuminfo.xml' % addon_name, addon_path).doModal()
            del gui

    else:
        MoveProperties(container, focuscontrol)
    sys.modules.clear()
