from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
D=Path(__file__).parent/'dist';errors=[];pages=list(D.rglob('*.html'))
class Check(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='img' and a.get('src') and not a.get('alt'):errors.append(f'{self.path}: missing alt')
  for k in ('src','href'):
   u=a.get(k,'');q=urlparse(u)
   if not u or q.scheme or u.startswith('#'):continue
   p=D/q.path.lstrip('/')
   if q.path.endswith('/'):p=p/'index.html'
   if not p.exists():errors.append(f'{self.path}: missing {u}')
for path in pages:
 c=Check();c.path=path;c.feed(path.read_text())
assert not errors,'\n'.join(errors)
assert len(pages)==56
print(f'Checked {len(pages)} pages: all local links and images resolve; image descriptions present.')
