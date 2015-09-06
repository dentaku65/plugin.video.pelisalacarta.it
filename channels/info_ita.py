# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para info_ita
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import xbmcaddon
import xbmcgui
 
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
 
line1 = "Pelisalacarta Italian repack"
line2 = "Coded: Zanzibar82, dentaku65, Dr-Zer0 and fenice82. BIG thanks: robalo, jesus"
line3 = "http://yep.it/forumita"
 
xbmcgui.Dialog().ok(__addonname__, line1, line2, line3)
