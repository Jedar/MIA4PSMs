import math
import argparse

def readPC(path, encoding='iso-8859-1'):
    with open(path, encoding=encoding) as f:
        raw = [x.lstrip()[:-1].split(' ') for x in f]
        raw = [[int(x[0]), ' '.join(x[1:])] for x in raw ]
        raw = sorted(raw, key=lambda x:x[0], reverse=True)
        total = sum([x[0] for x in raw])
        prob = [-math.log2(1.0*x[0]/total) for x in raw]
        uniq = [x[1] for x in raw]
    return uniq, prob

def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("-i", dest="input", type=str, help="input passwords (one line with frequency and text)")
    cli.add_argument("-o",dest="output",type=str,help="Output list")

    args = cli.parse_args()

    uniq_pwd, probs = readPC(args.input)
    with open(args.output, "w") as f:
        for prob in probs:
            f.write(f"{prob}\n")
    pass

if __name__ == '__main__':
    main()