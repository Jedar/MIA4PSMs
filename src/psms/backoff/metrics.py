import math
import argparse

def mu_alpha(probs, alpha):
    cumsum = 0.0
    ans = len(probs)
    for i, v in enumerate(probs):
        v = math.pow(2, -v)
        cumsum += v
        if cumsum >= alpha:
            ans = i
            break
    print(cumsum)
    return ans

def lambda_beta(probs, beta):
    cumsum = 0.0
    for i, v in enumerate(probs):
        v = math.pow(2, -v)
        cumsum += v
        if i >= beta:
            break
    return cumsum

def expect_guess(probs, num):
    cumsum = 0.0
    for i, v in enumerate(probs):
        v = math.pow(2, -v)
        cumsum += v * i
        if i >= num:
            break
    return cumsum

def min_entropy(probs):
    return probs[0]

def guess_alpha(probs, alpha):
    mu_ = mu_alpha(probs, alpha)
    print(mu_, alpha)
    lambda_ = lambda_beta(probs, mu_)
    v = (1-lambda_)*mu_ + expect_guess(probs, mu_)
    return v

def read_prob(path):
    res = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            v = float(line)
            res.append(v)
    return res

def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("-i", dest="input",type=str,help="Input probability(minus logarithm format)")
    cli.add_argument("-a", dest="alpha",type=float,default=0.5,help="Alpha value for u_a")
    cli.add_argument("-b",dest="beta",type=int,default=1000,help="Beta value for lambda_b")
    args = cli.parse_args()


    probs = read_prob(args.input)

    # Min entropy
    H_ = min_entropy(probs)

    # Lambda 10/1000
    L_10 = lambda_beta(probs, 10)
    L_1000 = lambda_beta(probs, 1000)

    # Guess 0.25/0.5
    G_1 = guess_alpha(probs, 0.25)
    G_2 = guess_alpha(probs, 0.5)

    print(f"Min entropy: {H_}")
    print(f"Lambda 10: {L_10}")
    print(f"Lambda 1000: {L_1000}")
    print(f"Guess 0.25: {G_1}")
    print(f"Guess all: {G_2}")
    pass

if __name__ == '__main__':
    main()