from pathlib import Path

import json

import re

import MeCab

from collections import Counter

import pickle

import sys

import numpy as np

import re

import math

import dill
if '--step1' in sys.argv:
  m = MeCab.Tagger('-Owakati')
  term_id = {}
  data = []
  for name in Path('test').glob('*'):
    obj = (json.load(name.open()))
    income = int(re.search('(\d{1,})', obj['income']).group(1))
    explain = dict(Counter(m.parse(obj['explain']).strip().split()))
    detail  = dict(Counter(m.parse(obj['detail']).strip().split()))

    for term in explain.keys():
      if term_id.get(term) is None:
        term_id[term] = len(term_id)
    for term in detail.keys():
      if term_id.get(term) is None:
        term_id[term] = len(term_id)

    source = {}
    for term in explain.keys():
      if re.search(r'\d', term) is not None:
        continue
      if source.get(term) is None:
        source[term] = 0.0
      source[term] += explain[term]
    for term in detail.keys():
      if re.search(r'\d', term) is not None:
        continue
      if source.get(term) is None:
        source[term] = 0.0
      source[term] += detail[term]
    data.append( (income, source) )

  pickle.dump(data, open('make-sparse.pkl', 'wb'))
  json.dump(term_id, fp=open('term_id.json', 'w'), indent=2, ensure_ascii=False)

if '--step2' in sys.argv:
  sparse = pickle.load(open('make-sparse.pkl', 'rb')) 
    
  term_id = json.load(fp=open('term_id.json'))

  Xs = np.zeros( (len(sparse), len(term_id)), dtype=float ) 
  Ys = np.zeros( (len(sparse)), dtype=float)
  for index1, (y, term_freq) in enumerate(sparse):
    Ys[index1] = y
    for term, freq in term_freq.items():
      Xs[index1, term_id[term] ] = math.log(freq+1.0)
  np.save('Xs.np', Xs) 
  np.save('Ys.np', Ys)
