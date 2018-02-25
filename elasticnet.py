import pickle

import numpy as np

from sklearn.linear_model import ElasticNet

from sklearn.metrics import mean_absolute_error as mae

import random

import concurrent.futures

Xs, Ys = np.load('./Xs.np.npy'), np.load('./Ys.np.npy')
size = len(Xs)

Xs, Ys, Xst, Yst = Xs[:int(size*0.8)], Ys[:int(size*0.8)], Xs[int(size*0.8):], Ys[int(size*0.8):]


def _map(arg):
  param = arg
  
  alpha, l1_ratio = param
  elasticnet = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, selection='random', random_state=0)

  elasticnet.fit(Xs,Ys)

  yps = elasticnet.predict(Xst)

  name = (f'mae={mae(Yst, yps):018.09f}_alpha={alpha:0.4f}_l1_ratio={l1_ratio:0.4f}')

  print(name)

  open(f'models/{name}', 'wb').write( pickle.dumps(elasticnet) )


alphas    = [0.1*i for i in range(20)]
l1_ratios = [0.1*i for i in range(1,11)]
params = []
for alpha in alphas:
  for l1_ratio in l1_ratios:
    params.append( (alpha, l1_ratio) )
params = random.sample(params, len(params))
print(params)
with concurrent.futures.ProcessPoolExecutor(max_workers=3) as exe:
  exe.map(_map, params)
