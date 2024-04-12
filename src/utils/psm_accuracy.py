from collections import defaultdict
import random
import scipy
import numpy as np
import pandas as pd
from scipy.stats import rankdata
import argparse
import math
import json

RANDOM_NUM = 100

class WeightedCorr:
    def __init__(self, xyw=None, x=None, y=None, w=None, df=None, wcol=None):
        ''' Weighted Correlation class. Either supply xyw, (x, y, w), or (df, wcol). Call the class to get the result, i.e.:
        WeightedCorr(xyw=mydata[[x, y, w]])(method='pearson')
        :param xyw: pd.DataFrame with shape(n, 3) containing x, y, and w columns (column names irrelevant)
        :param x: pd.Series (n, ) containing values for x
        :param y: pd.Series (n, ) containing values for y
        :param w: pd.Series (n, ) containing weights
        :param df: pd.Dataframe (n, m+1) containing m phenotypes and a weight column
        :param wcol: str column of the weight column in the dataframe passed to the df argument.
        '''
        if (df is None) and (wcol is None):
            if np.all([i is None for i in [xyw, x, y, w]]):
                raise ValueError('No data supplied')
            if not ((isinstance(xyw, pd.DataFrame)) != (np.all([isinstance(i, pd.Series) for i in [x, y, w]]))):
                raise TypeError('xyw should be a pd.DataFrame, or x, y, w should be pd.Series')
            xyw = pd.concat([x, y, w], axis=1).dropna() if xyw is None else xyw.dropna()
            self.x, self.y, self.w = (pd.to_numeric(xyw[i], errors='coerce').values for i in xyw.columns)
            self.df = None
        elif (wcol is not None) and (df is not None):
            if (not isinstance(df, pd.DataFrame)) or (not isinstance(wcol, str)):
                raise ValueError('df should be a pd.DataFrame and wcol should be a string')
            if wcol not in df.columns:
                raise KeyError('wcol not found in column names of df')
            self.df = df.loc[:, [x for x in df.columns if x != wcol]]
            self.w = pd.to_numeric(df.loc[:, wcol], errors='coerce')
        else:
            raise ValueError('Incorrect arguments specified, please specify xyw, or (x, y, w) or (df, wcol)')

    def _wcov(self, x, y, ms):
        return np.sum(self.w * (x - ms[0]) * (y - ms[1]))

    def _pearson(self, x=None, y=None):
        x, y = (self.x, self.y) if ((x is None) and (y is None)) else (x, y)
        mx, my = (np.sum(i * self.w) / np.sum(self.w) for i in [x, y])
        return self._wcov(x, y, [mx, my]) / np.sqrt(self._wcov(x, x, [mx, mx]) * self._wcov(y, y, [my, my]))

    def _wrank(self, x):
        (unique, arr_inv, counts) = np.unique(rankdata(x), return_counts=True, return_inverse=True)
        a = np.bincount(arr_inv, self.w)
        return (np.cumsum(a) - a)[arr_inv]+((counts + 1)/2 * (a/counts))[arr_inv]

    def _spearman(self, x=None, y=None):
        x, y = (self.x, self.y) if ((x is None) and (y is None)) else (x, y)
        return self._pearson(self._wrank(x), self._wrank(y))

    def __call__(self, method='pearson'):
        '''
        :param method: Correlation method to be used: 'pearson' for pearson r, 'spearman' for spearman rank-order correlation.
        :return: if xyw, or (x, y, w) were passed to __init__ returns the correlation value (float).
                 if (df, wcol) were passed to __init__ returns a pd.DataFrame (m, m), the correlation matrix.
        '''
        if method not in ['pearson', 'spearman']:
            raise ValueError('method should be one of [\'pearson\', \'spearman\']')
        cor = {'pearson': self._pearson, 'spearman': self._spearman}[method]
        if self.df is None:
            return cor()
        else:
            out = pd.DataFrame(np.nan, index=self.df.columns, columns=self.df.columns)
            for i, x in enumerate(self.df.columns):
                for j, y in enumerate(self.df.columns):
                    if i >= j:
                        out.loc[x, y] = cor(x=pd.to_numeric(self.df[x], errors='coerce'), y=pd.to_numeric(self.df[y], errors='coerce'))
                        out.loc[y, x] = out.loc[x, y]
            return out

def read_sample_pwds(path):
    pwds = []
    # 口令，采样频次，总频次
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            ss = line.split("\t")
            pwds.append((ss[0], int(ss[1]), int(ss[2])))
    return pwds

def read_pwds(path):
    pwds = defaultdict(int)
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            if line.find(" ") != -1:
                # print(f"Skip {line}")
                continue
            pwds[line] += 1
    return pwds

def read_probs(path, gn_idx=3):
    pwds = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ss = line.split("\t")
            pwds[ss[0]] = float(ss[gn_idx])
    return pwds

def nnmia_read_probs(path):
    pwds = []
    with open(path, "r") as f:
        for line in f:
            final_prob = 0.0
            line = line.strip("\r\n").split("\t")
            pwd = line[0]
            probs = json.loads(line[1])
            for prob in probs:
                if prob[0] <= 0:
                    logprob = 50
                else:    
                    logprob = -math.log2(prob[0])
                final_prob += logprob
            pwds.append((pwd, final_prob))
    return pwds

def nnmia_read_probs1(path):
    pwds = []
    with open(path, "r") as f:
        for line in f:
            final_prob = 0.0
            line = line.strip("\r\n").split("\t")
            pwd = line[0]
            prob = float(line[1])
            pwds.append((pwd, prob))
    return pwds

def sample_data(data):
    random.seed(48)
    keys = [x for x in data.keys()]
    random.shuffle(keys)
    keys = keys[:RANDOM_NUM]
    values = [-data[x] for x in keys]
    return keys, values

def weight_spearman(freqs, strength):
    weight = [x for x in freqs]
    values = strength
    targets = [-x for x in freqs]
    data_array = np.array([targets, values, weight]).T
    data_frame = pd.DataFrame(data_array,index=None,columns = ['x', 'y', 'w'])
    corr = WeightedCorr(x=data_frame['x'], y=data_frame['y'], w=data_frame['w'])("spearman")
    print(f"Weight Spearman Corr: {corr}")

def init_cli():
    cli = argparse.ArgumentParser("Spearman")
    cli.add_argument("-p", "--pwd", dest="pwd", type=str)
    cli.add_argument("-m", "--model", dest="model", type=str)
    args = cli.parse_args()
    return args

def main():
    args = init_cli()
    print(f">>> Read PSM Result")
    psm = nnmia_read_probs1(args.model)
    print(f">>> Evaluated Passwords: {len(psm)}")

    print(f">>> Read Target Passwords")
    targets = read_pwds(args.pwd)

    pwds = [x[0] for x in psm]
    
    freqs = [targets[x] for x in pwds]

    print(freqs[:10])

    scores = [x[1] for x in psm]

    weight_spearman(freqs, scores)

if __name__ == '__main__':
    main()
