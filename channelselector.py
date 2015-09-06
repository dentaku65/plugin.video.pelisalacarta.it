# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "channelselector"

def getmainlist(preferred_thumb=""):
    logger.info("channelselector.getmainlist")
    itemlist = []

    # Obtiene el idioma, y el literal
    idioma = config.get_setting("languagefilter")
    logger.info("channelselector.getmainlist idioma=%s" % idioma)
    langlistv = [config.get_localized_string(30025),config.get_localized_string(30026),config.get_localized_string(30027),config.get_localized_string(30028),config.get_localized_string(30029)]
    try:
        idiomav = langlistv[int(idioma)]
    except:
        idiomav = langlistv[0]

    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30118) , channel="channelselector" , action="channeltypes", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales.png") ) )
    itemlist.append( Item(title=config.get_localized_string(30103) , channel="buscador" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_buscar.png")) )
    itemlist.append( Item(title=config.get_localized_string(30130) , channel="novedades" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_novedades.png") ) )
    #if config.is_xbmc(): itemlist.append( Item(title=config.get_localized_string(30128) , channel="trailertools" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_trailers.png")) )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_favoritos.png")) )
    itemlist.append( Item(title=config.get_localized_string(30131) , channel="wiideoteca" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_biblioteca.png")) )
    if config.get_platform()=="rss":itemlist.append( Item(title="pyLOAD (Beta)" , channel="pyload" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"pyload.png")) )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_descargas.png")) )

    if "xbmceden" in config.get_platform():
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_configuracion.png"), folder=False) )
    else:
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_configuracion.png")) )

    #if config.get_setting("fileniumpremium")=="true":
    #	itemlist.append( Item(title="Torrents (Filenium)" , channel="descargasfilenium" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"torrents.png")) )

    #if config.get_library_support():
    if config.get_platform()!="rss": itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_ayuda.png")) )
    return itemlist

# TODO: (3.1) Pasar el código específico de XBMC al laucher
def mainlist(params,url,category):
    logger.info("channelselector.mainlist")

    # Verifica actualizaciones solo en el primer nivel
    if config.get_platform()!="boxee":
        try:
            from core import updater
        except ImportError:
            logger.info("channelselector.mainlist No disponible modulo actualizaciones")
        else:
            if config.get_setting("updatecheck2") == "true":
                logger.info("channelselector.mainlist Verificar actualizaciones activado")
                try:
                    updater.checkforupdates()
                except:
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    dialog.ok("No se puede conectar","No ha sido posible comprobar","si hay actualizaciones")
                    logger.info("channelselector.mainlist Fallo al verificar la actualización")
                    pass
            else:
                logger.info("channelselector.mainlist Verificar actualizaciones desactivado")

    itemlist = getmainlist()
    for elemento in itemlist:
        logger.info("channelselector.mainlist item="+elemento.title)
        addfolder(elemento.title , elemento.channel , elemento.action , thumbnail=elemento.thumbnail, folder=elemento.folder)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def getchanneltypes(preferred_thumb=""):
    logger.info("channelselector getchanneltypes")
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_todos")))
    itemlist.append( Item( title=config.get_localized_string(30122) , channel="channelselector" , action="listchannels" , category="F"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_peliculas")))
    itemlist.append( Item( title=config.get_localized_string(30123) , channel="channelselector" , action="listchannels" , category="S"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_series")))
    itemlist.append( Item( title=config.get_localized_string(30124) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_anime")))
    itemlist.append( Item( title=config.get_localized_string(30125) , channel="channelselector" , action="listchannels" , category="D"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_documentales")))
    itemlist.append( Item( title=config.get_localized_string(30136) , channel="channelselector" , action="listchannels" , category="VOS" , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_vos")))
    #itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="M"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_musica")))
    itemlist.append( Item( title="Bittorrent" , channel="channelselector" , action="listchannels" , category="T"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_torrent")))
    itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="L"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_latino")))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="X"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_adultos")))
    #itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="G"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_servidores")))
    #itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW" , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"novedades")))
    return itemlist
    
def channeltypes(params,url,category):
    logger.info("channelselector.mainlist channeltypes")

    lista = getchanneltypes()
    for item in lista:
        addfolder(item.title,item.channel,item.action,item.category,item.thumbnail,item.thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def listchannels(params,url,category):
    logger.info("channelselector.listchannels")

    lista = filterchannels(category)
    for channel in lista:
        if channel.type=="xbmc" or channel.type=="generic":
            if channel.channel=="personal":
                thumbnail=config.get_setting("personalchannellogo")
            elif channel.channel=="personal2":
                thumbnail=config.get_setting("personalchannellogo2")
            elif channel.channel=="personal3":
                thumbnail=config.get_setting("personalchannellogo3")
            elif channel.channel=="personal4":
                thumbnail=config.get_setting("personalchannellogo4")
            elif channel.channel=="personal5":
                thumbnail=config.get_setting("personalchannellogo5")
            else:
                thumbnail=channel.thumbnail
                if thumbnail == "":
                    thumbnail=urlparse.urljoin(get_thumbnail_path(),channel.channel+".png")
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel, thumbnail = thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def filterchannels(category,preferred_thumb=""):
    returnlist = []

    if category=="NEW":
        channelslist = channels_history_list()
        for channel in channelslist:
            channel.thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versión original subtitulada").replace("F","Películas").replace("S","Series").replace("D","Documentales").replace("A","Anime").replace(",",", ")
            returnlist.append(channel)
    else:
        try:
            idioma = config.get_setting("languagefilter")
            logger.info("channelselector.filterchannels idioma=%s" % idioma)
            langlistv = ["","ES","EN","IT","PT"]
            idiomav = langlistv[int(idioma)]
            logger.info("channelselector.filterchannels idiomav=%s" % idiomav)
        except:
            idiomav=""

        channelslist = channels_list()
    
        for channel in channelslist:
            # Pasa si no ha elegido "todos" y no está en la categoría elegida
            if category<>"*" and category not in channel.category:
                #logger.info(channel[0]+" no entra por tipo #"+channel[4]+"#, el usuario ha elegido #"+category+"#")
                continue
            # Pasa si no ha elegido "todos" y no está en el idioma elegido
            if channel.language<>"" and idiomav<>"" and idiomav not in channel.language:
                #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
                continue
            if channel.thumbnail == "":
                channel.thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versión original subtitulada").replace("F","Películas").replace("S","Series").replace("D","Documentales").replace("A","Anime").replace(",",", ")
            returnlist.append(channel)

    return returnlist

def channels_history_list():
    itemlist = []
    return itemlist

def channels_list():
    itemlist = []
    
    # En duda
    #itemlist.append( Item( title="Descarga Cine Clásico" , channel="descargacineclasico"  , language="ES"    , category="F,S"     , type="generic"  ))
    #itemlist.append( Item( title="Asia-Team"             , channel="asiateam"             , language="ES"    , category="F,S"     , type="generic"  ))
    #itemlist.append( Item( title="Buena Isla"            , channel="buenaisla"            , language="ES"    , category="A,VOS"       , type="generic"  ))
    #itemlist.append( Item( title="[COLOR yellow][REV][/COLOR] [COLOR azure]Reviewed code[/COLOR] [COLOR orange][NEW][/COLOR] [COLOR azure]New code[/COLOR] [COLOR red][DEV][/COLOR] [COLOR azure]Dev code[/COLOR]"       , channel="info_ita"           , language="IT"    , category="F,S,A,VOS"   , type="generic"     ,thumbnail="http://icons.tipografias.org/plog-content/images/iconos-de-moviles/iconos-de-filmes/movie_info.png"  ))
    itemlist.append( Item( viewmode="movie", title="Inserisci un URL"         , channel="tengourl"   , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname") , channel="personal" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel2")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname2") , channel="personal2" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel3")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname3") , channel="personal3" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel4")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname4") , channel="personal4" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel5")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname5") , channel="personal5" , language="" , category="" , type="generic"  ))
    itemlist.append( Item( title="Animeflv"                , channel="animeflv"           , language="ES" , category="A"       , type="generic"  ))
    itemlist.append( Item( title="Animeid"                 , channel="animeid"            , language="ES" , category="A"       , type="generic"  ))
    itemlist.append( Item( title="Aquitorrent"             , channel="aquitorrent"        , language="ES" , category="T,F,S,D,A,VOS"       , type="generic" ))
    itemlist.append( Item( title="Bajui"                   , channel="bajui"              , language="ES" , category="F,S,D,VOS" , type="generic"    ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Beeg"               , channel="beeg"            , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Bricocine"               , channel="bricocine"          , language="ES"   , category="T,F,S" , type="generic" , thumbnail="http://s6.postimg.org/9u8m1ep8x/bricocine.jpg"    ))
    #itemlist.append( Item( title="Cineblog01 (IT)"         , channel="cineblog01"         , language="IT" , category="F,S,A,VOS"   , type="generic"  ))
    itemlist.append( Item( title="Cinehanwer"              , channel="cinehanwer"         , language="ES" , category="F"   , type="generic"  ))
    itemlist.append( Item( title="Cinemaxx (RO)"           , channel="cinemax_rs"         , language="RU" , category="F"   , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Cinetemagay" , channel="cinetemagay"          , language="ES"    , category="X,F" , type="generic"    )) # sdfasd 15/4/2012
    itemlist.append( Item( title="Cinetux"                 , channel="cinetux"            , language="ES" , category="L,F" , type="generic"  ))# jesus 16/7/2012
    itemlist.append( Item( title="Cuevana"                 , channel="cuevana"            , language="ES" , category="F"     , type="generic"  ))
    itemlist.append( Item( title="Cuelgame"                , channel="cuelgame"           , language="ES" , category="T,F,A,D,VOS" , type="generic"  ))
    itemlist.append( Item( title="Discoverymx"             , channel="discoverymx"        , language="ES" , category="L,D"       , type="generic"  ))
    itemlist.append( Item( title="Divxatope"               , channel="divxatope"          , language="ES" , category="T,F,S"       , type="generic"  ))
    itemlist.append( Item( title="DocumaniaTV"             , channel="documaniatv"        , language="ES" , category="D"       , type="generic"  ))
    itemlist.append( Item( title="El señor del anillo"     , channel="elsenordelanillo"   , language="ES" , category="L,F"       , type="xbmc"  ))
    itemlist.append( Item( title="Elite Torrent"           , channel="elitetorrent"       , language="ES" , category="T,F,S,D"       , type="xbmc"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Filesmonster Catalogue"    , channel="filesmonster_catalogue"           , language="es"    , category="X,F"   , type="generic"     ))
    #itemlist.append( Item( title="Film per tutti (IT)"     , channel="filmpertutti"       , language="IT" , category="F,S,A"   , type="generic"     ))
    #itemlist.append( Item( title="Film Senza Limiti (IT)"  , channel="filmsenzalimiti"    , language="IT" , category="F,S"       , type="generic"     ))
    itemlist.append( Item( title="Gnula"                   , channel="gnula"              , language="ES" , category="L,F" , type="generic"  )) # vcalvo 15/12/2011
    itemlist.append( Item( title="HDFull"                  , channel="hdfull"             , language="ES" , category="F,S" , type="generic"  )) # jesus 14/12/2014
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Hentai FLV"    , channel="hentaiflv"           , language="es"    , category="X,A"   , type="generic"     ))
    #itemlist.append( Item( title="ItaliaFilms.tv (IT)"     , channel="italiafilm"         , language="IT" , category="A"   , type="generic"     ))
    itemlist.append( Item( title="JKanime"                 , channel="jkanime"            , language="ES" , category="A" , type="generic"  )) # jesus 15/10/2012
    itemlist.append( Item( title="La Guarida valencianista", channel="guaridavalencianista",language="ES" , category="D"       , type="generic"  ))
    itemlist.append( Item( title="Mega HD"                 , channel="megahd"             , language="ES" , category="F,S,D,A"       , type="generic"  ))
    itemlist.append( Item( title="Megaforo"                , channel="megaforo"           , language="ES" , category="F,S,D"       , type="generic"  ))
    itemlist.append( Item( title="Megaspain"               , channel="megaspain"          , language="ES" , category="F,S,D"       , type="generic"  ))
    itemlist.append( Item( title="Mejor Torrent"           , channel="mejortorrent"       , language="ES" , category="T,F,S,D"       , type="xbmc"  ))
    itemlist.append( Item( title="Mirapeli"                , channel="mirapeli"           , language="ES" , category="F"       , type="generic"  ))
    itemlist.append( Item( title="Mitube"                  , channel="mitube"             , language="ES" , category=""       , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="MocosoftX", channel="mocosoftx"            , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Newpct"                  , channel="newpct"             , language="ES" , category="F,S,D,A"       , type="generic"  )) # jesus 08/03/2013
    itemlist.append( Item( title="Newpct1"                 , channel="newpct1"            , language="ES" , category="F,S,A"       , type="generic"  )) # jesus 08/03/2013
    itemlist.append( Item( title="Oranline"                , channel="oranline"           , language="ES" , category="L,F,D"        , type="generic" ))# jesus 16/7/2012
    itemlist.append( Item( title="Peliculasaudiolatino"    , channel="peliculasaudiolatino",language="ES" , category="L,F"       , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="PeliculasEroticas" , channel="peliculaseroticas"    , language="ES" , category="X,F" , type="xbmc"  ))
    itemlist.append( Item( title="PeliculasDK"             , channel="peliculasdk"        , language="ES" , category="F" , type="generic" , thumbnail="http://s29.postimg.org/wzw749oon/pldklog.jpg"  )) 
    itemlist.append( Item( title="PeliculasMX"             , channel="peliculasmx"        , language="ES" , category="L,F"       , type="generic"  ))
    itemlist.append( Item( title="Pelis24"                 , channel="pelis24"            , language="ES" , category="L,F,VOS"        , type="generic"  ))
    itemlist.append( Item( title="Pelisadicto"             , channel="pelisadicto"        , language="ES" , category="F,L"        , type="generic"  ))
    itemlist.append( Item( title="Peliserie"               , channel="peliserie"          , language="ES" , category="F,S", type="generic"))
    itemlist.append( Item( title="PelisPekes"              , channel="pelispekes"         , language="ES" , category="F"        , type="generic"  ))
    #itemlist.append( Item( title="Pirate Streaming (IT)"   , channel="piratestreaming"    , language="IT" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="Pordede"                 , channel="pordede"            , language="ES" , category="F,S" , type="generic"    )) # jesus 16/6/2014
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="PornoActricesX"            , channel="pornoactricesx"          , language="ES" , category="X,F" , type="generic"    ))
    if config.get_setting("enableadultmode") == "true": itemlist.append(Item( title="PornHub", channel="pornhub", language="ES" , category="X,F" , type="generic" ,thumbnail="http://s22.postimg.org/5lzcocfqp/pornhub_logo.jpg" )) # superberny 19/01/2015
    itemlist.append( Item( title="Quebajamos"              , channel="quebajamos"         , language="ES" , category="F,S,D" , type="generic"  )) # jesus 16/06/2014
    itemlist.append( Item( title="Quiero Dibujos Animados" , channel="quierodibujosanimados",language="ES", category="S" , type="generic"  )) # jesus 12/11/2012
    itemlist.append( Item( title="Reyanime"                , channel="reyanime"           , language="ES" , category="A"          , type="generic"  ))
    #itemlist.append( Item( title="Robinfilm (IT)"          , channel="robinfilm"          , language="IT" , category="F"          , type="generic"  )) # jesus 16/05/2011
    itemlist.append( Item( title="Seriesadicto"            , channel="seriesadicto"       , language="ES" , category="S,A"          , type="generic" ))
    itemlist.append( Item( title="Seriesblanco"            , channel="seriesblanco"       , language="ES" , category="S,VOS"          , type="generic" ))
    itemlist.append( Item( title="Seriesdanko"             , channel="seriesdanko"        , language="ES" , category="S,VOS"          , type="generic" ))
    itemlist.append( Item( title="Seriesflv"               , channel="seriesflv"          , language="ES" , category="S,A"      , type="generic"  ))
    itemlist.append( Item( title="Series.ly"               , channel="seriesly"           , language="ES" , category="F,S,A,VOS"        , type="generic"  ))
    itemlist.append( Item( title="SeriesMu"                , channel="seriesmu"           , language="ES" , category="F,S,A,VOS"   , type="generic",  thumbnail="http://s17.postimg.org/jcasctj0v/smlogo.jpg"  ))
    itemlist.append( Item( title="Seriesyonkis"            , channel="seriesyonkis"       , language="ES" , category="S,A,VOS"        , type="generic" , extra="Series" ))
    #itemlist.append( Item( title="Serie TV Sub ITA"        , channel="serietvsubita"      , language="IT" , category="S"        , type="generic" , extra="Series" ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Serviporno", channel="serviporno"          , language="ES" , category="X,F" , type="generic"    ))
    itemlist.append( Item( title="Shurweb"                 , channel="shurweb"            , language="ES" , category="F,S,D,A" , type="generic"    ))
    itemlist.append( Item( title="Sinluces"                , channel="sinluces"           , language="ES" , category="F" , type="generic" , thumbnail="http://s14.postimg.org/cszkmr7a9/sinluceslogo.jpg"   ))
    #itemlist.append( Item( title="Somosmovies"             , channel="somosmovies"        , language="ES" , category="F,S"    , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Submit Your Flicks", channel="submityouflicks" , language="ES" , category="X,F" , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Submit Your Tapes", channel="submityourtapes" , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Teledocumentales"        , channel="teledocumentales"   , language="ES" , category="D"          , type="generic" )) # mrfloffy 19/10/2011
    itemlist.append( Item( title="Trailers ecartelera"     , channel="ecarteleratrailers" , language="ES" , category="F"       , type="generic"  ))
    itemlist.append( Item( title="Torrentestrenos"         , channel="torrentestrenos"    , language="ES" , category="T,F,S,D"          , type="generic" , thumbnail="http://s6.postimg.org/lq96iccb5/torrentestrenos.jpg" ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="tubehentai" , channel="tubehentai" , language="ES" , category="X,F" , type="xbmc"  ))
    itemlist.append( Item( title="Tus Novelas"             , channel="tusnovelas"         , language="ES" , category="S"        , type="generic" ))# jesus 3/7/2012
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="tuporno.tv" , channel="tupornotv" , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Txibitsoft"              , channel="txibitsoft"         , language="ES" , category="T,S,F"        , type="generic", thumbnail="http://s27.postimg.org/hx5ohryxf/tblogo.jpg" ))# neno 17/02/2015
    itemlist.append( Item( title="Unsoloclic"              , channel="unsoloclic"         , language="ES" , category="F,S" , type="generic"  ))# jesus 3/7/2012
    itemlist.append( Item( title="VePelis"                 , channel="vepelis"            , language="ES" , category="L,F" , type="generic"  ))# jjchao 28/05/2013
    itemlist.append( Item( title="Ver Telenovelas"         , channel="vertelenovelas"     , language="ES" , category="S" , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="xhamster"           , channel="xhamster"             , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Yaske.net"               , channel="yaske"              , language="ES" , category="L,F"       , type="generic"  ))
    itemlist.append( Item( title="YouAnime HD"             , channel="youanimehd"         , language="ES" , category="A"       , type="generic"  ))
    itemlist.append( Item( title="V Series"                , channel="vseries"            , language="ES" , category="F,S"       , type="generic"  ))
    itemlist.append( Item( title="Zentorrents"             , channel="zentorrents"        , language="ES" , category="T,F,S" , type="xbmc" , thumbnail="http://s6.postimg.org/9zv90yjip/zentorrentlogo.jpg"  ))
    itemlist.append( Item( title="Zpeliculas"              , channel="zpeliculas"         , language="ES" , category="F"       , type="generic"  ))
########## Start ITALIAN CHANNELS ###########
    #itemlist.append( Item( title="[COLOR cyan]-- ITA Channels Info --[/COLOR]"       , channel="info_ita"           , language="IT"    , category="F,S,A,VOS"   , type="generic"  ))
    itemlist.append( Item( title="[COLOR yellow][REV][/COLOR] Cineblog01 (IT)"       , channel="cineblog01"           , language="IT"    , category="F,S,A,VOS"   , type="generic"  ))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Altadefinizione01 (IT)"        , channel="altadefinizione01"       , language="IT"    , category="F,S,A"       , type="generic"     ,thumbnail="http://www.altadefinizione01.com/wp-content/uploads/2015/04/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Tantifilm (IT)"        , channel="tantifilm"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://www.tantifilm.net/wp-content/themes/smashingMultiMediaBrown/images/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Streaming01 (IT)"        , channel="streaming01"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://streaming01.com/templates/movie-groovie/images/logo.png"))
    itemlist.append( Item( title="[COLOR yellow][REV][/COLOR] Film per tutti (IT)"      , channel="filmpertutti"           , language="IT"    , category="F,S,A"   , type="generic"     ))
    itemlist.append( Item( title="[COLOR yellow][REV][/COLOR] Film Senza Limiti (IT)"        , channel="filmsenzalimiti"       , language="IT"    , category="F"       , type="generic"     ))
    itemlist.append( Item( title="[COLOR yellow][REV][/COLOR] Pirate Streaming (IT)" , channel="piratestreaming"      , language="IT" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Guardaserie (IT)"          , channel="guardaserie"         , language="IT" , category="S"        , type="generic" , extra="Series" ,thumbnail="http://www.guardaserie.net/wp-content/themes/guardaserie/images/new_logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Fastvideotv (IT)"        , channel="fastvideotv"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://www.fastvideo.tv/wp-content/uploads/2015/07/fastvideo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] AnimeSubIta (IT)"   , channel="animesubita"           , language="IT"    , category="A"   , type="generic" ,thumbnail="http://i.imgur.com/eSAxd4p.png" ))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Asian Sub-Ita (IT)"      , channel="asiansubita"           , language="IT"    , category="F,S,A,VOS"   , type="generic"  ,thumbnail="http://asiansubita.altervista.org/wp-content/uploads/2014/11/asiansubita1.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Casa-Cinema (IT)"        , channel="casacinema"       , language="IT"    , category="F,S"       , type="generic"     ,thumbnail="http://casa-cinema.net/wp-content/themes/casacinema/images/logo-Black.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] FilmStream pw (IT)"        , channel="filmstreampw"       , language="IT"    , category="F,S"       , type="generic"     ,thumbnail="http://filmstream.pw/templates/tvspirit/images/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Pianetastreaming (IT)"        , channel="pianetastreaming"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://www.pianetastreaming.net/wp-content/uploads/2014/03/PianetaStreaming.png"))
    itemlist.append( Item( title="[COLOR yellow][REV][/COLOR] ItaliaFilms.tv (IT)"      , channel="italiafilm"           , language="IT"    , category="F,S,A"   , type="generic"     ))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Italian-Stream (IT)"        , channel="italianstream"       , language="IT"    , category="F,S"       , type="generic"     ,thumbnail="http://italian-stream.tv/wp-content/uploads/2014/03/logo11.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Film-stream.org (IT)"        , channel="filmstream"       , language="IT"    , category="F,S"       , type="generic"     ,thumbnail="http://i.imgur.com/kSIfR3l.jpg"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Streamblog (IT)"        , channel="streamblog"       , language="IT"    , category="F,S,A"       , type="generic"     ,thumbnail="http://www.streamblog.tv/templates/Smotrikino/images/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Guardarefilm (IT)"        , channel="guardarefilm"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://www.guardarefilm.tv/templates/tvSpirit1/images/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Liberoita (IT)"        , channel="liberoita"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://liberoita.com/wp-content/themes/sito/images/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Cinemagratis (IT)"        , channel="cinemagratis"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://cinemagratis.org/wp-content/uploads/2015/05/cinemagratisimmagine.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] FilmSubito (IT)"          , channel="filmsubitotv"           , language="IT"    , category="F,S,A"   , type="generic"  ,thumbnail="http://i.imgur.com/4x1V7dZ.png" ))
    #itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] HubberFilm (IT)"        , channel="hubberfilm"       , language="IT"    , category="F,S"       , type="generic"     ,thumbnail="https://lh3.googleusercontent.com/-1GctnWIK15c/Ut50orGAIfI/AAAAAAAAACc/OATQdeKNoPg/s630-fcrop64=1,00000000ffffe786/1148930_614844365216006_1783180772_n.jpg"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Film Gratis cc (IT)"        , channel="filmgratiscc"       , language="IT"    , category="F"       , type="generic"     ,thumbnail="http://filmgratis.cc/wp-content/uploads/2014/06/logofilmgratis.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Cineblogfm (IT)"        , channel="cineblogfm"       , language="IT"    , category="F,S"       , type="generic"     ,thumbnail="http://www.cineblog01.fm/templates/KinoView/images/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Eurostreaming (IT)"        , channel="eurostreaming"       , language="IT"    , category="F,S"       , type="generic"     ,thumbnail="http://eurostreaming.tv/wp-content/uploads/2014/03/logo2.png"))
    itemlist.append( Item( title="[COLOR yellow][REV][/COLOR] Serie TV Sub ITA (IT)"          , channel="serietvsubita"         , language="IT" , category="S"        , type="generic" , extra="Series" ,thumbnail="https://i.imgur.com/jufYUPM.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Italiaserie (IT)"          , channel="italiaserie"         , language="IT" , category="S"        , type="generic" , extra="Series" ,thumbnail="http://www.italiaserie.com/wp-content/uploads/2015/03/logo.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] ItaFilm.tv (IT)"      , channel="itafilmtv"           , language="IT"    , category="F,S,A,D"   , type="generic"  ,thumbnail="http://www.itafilm.tv/templates/monsterfilm/images/logo.png"   ))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] Liberostreaming (IT)"          , channel="liberostreaming"         , language="IT" , category="F,S,A"        , type="generic", thumbnail="http://www.liberostreaming.org/wp-content/uploads/2015/01/cooltext1859870362.png"))
    itemlist.append( Item( title="[COLOR orange][NEW][/COLOR] PortaleHD (IT)"          , channel="portalehd"         , language="IT" , category="F,S,A"        , type="generic", thumbnail="http://www.portalehd.net/wp-content/uploads/2015/07/logo.png"))
    itemlist.append( Item( title="[COLOR red][DEV][/COLOR] Altadefinizione.click (IT)"          , channel="altadefinizioneclick"         , language="IT" , category="F,S,A"        , type="generic", thumbnail="http://i.imgur.com/FSHW6Zx.png"))
    itemlist.append( Item( title="[COLOR red][DEV][/COLOR] ItaStreaming (IT)"          , channel="itastreaming"         , language="IT" , category="F,S,A"        , type="generic", thumbnail="http://itastreaming.co/wp-content/uploads/2015/08/logo.png"))
    #itemlist.append( Item( title="[COLOR red][DEV][/COLOR] Ildocumento (IT)"          , channel="ildocumento"         , language="IT" , category="F,D"        , type="generic" , extra="Series" ,thumbnail="http://ildocumento.it/ildocumento-social.jpg"))
    itemlist.append( Item( title="[COLOR red][DEV][/COLOR] Documentaristreaming (IT)"          , channel="documentaristreaming"         , language="IT" , category="F,D"        , type="generic" , extra="Series" ,thumbnail="http://tvstreamingonline.org/images/IMG/documentari%20streaming.jpg"))
    itemlist.append( Item( title="[COLOR red][DEV][/COLOR] Documoo (IT)"          , channel="documoo"         , language="IT" , category="F,D"        , type="generic" , extra="Series" ,thumbnail="http://www.documoo.tv/wp-content/uploads/logo_documoo.jpg"))
##### End ITALIAN CHANNELS ######

    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname="",thumbnail="",folder=True):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=folder)

def get_thumbnail_path(preferred_thumb=""):

    WEB_PATH = ""
    
    if preferred_thumb=="":
        thumbnail_type = config.get_setting("thumbnail_type")
        if thumbnail_type=="":
            thumbnail_type="2"
        
        if thumbnail_type=="0":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/posters/"
        elif thumbnail_type=="1":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/banners/"
        elif thumbnail_type=="2":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/squares/"
    else:
        WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/"+preferred_thumb+"/"

    return WEB_PATH
