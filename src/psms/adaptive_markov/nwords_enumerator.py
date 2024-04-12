from math import log2
from typing import Dict, Tuple, TextIO, List


def minus_log2(backwords_dict_float: Dict[Tuple, Dict[str, float]]):
    for previous, items in backwords_dict_float.items():
        for item, prob in items.items():
            items[item] = -log2(prob)
            pass
    return backwords_dict_float
    pass

class NwordEnumerator:
    def __init__(self, backwords_dict_float: Dict[Tuple, Dict[str, float]], ngram, threshold: float, start_chr, end_chr, min_len,
               f_save):
        self.model = minus_log2(backwords_dict_float)
        self.cnt = 0
        self.threshold = threshold
        self.start_chr = start_chr
        self.end_chr = end_chr
        self.min_len = min_len
        self.f_save = f_save
        self.ngram = ngram
        self.max_len = 256
        
    def start(self):
        print(self.threshold, self.min_len, self.ngram)
        print(len(self.model))
        self.iter(tuple([self.start_chr] * (self.ngram-1)), 0.0, 0)
        pass
    
    def plain_text(self, cur_pwd):
        return "".join([x if x not in [self.start_chr, self.end_chr] else "" for x in cur_pwd])
    
    def iter(self, cur_pwd: Tuple, cur_prob: float, cur_len: int):
        context = cur_pwd[-(self.ngram-1):]
        if context not in self.model:
            return
        next_candidates = self.model[context]
        if cur_len > self.max_len or cur_prob >= self.threshold:
            return
        
        for char, prob in next_candidates.items():
            new_prob = cur_prob + prob
            if new_prob < self.threshold:
                if char == self.end_chr and cur_len >= self.min_len:
                    self.cnt += 1
                    self.f_save.write(f"{self.plain_text(cur_pwd)}\t{new_prob}\n")
                    continue
                self.iter(cur_pwd+(char,), new_prob, cur_len+1)
