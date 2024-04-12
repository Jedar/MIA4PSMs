import numpy
import argparse
import math
import bisect

def read_prob(value, mode="normal"):
    if mode == "normal":
        v = float(value)
        if v > 0:
            return -math.log(v)
        return -1
    if mode == "mlp":
        return float(value)
    if mode == "lp":
        return -float(value)

def read_csv(path, idx, mode="mlp"):
    pwds = []
    total = 0
    saw = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            line = line.split("\t")
            pwd = line[0]
            if len(pwd) < 3:
                continue
            if pwd in saw:
                continue 
            saw.add(pwd)
            prob = read_prob(line[idx], mode=mode)
            if prob > 0:
                total += 2**(-prob)
                pwds.append([pwd, prob])
    print(f"Total: {total}")
    total = math.log(total)
    print(pwds[:10])
    for i in range(len(pwds)):
        pwds[i][1] += total
    print(pwds[:10])
    return pwds

def sample_data(pwds, sample_num):
    if len(pwds) <= sample_num:
        return pwds
    rng = numpy.random.default_rng()
    v = rng.choice(pwds, sample_num).tolist()
    v = [(x[0], float(x[1])) for x in v]
    return sorted(v, key=lambda x:x[1])

def monte_carlo(pwds):
    n = len(pwds)
    probs = []
    guesses = []
    cum = 0
    guess = 0
    for item in pwds:
        prob = item[1]
        probs.append(prob)
        prob = 2**(-prob)
        cum = cum + (1.0/n) * (1.0/prob)
        guess = max(guess + 1, int(cum))
        guesses.append(guess)
    return probs, guesses

def generate_guesses(prob, probs, guesses):
    idx = bisect.bisect_right(probs, prob)
    gn = 10**30
    if idx < len(guesses):
        gn = guesses[idx]
    return gn 

def monte_carlo_evaluate(pwds, sample_num):
    sample_pwds = sample_data(pwds, sample_num)
    probs, guesses = monte_carlo(sample_pwds)
    print(probs[:10])
    print(guesses[:10])
    ans = []
    pwds = sorted(pwds, key=lambda x:x[1])
    gn = 0
    for pwd, prob in pwds:
        gn = max(gn+1, generate_guesses(prob, probs, guesses))
        ans.append((pwd, prob, gn))
    return ans

def output_csv(pwds, path):
    with open(path, "w") as f:
        for pwd, prob, gn in pwds:
            f.write(f"{pwd}\t{prob}\t{gn}\n")
    print(f"File saved in {path}")

def init_cli():
    cli = argparse.ArgumentParser("Generate Monte Carlo Guess Number from Probability")
    cli.add_argument("-c", "--csv", dest="csv")
    cli.add_argument("-p", "--prob", dest="prob", default=1, type=int)
    cli.add_argument("-s", "--sample", dest="sample", default=10000, type=int)
    cli.add_argument("-o", "--output", dest="output")
    return cli.parse_args()

def main():
    args = init_cli()
    pwds = read_csv(args.csv, args.prob, "lp")
    pwds = monte_carlo_evaluate(pwds, args.sample)
    output_csv(pwds, args.output)
    pass

if __name__ == '__main__':
    main()