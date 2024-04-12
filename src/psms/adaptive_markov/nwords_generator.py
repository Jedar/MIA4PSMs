"""
Simulator for N Words
"""
import argparse
import os
from typing import TextIO, List, Union, Tuple
import pickle
from nwords_enumerator import NwordEnumerator
from nwords_trainer import nwords_counter

def wrapper():
    cli = argparse.ArgumentParser("N words simulator")
    cli.add_argument("-i", "--input", dest="input", type=argparse.FileType('r'), required=True, help="nwords file")
    cli.add_argument("-s", "--save", dest="save", type=argparse.FileType('w'), required=True,
                     help="save Monte Carlo results here")
    cli.add_argument("-n", "--ngram", dest="ngram", type=int, required=False, default=2, choices=[2, 3, 4, 5, 6, 7, 8, 9],
                     help="ngram")
    cli.add_argument("--model", dest="model", type=str, required=False, default="empty", help="model path for saving ('empty' skip model training)")
    cli.add_argument("--size", dest="size", type=int, required=False, default=100000, help="generate number")
    cli.add_argument("--threshold", dest="threshold", type=float, required=True, default=10, help="password threshold of generated passwords")
    cli.add_argument("--min-len", dest="min_len", type=int, required=False, default=4, help="minimal length of generated passwords")
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
    start_chr="\x00"
    end_chr: str = "\x03"
    nword_model = None
    if args.model == "empty":
        nword_model, _ = nwords_counter(args.input, args.ngram, args.splitter, end_chr, args.start4word, args.skip4word, start_chr)
    elif not os.path.exists(args.model):
        nword_model, _ = nwords_counter(args.input, args.ngram, args.splitter, end_chr, args.start4word, args.skip4word, start_chr)
        with open(args.model, "wb") as f:
            pickle.dump(nword_model, f)
    else:
        with open(args.model, "rb") as f:
            nword_model = pickle.load(f)
    print(len(nword_model))
    nword_enumerator = NwordEnumerator(nword_model, args.ngram, args.threshold, start_chr, end_chr, args.min_len, args.save)
    nword_enumerator.start()
    pass


if __name__ == '__main__':
    wrapper()
    pass
