import MeCab

from pathlib import Path

import json

import re
m = MeCab.Tagger('-Owakati')

term_chaine = {}
for name in Path('./test').glob('*'):
  obj = json.load(name.open())
  income = int(re.search(r'(\d{1,})', obj['income']).group(1)) // 50
  explain = (obj['explain'])
  
  for term in m.parse(explain).strip().split():
    if term_chaine.get(term) is None:
      term_chaine[term] = {}

    if term_chaine[term].get( income ) is None:
      term_chaine[term][income] = 0
    term_chaine[term][income] += 1


for term, chaine in sorted(term_chaine.items(), key=lambda x: -1*sum(x[1].values())):
  print(term)
  for income, freq in sorted(chaine.items()):
    print(income*50, freq)

