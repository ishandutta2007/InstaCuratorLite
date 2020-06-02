from time import sleep
import requests
import urllib
import os
import sys
import json
import urllib.request
import pprint as pp
from pathlib import Path

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

__version__ = "v.0.2.7"

window = tkinter.Tk()
PROJHOME = "/".join(str(Path().absolute()).split("/")[:6])


def download(username):
    request_url = "https://www.instagram.com/" + username + "?__a=1"
    more_available = True
    end_cursors = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
    }

    make_folder(username)  # makes folder with given username

    # while more_available:
    if not end_cursors:
        response = requests.get(request_url, headers=headers)
    else:
        response = requests.get(request_url + "&max_id={}".format(end_cursors[-1]))

    try:
        data = response.json()
    except:
        print("\033[91mInvalid username!\033[0m")
        os.removedirs(PROJHOME + "/testdata/" + username)
        return

    nodes = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
    display_urls = []
    for node in nodes:
        display_urls.append(node["node"]["display_url"])
    for display_url in display_urls:
        print(display_url)
        display_url = display_url.replace("s640x640", "s1080x1080")
        file_name = display_url.split("/")[-1].split("?")[0]
        path = PROJHOME + "/testdata/" + username + "/" + username + "_" + file_name
        if os.path.exists(path):
            print("Already Downloaded")
        else:
            urllib.request.urlretrieve(display_url, path)
            print("Downloaded: " + path)
            print()
            sleep(1.5)


# Make folder with given username
def make_folder(username):
    if os.path.exists(PROJHOME + "/testdata/" + username):
        return
    try:
        os.makedirs(PROJHOME + "/testdata/" + username)
    except OSError:
        os.system("rm -rf " + username)
        os.makedirs(PROJHOME + "/testdata/" + username)


args = sys.argv[1:]
print(args)

uidx = -2
if "--users" in args or "-us" in args:
    try:
        uidx = args.index("--users")
    except Exception as e:
        try:
            uidx = args.index("-us")
        except Exception as e:
            pass

if uidx > -1:
    users = args[uidx + 1].split(",")

    for user in users:
        download(user)
