"""
N words

Modified by Yu Jitao
Feature: add noise to preotect the markov database
"""
import re
from collections import defaultdict
from typing import TextIO, Dict, Tuple
from tqdm import tqdm

from lib4mc.FileLib import wc_l
import numpy as np

def parse_line(line: str, splitter: str, start4words: int, skip4words: int):
    line = line.strip("\r\n")
    if splitter == '':
        return list(line)
    items = re.split(splitter, line)
    words = items[start4words:len(items):skip4words]
    return list([x for x in words[0]])

def add_noise(nwords_dict, Q, r):
    print(f"Adding noise: B({Q},{r})")
    for k in nwords_dict.keys():
        for trans in nwords_dict[k]:
            nwords_dict[k][trans] += np.random.binomial(Q, r, 1)[0]


def nwords_counter(nwords_list: TextIO, n: int, splitter: str, end_chr: str, start4words: int,
                   skip4words: int, start_chr: str = '\x00', r=5*10**(-6)):
    nwords_dict: Dict[Tuple, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    prefix_words_num = n - 1
    line_num = wc_l(nwords_list)
    section_dict = defaultdict(int)
    words: Dict[str, int] = defaultdict(int)
    default_start = start_chr * (n - 1)
    # 统计所有口令的出现频率
    for line in tqdm(nwords_list, total=line_num, desc="Reading: "):  # type: str
        line = line.strip("\r\n")
        sections = parse_line(default_start + line, splitter, start4words, skip4words)
        sections.append(end_chr)
        for sec in sections:
            words[sec] += 1
        section_dict[tuple(sections)] += 1
    nwords_list.close()
    print(len(section_dict))
    # 统计所有前缀的以及出现的频次
    for sections, cnt in tqdm(section_dict.items(), desc="Counting: "):
        if len(sections) < prefix_words_num:
            print(f"Error: {sections}")
        for i in range(len(sections) - prefix_words_num):
            grams = tuple(sections[i:i + prefix_words_num])
            transition = sections[i + prefix_words_num]
            nwords_dict[grams][transition] += cnt
            
    # 为模型增加噪声
    add_noise(nwords_dict, line_num, r)
    
    print(len(nwords_dict))
    print(len(words))
    del section_dict
    nwords_float_dict: Dict[Tuple, Dict[str, float]] = {}
    for prefix, ends in tqdm(nwords_dict.items(), "Converting: "):
        nwords_float_dict[prefix] = {}
        total = sum(ends.values())
        for e, v in ends.items():
            nwords_float_dict[prefix][e] = (v / total)
    del nwords_dict
    return nwords_float_dict, words
