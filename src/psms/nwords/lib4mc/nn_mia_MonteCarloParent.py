import abc
from collections import defaultdict
from math import log2
from typing import List, TextIO, Tuple

from tqdm import tqdm

from lib4mc.FileLib import wc_l


class MonteCarlo(metaclass=abc.ABCMeta):
    @staticmethod
    def minus_log2(prob: float) -> float:
        return -log2(prob)

    @abc.abstractmethod
    def calc_ml2p(self, pwd: str) -> Tuple[float, list]:
        """

        :param pwd: password
        :return:
        """
        return .0, []

    @abc.abstractmethod
    def sample1(self) -> (float, str):
        """
        get one sample
        :return: (prob, sample)
        """
        return .0, ""

    def sample(self, size: int) -> List[float]:
        results = []
        for _ in tqdm(iterable=range(size), desc="Sampling: "):
            prob, pwd = self.sample1()
            results.append(prob)
        return results

    def parse_file(self, testing_set: TextIO) -> List[Tuple[str, List[List[float]]]]:
        """
        get minus log prob for test set
        :param testing_set: test set
        :return: List of tuple (pwd, appearance, minus log prob)
        """
        line_num = wc_l(testing_set)
        pwd_counter = defaultdict(int)
        for line in tqdm(testing_set, desc="Reading: ", total=line_num):
            line = line.strip("\r\n")
            pwd_counter[line] += 1
        res: List[Tuple[str, List[List[float]]]] = []
        for pwd, num in tqdm(pwd_counter.items(), desc="Scoring: "):
            _mlp, possible_list = self.calc_ml2p(pwd)
            shadow_list : List[List[float]] = []
            for prob in possible_list:
                shadow_list.append([prob])
            res.append((pwd, shadow_list))
        return res
