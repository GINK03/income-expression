
from pathlib import Path

import bs4

import gzip

import concurrent.futures

import re

import hashlib

import json
def _map(arg):
  key, names = arg

  for name in names:
    try:
      html = gzip.decompress(name.open('rb').read())
      soup = bs4.BeautifulSoup(html)

      icon_disp = soup.find('h1', {'class':'iconDisp'})

      article = soup.find('article', {'class':'main1024'})

      explain = soup.find('p', {'class':'explain'})
      
      detail = soup.find('div', {'id':'shtTabContent1'})

      if article is None or explain is None or detail is None:
        continue

      icon_disp = re.sub(r'\s{1,}', ' ', icon_disp.text)
      explain = re.sub(r'\s{1,}', ' ', explain.text)
      detail = re.sub(r'\s{1,}', ' ', detail.text)

      print(name)
      print(icon_disp)
      # print(article)

      trs = soup.find_all('tr')
      for tr in trs:
        th = tr.find('th')

        if th is not None and '給与' in th.text:
          text =(re.sub(r'\s{1,}', ' ', tr.find('td').text))
          match = re.search(r'年収.*?(\d{1,}万円)', text)
          if match is None:
            continue
          print(text)
          print(icon_disp)
          print(explain)
          print(match.group(1))
          ha = hashlib.sha256(bytes(icon_disp, 'utf8')).hexdigest()
          obj = {'icon_disp':icon_disp, 'income':match.group(1), 'explain':explain, 'detail':detail}
          Path(f'test/{ha}').open('w').write( json.dumps(obj, indent=2, ensure_ascii=False) )
    except Exception as ex:
      print(ex)

args = {}
for index, name in enumerate(Path('../scraping-designs/doda-scrape/htmls').glob('*')):
  key = index%16
  if args.get(key) is None:
    args[key] = []
  args[key].append( name)
args = [(key,names) for key, names in args.items()]
# _map(args[0])
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  exe.map(_map, args)
