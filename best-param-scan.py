import pickle

from pathlib import Path

import json

best = sorted(Path('models/').glob('*')).pop(0)

elastic = pickle.load(best.open('rb'))

term_id = json.load(fp=open('term_id.json'))
id_term = { id:term for term, id in term_id.items() }

term_weight = {}
for index, weight in enumerate(elastic.coef_.tolist()):
  term = id_term[index]   
  if abs(weight) > 0.01:
    term_weight[term] = weight

for term, weight in sorted(term_weight.items(), key=lambda x:x[1]*-1):
  print(term, weight)

  
