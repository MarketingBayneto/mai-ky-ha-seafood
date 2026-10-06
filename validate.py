from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,urljoin
D=Path(__file__).parent/'dist';errors=[];pages=list(D.rglob('index.html'))
class Check(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='img' and a.get('src') and not a.get('alt'):errors.append(f'{self.path}: missing alt')
  for k in ('src','href'):
   u=a.get(k,'');q=urlparse(u)
   if not u or q.scheme or u.startswith('#'):continue
   if u.startswith('/'):errors.append(f'{self.path}: root-absolute link {u}')
   q=urlparse(urljoin(self.url,u))
   p=D/q.path.lstrip('/')
   if q.path.endswith('/'):p=p/'index.html'
   if not p.exists():errors.append(f'{self.path}: missing {u}')
for path in pages:
 c=Check();c.path=path;rel=path.parent.relative_to(D).as_posix();c.url='/' if rel=='.' else '/'+rel+'/';c.feed(path.read_text())
assert not errors,'\n'.join(errors)
import json
assert len(pages)==2*(12+len(json.loads((Path(__file__).parent/"products.json").read_text())))
# The 404 page is served at any depth, so its links start from the site root.
nf=(D/'404.html').read_text()
import re
for u in re.findall(r'(?:href|src)="(/[^"/][^"]*|/)"',nf):
 p=D/urlparse(u).path.lstrip('/')
 if not (p/'index.html' if str(u).endswith('/') else p).exists():errors.append('404.html: missing '+u)
assert not errors,'\n'.join(errors)
for f in ('sitemap.xml','robots.txt'):assert (D/f).exists(),f
assert (D/'sitemap.xml').read_text().count('<loc>')==len(pages)
print(f'Checked {len(pages)} pages: all local links and images resolve; image descriptions present.')
