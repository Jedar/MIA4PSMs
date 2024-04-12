import enum
from sklearn.model_selection import train_test_split # 拆分数据
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support, classification_report
from sklearn.metrics import auc
import math
import pickle
import os,sys

plt.switch_backend('agg')

SHADOW_TRAIN = "xato_shadow_train.txt"
TARGET_TRAIN = "rockyou_new.txt"

Labels = {
    "PCFG41":"V4.1_PCFG",
    "LSTM":"LSTM",
    "CharBackoff":"Backoff",
    "CKLPCFG":"CKL_PCFG",
    "4gram": "4-gram",
    "fuzzypsm":"fuzzyPSM",
    "adaptive_markov": "AdaptiveMarkov",
    "ippsm": "InterpretablePSM"
}  

SHADOW_RESULTS = {
    "4gram": "t_xato_q_xato_e_shadow_m_markov4_p.csv", 
    "adaptive_markov": "t_xato_q_xato_e_shadow_m_apsm_p.csv", 
    "CharBackoff": "t_xato_q_xato_e_shadow_m_backoff_p.csv", 
    "PCFG41": "t_xato_q_xato_e_shadow_m_pcfg41_p.csv",
    "fuzzypsm": "t_xato_q_xato_e_shadow_m_fuzzypsm_p.csv",
    "CKLPCFG": "t_xato_q_xato_e_shadow_m_cklpsm_p.csv.csv",
    "LSTM": "t_xato_q_xato_e_shadow_m_lstm_p.csv",
    "ippsm": "t_xato_q_xato_e_shadow_m_ippsm_p.csv"
}

QUERY_RESULTS = {
    "4gram": "t_rockyou_q_xato_e_target_m_markov4_p.csv", 
    "adaptive_markov": "t_rockyou_q_xato_e_target_m_apsm_p.csv", 
    "CharBackoff": "t_rockyou_q_xato_e_target_m_backoff_p.csv", 
    "PCFG41": "t_rockyou_q_xato_e_target_m_pcfg41_p.csv",
    "fuzzypsm": "t_rockyou_q_xato_e_target_m_fuzzypsm_p.csv",
    "CKLPCFG": "t_rockyou_q_xato_e_target_m_cklpsm_p.csv.csv",
    "LSTM": "t_rockyou_q_xato_e_target_m_lstm_p.csv",
    "ippsm": "t_rockyou_q_xato_e_target_m_ippsm_p.csv"
}

def read_passwords(path):
    ans = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            ans.add(line)
    return ans

def read_data(path, Q):
    X = []
    def prob(x):
        x = float(x)
        return x
    with open(path, "r") as f:
        for line in f:
            try:
                line = line.strip("\r\n").strip('\t ')
                ss = line.split("\t")
                pwd = ss[0]
                feature = prob(ss[1])
                X.append((feature,1 if pwd in Q else 0))
            except Exception as e:
                # print(f"Error parse: {line}")
                continue
    X = sorted(X, key=lambda x:x[0])
    return X

def compute_thresholds(data, stones):
    thresholds = [data[0][0]] * len(stones)
    ans = []
    idx = 0
    positive = 0
    
    for i in range(len(data)):
        positive += data[i][1]
        p = positive / (i if i > 0 else 1)
        for j in range(len(stones)):
            if p > stones[j]:
                thresholds[j] = data[i][0]
    return thresholds

def mark_data(X, threshold):
    X = [x[0] for x in X]
    ans = []
    for i in X:
        if i > threshold:
            ans.append(0)
        else:
            ans.append(1)
    return np.array(ans)

def calculate(key, stones, shadow_train, target_train):
    print(key)
    
    shadow_query = SHADOW_RESULTS[key]
    target_query = QUERY_RESULTS[key]
    
    shadow_data = read_data(shadow_query, shadow_train)
    target_data = read_data(target_query, target_train)
    
    thresholds = compute_thresholds(shadow_data, stones)
    
    A = [0] * len(stones)
    P = [0] * len(stones)
    
    R = [0] * len(stones)
    F1 = [0] * len(stones)
    
    Y = [x[1] for x in target_data]
    
    for i in range(len(stones)):
        predict = mark_data(target_data, thresholds[i])
        
        ans = precision_recall_fscore_support(Y, predict)
        A[i] = accuracy_score(Y, predict)
        P[i] = ans[0][1]
        R[i] = ans[1][1]
        F1[i] = ans[2][1]
    
    print("Accuracy: ", A)
    print("Precision: ",P)
    print("Recall: ",R)
    print("F1-score: ",F1)
    print("Threshold: ",thresholds)
    
    return A, P, R, F1, thresholds

def main():
    save_cache = True
    cache_path = "/disk/yjt/InferAttack/src/membership_new/cache/threshold_based_attack_xato.pickle"
    
    Keys = ["4gram","adaptive_markov", "CharBackoff","PCFG41","fuzzypsm", "CKLPCFG", "LSTM", "ippsm"]
    # Keys = ["CharBackoff", "CKLPCFG"]
    shadow_train = read_passwords(SHADOW_TRAIN)
    target_train = read_passwords(TARGET_TRAIN)
    
    stones = [0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
    
    ans = {}
    
    for key in Keys:
        A, P, R, F1, thresholds = calculate(key, stones, shadow_train, target_train)
        ans[key] = {
            "accuracy": A, 
            "precision": P,
            "recall": R,
            "f1": F1, 
            "thresholds": thresholds
        }
    ans["stones"] = stones
    
    if save_cache:
        print(f"Cache saved in: {cache_path}")
        with open(cache_path, "wb") as f:
            pickle.dump(ans, f)
    pass

if __name__ == '__main__':
    main()