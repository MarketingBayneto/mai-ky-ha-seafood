from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,parse_qs
import sys,re,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from english import ROUTES
D=Path('dist')
class Page(HTMLParser):
 def __init__(self):super().__init__();self.lang=None;self.links=[];self.ids=[];self.h1=0;self.text=[];self.labels=[];self.options=[];self.alternates={};self.meta='';self.disabled=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='html':self.lang=a['lang']
  if t=='h1':self.h1+=1
  if 'id' in a:self.ids.append(a['id'])
  if t=='a':self.links.append(a)
  if t=='option':self.options.append(a.get('value'))
  if t=='meta' and a.get('name')=='description':self.meta=a['content']
  if t=='link' and a.get('rel')=='alternate':self.alternates[a['hreflang']]=urlsplit(a['href']).path
  for k in ['alt','aria-label','placeholder','data-caption']:
   if a.get(k):self.text.append(a[k])
 def handle_data(self,d):self.text.append(d)

def read(route):
 p=Page();p.feed((D/route.lstrip('/')/'index.html').read_text());return p
products={p['slug'] for p in json.loads(Path('products.json').read_text())}
for vi,en in ROUTES.items():
 for lang,route in [('vi',vi),('en',en)]:
  p=read(route);assert p.lang==lang;assert p.h1==1;assert len(p.ids)==len(set(p.ids));assert p.meta
  assert p.alternates['vi']==vi and p.alternates['en']==en
  switches=[a for a in p.links if 'data-language-switch' in a];assert {a['href'] for a in switches}=={vi,en}
  assert len([a for a in switches if a.get('aria-current')=='true'])==1
  for a in p.links:
   u=urlsplit(a['href'])
   if a['href'].startswith('#'):assert u.fragment in p.ids
   if 'san-pham' in parse_qs(u.query):assert parse_qs(u.query)['san-pham'][0] in products
   if lang=='en' and u.path.startswith('/') and 'data-language-switch' not in a:assert u.path.startswith('/en/'),(route,u.path)
  if lang=='en':
   for text in p.text+[p.meta]:
    text=text.replace('MAI KỲ HÀ','').replace('Tiếng Việt','').replace('×','')
    assert not re.search('[À-ỹĐđ]',text),(route,text)
assert products<=set(read('/en/contact/').options)
assert products<=set(read('/lien-he/').options)
print('PASS: 56 language declarations, reciprocal switches, translated text/attributes, links, anchors and inquiry options.')
