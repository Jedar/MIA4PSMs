import tqdm


def read_blocklist(path):
    pwds = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            pwds.add(line)    
    return pwds

def read_names(path):
    names = set()
    
    with open(path, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            if len(line) > 3:
                names.add(line)
    return names

def main():
    # name_path = '/disk/clw/membership/zxcvbn/data/english_wikipedia.txt'
    name_path = '/disk/clw/membership/zxcvbn/data/names.txt'
    # blocklist_path = '/disk/yjt/InferAttack/data/blocklist/KeePass.txt'
    blocklist_path = "/disk/data/general/cit0day_new.txt"
    blocklist = read_blocklist(blocklist_path)
    names = read_names(name_path)
    
    total = len(blocklist)
    count = 0

    for b in tqdm.tqdm(blocklist):
        n = len(b)
        found = False
        for i in range(n):
            if found:
                break
            for j in range(1, n+1):
                if found:
                    break
                if b[i:j] in names:
                    count += 1
                    found = True
    print(f"File: {blocklist_path}")
    print(f"Passwords with names: {count/total} ({count})")
    pass

if __name__ == '__main__':
    main()

