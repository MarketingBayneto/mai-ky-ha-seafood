"""Tell Bing (and the other IndexNow search engines) which pages exist, right after each deploy.

Reads every address from dist/sitemap.xml and the key from indexnow-key.txt.
The key file dist/<key>.txt is published with the site so the search engines can confirm ownership.
"""
import json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = 'maikyha.com'
key = (ROOT / 'indexnow-key.txt').read_text().strip()
urls = re.findall(r'<loc>([^<]+)</loc>', (ROOT / 'dist' / 'sitemap.xml').read_text())

# Wait until the freshly deployed key file is reachable, so the engines can verify it.
key_url = f'https://{HOST}/{key}.txt'
for attempt in range(12):
    try:
        if urllib.request.urlopen(key_url, timeout=20).read().decode().strip() == key:
            break
    except Exception as error:
        print('Key file not reachable yet:', error)
    time.sleep(15)
else:
    sys.exit('Key file never became reachable; skipping IndexNow.')

body = json.dumps({'host': HOST, 'key': key, 'keyLocation': key_url, 'urlList': urls}).encode()
request = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        print(f'IndexNow accepted {len(urls)} addresses: HTTP {response.status}')
except urllib.error.HTTPError as error:
    print(f'IndexNow answered HTTP {error.code}: {error.read()[:300]!r}')
    sys.exit(1 if error.code not in (200, 202) else 0)
