"""
Simulator for N Words
"""
import argparse
from typing import TextIO, List, Union, Tuple

from lib4mc.MonteCarloLib import MonteCarloLib
from lib4mc.MonteCarloParent import MonteCarlo
from lib4mc.ProbLib import expand_2d, pick_expand
from nwords_trainer import nwords_counter

MAX_ITER_DEPTH=1000
# MAX_ITER_DEPTH=100000000000000000000000000000000000

class NWordsMonteCarlo(MonteCarlo):
    def __init__(self, training_set: Union[TextIO, None], n: int = 2, splitter: str = ' ', start4word: int = 0,
                 skip4word: int = 1, start_chr="\x00",
                 end_chr: str = "\x03", noise=5*10**(-6)):
        if training_set is None:
            return
        # nwords：
        # words：
        nwords, words = nwords_counter(training_set, n, splitter, end_chr, start4word, skip4word,
                                       start_chr=start_chr, r=noise)
        self.nwords = expand_2d(nwords)
        self.__n = n
        self.words = words
        self.end_chr = end_chr
        self.min_len = 4
        self.default_start = tuple([start_chr for _ in range(n - 1)])
        self.start_chr = start_chr
        pass

    def _get_prefix(self, pwd: Union[List, Tuple], transition: str):
        if len(pwd) < self.__n:
            return tuple(pwd)
        else:
            return tuple(pwd[1 - self.__n:])


    # 优化为dp版本的结构搜索函数
    # pwd包含end character
    def _structure_dp(self, pwd):
        size = len(pwd)
        dp = [0.0 for _ in range(size)]

        pass

    # 核心耗时函数，主体功能为寻找某条口令最大概率的结构
    # 这里的循环在于遍历所有可能的结构
    # 可能的优化方案是：
    # pwd：口令
    # possible_list:
    # container: 当前口令前缀情况。假如n为2，那么container为^^,第一个位置为^1
    # probabilisties: 结构中每个pre-terminal的概率列表
    # target_len: 目标口令长度
    # iter_max: 最大遍历深度，这里的遍历指的是模板遍历的数量
    # cur_iter: 虽然是个列表，但是只会用到第一个元素？表示的是当前搜索个数
    def _structures(self, pwd, possible_list: List[float], container: List, probabilities: List, target_len: int,
                    iter_max: int, cur_iter: List[int]):
        # 迭代深度过大，中断搜索
        if cur_iter[0] >= iter_max:
            return
        # 搜索所有可能的前缀
        for index in range(1, len(pwd) + 1):
            left = pwd[0:index]
            # 前缀在字典当中
            if left in self.words:
                # 搜索可能的前缀
                prev = self._get_prefix(container, left)
                # 
                if prev in self.nwords and left in self.nwords.get(prev)[0]:
                    container.append(left)
                    probabilities.append(self.nwords.get(prev)[0].get(left))
                else:
                    continue
                if len("".join([c for c in container if c != self.start_chr])) == target_len:
                    minus_log2_prob = sum([self.minus_log2(p) for p in probabilities])
                    if possible_list[0] > minus_log2_prob:
                        possible_list[0] = minus_log2_prob
                    cur_iter[0] += 1
                self._structures(pwd[index:], possible_list, container, probabilities, target_len, iter_max, cur_iter)
                container.pop()
                probabilities.pop()

    def __for_all_same(self, pwd: str, probabilities: List[float]):
        """
        Specifically for passwords like `11111111...`, `2222222...``, etc.
        :param pwd:  given password
        :return: the probability of the given password
        """
        container = list(self.default_start)
        prob = .0
        for index in range(0, len(pwd)):
            left = pwd[index: index + 1]
            if left in self.words:
                prev = self._get_prefix(container, left)
                if prev in self.nwords and left in self.nwords.get(prev)[0]:
                    container.append(left)
                    prob += self.minus_log2(self.nwords.get(prev)[0].get(left))
                else:
                    return
            else:
                return
        probabilities[0] = min(prob, probabilities[0])
        pass

    def calc_ml2p(self, pwd: str) -> float:
        possible_list = [float(1022)]
        depth = [0]
        self._structures(pwd + self.end_chr, possible_list, list(self.default_start),
                         [], len(pwd) + len(self.end_chr), MAX_ITER_DEPTH, depth)
        return possible_list[0]

    def sample1(self) -> Tuple[float, str]:
        pwd = self.default_start
        prob = .0
        pwd_len = 0
        while True:
            tar = self._get_prefix(pwd, "")
            p, addon = pick_expand(self.nwords.get(tar))
            prob += self.minus_log2(p)
            if addon == self.end_chr:
                if pwd_len >= self.min_len:
                    break
                else:
                    pwd = self.default_start
                    prob = .0
                    pwd_len = 0
                    continue
            _tmp = list(pwd)
            _tmp.append(addon)
            pwd = tuple(_tmp)
            pwd_len += len(addon)
            if pwd_len >= 256:
                pwd = self.default_start
                prob = .0
                pwd_len = 0
        return prob, "".join(pwd)


def wrapper():
    cli = argparse.ArgumentParser("N words simulator")
    cli.add_argument("-i", "--input", dest="input", type=argparse.FileType('r'), required=True, help="nwords file")
    cli.add_argument("-t", "--test", dest="test", type=argparse.FileType('r'), required=True, help="testing file")
    cli.add_argument("-s", "--save", dest="save", type=argparse.FileType('w'), required=True,
                     help="save Monte Carlo results here")
    cli.add_argument("-n", "--ngram", dest="ngram", type=int, required=False, default=2, choices=[2, 3, 4, 5, 6],
                     help="ngram")
    cli.add_argument("--size", dest="size", type=int, required=False, default=100000, help="sample size")
    cli.add_argument("--noise", dest="noise", type=float, required=False, default=5*10**(-6), help="noise add to the markov model")
    cli.add_argument("--splitter", dest="splitter", type=lambda x: str(x).replace("\\\\", "\\"), required=False,
                     default="\t",
                     help="how to divide different columns from the input file. "
                          "Set it \"empty\" to represent \'\'")
    cli.add_argument("--start4word", dest="start4word", type=int, required=False, default=0,
                     help="start index for words, to fit as much as formats of input. An entry per line. "
                          "We get an array of words by splitting the entry. "
                          "\"start4word\" is the index of the first word in the array")
    cli.add_argument("--skip4word", dest="skip4word", type=int, required=False, default=1,
                     help="there may be other elements between words, such as tags. "
                          "Set skip4word larger than 1 to skip unwanted elements.")
    args = cli.parse_args()
    if args.splitter == 'empty':
        args.splitter = ''
    nword_mc = NWordsMonteCarlo(args.input, splitter=args.splitter, n=args.ngram, start4word=args.start4word,
                                skip4word=args.skip4word, noise=args.noise)
    ml2p_list = nword_mc.sample(size=args.size)
    mc = MonteCarloLib(ml2p_list)
    scored_testing = nword_mc.parse_file(args.test)
    mc.ml2p_iter2gc(minus_log_prob_iter=scored_testing)
    mc.write2(args.save)
    pass


if __name__ == '__main__':
    wrapper()
    pass
