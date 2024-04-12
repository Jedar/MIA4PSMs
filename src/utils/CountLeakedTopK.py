from collections import defaultdict

def read_leaked_pwds(path):
    ans = defaultdict(int)
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ans[line] += 1
    return ans 

def read_block_list(path):
    ans = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ans.add(line)
    return ans 

def filter(pwds, threshold=5):
    ans = []
    for k in pwds.keys():
        if pwds[k] >= threshold:
            ans.append((k, pwds[k]))
    print(f"Info: after filter the rest password number is {len(ans)}")
    return sorted(ans, key=lambda x:x[1], reverse=True)

def analyze(pwds, block_list):
    stones = [10, 50, 100, 300, 600, 800, 1000, 3000, 5000, 10000, 30000, 50000, 80000, 100000]
    s = 0
    leaked_number = 0
    ans = []
    for idx, v in enumerate(pwds):
        if s < len(stones) and idx == stones[s]:
            ans.append(leaked_number / stones[s])
            print(f"top {stones[s]}: {leaked_number / stones[s]}")
            s += 1
        if v[0] in block_list:
            leaked_number += 1
    print(ans)

def main():
    leaked_path = '/disk/xm/data_xm/rockyou_new.txt'
    leaked_path = '/disk/xm/data_xm/cityday_new.txt'
    # leaked_path = '/disk/xm/data_xm/xato_new.txt'
    # leaked_path = '/disk/xm/data_xm/neopets_new.txt'
    # block_path = '/disk/yjt/PasswordSimilarity/data/blocklist/explainable_psm.txt'
    block_path = '/disk/yjt/InferAttack/data/blocklist/KeePass.txt'
    block_list = read_block_list(block_path)
    leaked_pwds = read_leaked_pwds(leaked_path)
    pwds = filter(leaked_pwds)
    analyze(pwds, block_list)
    pass

if __name__ == '__main__':
    main()