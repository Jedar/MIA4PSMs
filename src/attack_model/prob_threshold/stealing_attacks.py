import argparse 
import math
from collections import defaultdict

Keys = ["4gram","adaptive_markov", "CharBackoff","PCFG41","fuzzypsm", "CKLPCFG", "LSTM", "ippsm"]

mode = 'gan'
data = 'xato'
target="rockyou_new.txt"
attack_dataset = f"{data}_new.txt"

Paths={
    "adaptive_markov": f'markov_new.csv',
    "CharBackoff":f'backoff_new.csv',
    "4gram": f'4gram_new.csv',
    "fuzzypsm":f'fuzzypsm_new.csv',
    "PCFG41":f'pcfg41_new.csv',
    "CKLPCFG":f'cklpcfg_new.csv',
    "LSTM":f'lstm_new.csv',
    "ippsm": f'ppsm.csv'
}

thresholds = {
    "4gram": {
        "xato": 24.19,
        "178": 22.68878064
    },
    "adaptive_markov": {
        "xato": 25.22,
        "178": 23.00
    },
    "CharBackoff":{
        "xato": 24.99,
        "178": 23.25
    },
    "PCFG41":{
        "xato": 24.92,
        "178": 24.62
    },
    "fuzzypsm":{
        "xato": 24.92,
        "178": 20.92
    },
    "CKLPCFG":{
        "xato": 21.35,
        "178": 25.06
    },
    "LSTM":{
        "xato": 16.55,
        "178": 16.23
    },
    "ippsm": {
        "xato": 12.02,
        "178": 6.36
    }
}

def read_crack_result(key, path, attack_data, target, threshold, prob_idx=1):
    ans = []
    total_cnt = 0
    hit_cnt = 0
    inner_cnt = 0
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ss = line.split("\t")
            pwd = ss[0]
            prob = float(ss[prob_idx])
            if prob < threshold:
                total_cnt += 1
            if pwd in target and prob < threshold:
                hit_cnt += 1
                if pwd in attack_data:
                    inner_cnt += 1
    print(f"Key: {key}")
    print(f"Total Count: {total_cnt}")
    print(f"Hit Count: {hit_cnt}")
    print(f"Inner Count: {inner_cnt}")
    print(f"Outer Count: {hit_cnt - inner_cnt}")

def read_target_pwds(path, cnt_threshold=0):
    ans = defaultdict(int)
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ans[line] += 1
    return ans

def main():
    stones = [0.1,0.6, 0.7, 0.8, 0.9]
    target_data = read_target_pwds(target)
    attack_data = read_target_pwds(attack_dataset)
    
    print(f"Data: {data}")
    print(f"Mode: {mode}")

    for key in Keys:
        read_crack_result(key, Paths[key], attack_data, target_data, thresholds[key][data], prob_idx=1)

if __name__ == '__main__':
    main()
