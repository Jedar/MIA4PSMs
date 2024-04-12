from sklearn.metrics import precision_recall_fscore_support, accuracy_score

def validate(y_pred, y_true):
    A = accuracy_score(y_true, y_pred)
    pcf = precision_recall_fscore_support(y_true=y_true, y_pred=y_pred,average="binary")
    P = pcf[0]
    R = pcf[1]
    F1 = pcf[2]
    return (A, P, R, F1)
