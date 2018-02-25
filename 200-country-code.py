import MeCab

from pathlib import Path

import json

import re

import statistics

m = MeCab.Tagger('-Owakati')

cs = [c.strip() for c in open('misc/都道府県.txt')]
term_incomes = {}
for name in Path('./test').glob('*'):
  obj = json.load(name.open())
  income = int(re.search(r'(\d{1,})', obj['income']).group(1)) 
  explain = (obj['explain'])
 
  terms = [term for term in m.parse(explain).strip().split() if term in cs]
  for term in terms:
    if term_incomes.get(term) is None:
      term_incomes[term] = []
    term_incomes[term].append( income )

term_ave = [ (term, statistics.mean(incomes)) for term, incomes in term_incomes.items() if len(incomes) > 5 ]

for term, ave in sorted( term_ave, key=lambda x:x[1]*-1):
  print(term, int(ave))
