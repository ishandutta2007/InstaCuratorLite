from time import sleep
import requests
import urllib
import os
import sys
import shutil
import json
import urllib.request
import pprint as pp
from pathlib import Path
from datetime import date

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

__version__ = "v.0.2.7"

PROJHOME = "/".join(str(Path().absolute()).split("/")[:6])
MYDATAPATH = PROJHOME + "/testdata/"
MYUPLOADDIR = str(Path.home()) + "/Dropbox"
today = date.today()


def merge_and_copy_sources(target_profile, source_profiles, downloaded_path, dest_path):
    make_folder(MYUPLOADDIR, target_profile)
    print(target_profile, source_profiles)
    for thisprofile in source_profiles:
        print(thisprofile)
        src_files = os.listdir(downloaded_path + "/" + thisprofile)
        for file_name in src_files:
            full_file_name = os.path.join(downloaded_path + "/" + thisprofile, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest_path + "/" + target_profile)
                print("copying", full_file_name, "to", dest_path + "/" + target_profile)


def download(username):
    request_url = "https://www.instagram.com/" + username + "?__a=1"
    more_available = True
    end_cursors = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
    }

    make_folder(MYDATAPATH, username)  # makes folder with given username

    # while more_available:
    if not end_cursors:
        response = requests.get(request_url, headers=headers)
    else:
        response = requests.get(request_url + "&max_id={}".format(end_cursors[-1]))

    try:
        data = response.json()
    except:
        print("\033[91mInvalid username!\033[0m")
        os.removedirs(MYDATAPATH + username)
        return

    nodes = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
    display_urls = []
    captions = []
    for node in nodes:
        inndernode = node["node"]  # inndernode["accessibility_caption"]
        display_urls.append(inndernode["display_url"])
        try:
            caption = inndernode["edge_media_to_caption"]["edges"][0]["node"]["text"]
            captions.append(caption)
        except Exception as e:
            captions.append("")

    for idx, display_url in enumerate(display_urls):
        print(display_url)
        display_url = display_url.replace("s640x640", "s1080x1080")
        file_name = display_url.split("/")[-1].split("?")[0]
        path = MYDATAPATH + username + "/" + username + "_" + file_name
        if os.path.exists(path):
            print("Already Downloaded image")
        else:
            urllib.request.urlretrieve(display_url, path)
            print("Downloaded image to: " + path)
        print(captions[idx])
        file_name = display_url.split("/")[-1].split("?")[0]
        path = MYDATAPATH + username + "/" + username + "_" + file_name
        path = path.replace(".jpg", ".txt")
        if os.path.exists(path):
            print("Already Written caption")
        else:
            f = open(path, "a")
            f.write(str(captions[idx]))
            f.close()
            print("Written caption to: " + path)
        print()
        sleep(1.5)


def make_folder(path, username):
    if os.path.exists(path + "/" + username):
        return
    try:
        os.makedirs(path + "/" + username)
    except OSError:
        os.system("rm -rf " + path + "/" + username)
        os.makedirs(path + username)


args = sys.argv[1:]
print(args)


sourceuser_idx = -2
if "--sourceusers" in args or "-su" in args:
    try:
        sourceuser_idx = args.index("--sourceusers")
    except Exception as e:
        try:
            sourceuser_idx = args.index("-su")
        except Exception as e:
            pass

if sourceuser_idx > -1:
    sourceusernames = args[sourceuser_idx + 1].split(",")

    for user in sourceusernames:
        download(user)


    destuser_idx = -2
    if "--destusers" in args or "-du" in args:
        try:
            destuser_idx = args.index("--destusers")
        except Exception as e:
            try:
                destuser_idx = args.index("-du")
            except Exception as e:
                pass

    if destuser_idx > -1:
        destusername = args[destuser_idx + 1]
        merge_and_copy_sources(
            target_profile=destusername,
            source_profiles=sourceusernames,
            downloaded_path=MYDATAPATH,
            dest_path=MYUPLOADDIR,
        )
