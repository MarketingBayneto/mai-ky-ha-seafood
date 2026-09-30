"""Rewrite root-absolute links (/assets/..., /en/...) into page-relative links.

Relative links let the same dist/ folder work at a domain root, under a
GitHub Pages project path such as https://user.github.io/maikyha/, or locally.
Canonical and hreflang tags keep absolute URLs built from SITE_URL.
"""
from pathlib import Path
import posixpath, re

ATTR = re.compile(r'\b(href|src|data-photo)="(/(?!/)[^"]*)"')

def page_url(dist, html_file):
    rel = html_file.parent.relative_to(dist).as_posix()
    return '/' if rel == '.' else '/' + rel + '/'

def relative(target, base):
    path, sep, rest = target.partition('?')
    if not sep:
        path, sep, rest = target.partition('#')
    rel = posixpath.relpath(path, base)
    if path.endswith('/') and rel != '.':
        rel += '/'
    if rel == '.':
        rel = './'
    return rel + (sep + rest if sep else '')

def make_relative(dist):
    dist = Path(dist)
    for html_file in dist.rglob('*.html'):
        base = page_url(dist, html_file)
        text = html_file.read_text()
        html_file.write_text(ATTR.sub(lambda m: f'{m.group(1)}="{relative(m.group(2), base)}"', text))
