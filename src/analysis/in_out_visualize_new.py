import numpy as np
import matplotlib.pyplot as plt
import math
import numpy as np
plt.switch_backend('agg')

MAX_PROB = 100

Keys = ["PCFG41", "CKLPCFG", "CharBackoff", "CKLBackoff", "LSTM", "CKLLSTM"]
Keys = ["fuzzypsm"]
# Keys = ["PCFG41"]

Labels = {
    "PCFG41":"PCFG v4.1",
    "LSTM":"LSTM",
    "CharBackoff":"Backoff",
    "CKLBackoff":"CKL_Backoff",
    "CKLPCFG":"CKL_PCFG",
    "CKLLSTM":"CKL_LSTM",
    "fuzzypsm": "fuzzyPSM",
    "ippsm":"ippsm"
}  

# 178 #

Query_path=''
Query_path=''

TargetPaths = {
    "PCFG41":"",
    "LSTM":"",
    "CharBackoff":"",
    "CKLBackoff":"",
    "CKLPCFG": "",
    "CKLLSTM":"",
    "fuzzypsm":"",
    "ippsm":""
}

LogOps = {
    "PCFG41":0,
    "LSTM":2,
    "CharBackoff":0,
    "CKLBackoff":0,
    "CKLPCFG":0,
    "CKLLSTM":2,
    "fuzzypsm": 2,
    "ippsm": 1
}

def read_query_set(path):
    pwds = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            pwds.add(line)
    return pwds

def read_data(path, Q, logop=0):
    X = []
    Y = []
    Z = []
    def prob(x):
        x = float(x)
        if logop == 0:
            return x 
        if logop == 1:
            return -x
        return -math.log(x) if x < 1.0 and x > 0.0 else 1022
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n").strip('\t ')
            ss = line.split("\t")
            feature = [prob(x) for x in ss[1].split(",")]
            if feature[0] > MAX_PROB:
                continue
            label = 1 if ss[0] in Q else 0
            if label == 0:
                Y.append(feature[0])
            else:
                X.append(feature[0])
            Z.append((feature[0], label))
    Z = sorted(Z, key=lambda x:x[0])
    return X, Y, Z


def parse_data(data, stones):
    thresholds = [0] * len(stones)
    ans = []
    idx = 0
    positive = 0
    for i in range(len(stones)):
        while idx < len(data) and (positive / (idx if idx > 0 else 1) > stones[i] or idx == 0):
            if data[idx][1] == 1:
                positive += 1
            idx += 1
        if idx < len(data):
            thresholds[i] = data[idx][0]
        else:
            thresholds[i] = data[-1][0]
        print(thresholds[i], idx)
    return thresholds

def main():
    output_figure = ''
    
    stones = [0.99, 0.95, 0.9, 0.85, 0.8]
    
    Q = read_query_set(Query_path)

    for key in Keys:
        plt.rc('legend', fontsize=16)
        plt.figure(figsize=(10, 7))
        plt.tick_params(labelsize=10)
        plt.xticks([x for x in range(1, MAX_PROB, 5)], rotation=45)
        
        path = TargetPaths[key]
        
        print(f"Using path: {path}")
        
        X,Y,Z = read_data(path, Q, logop=LogOps[key])
        
        X = np.random.choice(X, size=int(len(X) / 1000))
        Y = np.random.choice(Y, size=int(len(Y) / 1000))
        
        PX = np.random.rand((len(X)))
        PY = np.random.rand((len(Y)))
        
        thresholds = parse_data(Z, stones)
        print(thresholds)
        
        for i in thresholds:
            plt.axvline(x=i,ls="-",c="b")
        
        plt.scatter(np.array(X), PX, color=["r"],s=[1])
        plt.scatter(np.array(Y), PY, color=["g"], s=[1])
        # plt.scatter(np.array(Y), PY, "g")

        plt.xlabel('Negative Logarithmic Probability',fontsize=24)
        plt.legend(loc = 'best')
        
        path = f''
        plt.savefig(path)
        print(f"Figure saved in: {path}")
        
        plt.clf()
    pass

if __name__ == '__main__':
    main()
