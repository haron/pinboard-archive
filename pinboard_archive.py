#!/usr/bin/env python3
import sys
import re
import requests
from pathlib import Path
from urllib.parse import urlparse
import pdfkit
import subprocess
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = Path(sys.argv[0]).parent / "archive"
AUTH_TOKEN = open(Path(sys.argv[0]).parent / ".token").read().strip()
CMD = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --incognito --print-to-pdf='{fn}' '{url}' 2> /dev/null"

def recent():
    url = f"https://api.pinboard.in/v1/posts/recent?format=json&auth_token={AUTH_TOKEN}"
    return requests.get(url).json()["posts"]


def entry_to_filename(e):
    safe_url = (urlparse(e["href"]).hostname + "-" + re.sub(r'\W+', "-", urlparse(e["href"]).path))[:80]
    return BASE_DIR / (e["time"].split("T")[0] + "-" + safe_url + "-" + e["hash"][:5] + ".pdf")


def system(cmd):
    cmd = "timeout 60 " + cmd
    print(f"Running command: {cmd}")
    return subprocess.check_output(cmd, shell=True)


def save_entry(e):
    fn = entry_to_filename(e)
    if not fn.exists():
        system(CMD.format(url=e["href"], fn=fn))


BASE_DIR.mkdir(parents=True, exist_ok=True)

with ThreadPoolExecutor(max_workers=4) as executor:
    list(map(save_entry, recent()))
