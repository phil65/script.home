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

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ADDON_NAME = ADDON.getAddonInfo('name')
SKIN_DIR = xbmc.getSkinDir()

CONTROL_SEARCH = 101
ACTION_CONTEXT_MENU = [117]
ACTION_OSD = [122]
ACTION_PREVIOUS_MENU = [9, 92, 10]
ACTION_SHOW_INFO = [11]
ACTION_EXIT_SCRIPT = [13]
ACTION_DOWN = [4]
ACTION_UP = [3]
ACTION_SCROLL = [1, 2, 5, 6, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 104, 105]
ACTION_LEFT = [1]
ACTION_PAGE_UP = [5]
ACTION_PAGE_DOWN = [6]
ACTION_RIGHT = [2]
ACTION_0 = [58, 18]
ACTION_PLAY = [79]
ACTION_SELECT_ITEM = [7]
CANCEL_DIALOG = [9, 10, 92, 216, 247, 257, 275, 61467, 61448]
HOME = xbmcgui.Window(10000)


class GUI(xbmcgui.WindowXML):

    def __init__(self, *args, **kwargs):
        log('__init__')

    def onInit(self, startGUI=True):
        log('onInit')
        if xbmc.getSkinDir() != SKIN_DIR:
            self.close()

    def getControls(self):
        pass

    def onAction(self, action):
        action_id = action.getId()
        focus_id = self.getFocusId()
        widgets = {5010: xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget1Type)"),
                   6010: xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget2Type)"),
                   7010: xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget3Type)"),
                   8010: xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget4Type)"),
                   10010: xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget5Type)"),
                   11010: xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget6Type)"),
                   }
        if action_id in ACTION_SCROLL:
            if focus_id == 9000:
                Main_Menu_Move()
        # elif action_id in ACTION_DOWN:
        #     if focus_id == 9010:
        #         offsetleft = False
        #         offsetright = False
        #         for i in range(1, 10):
        #             temp_offsetleft = xbmc.getInfoLabel("Container(9010).ListItemNoWrap(%i).Label" % (i))
        #             temp_offsetright = xbmc.getInfoLabel("Container(9010).ListItemNoWrap(%i).Label" % (i * -1))
        #             if (temp_offsetleft == "") and (offsetleft is False):
        #                 offsetleft = i
        #             if (temp_offsetright == "") and (offsetright is False):
        #                 offsetright = i
        #         steps = (offsetleft - offsetright) / 2
        #         xbmc.executebuiltin("Control.Move(9010, %i)" % steps)
        elif action_id in ACTION_CONTEXT_MENU:
            log(widgets.get(focus_id, ""))
            if focus_id == 9000:
                self.HomeContextMenu()
            elif "info" in widgets.get(focus_id, "").lower():
                item_id = xbmc.getInfoLabel("Container(%i).ListItem.Property(ID)" % focus_id)
                HOME.setProperty("MenuItem", item_id)
                for item in ["Type", "MultiFanart", "Label", "Path", "Icon"]:
                    builtin = "Skin.SetString(ItemToEdit." + item + "," + xbmc.getInfoLabel("Skin.String(" + item_id + "." + item + ")") + ")"
                    xbmc.executebuiltin(builtin)
                xbmc.executebuiltin("ActivateWindow(1135)")

    def HomeContextMenu(self):
        xbmc.executebuiltin("SetProperty(" + xbmc.getInfoLabel("Window(home).Property(MenuName)") + "," + xbmc.getInfoLabel("Container(9000).ListItem.Property(ID)") + ",home)")
        xbmc.executebuiltin("SetProperty(MenuItem," + xbmc.getInfoLabel("Container(9000).ListItem.Property(ID)") + ",home)")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Label," + xbmc.getInfoLabel("Container(9000).ListItem.Label") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.MultiFanart," + xbmc.getInfoLabel("Container(9000).ListItem.Icon") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Icon," + xbmc.getInfoLabel("Container(9000).ListItem.Property(BigIcon)") + ")")
        for i in range(0, 7):
            xbmc.executebuiltin("Skin.SetString(ItemToEdit.Widget%iType," % i + xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget%iType)" % i) + ")")
            xbmc.executebuiltin("Skin.SetString(ItemToEdit.Widget%iTitle," % i + xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget%iTitle)" % i) + ")")
            xbmc.executebuiltin("Skin.SetString(ItemToEdit.Widget%iContent," % i + xbmc.getInfoLabel("Container(9000).ListItem.Property(Widget%iContent)" % i) + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.BackgroundOverlay," + xbmc.getInfoLabel("Container(9000).ListItem.Property(BackgroundOverlay)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.InfoLine," + xbmc.getInfoLabel("Container(9000).ListItem.Property(InfoLine)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.SubMenu," + xbmc.getInfoLabel("Container(9000).ListItem.Property(submenuVisibility)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Disable," + xbmc.getInfoLabel("Container(9000).ListItem.Property(DisableIcon)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Type," + xbmc.getInfoLabel("Container(9000).ListItem.Property(Type)") + ")")
        xbmc.executebuiltin("Skin.Setstring(ItemToEdit.Path," + xbmc.getInfoLabel("Container(9000).ListItem.Property(Path)") + ")")
        context_menu = ContextMenu(u'script-globalsearch-contextmenu.xml', ADDON_PATH, labels=["Edit Main Menu Item", "Exchange Position", "Hide / Unhide All Items", "Color Settings", "Furniture Settings"])
        context_menu.doModal()
        if context_menu.selection == 0:
            xbmc.executebuiltin("ActivateWindow(1122)")
        elif context_menu.selection == 1:
            xbmc.executebuiltin("ActivateWindow(1151)")
        elif context_menu.selection == 2:
            if xbmc.getCondVisibility("IsEmpty(Window(home).Property(EditMode))"):
                xbmc.executebuiltin("SetProperty(EditMode,True,home)")
            else:
                xbmc.executebuiltin("ClearProperty(EditMode,home)")
        elif context_menu.selection == 3:
            xbmc.executebuiltin("ActivateWindow(1128)")
        elif context_menu.selection == 4:
            xbmc.executebuiltin("ActivateWindow(1131)")

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
            HOME.setProperty("homewindowactive", "true")
            gui = GUI(u'script-%s-main.xml' % ADDON_NAME, ADDON_PATH).doModal()
            HOME.clearProperty("homewindowactive")
            del gui
        elif window == "colorconfig":
            from ColorConfigDialog import ColorConfigDialog
            gui = ColorConfigDialog(u'script-%s-colorconfig.xml' % ADDON_NAME, ADDON_PATH).doModal()
            del gui
        elif window == "trailers":
            from TrailerWindow import TrailerWindow
            gui = TrailerWindow(u'script-%s-trailers.xml' % ADDON_NAME, ADDON_PATH).doModal()
            del gui
        elif window == "favourites":
            from FavWindow import FavWindow
            gui = FavWindow(u'script-globalsearch-main.xml', ADDON_PATH).doModal()
            del gui
        elif window == "dialogalbuminfo":
            from DialogAlbumInfo import DialogAlbumInfo
            gui = DialogAlbumInfo(u'script-%s-dialogalbuminfo.xml' % ADDON_NAME, ADDON_PATH).doModal()
            del gui
        elif window == "fullscreeninfo":
            from FullscreenInfo import FullscreenInfo
            gui = FullscreenInfo(u'script-%s-fullscreeninfo.xml' % ADDON_NAME, ADDON_PATH).doModal()
            del gui
        elif window == "downloader":
            from Downloader import Downloader
            dialog = Downloader()
            dialog.show_download_dialog()
            del dialog
    else:
        MoveProperties(container, focuscontrol)
