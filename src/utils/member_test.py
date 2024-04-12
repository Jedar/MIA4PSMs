
target_path = ""
data_path = ""


def read_target(path):
    ans = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            ans.add(line)
    return ans

def read_pwds(path):
    ans = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            ans.append(line)
    return ans

def read_csv(path):
    ans = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            line = line.split("\t")[0]
            ans.add(line)
    return ans

def main():
    pwds = read_csv(data_path)
    target = read_target(target_path)
    cnt = 0

    for pwd in pwds:
        if pwd in target:
            cnt += 1
    print(f">>> Password in Target:{len(pwds)}, {cnt/len(pwds)}, {cnt}")


# def main():
#     pwds = read_pwds(data_path)
#     target1 = read_target(target_path)
#     target2 = read_target(rockyou_path)
#     cnt1 = set()
#     cnt2 = set()
#     for pwd in pwds:
#         if pwd in target1:
#             cnt1.add(pwd)
#         if pwd in target2:
#             cnt2.add(pwd)
#     num = 0
#     for pwd in cnt1:
#         if pwd in cnt2:
#             num+=1
    
    # print(f">>> Password in Target: {num/ len(pwds)}")
    
if __name__ == '__main__':
    main()
    