import MeCab

from pathlib import Path

import json

import re

import statistics

m = MeCab.Tagger('-Ochasen')

term_incomes = {}
for name in Path('./test').glob('*'):
  obj = json.load(name.open())
  income = int(re.search(r'(\d{1,})', obj['income']).group(1)) 
  explain = (obj['explain'])
  
  terms = [line.split('\t').pop(0) for line in m.parse(explain).strip().split('\n') if '固有名詞' in line and re.search(r'\d', line) is None]
  for term in terms:
    if term_incomes.get(term) is None:
      term_incomes[term] = []
    term_incomes[term].append( income )

term_ave = [ (term, statistics.mean(incomes)) for term, incomes in term_incomes.items() if len(incomes) > 5 ]

for term, ave in sorted( term_ave, key=lambda x:x[1]*-1):
  print(term, ave)
