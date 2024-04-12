import argparse
from sklearn.metrics import roc_curve, auc
import matplotlib as mpl  
import matplotlib.pyplot as plt
import tqdm
import random

def read_data(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ss = line.split("\t")
            pwd, prob, label = ss[0], float(ss[1].split(",")[0]), int(ss[2])
            if random.randint(0, 10) == 1:
                data.append((prob, label))
    return data

def test_on(data, threshold):
    total = len(data)
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for prob, label in data:
        if prob < threshold and label == 1:
            TP += 1
        if prob < threshold and label == 0:
            FP += 1
        if prob >= threshold and label == 1:
            FN += 1
        if prob >= threshold and label == 0:
            TN += 1
    # return (TP/total, FP/total, TN/total, FN/total)
    # return TPR, FPR
    return (TP/(TP+FN) if TP+FN > 0 else 0, FP/(FP+TN) if FP+TN > 0 else 0)

def plot(FPR, TPR, output):
    plt.figure(figsize=(15, 10))
    plt.title('ROC')
    plt.plot(FPR, TPR,'b',marker="o")
    plt.plot([0,1],[0,1],'r--')
    plt.ylabel('TPR')
    plt.xlabel('FPR')
    plt.savefig(output)


def main():
    cli = argparse.ArgumentParser("ROC data curver")
    cli.add_argument("-i","--input",dest="input",type=str)
    cli.add_argument("-s","--step", dest="step", type=int)
    cli.add_argument("-o","--output",dest="output",type=str)
    args = cli.parse_args()
    data = read_data(args.input)
    # print(data)
    start = 1
    step = 100/args.step
    steps = []
    while start < 1100:
        steps.append(start)
        start += step
    TPRs = []
    FPRs = []
    steps = tqdm.tqdm(steps)
    for i in steps:
        TPR, FPR = test_on(data, i)
        TPRs.append(TPR)
        FPRs.append(FPR)
        print(TPR, FPR, i)
    plot(FPRs,TPRs,args.output)

    pass

if __name__ == '__main__':
    main()

