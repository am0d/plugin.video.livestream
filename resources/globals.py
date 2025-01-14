import sys
import re, os, time
from datetime import datetime, timedelta

try:
    from kodi_six import xbmc, xbmcvfs, xbmcplugin, xbmcgui, xbmcaddon
except:
    import xbmc, xbmcvfs, xbmcplugin, xbmcgui, xbmcaddon

# import urllib, urllib2
import json
import requests, urllib
import calendar

from schemas import Account, Event


# from urllib2 import URLError, HTTPError

if sys.version_info[0] > 2:
    urllib = urllib.parse

addon_handle = int(sys.argv[1])

# App Variables
API_KEY = "98f12273997c31eab6cfbfbe64f99d92"
APP_ID = "7KJECL120U"

# Settings
USERNAME = str(xbmcaddon.Addon().getSetting(id="username"))
PASSWORD = str(xbmcaddon.Addon().getSetting(id="password"))
PLAYBACK_WINDOW = str(xbmcaddon.Addon().getSetting(id="playback_window"))

# Localisation
local_string = xbmcaddon.Addon().getLocalizedString
ROOTDIR = xbmcaddon.Addon().getAddonInfo("path")
ICON = os.path.join(ROOTDIR, "icon.png")
FANART = os.path.join(ROOTDIR, "fanart.jpg")

SEARCH_HITS = "25"
LIVE_COLOR = "FF00B7EB"
SECTION_COLOR = "FFFFFF66"

# User-Agents
UA_IPHONE = "AppleCoreMedia/1.0.0.14D27 (iPhone; U; CPU OS 10_2_1 like Mac OS X; en_us)"
UA_LIVESTREAM = "Livestream/4.1.3.1/Nemiroff (iPhone; iOS 10.2.1; Scale/2.00)"
UA_WEB = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36"

# Root URLS
ALGOLIA_URL = "https://7kjecl120u-3.algolia.io/1"
API_URL = "https://api.new.livestream.com"

last_server_response = ""

VERIFY = False


def categories():
    addDir("Browse by Category", "/livestream", 100, ICON, FANART)
    addDir("Following", "/login", 150, ICON, FANART)
    addDir("Search", "/search", 102, ICON, FANART)
    addDir("Search History", "/history", 107, ICON, FANART)
    addDir("Manually Enter", "/manual", 160, ICON, FANART)


def getCategories():
    live_events = []
    url = ALGOLIA_URL + "/indexes/categories/query"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "X-Algolia-Application-Id": APP_ID,
        "X-Algolia-API-Key": API_KEY,
        "User-Agent": UA_LIVESTREAM,
    }
    json_search = {
        "params": "attributes=id,name,category_live_events,category_live_viewers,parent_id,parent_name&facetFilters=parent_id:null&hitsPerPage=100&numerics=id%3E0"
    }

    r = requests.post(url, headers=headers, json=json_search, verify=VERIFY)
    last_server_response = r.text
    if r.ok:
        json_source = r.json()

        if "hits" in json_source:
            for category in json_source["hits"]:
                cat_info = json.dumps(category)
                name = (
                    category["name"]
                    + " ("
                    + str(category["category_live_events"])
                    + ")"
                )
                live_events.append([name, ICON, FANART, None, None, None, cat_info])

            for event in sorted(live_events, key=lambda tup: tup[0]):
                addDir(
                    event[0],
                    "/livestream",
                    106,
                    event[1],
                    event[2],
                    event[3],
                    event[4],
                    event[5],
                    event[6],
                )
    else:
        msg = "Error getting categories"
        dialog = xbmcgui.Dialog()
        ok = dialog.ok("Error", msg)


def getCategoryEvents(cat_info):
    cat_info = json.loads(cat_info)
    cat_id = str(cat_info["id"])
    live_events = str(cat_info["category_live_events"])
    url = ALGOLIA_URL + "/indexes/events/query"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "X-Algolia-Application-Id": APP_ID,
        "X-Algolia-API-Key": API_KEY,
        "User-Agent": UA_LIVESTREAM,
    }

    json_search = {
        "params": "attributes=id,full_name,tags,description,short_name,owner_account_id,broadcast_id,is_password_protected,is_geo_restricted,likes_count,concurrent_viewers_count,category_name,category_id,subcategory_name,subcategory_id,location_formatted_address,location_name,live_video_post_comments_count,live_chat_enabled,live_video_post_id,post_comments_enabled,viewer_count_visible,owner_account_id,owner_account_full_name,owner_account_features,owner_logo,logo,live_thumbnail,featured_by,start_time,end_time,expires_at&facetFilters=category_id:"
        + cat_id
        + "&hitsPerPage="
        + live_events
        + "&numerics=broadcast_id%3E0,is_geo_restricted=0,is_password_protected=0"
    }

    r = requests.post(url, headers=headers, json=json_search, verify=VERIFY)
    last_server_response = r.text
    if r.ok:
        json_source = r.json()

    live_streams = []
    for event in json_source["hits"]:
        # try:
        event_id = str(event["id"])
        owner_id = str(event["owner_account_id"])

        owner_name = str(event["owner_account_full_name"])
        full_name = str(event["full_name"])
        name = owner_name + " - " + full_name

        icon = None
        fanart = FANART
        try:
            icon = str(event["logo"]["large"]["url"])
            # fanart = event['background_image']['url']
        except:
            pass

        aired = ""
        length = ""
        desc = ""
        try:
            desc = str(event["_highlightResult"]["description"]["value"])
        except:
            pass

        info = {
            "plot": desc,
            "tvshowtitle": "Livestream",
            "title": name,
            "originaltitle": name,
            "duration": length,
            "aired": aired,
        }

        # name = '[COLOR=FF00B7EB]'+name+'[/COLOR]'
        live_streams.append([name, icon, event_id, owner_id, info, fanart])

    for stream in sorted(live_streams, key=lambda tup: tup[0]):
        addDir(
            stream[0],
            "/live_now",
            101,
            stream[1],
            stream[5],
            stream[2],
            stream[3],
            stream[4],
        )


def search(search_txt=""):
    if search_txt == "":
        dialog = xbmcgui.Dialog()
        search_txt = dialog.input("Enter search text", type=xbmcgui.INPUT_ALPHANUM)
        if search_txt == "":
            sys.exit()
        addHistory(search_txt)

    json_source = ""
    if search_txt != "":
        url = ALGOLIA_URL + "/indexes/*/queries"
        # req = urllib2.Request(url)
        # req.addheaders = [ ("Accept", "*/*"),
        #                     ("Origin", "http://livestream.com"),
        #                     ("Accept-Language", "en-US,en;q=0.8"),
        #                     ("Accept-Encoding", "gzip, deflate"),
        #                     ("X-Algolia-Application-Id", APP_ID),
        #                     ("X-Algolia-API-Key", API_KEY),
        #                     ("Content-type", "application/json"),
        #                     ("Connection", "keep-alive"),
        #                     ("Referer", "http://livestream.com/watch"),
        #                     ("User-Agent", UA_WEB)]
        #
        #
        # json_search = '{"requests":[{"indexName":"events","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"accounts","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"},{"indexName":"videos","params":"query='+search_txt+'&hitsPerPage='+SEARCH_HITS+'"}],"apiKey":"'+API_KEY+'","appID":"'+APP_ID+'"}'
        # response = urllib2.urlopen(req,json_search)
        # json_source = json.load(response)
        # response.close()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "X-Algolia-Application-Id": APP_ID,
            "X-Algolia-API-Key": API_KEY,
            "User-Agent": UA_LIVESTREAM,
        }
        json_search = {
            "requests": [
                {
                    "indexName": "events",
                    "params": "query="
                    + search_txt
                    + "&hitsPerPage="
                    + SEARCH_HITS
                    + "",
                },
                {
                    "indexName": "accounts",
                    "params": "query="
                    + search_txt
                    + "&hitsPerPage="
                    + SEARCH_HITS
                    + "",
                },
                {
                    "indexName": "videos",
                    "params": "query="
                    + search_txt
                    + "&hitsPerPage="
                    + SEARCH_HITS
                    + "",
                },
            ],
            "apiKey": "" + API_KEY + "",
            "appID": "" + APP_ID + "",
        }

        r = requests.post(url, headers=headers, json=json_search, verify=VERIFY)
        last_server_response = r.text

    searchResults(r.json())


def getHistory():
    lines = []
    addon_profile_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
    fname = os.path.join(addon_profile_path, "search_history.txt")
    if not os.path.isfile(fname):
        if not os.path.exists(addon_profile_path):
            os.makedirs(addon_profile_path)
    else:
        with open(fname) as file:
            for line in file:
                line = line.strip()
                lines.append(line)

    dialog = xbmcgui.Dialog()
    ret = dialog.select("Search History", lines)
    if ret > -1:
        search_txt = lines[ret]
        search(search_txt)
    else:
        sys.exit()


def addHistory(search_text):
    lines = []
    addon_profile_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
    fname = os.path.join(addon_profile_path, "search_history.txt")
    if not os.path.isfile(fname):
        if not os.path.exists(addon_profile_path):
            os.makedirs(addon_profile_path)
    else:
        with open(fname) as file:
            for line in file:
                line = line.strip()
                lines.append(line)

    search_file = open(fname, "w")
    lines.insert(0, search_text)
    i = 0
    for line in lines:
        search_file.write(line)
        search_file.write("\n")
        i += 1
        if i >= 10:
            break

    search_file.close()


def searchResults(json_source):
    if json_source != "":
        i = 0

        for hits in json_source["results"]:
            i = i + 1
            if i == 1:
                addDir(
                    "[B][I][COLOR=" + SECTION_COLOR + "]Events[/COLOR][/B][/I]",
                    "/accounts",
                    999,
                    ICON,
                    FANART,
                )
            elif i == 2:
                addDir(
                    "[B][I][COLOR=" + SECTION_COLOR + "]Accounts[/COLOR][/B][/I]",
                    "/accounts",
                    999,
                    ICON,
                    FANART,
                )
            elif i == 3:
                addDir(
                    "[B][I][COLOR=" + SECTION_COLOR + "]Videos[/COLOR][/B][/I]",
                    "/accounts",
                    999,
                    ICON,
                    FANART,
                )

            for event in hits["hits"]:
                try:
                    if i != 2:
                        owner_id = str(event["owner_account_id"])

                        if i == 1:
                            # Events
                            name = event["full_name"].encode("utf-8")
                            name = (
                                event["owner_account_full_name"].encode("utf-8")
                                + " - "
                                + name
                            )
                            event_id = str(event["id"])
                            icon = event["logo"]["large"]["url"]
                            start_time = str(event["start_time"])
                        elif i == 3:
                            # Videos
                            name = (
                                event["owner_account_full_name"].encode("utf-8")
                                + " - "
                                + event["caption"].encode("utf-8")
                            )
                            event_id = str(event["owner_event_id"])
                            icon = event["thumbnail"]["large"]["url"]
                            start_time = str(event["publish_at"])

                        duration = 0
                        try:
                            duration = int(item["duration"])
                        except:
                            pass

                        aired = (
                            start_time[0:4]
                            + "-"
                            + start_time[5:7]
                            + "-"
                            + start_time[8:10]
                        )
                        desc = ""
                        try:
                            desc = str(event["description"]).encode("utf-8")
                        except:
                            pass

                        info = {
                            "plot": desc,
                            "tvshowtitle": "Livestream",
                            "title": name,
                            "originaltitle": name,
                            "duration": duration,
                            "aired": aired,
                        }
                        addDir(
                            name,
                            "/live_now",
                            101,
                            icon,
                            FANART,
                            event_id,
                            owner_id,
                            info,
                        )
                    else:
                        # Accounts
                        name = event["full_name"].encode("utf-8")
                        owner_id = str(event["id"])
                        icon = event["picture"]["large"]["url"]
                        addDir(name, "/accounts", 105, icon, FANART, None, owner_id)
                except:
                    pass


def getJsonFile(url):
    # req = urllib2.Request(url)
    # req.add_header('User-Agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36')
    # response = urllib2.urlopen(req)
    # json_source = json.load(response)
    # response.close()
    r = requests.get(url, headers={"User-Agent": UA_WEB}, verify=VERIFY)
    last_server_response = r.text
    return r.json()


def getStream(owner_id, event_id, video_id):
    m3u8_url = ""
    if video_id == None:

        # url = API_URL+'/accounts/'+owner_id+'/events/'+event_id+'/'
        url = "%s/accounts/%s/events/%s/" % (API_URL, owner_id, event_id)
        # req = urllib2.Request(url)
        # req.add_header('User-Agent', UA_IPHONE)
        r = requests.get(url, headers={"User-Agent": UA_IPHONE}, verify=VERIFY)
        last_server_response = r.text
        if not r.ok:
            # try:
            #     response = urllib2.urlopen(req)
            # except HTTPError as e:
            xbmc.log("The server couldn't fulfill the request.")
            xbmc.log("Error code: ", e.code)
            xbmc.log(url)

            # Error 401 for invalid login
            if r.status_code == 401:
                msg = "Please check that your username and password are correct"
                dialog = xbmcgui.Dialog()
                ok = dialog.ok("Invalid Login", msg)

            sys.exit()

        json_source = r.json()
        # json_source = json.load(response)
        # response.close()

        if None != json_source.get("stream_info") and None != json_source[
            "stream_info"
        ].get("live_video_post"):
            event_info = extractEventInfo(json_source["stream_info"]["live_video_post"])
            icon = ""
            if "thumbnail_url" in json_source["stream_info"]:
                icon = json_source["stream_info"]["thumbnail_url"]

            addStream(
                str(event_info["name"]),
                "/live_now",
                str(event_info["name"]),
                icon,
                str(event_info["fanart"]),
                event_id,
                owner_id,
                str(event_info["info"]),
                "LIVE",
            )

        # Get the total number of feeds and request all of them to display
        feed_total = str(json_source["feed"]["total"])
        url = (
            "https://api.new.livestream.com/accounts/"
            + owner_id
            + "/events/"
            + event_id
            + "/feed/?maxItems="
            + feed_total
        )
        # req = urllib2.Request(url)
        # req.add_header('User-Agent', UA_IPHONE)
        # response = urllib2.urlopen(req)
        # json_source = json.load(response)
        # response.close()
        r = requests.get(url, headers={"User-Agent": UA_IPHONE}, verify=VERIFY)
        last_server_response = r.text
        json_source = r.json()
        for event in json_source["data"]:
            try:
                event_info = extractEventInfo(event["data"])
                addStream(
                    event_info["name"],
                    "/live_now",
                    event_info["name"],
                    event_info["icon"],
                    event_info["fanart"],
                    event_id,
                    owner_id,
                    event_info["info"],
                    event_info["broadcast_id"],
                )
            except:
                pass
    else:
        if video_id == "LIVE":
            url = API_URL + "/accounts/" + owner_id + "/events/" + event_id
            r = requests.get(url, headers={"User-Agent": UA_IPHONE}, verify=VERIFY)
            last_server_response = r.text
            url = (
                adjust_playback_url(r.json()["stream_info"]["m3u8_url"])
                + "|User-Agent="
                + UA_IPHONE
            )
            listitem = xbmcgui.ListItem(path=url)
            listitem.setProperty("inputstream", "inputstream.adaptive")
            listitem.setProperty("inputstream.adaptive.manifest_type", "hls")
            listitem.setProperty("inputstream.adaptive.play_timeshift_buffer", "true")
            xbmcplugin.setResolvedUrl(addon_handle, True, listitem)
        else:
            url = (
                API_URL
                + "/accounts/"
                + owner_id
                + "/events/"
                + event_id
                + "/videos/"
                + video_id
            )
            r = requests.get(url, headers={"User-Agent": UA_IPHONE}, verify=VERIFY)
            last_server_response = r.text
            stream_url = (
                adjust_playback_url(r.json()["m3u8_url"]) + "|User-Agent=" + UA_IPHONE
            )
            listitem = xbmcgui.ListItem(path=stream_url)
            listitem.setProperty("inputstream", "inputstream.adaptive")
            listitem.setProperty("inputstream.adaptive.manifest_type", "hls")
            listitem.setProperty("inputstream.adaptive.play_timeshift_buffer", "true")
            xbmcplugin.setResolvedUrl(addon_handle, True, listitem)


def adjust_playback_url(url):
    xbmc.log("getStream: original stream_url={}".format(url), xbmc.LOGDEBUG)
    url = re.sub(r"\bdw=\d+\b", "dw=" + PLAYBACK_WINDOW, url)
    xbmc.log("getStream: stream_url={}".format(url), xbmc.LOGDEBUG)
    return url


def natural_sort_key(s):
    _nsre = re.compile("([0-9]+)")
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


def getAccountStreams(owner_id: str):
    # url = 'https://api.new.livestream.com/accounts/'+owner_id
    url = API_URL + "/accounts/" + owner_id
    json_source = getJsonFile(url)
    account = Account.from_json_data(json_source)

    ###########################################################
    # Live & Upcoming
    ###########################################################
    addDir(
        "[B][I][COLOR=" + SECTION_COLOR + "]Live & Upcoming Events[/COLOR][/B][/I]",
        "/accounts",
        999,
        ICON,
        FANART,
    )
    event_list = []
    for event in account.upcoming_events.data:
        event_info = extractEventInfo(event)
        event_list.append(event_info)

    # Reversed order so upcoming videos are displayed by date ascending
    for event in reversed(event_list):
        addDir(
            event["name"],
            "/videos",
            101,
            event["icon"],
            event["fanart"],
            event["event_id"],
            owner_id,
            event["info"],
        )

    ###########################################################
    # Archived
    ###########################################################
    addDir(
        "[B][I][COLOR=" + SECTION_COLOR + "]Archived Events[/COLOR][/B][/I]",
        "/accounts",
        999,
        ICON,
        FANART,
    )
    event_list = []
    for event in json_source.past_events.data:
        event_info = extractEventInfo(event)
        event_list.append(event_info)

    # Past videos are displayed by date descending
    for event in event_list:
        addDir(
            event["name"],
            "/videos",
            101,
            event["icon"],
            event["fanart"],
            event["event_id"],
            owner_id,
            event["info"],
        )


def extractEventInfo(event: Event):

    event_info = {}
    try:
        event_id = str(event["event_id"])
    except:
        event_id = str(event["id"])

    broadcast_id = None
    try:
        broadcast_id = str(event["id"])
    except:
        broadcast_id = str(event["broadcast_id"])

    try:
        name = str(event["full_name"])
    except:
        name = str(event["caption"])

    icon = None
    fanart = None
    try:
        icon = str(event["logo"]["url"])
        fanart = str(event["background_image"]["url"])
    except:
        try:
            icon = str(event["thumbnail_url"])
        except:
            pass

    try:
        start_time = str(event.start_time)
    except:
        try:
            start_time = str(event.streamed_at)
        except:
            start_time = str(event.publish_at)

    duration = 0
    try:
        duration = int(event.duration)
    except:
        pass

    desc = ""
    try:
        desc = str(event["description"])
    except:
        pass

    aired = start_time[0:4] + "-" + start_time[5:7] + "-" + start_time[8:10]
    info = {
        "plot": desc,
        "tvshowtitle": "Livestream",
        "title": name,
        "originaltitle": name,
        "duration": duration,
        "aired": aired,
    }
    event_info = {
        "name": name,
        "event_id": event_id,
        "icon": icon,
        "fanart": fanart,
        "info": info,
        "broadcast_id": broadcast_id,
    }

    return event_info


def login():
    # Check if username and password are provided
    global USERNAME
    if USERNAME == "":
        dialog = xbmcgui.Dialog()
        USERNAME = dialog.input(
            "Please enter your username", type=xbmcgui.INPUT_ALPHANUM
        )

    global PASSWORD
    if PASSWORD == "":
        dialog = xbmcgui.Dialog()
        PASSWORD = dialog.input(
            "Please enter your password",
            type=xbmcgui.INPUT_ALPHANUM,
            option=xbmcgui.ALPHANUM_HIDE_INPUT,
        )

    if USERNAME != "" and PASSWORD != "":

        # url = 'https://oauth.new.livestream.com/oauth/access_token/'
        url = "https://oauth.new.livestream.com/tokens/ "
        req = urllib2.Request(url)
        req.add_header("Accept", "*/*")
        req.add_header("Accept-Language", "en-US,en;q=1")
        req.add_header("Accept-Encoding", "deflate")
        # req.add_header("X-Algolia-Application-Id", APP_ID)
        # req.add_header("X-Algolia-API-Key", API_KEY)
        req.add_header(
            "Content-type", "application/x-www-form-urlencoded; charset=utf-8"
        )
        req.add_header("Connection", "keep-alive")
        req.add_header("User-Agent", UA_LIVESTREAM)

        body = urllib.urlencode(
            {
                "grant_type": "password",
                "username": USERNAME,
                "password": PASSWORD,
                "client_id": "289ef33f7caa0c346c3025ff518ada99",
                "client_secret": "511901d55797644f2bf78716518adaa3",
            }
        )
        try:
            response = urllib2.urlopen(req, body)
            json_source = json.load(response)
            response.close()
            # Good login, save credentials
            settings.setSetting(id="username", value=USERNAME)
            settings.setSetting(id="password", value=PASSWORD)
        except HTTPError as e:
            status_code = e.code
            json_source = json.load(e)
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(json_source["name"], json_source["message"])
            sys.exit()
        except:
            pass

        access_token = json_source["access_token"]
        user_id = str(json_source["grant"]["account_id"])

        ########################
        # Get Accounts Following
        ########################
        req = urllib2.Request(API_URL + "/accounts/" + user_id + "/following")
        req.add_header("Accept", "*/*")
        req.add_header("Accept-Language", "en-US,en;q=1")
        req.add_header("Accept-Encoding", "deflate")
        req.add_header("User-Agent", UA_LIVESTREAM)

        response = urllib2.urlopen(req)
        json_source = json.load(response)
        response.close()

        for account in json_source["data"]:
            name = account["full_name"].encode("utf-8")
            owner_id = str(account["id"])
            icon = ICON
            fanart = FANART
            try:
                icon = account["picture"]["url"]
                fanart = account["background_image"]["url"]
            except:
                pass

            addDir(name, "/accounts", 105, icon, fanart, None, owner_id)


def manualEvent():
    dialog = xbmcgui.Dialog()
    owner_id = dialog.input("Please enter the account id", type=xbmcgui.INPUT_ALPHANUM)
    event_id = dialog.input("Please enter the event id", type=xbmcgui.INPUT_ALPHANUM)
    if owner_id != "" and event_id != "":
        getStream(owner_id, event_id, None)


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace("?", "")
        if params[len(params) - 1] == "/":
            params = params[0 : len(params) - 2]
        pairsofparams = cleanedparams.split("&")
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split("=")
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def addStream(
    name,
    link_url,
    title,
    icon,
    fanart=None,
    event_id=None,
    owner_id=None,
    info=None,
    video_id=None,
):
    ok = True
    u = (
        sys.argv[0]
        + "?url="
        + urllib.quote_plus(link_url)
        + "&mode="
        + str(104)
        + "&name="
        + urllib.quote_plus(name)
    )
    if icon is not None:
        u = u + "&icon=" + urllib.quote_plus(icon)
    if event_id is not None:
        u = u + "&event_id=" + urllib.quote_plus(event_id)
    if owner_id is not None:
        u = u + "&owner_id=" + urllib.quote_plus(owner_id)
    if video_id is not None:
        u = u + "&video_id=" + urllib.quote_plus(video_id)

    # if iconimage is not None:
    #     liz=xbmcgui.ListItem(name, icon="DefaultVideo.png", thumb=iconimage)
    # else:
    #     liz=xbmcgui.ListItem(name, icon="DefaultVideo.png", thumb=ICON)
    #
    # if fanart is not None:
    #     liz.setProperty('fanart_image', fanart)
    # else:
    #     liz.setProperty('fanart_image', FANART)
    if icon is None:
        icon = ICON
    if fanart is None:
        fanart = FANART
    liz = xbmcgui.ListItem(name)
    liz = xbmcgui.ListItem(name)
    liz.setArt({"icon": icon, "thumb": icon, "fanart": fanart})
    liz.setInfo(type="Video", infoLabels={"Title": name})

    liz.setProperty("IsPlayable", "true")
    liz.setInfo(type="Video", infoLabels={"Title": title})
    if info is not None:
        liz.setInfo(type="Video", infoLabels=info)
    ok = xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False
    )
    xbmcplugin.setContent(addon_handle, "episodes")

    return ok


def addLink(name, url, title, iconimage, fanart=None):
    ok = True
    liz = xbmcgui.ListItem(name, icon="DefaultVideo.png", thumb=iconimage)
    liz.setProperty("IsPlayable", "true")
    liz.setInfo(type="Video", infoLabels={"Title": title})
    if iconimage is not None:
        liz = xbmcgui.ListItem(name, icon="DefaultVideo.png", thumb=iconimage)
    else:
        liz = xbmcgui.ListItem(name, icon="DefaultVideo.png", thumb=ICON)

    if fanart is not None:
        liz.setProperty("fanart_image", fanart)
    else:
        liz.setProperty("fanart_image", FANART)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


def addDir(
    name,
    url,
    mode,
    icon,
    fanart=None,
    event_id=None,
    owner_id=None,
    info=None,
    cat_info=None,
):
    ok = True
    u = (
        sys.argv[0]
        + "?url="
        + urllib.quote_plus(url)
        + "&mode="
        + str(mode)
        + "&name="
        + urllib.quote_plus(name)
    )

    if event_id is not None:
        u = u + "&event_id=" + urllib.quote_plus(event_id)
    if owner_id is not None:
        u = u + "&owner_id=" + urllib.quote_plus(owner_id)

    if icon is not None:
        u = u + "&icon=" + urllib.quote_plus(icon)

    if cat_info is not None:
        u = u + "&cat_info=" + urllib.quote_plus(cat_info)

    if icon is None:
        icon = ICON
    if fanart is None:
        fanart = FANART
    liz = xbmcgui.ListItem(name)
    liz = xbmcgui.ListItem(name)
    liz.setArt({"icon": icon, "thumb": icon, "fanart": fanart})
    liz.setInfo(type="Video", infoLabels={"Title": name})

    if info is not None:
        liz.setInfo(type="Video", infoLabels=info)

    ok = xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True
    )
    xbmcplugin.setContent(int(sys.argv[1]), "episodes")
    return ok
