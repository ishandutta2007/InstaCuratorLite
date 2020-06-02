from time import sleep
import requests
import urllib
import os
import json
import urllib.request
import pprint as pp
from pathlib import Path

from instadownload import download, make_folder

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

__version__ = "v.0.2.7"
PROJHOME = "/".join(str(Path().absolute()).split("/")[:6])


def action():
    download(entry.get())


# Building the UI
window = tkinter.Tk()
window.configure(background="grey90")
window.title("insta-downloader" + __version__)
window.geometry("300x200")
window.resizable(False, False)

entry = tkinter.Entry(window)
entry.place(x=70, y=68)
entry.configure(highlightbackground="grey90")

button = tkinter.Button(window, text="Download")
button.place(x=110, y=120)
button.configure(command=lambda: action(), highlightbackground="grey90")

notice = tkinter.Label(
    window, text="insta-dl is not affiliated with Instagram", fg="grey60", bg="grey90"
)
notice.place(x=30, y=180)

window.mainloop()
