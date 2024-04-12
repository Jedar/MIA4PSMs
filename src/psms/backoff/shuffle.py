import random


path = "/disk/xm/data_xm/178_new.txt"


def main():
    s1 = set()
    s2 = set()
    with open(path, "r") as f:
        for line in f:
            line = line.strip("\r\n")
            if random.random() < 0.5:
                s1.add(line)
            else:
                s2.add(line)
    print("Size of s1: ",len(s1))
    print("Size of s2: ",len(s2))
    print(len(s1 & s2))
    print(len(s1 - s2))
    print(len(s2 - s1))
    pass 

if __name__ == '__main__':
    main()

