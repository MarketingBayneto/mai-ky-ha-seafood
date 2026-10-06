"""Search and sharing extras, added after the pages are built.

- Open Graph / Twitter tags so links shared on Zalo, Facebook, LinkedIn show a title, text and photo.
- Organization data (JSON-LD) on the home and contact pages for Google.
- sitemap.xml with both languages, robots.txt, and a 404 page.
"""
from pathlib import Path
from html import escape, unescape
import json, re
from english import ORIGIN

COMPANY = 'MAI KỲ HÀ SEAFOOD'
ORG = {
    '@context': 'https://schema.org', '@type': 'Organization',
    'name': COMPANY, 'legalName': 'Công ty TNHH Chế biến Thuỷ hải sản Mai Kỳ Hà',
    'url': ORIGIN + '/', 'logo': ORIGIN + '/assets/logo.png',
    'email': 'maikyhaseafood01@gmail.com', 'telephone': '+84 235 356 5568',
    'address': {'@type': 'PostalAddress', 'streetAddress': '452 Phạm Văn Đồng, Xã Núi Thành',
                'addressLocality': 'Đà Nẵng', 'addressCountry': 'VN'},
    'contactPoint': {'@type': 'ContactPoint', 'telephone': '+84 235 356 5568', 'email': 'maikyhaseafood01@gmail.com',
                     'contactType': 'sales', 'availableLanguage': ['Vietnamese', 'English']},
}
ORG_ADDRESS_EN = {'@type': 'PostalAddress', 'streetAddress': '452 Pham Van Dong, Nui Thanh Commune',
                  'addressLocality': 'Da Nang City', 'addressCountry': 'VN'}


def first(pattern, text):
    m = re.search(pattern, text, re.S)
    return unescape(m.group(1)) if m else ''


def text_of(html):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', html))).strip()


def page_description(text):
    """The page's own intro sentence, led by its heading when the sentence alone is short."""
    main = text.split('<main', 1)[-1]
    h1 = text_of(first(r'<h1[^>]*>(.*?)</h1>', main))
    lead = text_of(first(r'<p class="lead">(.*?)</p>', main))
    if not lead:
        return h1
    return lead if len(lead) >= 110 else f'{h1}. {lead}'


def share_image(dist, text):
    """A 1200x630 JPG of the page's first real photo; social apps read JPG more reliably than WebP."""
    from PIL import Image, ImageOps
    main = text.split('<main', 1)[-1]
    sources = [re.sub(r'^(\.\./|\./)+', '', s.split('?')[0]) for s in re.findall(r'<img[^>]+src="([^"]+)"', main)]
    sources = [s for s in sources if 'logo' not in s and s.endswith(('.webp', '.jpg', '.png'))] or ['assets/dong-hang-0.webp']
    source = dist / sources[0]
    if not source.exists():
        source = dist / 'assets' / 'logo.png'
    target = dist / 'assets' / 'share' / (source.stem + '.jpg')
    if not target.exists():
        target.parent.mkdir(exist_ok=True)
        with Image.open(source) as im:
            ImageOps.fit(im.convert('RGB'), (1200, 630), Image.LANCZOS, centering=(0.5, 0.45)).save(target, 'JPEG', quality=82, optimize=True, progressive=True)
    return f'{ORIGIN}/assets/share/{target.name}'


def add_tags(dist):
    urls = []
    for html_file in sorted(dist.rglob('index.html')):
        text = html_file.read_text()
        canonical = first(r'<link rel="canonical" href="([^"]+)"', text)
        title = first(r'<title>(.*?)</title>', text)
        lang = first(r'<html lang="([a-z]+)"', text)
        path = canonical[len(ORIGIN):]
        desc = first(r'<meta name="description" content="([^"]*)"', text)
        if path not in ('/', '/en/'):
            desc = page_description(text) or desc
            text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(desc)}">', text, count=1)
        image = share_image(dist, text)
        tags = ''.join([
            '<meta property="og:type" content="website">',
            f'<meta property="og:site_name" content="{COMPANY}">',
            f'<meta property="og:title" content="{escape(title)}">',
            f'<meta property="og:description" content="{escape(desc)}">',
            f'<meta property="og:url" content="{canonical}">',
            f'<meta property="og:image" content="{image}">',
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
            f'<meta property="og:locale" content="{"en_US" if lang == "en" else "vi_VN"}">',
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="theme-color" content="#052540">',
        ])
        if path in ('/', '/en/', '/lien-he/', '/en/contact/'):
            org = ORG if lang != 'en' else {**{k: v for k, v in ORG.items() if k != 'legalName'}, 'address': ORG_ADDRESS_EN}
            tags += '<script type="application/ld+json">' + json.dumps(org, ensure_ascii=False) + '</script>'
        html_file.write_text(text.replace('</head>', tags + '</head>', 1))
        alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', text)
        urls.append((canonical, alts))
    return urls


def write_sitemap(dist, urls):
    rows = []
    for loc, alts in sorted(urls, key=lambda u: (u[0].count('/'), u[0])):
        links = ''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{escape(u)}"/>' for h, u in alts)
        rows.append(f'<url><loc>{escape(loc)}</loc>{links}</url>')
    (dist / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(rows) + '\n</urlset>\n')
    (dist / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')


def write_404(dist):
    """A bilingual 'page not found' page. It can be served at any depth, so links start from the site root."""
    text = (dist / 'lien-he' / 'index.html').read_text()
    text = re.sub(r'(href|src|poster|data-photo)="\.\./', r'\1="/', text).replace('href="./"', 'href="/lien-he/"')
    text = re.sub(r'<link rel="(alternate|canonical)"[^>]*>', '', text)
    text = re.sub(r'<script type="application/ld\+json">.*?</script>', '', text)
    text = re.sub(r'<meta property="og:[^>]*>|<meta name="twitter:[^>]*>', '', text)
    text = re.sub(r'<title>.*?</title>', f'<title>Không tìm thấy trang | {COMPANY}</title><meta name="robots" content="noindex">', text)
    text = re.sub(r'<div class="language-switch".*?</div>', '', text, count=1, flags=re.S)
    body = ('<section class="page-intro sea"><div class="wrap"><p class="eyebrow">404</p>'
            '<h1>Không tìm thấy trang</h1><p class="lead">Trang bạn tìm có thể đã được đổi địa chỉ. '
            'Page not found — the page may have moved.</p><p class="not-found-links">'
            '<a class="button" href="/">Về trang chủ</a> <a class="button secondary light" href="/san-pham/">Xem sản phẩm</a> '
            '<a class="button secondary light" href="/en/">English site</a></p></div></section>')
    text = re.sub(r'<main id="main">.*</main>', f'<main id="main">{body}</main>', text, flags=re.S)
    (dist / '404.html').write_text(text)


def build_seo(dist):
    dist = Path(dist)
    urls = add_tags(dist)
    write_sitemap(dist, urls)
    write_404(dist)
    print('Added sharing tags to', len(urls), 'pages; wrote sitemap.xml, robots.txt and 404.html.')
