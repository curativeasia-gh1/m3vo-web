"""Notify IndexNow (Bing and other participating engines) about m3vo.com URLs.

Run after a deployment is live, because the engines fetch https://m3vo.com/<key>.txt to
confirm ownership before accepting the URLs.

    python3 scripts/indexnow.py                 # dry run: show what would be sent
    python3 scripts/indexnow.py --submit        # submit every URL in sitemap.xml
    python3 scripts/indexnow.py --submit URL..  # submit only the given URLs (e.g. changed pages)

Standard library only. The key comes from the root key file written by _generator/build.py.
"""
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
HOST = "m3vo.com"
ENDPOINT = "https://api.indexnow.org/indexnow"

def find_key():
    keys = [f.stem for f in ROOT.glob("*.txt")
            if re.fullmatch(r"[0-9a-f]{32}", f.stem) and f.read_text(encoding="utf-8").strip() == f.stem]
    if len(keys) != 1:
        sys.exit(f"Expected exactly one IndexNow key file in {ROOT}, found {len(keys)}")
    return keys[0]

def main(argv):
    submit = "--submit" in argv
    urls = [a for a in argv if not a.startswith("--")]
    if not urls:
        urls = [n.text for n in ET.parse(ROOT / "sitemap.xml").findall(".//{*}loc")]
    for u in urls:
        if urlsplit(u).netloc != HOST:
            sys.exit(f"Refusing URL outside {HOST}: {u}")
    key = find_key()
    payload = {"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}
    print(f"{len(urls)} URL(s); keyLocation {payload['keyLocation']}")
    if not submit:
        print("Dry run. Add --submit to send to", ENDPOINT)
        return
    req = urllib.request.Request(ENDPOINT, json.dumps(payload).encode(),
                                 {"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("HTTP", r.status, "(200 OK, 202 accepted: key validation pending)")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.reason} (403 = key file not reachable yet, 422 = URL/host mismatch)")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {ENDPOINT}: {e.reason}")

main(sys.argv[1:])
