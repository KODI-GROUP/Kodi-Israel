#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import shutil
import random
import socket
import urllib
import urllib2
import datetime
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import xbmc
import time
from PlayListRipper import PlayListRipper
from PlayListSearcher import PlayListSearcher

#addon = xbmcaddon.Addon()
#addonID = addon.getAddonInfo('id')
addonID = 'plugin.video.spotitube'
addon = xbmcaddon.Addon(id=addonID)
pluginhandle = int(sys.argv[1])
socket.setdefaulttimeout(30)
opener = urllib2.build_opener()
xbox = xbmc.getCondVisibility("System.Platform.xbox")
region = xbmc.getLanguage(xbmc.ISO_639_1, region=True).split("-")[1]
icon = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
pl_file = xbmc.translatePath(addon.getSetting("playlistFile"))
addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
cacheDir = xbmc.translatePath(addon.getSetting("cacheDir"))
blacklist = addon.getSetting("blacklist").split(',')
infoEnabled = addon.getSetting("showInfo") == "true"
infoType = addon.getSetting("infoType")
infoDelay = int(addon.getSetting("infoDelay"))
infoDuration = int(addon.getSetting("infoDuration"))
forceView = addon.getSetting("forceView") == "true"
viewIDVideos = str(addon.getSetting("viewIDVideos"))
viewIDPlaylists = str(addon.getSetting("viewIDPlaylists"))
viewIDGenres = str(addon.getSetting("viewIDGenres"))
itunesShowSubGenres = addon.getSetting("itunesShowSubGenres") == "true"
itunesForceCountry = addon.getSetting("itunesForceCountry") == "true"
itunesCountry = addon.getSetting("itunesCountry")
spotifyForceCountry = addon.getSetting("spotifyForceCountry") == "true"
spotifyCountry = addon.getSetting("spotifyCountry")
userAgent = "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0"
opener.addheaders = [('User-Agent', userAgent)]
urlMainBB = "http://www.billboard.com"
urlMainOC = "http://www.officialcharts.com"
urlMainBP = "http://www.beatport.com"
urlMainGLZ = "http://www.glgltz.co.il"
googleImgUrl = 'http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='
if itunesForceCountry and itunesCountry:
    iTunesRegion = itunesCountry
else:
    iTunesRegion = region
if spotifyForceCountry and spotifyCountry:
    spotifyRegion = spotifyCountry
else:
    spotifyRegion = region

if not os.path.isdir(addonUserDataFolder):
    os.mkdir(addonUserDataFolder)
if not cacheDir.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')) and not os.path.isdir(cacheDir):
    os.mkdir(cacheDir)


def index():	
	addDir("Beatport", "", "bpMain", "")
	addDir("Billboard", "", "billboardMain", "")
	addDir(translation(30043), "", "itunesMain", "")
	addDir("Official Charts Company (UK)", "", "ocMain", "")
	addDir(translation(30044), "", "spotifyMain", "")	
	addDir('גלגל"צ', "", "GalgalatzMain", "http://www.exioma.co.il/wp-content/uploads/2013/11/galgalaz.png")
	addDir('1FM', "", "OneFmMain", "http://www.onefmonline.com/images/logo.jpg")
	addDir('Disi', "", "DisiMain", "http://creatives.co.il/upload/files/1ff4b1bc493d86739b256ec6d274b2e4.png")
	addDir('Youtube Playlists', "", "YotubePlayListMain", "")
	xbmcplugin.endOfDirectory(pluginhandle)	
	
def YotubePlayListMain():
	addDir("Search Playlist", "", "YoutubeSearchPlaylist", "")
	addDir("My Playlists", "", "YotubeMyPlayListMain", "")
	xbmcplugin.endOfDirectory(pluginhandle)	
	
def YoutubeSearchPlaylist():
	searcher = PlayListSearcher()    	
	output = searcher.start_search()
	data = json.loads(output.decode('utf-8'))
	for playlist in data['playlists']:
		addAutoPlayDirYT(playlist['name'], playlist['url'], "listYoutubePlayList", playlist['img'], "", "browse")		
	xbmcplugin.endOfDirectory(pluginhandle)	

def YotubeMyPlayListMain():
	fh = open(pl_file, 'r')	
	data = json.loads(fh.read().decode('utf-8'))
	for playlist in data['playlists']:
		addAutoPlayDirYT(playlist['name'], playlist['url'], "listYoutubePlayList", playlist['img'], "", "browse")		
	fh.close()	
	xbmcplugin.endOfDirectory(pluginhandle)
	
def ripYoutubePlaylist(playlist_id):	
	ripper = PlayListRipper()    	
	#if not exist in cache than rip & save		
	data = ripper.getRipped("youtube_playlist_"+playlist_id, cacheDir, 30)
	if (data is None):				
		ripper.rip(playlist_id)
		data = ripper.save("youtube_playlist_"+playlist_id, cacheDir)
	return data
	
def add_playlist_to_fav_file(playlist_id, title , image):    	
    img_url = 'https://i.ytimg.com/vi/'+image+'/hqdefault.jpg'
    fh = open(pl_file, 'a+')	
    data = json.loads(fh.read().decode('utf-8'))
    new_entry={"url":playlist_id, "name":title, "img":img_url}
    dialog = xbmcgui.Dialog()				
    if new_entry not in data['playlists']:
		data['playlists'].append(new_entry)    
		with open(pl_file, 'w') as outfile:
			json.dump(data, outfile)       
		dialog.ok("Youtube Music", "Playlist added to Favourites file")				
    else:
		dialog.ok("Youtube Music", "Playlist Already exists in Favourites file")    
	
def listYoutubePlayList(type, url, limit, name="", img=""):
	pos = 1		
	playlist_id=url	
	if type=="add":
		add_playlist_to_fav_file(url, name , img)
		return
	if type=="remove":
		fh = open(pl_file, 'r')	
		data = json.loads(fh.read().decode('utf-8'))
		for playlist in data['playlists']:
			if playlist.get('url') == playlist_id:
				dialog = xbmcgui.Dialog()				
				del data['playlists'][data['playlists'].index(playlist)]
				fh = open(pl_file,"w")
				fh.write(json.dumps(data))
				fh.close()
				dialog.ok("Youtube Music", "Playlist Removed from Favourites file")				
				xbmc.executebuiltin("Container.Refresh")
				break
		return		
	if type=="play":
		musicVideos = []
		xbmc_playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		xbmc_playlist.clear()	    
	data = json.loads(ripYoutubePlaylist(playlist_id))	
	for item in data['items']:
		if type=="browse":	
			addLinkId(item['title'], item['video_id'], "playYTById", item['img'])
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?videoid="+item['video_id']+"&mode=autoPlayYTById"
			else:
				url = "plugin://"+addonID+"/?videoid="+item['video_id']+"&mode=autoPlayYTById"
			musicVideos.append([item['title'], url, item['img']])
			if limit and int(limit)==pos:
				break
			pos+=1				
	if type=="browse":		
		xbmcplugin.endOfDirectory(pluginhandle)
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			xbmc_playlist.add(url, listitem)
		xbmc.Player().play(xbmc_playlist)		

def GalgalatzMain():
	addAutoPlayDirGlz("המצעד הבינלאומי", "http://www.glgltz.co.il/Shared/Ajax/GetTophitsByCategory.aspx?FolderId=1183&amp;lang=he", "listGalgalatzCharts", "http://www.glgltz.co.il/SIP_STORAGE/files/7/1647.jpg", "", "browse")	
	addAutoPlayDirGlz("המצעד הישראלי", "http://www.glgltz.co.il/Shared/Ajax/GetTophitsByCategory.aspx?FolderId=1182&amp;lang=he", "listGalgalatzCharts", "http://www.glgltz.co.il/SIP_STORAGE/files/6/1646.jpg", "", "browse")		
	addAutoPlayDirGlz("פלייליסט בינלאומי", "http://www.glgltz.co.il/1215-he/Galgalatz.aspx", "listGalgalatzPlaylist", "http://3.bp.blogspot.com/_bhUS7ZA74pc/S7PPvRLkueI/AAAAAAAABzw/lYSKxhj6beE/s1600/world-music.jpg", "", "browse")		
	addAutoPlayDirGlz("פלייליסט ישראלי", "http://www.glgltz.co.il/1213-he/Galgalatz.aspx", "listGalgalatzPlaylist", "http://3.bp.blogspot.com/_bhUS7ZA74pc/S7PPvRLkueI/AAAAAAAABzw/lYSKxhj6beE/s1600/world-music.jpg", "", "browse")		
	addAutoPlayDirGlz("פלייליסט מעורב", "", "listGalgalatzPlaylistMix", "http://3.bp.blogspot.com/_bhUS7ZA74pc/S7PPvRLkueI/AAAAAAAABzw/lYSKxhj6beE/s1600/world-music.jpg", "", "browse")		
	addAutoPlayDirGlz("מצעד שנות ה-80", "http://www.glgltz.co.il/1236-he/Galgalatz.aspx", "listGalgalatzDecadeChart80", "http://www.bawa.biz/bristol-entertainment-sports/sites/default/files/events/ilovethe80s.jpg", "", "browse")		
	addAutoPlayDirGlz("מצעד שנות ה-90", "http://www.glgltz.co.il/1236-he/Galgalatz.aspx", "listGalgalatzDecadeChart90", "https://origin.ih.constantcontact.com/fs145/1102250365124/img/615.jpg", "", "browse")		
	addAutoPlayDirGlz("מצעד שנות ה-2000", "http://www.glgltz.co.il/1236-he/Galgalatz.aspx", "listGalgalatzDecadeChart00", "http://8tracks.imgix.net/i/000/570/047/Ultimate2000s-4208.jpg?q=65&sharp=15&vib=10&fm=jpg&fit=crop&w=521&h=521", "", "browse")		
	addAutoPlayDirGlz('גלגל"צ live', "http://www.glgltz.co.il/Shared/Ajax/BroadcastMonitor.aspx", "PlayGalgalatzRadio", "http://www.glgltz.co.il/Sip_Storage/FILES/9/2099.jpg", "", "browse")		
	xbmcplugin.endOfDirectory(pluginhandle)
	
def OneFmMain():
	addAutoPlayDir("The Playlist", "http://www.onefmonline.com", "listOneFmPlaylist", "http://warnerboutique.com/wp-content/uploads/music-dance-hd-wallpaper-50267-hd-wallpapers-background-750x498.jpg", "", "browse")	
	addAutoPlayDir("Last Played", "http://www.onefmonline.com/common/Radio.aspx", "listOneFmLastPlayed", "http://www.desktopaper.com/wp-content/uploads/unusual-abstract-wallpaper-dance-digital-art-music.jpg", "", "browse")		
	addAutoPlayDir("Live", "http://www.onefmonline.com/common/Radio.aspx", "PlayOneFmRadio", "http://cdn.superbwallpapers.com/wallpapers/music/microphone-19151-1920x1080.jpg", "", "browse")			
	xbmcplugin.endOfDirectory(pluginhandle)
	
def DisiMain():
	addAutoPlayDir("פלייליסט", "http://www.disi.co.il", "listDisiPlaylist", "", "", "browse")	
	addAutoPlayDir("מצעד", "http://www.disi.co.il/best.php", "listDisiChart", "", "", "browse")			
	xbmcplugin.endOfDirectory(pluginhandle)

def spotifyMain():
    addDir(translation(30041), "http://api.tunigo.com/v3/space/toplists?region="+spotifyRegion+"&page=0&per_page=50&platform=web", "listSpotifyPlaylists", "")
    addDir(translation(30042), "http://api.tunigo.com/v3/space/featured-playlists?region="+spotifyRegion+"&page=0&per_page=50&dt="+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M").replace(":","%3A")+"%3A00&platform=web", "listSpotifyPlaylists", "")
    addDir(translation(30006), "http://api.tunigo.com/v3/space/genres?region="+spotifyRegion+"&per_page=1000&platform=web", "listSpotifyGenres", "")
    xbmcplugin.endOfDirectory(pluginhandle)


def ocMain():
    addAutoPlayDir("Official", urlMainOC+"/singles-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Sales", urlMainOC+"/singles-sales-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Downloads", urlMainOC+"/singles-download-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Streaming", urlMainOC+"/official-audio-streaming-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Classical", urlMainOC+"/official-classical-singles-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Rock & Metal", urlMainOC+"/rock-and-metal-singles-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Independent", urlMainOC+"/independent-singles-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Catalogue", urlMainOC+"/catalogue-singles-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("R&B", urlMainOC+"/r-and-b-singles-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Dance", urlMainOC+"/dance-singles-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Asian", urlMainOC+"/asian-chart/", "listOC", "", "", "browse")
    addAutoPlayDir("Scottish", urlMainOC+"/scottish-singles-chart/", "listOC", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def bpMain():
    addAutoPlayDir("All Genres", urlMainBP+"/top-100", "listBP", "", "", "browse")
    content = cache(urlMainBP, 30)
    match=re.compile('<span class="fl.+?">  <a href="http://www.beatport.com/genre/(.+?)">(.+?)<', re.DOTALL).findall(content)
    for genreID, title in match:
        title = cleanTitle(title)
        addAutoPlayDir(title, urlMainBP+"/genre/"+genreID+"/top-100", "listBP", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def itunesMain():
    content = cache("https://itunes.apple.com/"+iTunesRegion+"/genre/music/id34", 30)
    content = content[content.find('id="genre-nav"'):]
    content = content[:content.find('</div>')]
    match=re.compile('<li><a href="https://itunes.apple.com/.+?/genre/.+?/id(.+?)"(.+?)title=".+?">(.+?)<', re.DOTALL).findall(content)
    title = "All Genres"
    if itunesShowSubGenres:
        title = '[B]'+title+'[/B]'
    addAutoPlayDir(title, "0", "listItunesVideos", "", "", "browse")
    for genreID, type, title in match:
        title = cleanTitle(title)
        if 'class="top-level-genre"' in type:
            if itunesShowSubGenres:
                title = '[B]'+title+'[/B]'
            addAutoPlayDir(title, genreID, "listItunesVideos", "", "", "browse")
        elif itunesShowSubGenres:
            title = '   '+title
            addAutoPlayDir(title, genreID, "listItunesVideos", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def billboardMain():
    addAutoPlayDir(translation(30005), urlMainBB+"/rss/charts/hot-100", "listBillboardCharts", "", "", "browse")
    addAutoPlayDir("Trending 140", "Top 140 in Trending", "listBillboardChartsNew", "", "", "browse")
    addAutoPlayDir("Last 24 Hours", "Top 140 in Overall", "listBillboardChartsNew", "", "", "browse")
    addDir(translation(30006), "genre", "listBillboardChartsTypes", "", "", "browse")
    addDir(translation(30007), "country", "listBillboardChartsTypes", "", "", "browse")
    addDir(translation(30008), "other", "listBillboardChartsTypes", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listBillboardChartsTypes(type):
    if type=="genre":
        addAutoPlayDir(translation(30009), urlMainBB+"/rss/charts/pop-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30010), urlMainBB+"/rss/charts/rock-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30011), urlMainBB+"/rss/charts/alternative-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30012), urlMainBB+"/rss/charts/r-b-hip-hop-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30013), urlMainBB+"/rss/charts/r-and-b-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30014), urlMainBB+"/rss/charts/rap-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30015), urlMainBB+"/rss/charts/country-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30016), urlMainBB+"/rss/charts/latin-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30017), urlMainBB+"/rss/charts/jazz-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30018), urlMainBB+"/rss/charts/dance-club-play-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30019), urlMainBB+"/rss/charts/dance-electronic-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30020), urlMainBB+"/rss/charts/heatseekers-songs", "listBillboardCharts", "", "", "browse")
    elif type=="country":
        addAutoPlayDir(translation(30021), urlMainBB+"/rss/charts/canadian-hot-100", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30022), urlMainBB+"/rss/charts/k-pop-hot-100", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30023), urlMainBB+"/rss/charts/japan-hot-100", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30024), urlMainBB+"/rss/charts/germany-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30025), urlMainBB+"/rss/charts/france-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30026), urlMainBB+"/rss/charts/united-kingdom-songs", "listBillboardCharts", "", "", "browse")
    elif type=="other":
        addAutoPlayDir(translation(30028), urlMainBB+"/rss/charts/radio-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30029), urlMainBB+"/rss/charts/digital-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30030), urlMainBB+"/rss/charts/streaming-songs", "listBillboardCharts", "", "", "browse")
        addAutoPlayDir(translation(30031), urlMainBB+"/rss/charts/on-demand-songs", "listBillboardCharts", "", "", "browse")
    xbmcplugin.endOfDirectory(pluginhandle)


def listSpotifyGenres(url):
    content = cache(url, 30)
    content = json.loads(content)
    for item in content['items']:
        genreID = item['genre']['templateName']
        try:
            thumb = item['genre']['iconImageUrl']
        except:
            thumb = ""
        title = item['genre']['name'].encode('utf-8')
        if title.strip().lower()!="top lists":
            addDir(title, "http://api.tunigo.com/v3/space/"+genreID+"?region="+spotifyRegion+"&page=0&per_page=50&platform=web", "listSpotifyPlaylists", thumb)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')


def listSpotifyPlaylists(url):
    content = cache(url, 1)
    content = json.loads(content)
    for item in content['items']:
        uri = item['playlist']['uri'].encode('utf-8')
        try:
            thumb = "http://d3rt1990lpmkn.cloudfront.net/300/"+item['playlist']['image']
        except:
            thumb = ""
        title = item['playlist']['title'].encode('utf-8')
        description = item['playlist']['description'].encode('utf-8')
        addAutoPlayDir(title, uri, "listSpotifyVideos", thumb, description, "browse")
    match=re.compile('page=(.+?)&per_page=(.+?)&', re.DOTALL).findall(url)
    currentPage = int(match[0][0])
    perPage = int(match[0][1])
    nextPage = currentPage+1
    if nextPage*perPage<content['totalItems']:
        addDir(translation(30001), url.replace("page="+str(currentPage),"page="+str(nextPage)), "listSpotifyPlaylists", "")
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceView:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')


def listSpotifyVideos(type, url, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache("https://embed.spotify.com/?uri="+url, 1)
    spl=content.split('music-paused item')
    pos = 1
    for i in range(1,len(spl),1):
        entry=spl[i]
        match=re.compile('class="artist.+?>(.+?)<', re.DOTALL).findall(entry)
        artist=match[0]
        match=re.compile('class="track-title.+?>(.+?)<', re.DOTALL).findall(entry)
        videoTitle=match[0]
        videoTitle=videoTitle[videoTitle.find(".")+1:].strip()
        if " - " in videoTitle:
            videoTitle=videoTitle[:videoTitle.rfind(" - ")]
        if " [" in videoTitle:
            videoTitle=videoTitle[:videoTitle.rfind(" [")]
        if "," in artist:
            artist = artist.split(",")[0]
        title=cleanTitle(artist+" - "+videoTitle)
        match=re.compile('data-ca="(.+?)"', re.DOTALL).findall(entry)
        thumb=match[0]
        filtered = False
        for entry2 in blacklist:
            if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                filtered = True
        if filtered:
            continue
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", thumb)
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, thumb])
            if limit and int(limit)==pos:
                break
            pos+=1
    if type=="browse":
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listOC(type, url, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 1)
    spl=content.split('class="entry"')
    pos = 1
    for i in range(1,len(spl),1):
        entry=spl[i]
        match=re.compile('<h4>(.+?)</h4>', re.DOTALL).findall(entry)
        artist=match[0]
        match=re.compile('<h3>(.+?)</h3>', re.DOTALL).findall(entry)
        videoTitle=match[0]
        if " FT " in artist:
            artist=artist[:artist.find(" FT ")].strip()
        if "/" in artist:
            artist=artist[:artist.find("/")].strip()
        if "&amp;" in artist:
            artist=artist[:artist.find("&amp;")].strip()
        title=cleanTitle(artist+" - "+videoTitle)
        match=re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb=match[0].replace("_50.jpg","_500.jpg")
        filtered = False
        for entry2 in blacklist:
            if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                filtered = True
        if filtered:
            continue
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", thumb)
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, thumb])
            if limit and int(limit)==pos:
                break
            pos+=1
    if type=="browse":
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listBP(type, url, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = cache(url, 1)
    spl=content.split('"type":"track"')
    pos = 1
    for i in range(1,len(spl),1):
        entry=spl[i]
        match=re.compile('"artists":.+?"name":"(.+?)"', re.DOTALL).findall(entry)
        artist=match[0]
        match=re.compile('"title":"(.+?)"', re.DOTALL).findall(entry)
        videoTitle=match[0]
        if "(Original Mix)" in videoTitle:
            videoTitle=videoTitle[:videoTitle.find("(Original Mix)")].strip()
        if "feat" in videoTitle:
            videoTitle=videoTitle[:videoTitle.find("feat")].strip()
        title=cleanTitle(artist+" - "+videoTitle)
        match=re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb=match[0].replace("/24x24/","/500x500/")
        filtered = False
        for entry2 in blacklist:
            if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                filtered = True
        if filtered:
            continue
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", thumb)
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, thumb])
            if limit and int(limit)==pos:
                break
            pos+=1
    if type=="browse":
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)


def listItunesVideos(type, genreID, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    url = "https://itunes.apple.com/"+iTunesRegion+"/rss/topsongs/limit=100"
    if genreID!="0":
        url += "/genre="+genreID
    url += "/explicit=true/json"
    content = cache(url, 1)
    content = json.loads(content)
    pos = 1
    for item in content['feed']['entry']:
        artist=item['im:artist']['label'].encode('utf-8')
        videoTitle=item['im:name']['label'].encode('utf-8')
        if " (" in videoTitle:
            videoTitle=videoTitle[:videoTitle.rfind(" (")]
        title=cleanTitle(artist+" - "+videoTitle)
        try:
            thumb=item['im:image'][2]['label'].replace("170x170-75.jpg","400x400-75.jpg")
        except:
            thumb=""
        filtered = False
        for entry2 in blacklist:
            if entry2.strip().lower() and entry2.strip().lower() in title.lower():
                filtered = True
        if filtered:
            continue
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", thumb)
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, thumb])
            if limit and int(limit)==pos:
                break
            pos+=1
    if type=="browse":
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceView:
            xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)

        
def listBillboardCharts(type, url, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()	
    content = cache(url, 1)
    match = re.compile('<item>.+?<artist>(.+?)</artist>.+?<chart_item_title>(.+?)</chart_item_title>', re.DOTALL).findall(content)
    pos = 1	
    for artist, title in match:
        title = cleanTitle(artist+" - "+title[title.find(":")+1:]).replace("Featuring", "Feat.")
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, ""])
            if limit and int(limit)==pos:
                break
            pos+=1	
    if type=="browse":		
		xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)
		
def listGalgalatzPlaylist(type, url, limit):
	if type=="play" or type=="add":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()		
	content = cache(url, 1)
	match = re.compile('<td><span>(.+?)</span>', re.DOTALL).findall(content)	
	pos = 1
	artist_list = match[0:len(match):2]
	song_list = match[1:len(match):2]
	for artist,song in zip(artist_list,song_list):		
		title = artist + " - " + song		
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle", "")		
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			musicVideos.append([title, url, ""])
			if limit and int(limit)==pos:
				break
			pos+=1			
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	elif type=="add":
		return musicVideos	
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
		
def listGalgalatzPlaylistMix(type, url, limit):
	musicVideos = listGalgalatzPlaylist("add","http://www.glgltz.co.il/1213-he/Galgalatz.aspx","")
	musicVideos += listGalgalatzPlaylist("add","http://www.glgltz.co.il/1215-he/Galgalatz.aspx","")
	if type=="play" or type=="add":
		random.shuffle(musicVideos)
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()		
	for title, url, thumb in musicVideos:
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
		else:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)		
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	else:
		xbmc.Player().play(playlist)	
		
def listGalgalatzCharts(type, url, limit):
	if type=="play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()	
	content = cache(url, 1)
	pos = 1
	song_list = re.compile('<h4>(.+?)</h4>', re.DOTALL).findall(content)
	artist_list = re.compile('spanPerformer">(.+?)</span>', re.DOTALL).findall(content)
	for artist,song in zip(artist_list,song_list):		
		title = artist + " - " + song 		
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			musicVideos.append([title, url, ""])
			if limit and int(limit)==pos:
				break
			pos+=1			
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)


def listDisiPlaylist(type, url, limit):
	if type=="play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()	
	content = cache(url, 1)
	pos = 1
	artist_list = re.compile(" artist: '(.+?)'", re.DOTALL).findall(content)
	song_list = re.compile(" song: '(.+?)'", re.DOTALL).findall(content)
	poster_list = re.compile(" pic: '(.+?)'", re.DOTALL).findall(content)
	for artist,song,poster in zip(artist_list,song_list,poster_list):		
		title = artist + " - " + song 		
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle","http://www.disi.co.il"+ poster)
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			musicVideos.append([title, url, poster])
			if limit and int(limit)==pos:
				break
			pos+=1			
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)		
		
def listDisiChart(type, url, limit):
	if type=="play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()	
	content = cache(url, 1)
	pos = 1
	artist_list = re.compile('artist:"(.+?)"', re.DOTALL).findall(content)
	song_list = re.compile('song:"(.+?)"', re.DOTALL).findall(content)
	poster_list = re.compile('poster: "(.+?)"', re.DOTALL).findall(content)
	for artist,song,poster in zip(artist_list,song_list,poster_list):		
		title = artist + " - " + song 		
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle", poster)
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			musicVideos.append([title, url, poster])
			if limit and int(limit)==pos:
				break
			pos+=1			
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
		
def listGalgalatzDecadeChart80(type, url, limit):
	if type=="play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	idx1 = []
	idx2 = []
	idx3 = []
	idx4 = []
	pos = 1
	content = cache(url, 1)
	for it in re.finditer('</h3>', str(content)):
		idx1.append(it.start())	
	for it in re.finditer('<ul class="FileLinksList">', str(content)):	
		idx2.append(it.start()) 
	#80's idx1[1]:idx2[0]
	cut_file = str(content)[idx1[1]:idx2[0]]	
	cut_file = cut_file.replace('dir="ltr">','<br />')
	#for 80's
	for it in re.finditer('<br />', cut_file):
		idx3.append(it.start())		
	#for 80's
	cut_file = cut_file[idx3[0]:idx3[len(idx3)-1]]
	cut_file = cut_file.replace('</p>','<FINISH!!!>')
	for it in re.finditer('<FINISH!!!>', cut_file):
		idx4.append(it.start())
	clean_file = cut_file[:idx4[len(idx4)-1]]
	clean_file = clean_file.replace('<FINISH!!!>','<br />')
	clean_file = clean_file.replace('<br /> <br />','<br />')
	tokens = clean_file.split("<br />")
	new_t = tokens[1:len(tokens):2]
	for title in new_t:
		title = title[title.find(".")+2:].replace('\\','')
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			musicVideos.append([title, url, ""])
			if limit and int(limit)==pos:
				break
			pos+=1				
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def listGalgalatzDecadeChart90(type, url, limit):
	if type=="play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	idx1 = []
	idx2 = []
	idx3 = []
	idx4 = []
	pos = 1
	content = cache(url, 1)
	for it in re.finditer('</h3>', str(content)):
		idx1.append(it.start())	
	for it in re.finditer('<ul class="FileLinksList">', str(content)):	
		idx2.append(it.start()) 
	cut_file = str(content)[idx1[2]:idx2[1]]
	cut_file = cut_file.replace('dir="ltr">','<br />')
	#for 90's
	start_idx = cut_file.index('<p>')
	end_idx = cut_file.index('</p>')
	#for 90's
	cut_file = cut_file[start_idx:end_idx]
	clean_file = cut_file.replace('<p>','<br />')
	tokens = clean_file.split("<br />")
	tokens = list(filter(lambda x:x != '', tokens))
	new_t = tokens[0:len(tokens):2]
	for title in new_t:
		title = title[title.find(".")+1:].replace('\\','')	
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			musicVideos.append([title, url, ""])
			if limit and int(limit)==pos:
				break
			pos+=1				
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
		
def listGalgalatzDecadeChart00(type, url, limit):
	if type=="play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	idx1 = []
	idx2 = []
	idx3 = []
	idx4 = []
	pos = 1
	content = cache(url, 1)
	for it in re.finditer('</h3>', str(content)):
		idx1.append(it.start())	
	for it in re.finditer('<ul class="FileLinksList">', str(content)):	
		idx2.append(it.start()) 
	cut_file = str(content)[idx1[3]:idx2[2]]
	cut_file = cut_file.replace('dir="ltr">','<br />')
	start_idx = cut_file.index('<p>')
	end_idx = cut_file.index('</p>')
	cut_file = cut_file[start_idx:end_idx]
	clean_file = cut_file.replace('<p>','<br />')
	tokens = clean_file.split("<br />")
	tokens = list(filter(lambda x:x != '', tokens))
	new_t = tokens[0:len(tokens):2]
	for title in new_t:
		title = title[title.find(".")+1:].replace('\\','')		
		if type=="browse":
			addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
		else:
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
			musicVideos.append([title, url, ""])
			if limit and int(limit)==pos:
				break
			pos+=1				
	if type=="browse":
		xbmcplugin.endOfDirectory(pluginhandle)	
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)

def PlayGalgalatzRadio(type, url, limit):
	mix_playlist = listGalgalatzPlaylist("add","http://www.glgltz.co.il/1213-he/Galgalatz.aspx","")
	mix_playlist += listGalgalatzPlaylist("add","http://www.glgltz.co.il/1215-he/Galgalatz.aspx","")
	random.shuffle(mix_playlist)
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	main_url = url
	content = cache(url, 0)
	title = str(content)
	title = title.replace("\\"," ").replace(","," ").replace("_"," ")
	title = ' '.join(title.split())	
	if xbox:
		url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title)+"&mode=playYTByTitle"
	else:
		url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title)+"&mode=playYTByTitle"	
	listitem = xbmcgui.ListItem(title,"")
	playlist.add(url, listitem)	
	xbmc.Player().play(playlist)	
	while not (xbmc.Player().isPlaying()):
		xbmc.sleep(2000)				
	old_title = title		
	elapsed_time = 0	
	clip_time = 0	
	while (clip_time == 0):
		clip_time = xbmc.Player().getTotalTime()
		xbmc.sleep(2000)
	file_name = xbmc.Player().getPlayingFile()
	while not xbmc.abortRequested:
		if (title != old_title):		
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title)+"&mode=playYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title)+"&mode=playYTByTitle"
			listitem = xbmcgui.ListItem(title,"")
			playlist.add(url, listitem)	
			old_title = title
			elapsed_time = 0			
		try:				
			if (file_name != xbmc.Player().getPlayingFile()):
				need_refresh = True
				while (clip_time == 0):
					clip_time = xbmc.Player().getTotalTime()					
				file_name = xbmc.Player().getPlayingFile()
				elapsed_time = int(xbmc.Player().getTime())							
		except:				
			count = 3
			while not xbmc.abortRequested and count > 0:
				count = count-1
				xbmc.sleep(2000)			
			if not (xbmc.Player().isPlaying()):				
				return
		if (elapsed_time >= int(clip_time)- 8):
			#add file from mix shuffle	
			shuffle_id = random.randint(0,len(mix_playlist)-1)
			mix_title = mix_playlist[shuffle_id][0]
			listitem = xbmcgui.ListItem(mix_title,"")
			playlist.add(mix_playlist[shuffle_id][1], listitem)	
			elapsed_time = 0			
		count = 2
		while not xbmc.abortRequested and count > 0:
			count = count-1			
			xbmc.sleep(2000)					
			elapsed_time = elapsed_time +2
		if xbmc.abortRequested:
			xbmc.abortRequested = False
			xbmc.sleep(2000)				
		content = cache(main_url, 0)
		title = str(content)
		title = title.replace("\\"," ").replace(","," ").replace("_"," ")
		title = ' '.join(title.split())			

def listOneFmPlaylist(type, url, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = opener.open(url).read()
    content = content[content.find('<div id="listsBg"'):]
    content = content[:content.find('class="listContent ">')]
    match = re.compile("<li title='(.+?)'>", re.DOTALL).findall(content)
    pos = 1
    for title in match:    
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, ""])
            if limit and int(limit)==pos:
                break
            pos+=1
    if type=="browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)
	
def listOneFmLastPlayed(type, url, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = opener.open(url).read()
    content = content[content.find('<h3>Last Played</h3>'):]
    content = content[:content.find('</ul>')]
    match = re.compile('<li title="(.+?)">', re.DOTALL).findall(content)
    pos = 1
    for title in match:    
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, ""])
            if limit and int(limit)==pos:
                break
            pos+=1
    if type=="browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)
		
def PlayOneFmRadio(type, url, limit):
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	main_url = url
	content = opener.open(url).read()
	content = content[content.find('<h3>Now Playing</h3>'):]
	content = content[:content.find('</h4>')]
	match = re.compile('<h4 title="(.+?)" class="recentSong">', re.DOTALL).findall(content)	
	title = match[0]
	if xbox:
		url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
	else:
		url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"	
	listitem = xbmcgui.ListItem(title,"")
	playlist.add(url, listitem)	
	xbmc.Player().play(playlist)			
	old_title = title	
	while (xbmc.Player().isPlaying()):					
		if (title != old_title):			
			if xbox:
				url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			else:
				url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			listitem = xbmcgui.ListItem(title,"")
			playlist.add(url, listitem)	
			old_title = title
		else:			
			time.sleep(10)			
			content = opener.open(main_url).read()
			content = content[content.find('<h3>Now Playing</h3>'):]
			content = content[:content.find('</h4>')]
			match = re.compile('<h4 title="(.+?)" class="recentSong">', re.DOTALL).findall(content)
			title = match[0]

def listBillboardChartsNew(type, url, limit):
    if type=="play":
        musicVideos = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    content = opener.open("http://realtime.billboard.com/").read()
    content = content[content.find("<h1>"+url+"</h1>"):]
    content = content[:content.find("</table>")]
    match = re.compile('<tr>.*?<td>(.+?)</td>.*?<td><a href=".*?">(.+?)</a></td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?</tr>', re.DOTALL).findall(content)
    pos = 1
    for nr, artist, title, rating in match:
        if "(" in title:
            title = title[:title.find("(")].strip()
        title = cleanTitle(artist+" - "+title).replace("Featuring", "Feat.")
        if type=="browse":
            addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
        else:
            if xbox:
                url = "plugin://video/Youtube Music/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            else:
                url = "plugin://"+addonID+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=autoPlayYTByTitle"
            musicVideos.append([title, url, ""])
            if limit and int(limit)==pos:
                break
            pos+=1
    if type=="browse":
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        random.shuffle(musicVideos)
        for title, url, thumb in musicVideos:
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            playlist.add(url, listitem)
        xbmc.Player().play(playlist)
		
def playYTById(youtubeID):
	try:		
		if xbox:
			url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + youtubeID
		else:
			url = "plugin://plugin.video.youtube/play/?video_id=" + youtubeID			
		listitem = xbmcgui.ListItem(path=url)
		xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	except:
		pass

def playYTByTitle(title):
	try:		
		youtubeID = getYoutubeId(title)		
		if xbox:
			url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + youtubeID
		else:
			url = "plugin://plugin.video.youtube/play/?video_id=" + youtubeID			
		listitem = xbmcgui.ListItem(path=url)
		xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	except:
		pass

def autoPlayYTById(youtubeID):
	try:		
		if xbox:
			url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + youtubeID
		else:
			url = "plugin://plugin.video.youtube/play/?video_id=" + youtubeID
		listitem = xbmcgui.ListItem(path=url)
		xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
		if infoEnabled:
			showInfo()
	except:
		pass


def autoPlayYTByTitle(title):
    try:
        youtubeID = getYoutubeId(title)
        if xbox:
            url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + youtubeID
        else:
            url = "plugin://plugin.video.youtube/play/?video_id=" + youtubeID
        listitem = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        if infoEnabled:
            showInfo()
    except:
        pass
        

def getYoutubeId(title):
	content = cache("http://gdata.youtube.com/feeds/api/videos?vq="+urllib.quote_plus(title)+"&max-results=1&start-index=1&orderby=relevance&time=all_time&v=2", 1)	
	match=re.compile('<yt:videoid>(.+?)</yt:videoid>', re.DOTALL).findall(content)
	return match[0]

def getImgFromGoogle(title):
	content = opener.open(googleImgUrl+urllib.quote_plus(title)+"&as_filetype=jpg&imgsz=medium").read()
	match=re.compile('"url":"(.+?)",', re.DOTALL).findall(content)
	return match[0]

def queueVideo(url, name):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    listitem = xbmcgui.ListItem(name)
    playlist.add(url, listitem)        


def cache(url, duration):
	cacheFile = os.path.join(cacheDir, (''.join(c for c in unicode(url, 'utf-8') if c not in '/\\:?"*|<>')).strip())
	if len(cacheFile) > 255:
		cacheFile = cacheFile[:255]		
	if os.path.exists(cacheFile) and duration!=0 and (time.time()-os.path.getmtime(cacheFile) < 60*60*24*duration):		
		fh = open(cacheFile, 'r')
		content = fh.read()
		fh.close()
	else:		
		content = opener.open(url).read()				
		fh = open(cacheFile, 'w')		
		fh.write(content)
		fh.close()
	return content


def showInfo():
    count = 0
    while not xbmc.Player().isPlaying():
        xbmc.sleep(200)
        if count==50:
            break
        count+=1
    xbmc.sleep(infoDelay*1000)
    if infoType == "0":
        xbmc.executebuiltin('XBMC.ActivateWindow(12901)')
        xbmc.sleep(infoDuration*1000)
        xbmc.executebuiltin('XBMC.ActivateWindow(12005)')
    elif infoType == "1":
        title = 'Now playing:'
        videoTitle = xbmc.getInfoLabel('VideoPlayer.Title').replace(","," ")
        thumb = xbmc.getInfoImage('VideoPlayer.Cover')
        xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title, videoTitle, infoDuration*1000, thumb))


def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


def cleanTitle(title):
    title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
    title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö")
    title = title.strip()
    return title


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict
	
def addLinkId(name, videoid, mode, iconimage):
	u = sys.argv[0]+"?videoid="+videoid+"&mode="+str(mode)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty('IsPlayable', 'true')
	entries = []    
	entries.append((translation(30004), 'RunPlugin(plugin://'+addonID+'/?mode=queueVideo&url='+urllib.quote_plus(u)+'&videoid='+videoid+')',))
	liz.addContextMenuItems(entries)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok

def addLink(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    entries = []
    entries.append((translation(30004), 'RunPlugin(plugin://'+addonID+'/?mode=queueVideo&url='+urllib.quote_plus(u)+'&name='+urllib.quote_plus(name)+')',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok

def addDir(name, url, mode, iconimage="", description="", type="", limit=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def addAutoPlayDir(name, url, mode, iconimage="", description="", type="", limit=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    entries = []
    entries.append(("Autoplay All", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=)',))
    entries.append(("Autoplay Top10", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=10)',))
    entries.append(("Autoplay Top20", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=20)',))
    entries.append(("Autoplay Top30", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=30)',))
    entries.append(("Autoplay Top40", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=40)',))
    entries.append(("Autoplay Top50", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=50)',))    
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
	
def addAutoPlayDirYT(name, url, mode, iconimage="", description="", type="", limit=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    entries = []
    entries.append(("Autoplay All", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=)',))
    entries.append(("Autoplay Top10", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=10)',))
    entries.append(("Autoplay Top20", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=20)',))
    entries.append(("Autoplay Top30", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=30)',))
    entries.append(("Autoplay Top40", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=40)',))
    entries.append(("Autoplay Top50", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=50)',))
    img_id = iconimage[iconimage.find("vi/")+3:iconimage.find("/hq")]
    entries.append(("Add to playlist file", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=add&limit=50&name='+urllib.quote_plus(name.encode('utf-8'))+'&img='+str(img_id)+')',))    
    entries.append(("Remove from playlist file", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=remove)',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
	
def addAutoPlayDirGlz(name, url, mode, iconimage="", description="", type="", limit=""):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
	entries = []
	entries.append(("נגן הכל", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=)',))
	entries.append(("נגן טופ 10", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=10)',))
	entries.append(("נגן טופ 20", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=20)',))
	entries.append(("נגן טופ 30", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=30)',))
	entries.append(("נגן טופ 40", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=40)',))
	entries.append(("נגן טופ 50", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=50)',))
	entries.append(("נגן טופ 100", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=100)',))
	liz.addContextMenuItems(entries)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))
videoid = urllib.unquote_plus(params.get('videoid', ''))
type = urllib.unquote_plus(params.get('type', ''))
limit = urllib.unquote_plus(params.get('limit', ''))
chartTitle = urllib.unquote_plus(params.get('chartTitle', ''))
img = urllib.unquote_plus(params.get('img', ''))

if mode == 'playYTByTitle':
    playYTByTitle(url)
elif mode == 'autoPlayYTByTitle':
    autoPlayYTByTitle(url)
elif mode == 'playYTById':
    playYTById(videoid)
elif mode == 'autoPlayYTById':
    autoPlayYTById(videoid)
elif mode == 'spotifyMain':
    spotifyMain()
elif mode == 'itunesMain':
    itunesMain()
elif mode == 'billboardMain':
    billboardMain()
elif mode == 'GalgalatzMain':
    GalgalatzMain()
elif mode == 'ocMain':
    ocMain()
elif mode == 'bpMain':
    bpMain()
elif mode == 'OneFmMain':
    OneFmMain()
elif mode == 'DisiMain':
    DisiMain()
elif mode == 'YotubePlayListMain':
    YotubePlayListMain()
elif mode == 'YoutubeSearchPlaylist':
    YoutubeSearchPlaylist()	
elif mode == 'YotubeMyPlayListMain':
    YotubeMyPlayListMain()	
elif mode == 'listOC':
    listOC(type, url, limit)
elif mode == 'listBP':
    listBP(type, url, limit)	
elif mode == 'listSpotifyGenres':
    listSpotifyGenres(url)
elif mode == 'listSpotifyPlaylists':
    listSpotifyPlaylists(url)
elif mode == 'listSpotifyVideos':
    listSpotifyVideos(type, url, limit)
elif mode == 'playSpotifyVideos':
    playSpotifyVideos(url)
elif mode == 'listItunesVideos':
    listItunesVideos(type, url, limit)
elif mode == 'playItunesVideos':
    playItunesVideos(url)
elif mode == 'listBillboardCharts':
    listBillboardCharts(type, url, limit)
elif mode == 'listBillboardChartsNew':
    listBillboardChartsNew(type, url, limit)
elif mode == 'listBillboardChartsTypes':
    listBillboardChartsTypes(url)
elif mode == 'listGalgalatzCharts':
    listGalgalatzCharts(type, url, limit)
elif mode == 'listGalgalatzPlaylist':
    listGalgalatzPlaylist(type, url, limit)
elif mode == 'listGalgalatzPlaylistMix':
    listGalgalatzPlaylistMix(type, url, limit)	
elif mode == 'listGalgalatzDecadeChart80':
    listGalgalatzDecadeChart80(type, url, limit)
elif mode == 'listGalgalatzDecadeChart90':
    listGalgalatzDecadeChart90(type, url, limit)
elif mode == 'listGalgalatzDecadeChart00':
    listGalgalatzDecadeChart00(type, url, limit)	
elif mode == 'PlayGalgalatzRadio':
    PlayGalgalatzRadio(type, url, limit)	
elif mode == 'listOneFmPlaylist':
    listOneFmPlaylist(type, url, limit)	
elif mode == 'listOneFmLastPlayed':
    listOneFmLastPlayed(type, url, limit)	
elif mode == 'PlayOneFmRadio':
    PlayOneFmRadio(type, url, limit)	
elif mode == 'listDisiChart':
    listDisiChart(type, url, limit)	
elif mode == 'listDisiPlaylist':
    listDisiPlaylist(type, url, limit)	
elif mode == 'listYoutubePlayList':
    listYoutubePlayList(type, url, limit, name, img)	
elif mode == 'queueVideo':
    queueVideo(url, name)
else:
    index()
