import matplotlib.pyplot as plt
import matplotlib
import pickle
import os,sys

plt.switch_backend('agg')
plt.rcParams['font.sans-serif']=['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

FONTSIZE=22
ROTATION=30
LEGEND_LOC=(1, 0.4)
FIG_SIZE=(9, 4)
WIDTH = 0.2

METHODS = [
    "threshold_attack", 
    "classifier_attack", 
    "salem_attack"
]

METHOD_NAME = {
    "threshold_attack": r"概率阈值($t=80%$)", 
    "classifier_attack": r"二元分类器($F(w|M)$)", 
    "salem_attack": r"Salem等人($k=10$)"
}

Keys = ["4gram","adaptive_markov", "CharBackoff","PCFG41","fuzzypsm", "CKLPCFG", "LSTM", "ippsm"]

Labels = {
    "PCFG41":"PCFG_Cracker",
    "LSTM":"FLA PSM",
    "CharBackoff":"Backoff",
    "CKLPCFG":"CKL_PSM",
    "4gram": "4gram",
    "fuzzypsm":"fuzzyPSM",
    "adaptive_markov": "Adaptive PSM",
    "ippsm": "IPPSM"
}  

METRICS = ["accuracy", "precision", "recall"]

METRICS_NAME = {
    "accuracy": r"准确率($Accuracy$)", 
    "precision": r"精确率($Precision$)", 
    "recall": r"召回率($Recall$)"
}

COLORS = {
    "threshold_attack": "steelblue", 
    "classifier_attack": "mediumseagreen", 
    "salem_attack": "indianred"
}

DATA = {
    "threshold_attack": {
        "4gram": {
            "accuracy": 0.911, 
            "precision": 0.918, 
            "recall": 0.236
        },
        "adaptive_markov": {
            "accuracy": 0.901, 
            "precision": 0.948, 
            "recall": 0.139
        },
        "CharBackoff":{
            "accuracy": 0.947, 
            "precision": 0.893, 
            "recall": 0.608
        },
        "PCFG41":{
            "accuracy": 0.969, 
            "precision": 0.802, 
            "recall": 0.965
        },
        "fuzzypsm":{
            "accuracy": 0.911, 
            "precision": 0.967, 
            "recall": 0.220
        },
        "CKLPCFG":{
            "accuracy":0.937, 
            "precision": 0.836, 
            "recall": 0.555
        },
        "LSTM":{
            "accuracy": 0.924, 
            "precision": 0.764, 
            "recall": 0.481
        },
        "ippsm": {
            "accuracy": 0.891, 
            "precision": 0.824, 
            "recall": 0.045
        }
    },
    "classifier_attack": {
        "4gram": {
            "accuracy": 0.921, 
            "precision": 0.745, 
            "recall": 0.329
        },
        "adaptive_markov": {
            "accuracy": 0.908, 
            "precision": 0.740, 
            "recall": 0.253
        },
        "CharBackoff":{
            "accuracy": 0.937, 
            "precision": 0.870, 
            "recall": 0.546
        },
        "PCFG41":{
            "accuracy": 0.947, 
            "precision": 0.769, 
            "recall": 0.882
        },
        "fuzzypsm":{
            "accuracy": 0.903, 
            "precision": 0.983, 
            "recall": 0.145
        },
        "CKLPCFG":{
            "accuracy": 0.922, 
            "precision": 0.976, 
            "recall": 0.317
        },
        "LSTM":{
            "accuracy": 0.921, 
            "precision": 0.780, 
            "recall": 0.393
        },
        "ippsm": {
            "accuracy": 0.916, 
            "precision": 0.754, 
            "recall": 0.379
        }
    },
    "salem_attack": {
        "4gram": {
            "accuracy": 0.902, 
            "precision": 0.679, 
            "recall": 0.601
        },
        "adaptive_markov": {
            "accuracy": 0.902, 
            "precision": 0.676, 
            "recall": 0.599
        },
        "CharBackoff":{
            "accuracy": 0.906, 
            "precision": 0.797, 
            "recall": 0.706
        },
        "PCFG41":{
            "accuracy": 0.945, 
            "precision": 0.939, 
            "recall": 0.832
        },
        "fuzzypsm":{
            "accuracy": 0.906, 
            "precision": 0.597, 
            "recall": 0.529
        },
        "CKLPCFG":{
            "accuracy": 0.911, 
            "precision": 0.771, 
            "recall": 0.683
        },
        "LSTM":{
            "accuracy": 0.904, 
            "precision": 0.687, 
            "recall": 0.609
        },
        "ippsm": {
            "accuracy": 0.896, 
            "precision": 0.545, 
            "recall": 0.483
        }
    }
}

def draw_bars(metric, data, save_path):
    plt.cla()
    plt.figure(figsize=FIG_SIZE)
    
    X_tick = [Labels[x] for x in Keys]
    X_base = [x for x in range(len(Keys))]
    
    # "threshold_attack", 
    # "classifier_attack", 
    # "salem_attack"
    
    idx = -1
    for attack in METHODS:
        Y = [data[attack][key][metric] for key in Keys]
        X = [x+idx*WIDTH for x in X_base]
        plt.bar(X, Y,color=COLORS[attack], width=WIDTH)
        
        idx += 1
        
    plt.ylim((0, 1))
    
    plt.xticks(X_base, X_tick, fontsize=FONTSIZE-2, rotation=ROTATION)
    plt.yticks([x*0.2 for x in range(6)], fontsize=FONTSIZE-2)
    # plt.rc('legend', fontsize=22)
    # plt.xlabel(r'成员占比$t$',fontsize=FONTSIZE)
    plt.ylabel(f'{METRICS_NAME[metric]}',fontsize=FONTSIZE)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Figure saved in {save_path}")
    pass

def draw_f1(data, save_path):
    plt.cla()
    plt.figure(figsize=FIG_SIZE)
    
    X_tick = [Labels[x] for x in Keys]
    X_base = [x for x in range(len(Keys))]
    
    # "threshold_attack", 
    # "classifier_attack", 
    # "salem_attack"

    def f1(p, r):
        return (1+0.5**2)*p*r / (0.5**2*p + r)
    
    idx = -1
    for attack in METHODS:
        Y = [f1(data[attack][key]["precision"], data[attack][key]["recall"]) for key in Keys]
        X = [x+idx*WIDTH for x in X_base]
        plt.bar(X, Y,color=COLORS[attack], width=WIDTH)
        
        idx += 1
        
    plt.ylim((0, 1))
    
    plt.xticks(X_base, X_tick, fontsize=FONTSIZE-2, rotation=ROTATION)
    plt.yticks([x*0.2 for x in range(6)], fontsize=FONTSIZE-2)
    # plt.rc('legend', fontsize=22)
    # plt.xlabel(r'成员占比$t$',fontsize=FONTSIZE)
    plt.ylabel(f'F1',fontsize=FONTSIZE)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Figure saved in {save_path}")
    pass

def main():
    save_base = ""
    
    for metric in METRICS:
        save_path = f"{save_base}/comparison_178_{metric}.pdf"
        draw_bars(metric, DATA, save_path)
    save_path = f"{save_base}/comparison_178_f1.pdf"
    draw_f1(DATA, save_path)
    pass

if __name__ == '__main__':
    main()

