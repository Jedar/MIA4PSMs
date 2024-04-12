import numpy as np
import matplotlib.pyplot as plt
import math
import numpy as np
import random
from collections import defaultdict

VISIBLE_PROB = 0.00008
POINT_SIZE=4
plt.switch_backend('agg')
plt.rcParams['font.sans-serif']=['SimHei']

Query_path = "xato_new.txt"

Paths = {
    "PCFG41":"",
    "LSTM":"",
    "CharBackoff":"",
    "CKLPCFG":"",
    "3gram": "",
    "4gram": "",
    "6gram": "",
    "8gram": "",
    "adaptive_markov": "",
    "ippsm": ""
}

def read_target(path):
    ans = set()
    dp = defaultdict(int)
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ans.add(line)
            dp[line] += 1
    return dp

def read_data(path, target, max_gn):
    X = []
    Y = []
    idx = 0
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            pwd = line
            gn = idx
            idx += 1
            # if pwd not in target:
            #     continue 
            if gn > max_gn:
                break 
            if random.random() < VISIBLE_PROB:
                if pwd in target:
                    X.append(idx / (10**7))
                else:
                    Y.append(idx / (10**7))
    return X, Y

def main():
    key = "PCFG41"
    output_figure = f'xato_{key}.pdf'
    
    target =read_target(Query_path)
    X, Y = read_data(Paths[key], target, 2.0*(10**7))

    print(f"{Paths[key]}, {Query_path}")
    
    X = np.random.choice(X, size=int(len(X)))
    Y = np.random.choice(Y, size=int(len(Y)))
    
    PX = np.random.rand((len(X)))
    PY = np.random.rand((len(Y)))
    
    # plt.axvline(x=Q, ls="-", c="b")
    # plt.gcf().subplots_adjust(bottom=0.2)
    plt.figure(figsize=(10, 3))
    plt.xlim((0, 2))
    plt.ylim((0, 1))
    plt.yticks([])
    plt.xticks([0, 0.4, 0.8, 1.2, 1.6, 2.0],fontsize=22)
    # plt.xticks([0, 0.5, 1.0],fontsize=22)
    
    plt.scatter(np.array(X), PX, color=["r"],s=[POINT_SIZE])
    plt.scatter(np.array(Y), PY, color=["g"], s=[POINT_SIZE])
    
    plt.xlabel(r'猜测数($ \times 10^7$)',fontsize=25)
    # plt.legend(loc = 'best')
    plt.savefig(output_figure, bbox_inches='tight')
    print(f"Figure saved in: {output_figure}")

if __name__ == '__main__':
    main()
