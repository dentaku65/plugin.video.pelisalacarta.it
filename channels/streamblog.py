# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import urlparse
import re
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "streamblog"
__category__ = "F"
__type__ = "generic"
__title__ = "streamblog (IT)"
__language__ = "IT"

headers = [
    ['Host', 'www.streamblog.tv'],
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Cookie', '']
]

DEBUG = config.get_setting("debug")

host = "http://www.streamblog.tv"


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.streamblog mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Novita'[/COLOR]",
                     action="peliculas",
                     url=host),
                Item(channel=__channel__,
                     title="[COLOR azure]Categorie[/COLOR]",
                     action="categorias",
                     url=host),
                Item(channel=__channel__,
                     title="[COLOR azure]Serie TV[/COLOR]",
                     extra="serie",
                     action="peliculas",
                     url="%s/serie-tv/" % host),
                Item(channel=__channel__,
                     title="[COLOR azure]Animazione[/COLOR]",
                     action="peliculas",
                     url="%s/animazione/" % host),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search")]

    return itemlist


def categorias(item):
    logger.info("pelisalacarta.streamblog categorias")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data, '<li class="drop"><a href="#" class="navlink">(.*?)<div class="bl_search">')

    # The categories are the options for the combo
    patron = '<li><a href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url, titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url, url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot))

    return itemlist


def search(item, texto):
    logger.info("[streamblog.py] " + item.url + " search " + texto)
    item.url = "%s/index.php?story=%s&do=search&subaction=search" % (host, texto)
    try:
        return results(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def results(item):
    logger.info("pelisalacarta.streamblog results")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '.*?<h2><a href="([^"]+)">(.*?)</a></h2>\s*'
    patron += '</div>\s*'
    patron += '<.*?img src="([^"]+)".*?/>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"fstory_descr clear decor\">")
        end = html.find("<div class=\"fstory_treyler decor\">", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        scrapedplot = scrapertools.decodeHtmlentities(scrapedplot)
        # scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=host + scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True,
                 fanart=host + scrapedthumbnail))

    # Extrae el paginador
    patronvideos = '<div class="navigation".*?<span.*?/span>.*?<a href="([^"]+)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="results",
                 title="[COLOR orange]Avanti >>[/COLOR]",
                 url=scrapedurl,
                 folder=True))

    return itemlist


def peliculas(item):
    logger.info("pelisalacarta.streamblog peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers=headers)

    # Extrae las entradas (carpetas)
    patron = '<div class="poster"><a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)".*?</div>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        html = scrapertools.cache_page(scrapedurl, headers=headers)
        start = html.find("<div class=\"fstory_descr clear decor\">")
        end = html.find("<div class=\"fstory_treyler decor\">", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<[^>]*>', '', scrapedplot)
        # scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="episodios" if item.extra == "serie" else "findvideos",
                 title="[COLOR azure]" + scrapedtitle + "[/COLOR]",
                 url=scrapedurl,
                 thumbnail=host + scrapedthumbnail,
                 plot=scrapedplot,
                 folder=True,
                 fanart=host + scrapedthumbnail))

    # Extrae el paginador
    patronvideos = '<div class="navigation".*?<span.*?/span>.*?<a href="([^"]+)">'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="peliculas",
                 title="[COLOR orange]Avanti >>[/COLOR]",
                 url=scrapedurl,
                 folder=True))

    return itemlist


def episodios(item):
    logger.info("pelisalacarta.streamblog episodios")

    itemlist = []

    ## Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.decodeHtmlentities(data)

    patron = r'<!--colorstart:#(\d+)--><span style="color:#\1">(.+ StreamNowMovies HD </a>)'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for _, match in matches:
        for data in match.split('<br />'):
            ## Extrae las entradas
            season_title = scrapertools.find_single_match(data, '<b>([^<]+)</b>')
            if season_title != '':
                lang_title = 'SUB ITA' if 'SUB' in season_title.upper() else 'ITA'
            scrapedtitle = scrapertools.find_single_match(data, '\d+x\d+')
            if scrapedtitle != '':
                itemlist.append(
                    Item(channel=__channel__,
                         action="findvid_serie",
                         title="[COLOR azure]" + scrapedtitle + " (" + lang_title + ")" + "[/COLOR]",
                         url=item.url,
                         thumbnail=item.thumbnail,
                         extra=data,
                         fulltitle=item.title,
                         show=item.title))

    return itemlist


def findvid_serie(item):
    logger.info("pelisalacarta.streamblog findvideos")

    ## Descarga la página
    data = item.extra

    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist
