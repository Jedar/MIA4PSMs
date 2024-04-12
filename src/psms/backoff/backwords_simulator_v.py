import argparse
import sys
from typing import TextIO, Union, List, Tuple

from backwords.backwords_trainer import backwords_counter
from lib4mc.MonteCarloLib import MonteCarloLib
from lib4mc.ProbLib import expand_2d
from nwords_simulator import NWordsMonteCarlo
import pickle

class BackWordsMonteCarlo(NWordsMonteCarlo):
    def __init__(self, training_set: TextIO, splitter: str, start4word: int, skip4word: int,
                 threshold: int, start_chr: str = '\x00', end_chr: str = "\x03", max_gram: int = 256,
                 max_iter: int = 10 ** 100):
        super().__init__(None)
        backwords, words = backwords_counter(training_set, splitter, start_chr, end_chr, start4word, skip4word,
                                             threshold=threshold, max_gram=max_gram)
        self.nwords = expand_2d(backwords)
        self.end_chr = end_chr
        self.words = words
        self.min_len = 4
        self.default_start = start_chr
        self.start_chr = start_chr
        self.max_iter = max_iter

    def _get_prefix(self, pwd: Union[List, Tuple], transition: str):
        tar = (self.default_start,)
        found = False
        for i in range(0, len(pwd)):
            tmp_tar = tuple(pwd[i:])
            if tmp_tar not in self.nwords or \
                    (transition != "" and transition not in self.nwords.get(tmp_tar)[0]):
                continue
            tar = tmp_tar
            found = True
            break
        if not found:
            tar = tuple()
        return tar

    def calc_ml2p(self, pwd: str) -> float:
        possible_list = [float(1022), [0]]
        # print(self.max_iter)
        depth = [0]
        ans = []
        self._structures_log(pwd + self.end_chr, possible_list, list(self.default_start),
                         ans, len(pwd) + len(self.end_chr), self.max_iter, depth)
        if depth[0] >= self.max_iter:
            sys.stderr.write(f"{pwd}\n")
            # print(pwd)
        return possible_list[1]


def wrapper():
    cli = argparse.ArgumentParser("Backoff words simulator")
    cli.add_argument("-i", "--input", dest="input", type=argparse.FileType('r'), required=True, help="nwords file")
    cli.add_argument("-t", "--test", dest="test", type=argparse.FileType('r'), required=True, help="testing file")
    cli.add_argument("-s", "--save", dest="save", type=argparse.FileType('w'), required=True,
                     help="save Monte Carlo results here")
    cli.add_argument("--size", dest="size", type=int, required=False, default=100000, help="sample size")
    cli.add_argument("--splitter", dest="splitter", type=str, required=False, default="\t",
                     help="how to divide different columns from the input file, set it \"empty\" to represent \'\'")
    cli.add_argument("--start4word", dest="start4word", type=int, required=False, default=0,
                     help="start index for words, to fit as much as formats of input. An entry per line. "
                          "We get an array of words by splitting the entry. "
                          "\"start4word\" is the index of the first word in the array")
    cli.add_argument("--skip4word", dest="skip4word", type=int, required=False, default=1,
                     help="there may be other elements between words, such as tags. "
                          "Set skip4word larger than 1 to skip unwanted elements.")
    cli.add_argument("--threshold", dest="threshold", required=False, type=int, default=10,
                     help="grams whose frequencies less than the threshold will be ignored")
    cli.add_argument("--debug-mode", dest="debug_mode", required=False, action="store_true",
                     help="enter passwords and show probability of the password")
    cli.add_argument("--max-gram", dest="max_gram", required=False, type=int, default=256, help="max gram")
    cli.add_argument("--max-iter", dest="max_iter", required=False, default=10 ** 20, type=int,
                     help="max iteration when calculating the maximum probability of a password")
    args = cli.parse_args()
    if args.splitter.lower() == 'empty':
        args.splitter = ''
    backword_mc = BackWordsMonteCarlo(args.input, splitter=args.splitter, start4word=args.start4word,
                                      skip4word=args.skip4word,
                                      threshold=args.threshold, max_gram=args.max_gram, max_iter=args.max_iter)
    if args.debug_mode:
        usr_i = ""
        while usr_i != "exit":
            usr_i = input("type in passwords: ")
            prob = backword_mc.calc_ml2p(usr_i)
            # print(prob)
        return
    ml2p_list = backword_mc.sample(size=args.size)
    mc = MonteCarloLib(ml2p_list)
    scored_testing = backword_mc.parse_file(args.test)
    mc.ml2p_iter2gc_mock(minus_log_prob_iter=scored_testing)
    mc.write_v(args.save)

if __name__ == '__main__':
    try:
        wrapper()
        # Debug mode
        # import cProfile
        # cProfile.run("wrapper()", filename="/disk/xm/InferenceAttack/result/log/markov.out", sort="cumulative")
    except KeyboardInterrupt:
        print("You canceled the process", file=sys.stderr)
        sys.exit(-1)
