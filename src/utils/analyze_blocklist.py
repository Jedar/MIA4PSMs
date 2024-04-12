import argparse
import string
from collections import defaultdict
import re


D = set(string.digits)
C = set(string.ascii_letters)
S = set(string.punctuation)

def compose(pwd):
    P = [0, 0, 0]
    for x in pwd:
        if x in D:
            P[0] = 1
        if x in C:
            P[1] = 1
        if x in S:
            P[2] = 1
    return tuple(P)

def compose_str(pwd):
    c = compose(pwd)
    ans = ""
    if c[0] == 1:
        ans += "D"
    if c[1] == 1:
        ans += "C"
    if c[2] == 1:
        ans += "S"
    return ans

banned = set([
    "111111",
    "123123",
    "111000",
    "112233",
    "100200",
    "111222",
    "121212",
    "520520",
    "110110",
    "123000",
    "101010",
    "111333",
    "110120",
    "102030",
    "110119",
    "121314",
    "521125",
    "120120",
    "101203",
    "122333",
    "121121",
    "101101",
    "131211",
    "100100",
    "321123",
    "110112",
    "112211",
    "111112",
    "520521",
    "110111"
])

def is_banned(pwd):
    return pwd in banned

def check_date(pwd):
    pattern_all = [
            # YYYYMMDD
            r'((19|20)\d{2}0[123456789]0[123456789])',
            r'((19|20)\d{2}0[123456789][12]\d{1})',
            r'((19|20)\d{2}0[123456789]3[01])',
            r'((19|20)\d{2}1[012][0][123456789])',
            r'((19|20)\d{2}1[012][12]\d{1})',
            r'((19|20)\d{2}1[012]3[01])',
            # MMDDYYYY
            r'(0[123456789]0[123456789](19|20)\d{2})',
            r'(0[123456789][12]\d{1}(19|20)\d{2})',
            r'(0[123456789]3[01](19|20)\d{2})',
            r'(1[012][0][123456789](19|20)\d{2})',
            r'(1[012][12]\d{1}(19|20)\d{2})',
            r'(1[012]3[01](19|20)\d{2})',
            # DDMMYYYY
            r'(0[123456789]0[123456789](19|20)\d{2})',
            r'([12]\d{1}0[123456789](19|20)\d{2})',
            r'(3[01]0[123456789](19|20)\d{2})',
            r'([0][123456789]1[012](19|20)\d{2})',
            r'([12]\d{1}1[012](19|20)\d{2})',
            r'(3[01]1[012](19|20)\d{2})',
            # YYMMDD
            r'\d{2}0[123456789]0[123456789]',
            r'\d{2}0[123456789][12]\d{1}',
            r'\d{2}0[123456789]3[01]',
            r'\d{2}1[012][0][123456789]',
            r'\d{2}1[012][12]\d{1}',
            r'\d{2}1[012]3[01]',
            # MMDDYY
            r'0[123456789]0[123456789]\d{2}',
            r'0[123456789][12]\d{1}\d{2}',
            r'0[123456789]3[01]\d{2}',
            r'1[012][0][123456789]\d{2}',
            r'1[012][12]\d{1}\d{2}',
            r'1[012]3[01]\d{2}',
            # DDMMYY
            r'0[123456789]0[123456789]\d{2}',
            r'[12]\d{1}0[123456789]\d{2}',
            r'3[01]0[123456789]\d{2}',
            r'[0][123456789]1[012]\d{2}',
            r'[12]\d{1}1[012]\d{2}',
            r'3[01]1[012]\d{2}',
        ]
    for pattern in pattern_all:
        s = re.search(pattern, pwd)
        if s is None:
            continue
        s = s.group()
        if isinstance(s, tuple):
            s = s[0]
        if not is_banned(s):
            return True, s
    return False, None


def init_cli():
    cli = argparse.ArgumentParser("Analyze Block List")
    cli.add_argument("-f", dest="file", type=str)
    return cli.parse_args()

def read_block_list(path):
    ans = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            ans.append(line)
    return ans

def main():
    args = init_cli()
    B = read_block_list(args.file)
    cnt = defaultdict(int)
    date_cnt = 0
    for x in B:
        s = compose_str(x)
        cnt[s] += 1
        is_date, _ = check_date(x)
        if is_date:
            date_cnt += 1
    Keys = ["D", "C", "DC", "O"]
    K = {k:0 for k in Keys}
    K["O"] = 1
    for k in Keys:
        if k in cnt:
            K[k] = cnt[k]/len(B)
            K["O"] = K["O"] - cnt[k]/len(B)
    for k,v in K.items():
        print(f"{k}: {v}")
    
    print(f"Date Percentage: {date_cnt / len(B)}")


if __name__ == '__main__':
    main()