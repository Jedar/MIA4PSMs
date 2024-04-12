import argparse
import math

def read_prob(input_f, spliter, prob_index, max_len):
    res = []
    with open(input_f, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ss = line.split("\t")
            # print(ss)
            prob = float(ss[prob_index])
            # prob = - math.log2(prob)
            res.append(prob)
            # if len(res) > max_len:
            #     break
    return res

def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("-s",dest="spliter", default="'\\t",type=str,help="Spliter of current file")
    cli.add_argument("-i", dest="input",type=str,help="Input password file")
    cli.add_argument("-o", dest="output", type=str,help="Output probability file")
    args = cli.parse_args()
    probs = read_prob(args.input, args.spliter, 1, 5000_0000)
    with open(args.output, "w") as f:
        for prob in probs:
            f.write(f"{prob}\n")
    print("Done")

if __name__ == '__main__':
    main()
