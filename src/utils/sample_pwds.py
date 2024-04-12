import argparse
import random


def init_cli():
    cli = argparse.ArgumentParser("Sample Passwords")
    cli.add_argument("-i", dest="input")
    cli.add_argument("-n", default=100, dest="number", type=int)
    cli.add_argument("-o", dest="output")
    return cli.parse_args()

def read_pwds(path):
    ans = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            ans.append(line)
    return ans

def sample(pwds, cnt):
    random.shuffle(pwds)
    ans = pwds
    if len(pwds) > cnt:
        ans = pwds[:cnt]
    return ans
    
def output(pwds, path):
    with open(path, "w") as f:
        for line in pwds:
            f.write(f"{line}\n")

def fill(pwds, cnt, pwd_set):
    random.shuffle(pwds)
    for i in pwds:
        if len(pwd_set) < cnt:
            pwd_set.add(i)
        else: break
    return pwd_set


def main():
    args = init_cli()
    pwds = read_pwds(args.input)
    distinct_pwds = sample(pwds, args.number)
    distinct_pwds = set(distinct_pwds)

    print(f"set_size={ len(distinct_pwds) }")
    distinct_pwds = fill(pwds, args.number, distinct_pwds)
    output(distinct_pwds, args.output)
    pass

if __name__ == '__main__':
    main()