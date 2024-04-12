from collections import defaultdict
import matplotlib.pyplot as plt
import argparse

def ReadTxt(filename):
    #读了rockyou
    ans = defaultdict(int)
    with open(filename, "r") as f:
        for line in f:
            line = line.strip('\r\n')
            ans[line] += 1
    return ans

def handle_file(target, file, label, color):
    QueryingTime = 0
    QueryingMeet = 0
    TimeList = []
    MeetList = []
    QueryingList = []
    
    stones = set()
    for i in [10,100,1000,10000,100000,1000000,1000000]:
        for j in [1, 2,3,4,5,6,7,8,9]:
            stones.add(i*j)
    stones.add(10000000*1)
    stones.add(10000000*1.5)
    stones.add(10000000*2)
    
    MAX_GUESS = max([x for x in stones])
    
    with open(file, "r") as f:
        idx = 0
        for line in f:
            idx += 1
            QueryingList.append(line.strip('\r').strip('\n'))
            if idx > MAX_GUESS:
                break
    print(len(QueryingList))
    
    
    for Q in QueryingList:
        QueryingTime += 1
        if Q in target:
            QueryingMeet += 1
        if QueryingTime in stones:
            MeetList.append(QueryingMeet)
            TimeList.append(QueryingTime)
    print(MeetList, TimeList)
    plt.plot(TimeList,MeetList,c = color,label = label)
    pass

def Querying(mydict,filelist,label, color):
    #read querying list
    
    for i in range(len(filelist)):
        handle_file(mydict, filelist[i], label[i], color[i])
    plt.xlim((0, 2*(10**7)))
    plt.savefig('drawing_dp.pdf')

if __name__ == '__main__':
    My_Dict = ReadTxt('rockyou_new.txt')
    
    
    pwd_list = [
        "g_markov_3_d_rockyou.txt",
    ]
    label = ['markov3']
    color = ['r','black','g','grey']
    Querying(My_Dict,pwd_list, label, color)
    