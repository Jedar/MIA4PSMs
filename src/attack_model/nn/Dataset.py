import json
import torch
import torch.utils.data as Data
from math import log2, inf

def read_target(path):
    ans = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            ans.add(line)
    return ans

def read_nn_predict(path):
    ans = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n").split("\t")
            if len(line) > 2:
                continue
            pwd = line[0]
            try:
                probs = json.loads(line[1])
                probs = [[x] for x in probs]
            except Exception  as e:
                # print(line, pwd, probs)
                continue
            ans.append((pwd, probs))
    return ans

def optimized_predict_wrapper(pwds):
    def log_prob(prob):
        if prob <=0:
            logprob = 50
        else:
            logprob = -log2(prob)
        return logprob
    ans = []
    for pwd, probs in pwds:
        final_prob = None
        for prob in probs:
            prob = prob[0]
            if final_prob == None:
                final_prob = 0
            final_prob += log_prob(prob)
        if final_prob == None:
            final_prob = 1024
        new_prob = []
        for prob in probs:
            prob = prob[0]
            new_prob.append([log_prob(prob), final_prob])
        ans.append((pwd, new_prob))
    return ans

def final_prob_predict_wrapper(pwds):
    def log_prob(prob):
        if prob <=0:
            logprob = 50
        else:
            logprob = -log2(prob)
        return logprob
    ans = []
    for pwd, probs in pwds:
        final_prob = None
        for prob in probs:
            prob = prob[0]
            if final_prob == None:
                final_prob = 0
            final_prob += log_prob(prob)
        if final_prob == None:
            final_prob = 1024
        new_prob = [final_prob]
        ans.append((pwd, [new_prob]))
    return ans

prob_appender = optimized_predict_wrapper

def trim_data(prob, max_len, dict_size):
    if len(prob) > max_len:
        return prob[:max_len]
    while len(prob) < max_len:
        prob.append([0] * dict_size)
    return prob

def dataloader_wrapper(data, batch_size=32, shuffle=True, num_worker=2):
    return Data.DataLoader(
        dataset=Data.TensorDataset(data.x, data.y),
        shuffle = shuffle,
        batch_size = batch_size,
        num_workers=num_worker
    )

def direct_dataloader_wrapper(data, batch_size=32, shuffle=True, num_worker=2):
    return Data.DataLoader(
        dataset=data,
        shuffle = shuffle,
        batch_size = batch_size,
        num_workers=num_worker
    )

class dataset(Data.Dataset):
    def __init__(self, path, target, dict_size, max_len, with_pwd=False, padding=True):
        self.dict_size = dict_size
        self.max_len = max_len
        self.path = path 
        self.target_path = target 
        self.with_pwd = with_pwd
        self.x = []
        self.y = []
        self.pwds = []
        target = read_target(self.target_path)
        pwds = self.parse_nn_predict(path)
        self.init_dataset(target, pwds, padding=padding)
        self.n = len(self.x)
        # print(f"n: {self.n}")
        # print(self.x[-1:])
        self.x = torch.Tensor(self.x)
        self.y = torch.Tensor(self.y)

    def parse_nn_predict(self, path):
        return read_nn_predict(path)
    
    def init_dataset(self, target, pwds, padding):
        for pwd, prob in pwds:
            if self.with_pwd:
                self.pwds.append(pwd)
            if padding:
                prob = trim_data(prob, self.max_len, self.dict_size)
            self.x.append(prob)
            if pwd in target:
                self.y.append(1)
            else:
                self.y.append(0)
    
    def __len__(self):
        return self.n
    
    def __getitem__(self, idx):
        if self.with_pwd:
            return self.pwds[idx], self.x[idx], self.y[idx]
        return self.x[idx], self.y[idx]

class optimized_dataset(dataset):
    def __init__(self, path, target, dict_size, max_len, with_pwd=False, padding=True):
        super().__init__(path, target, dict_size, max_len, with_pwd, padding)
    
    def parse_nn_predict(self, path):
        pwds = read_nn_predict(path)
        return optimized_predict_wrapper(pwds)

class final_prob_dataset(dataset):
    def __init__(self, path, target, dict_size, max_len, padding=True):
        super().__init__(path, target, dict_size, max_len, padding)
    
    def parse_nn_predict(self, path):
        pwds = read_nn_predict(path)
        return final_prob_predict_wrapper(pwds)

class dataset_Ver_prob():
    def __init__(self, path, target, dict_size, max_len, padding=True):
        self.dict_size = dict_size
        self.max_len = max_len
        self.path = path 
        self.target_path = target 
        self.x = []
        self.y = []
        self.pwdlist = []
        self.target = read_target(self.target_path)
        pwds = read_nn_predict(path)
        pwds = prob_appender(pwds)
        for pwd, prob in pwds:
            self.pwdlist.append(pwd)
            if padding:
                prob = trim_data(prob, self.max_len, self.dict_size)
            self.x.append(prob)
            if pwd in self.target:
                self.y.append(1)
            else:
                self.y.append(0)
        self.n = len(self.x)
        self.x = torch.Tensor(self.x)
        self.y = torch.Tensor(self.y)
    
    def __len__(self):
        return self.n


def prob_appender_only_prob(pwds):
    final_prob = 0.0
    ans = []
    for pwd, probs in pwds:
        for prob in probs:
            if prob[0] <=0:
                logprob = 50
            else:    
                logprob = -log2(prob[0])
            final_prob+= logprob
        only_prob = [final_prob]
        ans.append((pwd,[only_prob]))  
        final_prob = 0.0  
    return ans

class dataset_only_prob():
    def __init__(self, path, target, dict_size, max_len, padding=True):
        self.dict_size = dict_size
        self.max_len = max_len
        self.path = path 
        self.target_path = target
        self.x = []
        self.y = []
        self.target = read_target(self.target_path)
        pwds = read_nn_predict(path)
        pwds = prob_appender_only_prob(pwds)
        for pwd, prob in pwds:
            
            if padding:
                prob = trim_data(prob, self.max_len, self.dict_size)
            self.x.append(prob)
            if pwd in self.target:
                self.y.append(1)
            else:
                self.y.append(0)
        self.n = len(self.x)
        self.x = torch.Tensor(self.x)
        self.y = torch.Tensor(self.y)
    
    def __len__(self):
        return self.n