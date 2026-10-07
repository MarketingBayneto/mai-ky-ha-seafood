"""Phone-sized copies of large photos.

Each photo wider than 760px gets a 720px-wide copy (name-720.webp). Every <img> that shows such a
photo lists both sizes, so phones download the smaller copy and large screens keep the original.
The lightbox still opens the full-size original.
"""
from pathlib import Path
import re

SMALL = 720


def small_copy(assets, name):
    from PIL import Image
    source = assets / name
    target = assets / name.replace('.webp', f'-{SMALL}.webp')
    with Image.open(source) as im:
        w, h = im.size
        if w <= SMALL + 40:
            return None, w
        if not target.exists() or target.stat().st_mtime < source.stat().st_mtime:
            im.resize((SMALL, round(h * SMALL / w)), Image.LANCZOS).save(target, 'WEBP', quality=80, method=6)
    return target.name, w


def add_srcset(dist):
    dist = Path(dist)
    assets = dist / 'assets'
    known = {}
    tag = re.compile(r'<img src="((?:\.\./|\./)*assets/)([a-z0-9-]+\.webp)"([^>]*)>')

    def swap(m):
        prefix, name, rest = m.groups()
        if "srcset=" in rest or name.endswith(f'-{SMALL}.webp'):
            return m.group(0)
        if name not in known:
            known[name] = small_copy(assets, name)
        small, width = known[name]
        if not small:
            return m.group(0)
        srcset = f'{prefix}{small} {SMALL}w, {prefix}{name} {width}w'
        return f'<img src="{prefix}{name}" srcset="{srcset}" sizes="(max-width: 760px) 90vw, 640px"{rest}>'

    for html_file in dist.rglob('*.html'):
        text = html_file.read_text()
        html_file.write_text(tag.sub(swap, text))
    print('Phone-sized copies for', sum(1 for v in known.values() if v[0]), 'photos.')
