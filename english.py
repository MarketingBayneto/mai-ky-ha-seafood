from pathlib import Path
import json,re
ROOT=Path(__file__).parent
TRANSLATIONS=dict(line.split('\t',1) for line in (ROOT/'en_translations.tsv').read_text().splitlines() if '\t' in line)
PRODUCTS=json.loads((ROOT/'products.json').read_text())
def lower_name(en):
 # Lowercase for use mid-sentence, keeping proper nouns and acronyms intact.
 return en.lower().replace('(hgt)','(HGT)').replace('indian','Indian')
for p in PRODUCTS:
 en='Head-cut Scad (HGT)' if p['slug']=='ca-nuc-hgt' else p['en']
 TRANSLATIONS[p['name']]=en
 TRANSLATIONS[p['name']+' — hình ảnh thực tế']=en+' — actual product photo'
 TRANSLATIONS['Bạn cần thêm thông tin về '+p['name'].lower()+'?']='Need more information about '+lower_name(en)+'?'
 TRANSLATIONS['Làm rõ yêu cầu cho '+p['name'].lower()]='Clarify your '+lower_name(en)+' requirements'
 TRANSLATIONS['MAI KỲ HÀ tiếp nhận yêu cầu giao dịch '+p['name'].lower()+' theo quy cách, khối lượng và điều kiện cụ thể.']='MAI KỲ HÀ welcomes inquiries for '+lower_name(en)+' based on your specifications, quantity and trading requirements.'
def translate(text):
 if text in TRANSLATIONS:return TRANSLATIONS[text]
 if text.startswith('Xem ảnh lớn: '):return 'Enlarge photo: '+translate(text[13:])
 if text.endswith(' | MAI KỲ HÀ'):return translate(text[:-12])+' | MAI KỲ HÀ'
 if re.search('[À-ỹĐđ]',text.replace('MAI KỲ HÀ','')):raise ValueError(text)
 return text
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit,urlunsplit

ROUTES={'/':'/en/','/gioi-thieu/':'/en/about/','/san-pham/':'/en/products/','/thuong-mai-xnk/':'/en/trading/','/nang-luc/':'/en/capabilities/','/hoat-dong/':'/en/activities/','/hoat-dong/hoi-cho/':'/en/activities/exhibitions/','/kien-thuc/':'/en/resources/','/kien-thuc/hoi-hang/':'/en/resources/seafood-inquiry/','/kien-thuc/quy-cach/':'/en/resources/specifications/','/kien-thuc/dieu-kien-giao-dich/':'/en/resources/trading-terms/','/lien-he/':'/en/contact/'}
for p in PRODUCTS:
 slug='head-cut-scad' if p['slug']=='ca-nuc-hgt' else re.sub(r'[^a-z0-9]+','-',p['en'].lower()).strip('-')
 ROUTES['/san-pham/'+p['slug']+'/']='/en/products/'+slug+'/'
TRANSLATIONS['Sản phẩm']='Products'

def polish_english(html):
 # The form's product field selects one product.
 html=html.replace('<label>Products<select name="product"','<label>Product<select name="product"')
 # English cards would repeat the product name as their subtitle; keep only the heading.
 html=re.sub(r'(<h3>([^<]+)</h3>)<p>([^<]+)</p>',lambda m:m.group(1) if m.group(3).lower() in m.group(2).lower() else m.group(0),html)
 return html

def english_url(url):
 parts=urlsplit(url)
 if not parts.scheme and not parts.netloc and parts.path in ROUTES:
  return urlunsplit(('', '', ROUTES[parts.path],parts.query,parts.fragment))
 return url

class EnglishHTML(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.out=[]
 def handle_decl(self,decl):self.out.append('<!'+decl+'>')
 def handle_starttag(self,tag,attrs):
  original=dict(attrs);result=[]
  for key,value in attrs:
   if value is not None:
    if key=='lang' and tag=='html':value='en'
    elif key=='href':value=english_url(value)
    elif key in ['alt','aria-label','placeholder','data-caption','data-name'] and value:value=translate(value)
    elif key=='content' and tag=='meta' and original.get('name')=='description':value=translate(value)
   result.append(key if value is None else key+'="'+escape(value,quote=True)+'"')
  self.out.append('<'+tag+(' '+' '.join(result) if result else '')+'>')
 def handle_endtag(self,tag):self.out.append('</'+tag+'>')
 def handle_data(self,data):
  value=data.strip()
  self.out.append(escape(data.replace(value,translate(value),1) if value else data,quote=False))
 def handle_comment(self,data):self.out.append('<!--'+data+'-->')

import os
# Public address of the site, without a trailing slash. Used only for canonical and hreflang tags.
ORIGIN=os.environ.get('SITE_URL','https://marketingbayneto.github.io/mai-ky-ha-seafood').rstrip('/')
def language_chrome(html,vi,en,lang):
 links=''.join(f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{url}">' for code,url in [('vi',vi),('en',en),('x-default',vi)])
 links+=f'<link rel="canonical" href="{ORIGIN}{en if lang=="en" else vi}">'
 html=html.replace('</head>',links+'</head>')
 label='Website language' if lang=='en' else 'Ngôn ngữ website'
 switch=f'<div class="language-switch" role="group" aria-label="{label}"><a href="{vi}" lang="vi" hreflang="vi" data-language-switch aria-label="Tiếng Việt"'+(' aria-current="true"' if lang=='vi' else '')+'>VI</a><span aria-hidden="true">/</span>'+f'<a href="{en}" lang="en" hreflang="en" data-language-switch aria-label="English"'+(' aria-current="true"' if lang=='en' else '')+'>EN</a></div>'
 return html.replace('<button class="menu-toggle"',switch+'<button class="menu-toggle"',1)

def build_languages(dist):
 for vi,en in ROUTES.items():
  source=dist/vi.lstrip('/')/'index.html'
  html=source.read_text()
  parser=EnglishHTML();parser.feed(html);parser.close();translated=''.join(parser.out)
  # International dialing format for English readers; telephone targets stay unchanged.
  translated=polish_english(translated.replace('>0235 356 5568<','>+84 235 356 5568<'))
  target=dist/en.lstrip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(language_chrome(translated,vi,en,'en'))
  source.write_text(language_chrome(html,vi,en,'vi'))
 print('Built',len(ROUTES),'English pages with paired language navigation.')
