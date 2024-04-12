from collections import defaultdict
from tqdm import tqdm

PATH='/disk/xm/InferenceAttack/result/stealingattack/candidate/pwds/candidate_g_pcfg41_d_178_small.txt'

def read(path):
    pwd_counter = defaultdict(int)
    pwds = [x.strip('\r\n') for x in open(path, "r")]
    for line in tqdm(pwds, desc="Reading: ", total=len(pwds)):
        pwd_counter[line] += 1
    return pwd_counter

def main():
    pwds = read(PATH)
    index_pwd = {i: (pwd) for i, pwd in enumerate(pwds.keys())}
    
    while True:
        print("Input lines:")
        line_num = int(input())
        if line_num < 0:
            print("Exit")
            return
        print(f"Pwd: {index_pwd[line_num]}")
        
    pass

if __name__ == '__main__':
    main()