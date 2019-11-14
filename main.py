# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
import json
from parseutils import *
from stats import *
import xbmcplugin,xbmcgui,xbmcaddon

_UserAgent_ = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
addon = xbmcaddon.Addon('plugin.video.tvnitricka.sk')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.tvnitricka.sk')
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

#Nacteni informaci o doplnku
__addon__      = xbmcaddon.Addon()
__addonname__  = __addon__.getAddonInfo('name')
__addonid__    = __addon__.getAddonInfo('id')
__cwd__        = __addon__.getAddonInfo('path').decode("utf-8")
__language__   = __addon__.getLocalizedString

def OBSAH():
    addDir('Komunálna politika','https://tvnitricka.sk/relacie/komunalne-volby-2018/',6,icon,1)
    addDir('Spravodajstvo','https://tvnitricka.sk/relacie/spravodajstvo/',6,icon,1)
    addDir('Nitriansky hlásnik','https://tvnitricka.sk/relacie/magazin/',6,icon,1)
    addDir('Magazín / Objektívom TV Nitrička','https://tvnitricka.sk/relacie/magazin/',6,icon,1)
    addDir('Relácie','https://tvnitricka.sk/relacie/magazin/',6,icon,1)
    addDir('Reklama','https://tvnitricka.sk/relacie/reklama/',6,icon,1)
    addDir('Súťaž a vyhraj','https://tvnitricka.sk/relacie/sutaz-a-vyhraj/',6,icon,1)
    addDir('Archív','https://tvnitricka.sk/relacie/archiv/',6,icon,1)
    addDir('Som redaktor','https://tvnitricka.sk/relacie/som-redaktor/',6,icon,1)

def EPISODES(url,page):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    for (url, other, title) in re.findall(r'<a href="(http\S*?)" class="vid box ">(.*?)<h3>(.*?)<\/h3>', httpdata, re.DOTALL):
        thumb = re.findall(r'url\(\'(\S+?)\'\)"',other)[0]
        date = re.findall(r'<div class="date">(.+?)<\/div>',other)[0]
        date = date.split(',')[0]   
        title = date + ': ' + title      
        addDir(title,url,3,thumb,1)
    next=re.findall(r'<a class="next page-numbers" href="(\S*?)">Ďalšie<\/a>',httpdata)
    if next:
        addDir('Ďalšie',next[0],6,icon,1)

def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    desc=''
    thumb=''
    url=re.findall(r'source: \'(.*?)\',',httpdata)[0]
    addLink('video',url,thumb,desc)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

def addLink(name,url,iconimage,popis):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": popis} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

params=get_params()
url=None
name=None
thumb=None
mode=None
page=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        page=int(params["page"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Page: "+str(page)

if mode==None or url==None or len(url)<1:
        STATS("OBSAH", "Function")
        OBSAH()

elif mode==6:
        STATS("EPISODES", "Function")
        EPISODES(url,page)

elif mode==3:
        STATS("VIDEOLINK", "Function")
        VIDEOLINK(url,page)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
