import sys, os
import argparse
from typing import TextIO, Tuple, Callable, List, Dict, Tuple
from zxcvbn import zxcvbn
import time

def measure(inputFile:TextIO, output:TextIO):
    number = 0
    for line in inputFile:
        if len(line) <= 1:
            continue
        line = line.strip('\r\n')
        pwd = line
        res = zxcvbn(pwd)
        output.write(f"{pwd},{res['guesses']}\n")
        number += 1
        if number % 3000 == 0:
            print(f"Batch {number}")
    if output != sys.stdout:
        output.close()
    return number


def main():
    cli = argparse.ArgumentParser("Zxcvbn: password evaluation")
    cli.add_argument("-i", "--input", required=True, dest="input", type=argparse.FileType('r'),
                     help="password list(one password a line)")
    cli.add_argument("-o", "--output", required=False, dest="output", type=argparse.FileType('w'), default=sys.stdout,
                     help="output file with password and password guessing number")
    args = cli.parse_args()
    start = time.time()
    number = measure(args.input, args.output)
    end = time.time()
    speed = end - start
    print(f"Total time: {speed} s")
    print(f"Speed: {speed/number} s")



if __name__ == '__main__':
    main()
