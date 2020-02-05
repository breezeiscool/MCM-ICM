import random
import numpy as np
import matplotlib.pyplot as plt
import csv

"""
c超参设定
"""
epoch=50
population=5000
DenseParam=5                                                      #稠密系数
VaryParam=2

focus=2                                                #注意力周期
PropogateRate=0.2                                       #传播概率

"""
网络搭建.
"""
Net=np.zeros([population,population])
Nodes=list(range(0,population))
random.shuffle(Nodes)
for i in range(1,population):
    Net[Nodes[i-1],Nodes[i]]=Net[Nodes[i],Nodes[i-1]]=1


for i in  Nodes:
    Neighbor=max(1,int(random.gauss(DenseParam/2,VaryParam**2)))   #邻接节点数符合正态分布，由于过于稀疏，取稠密系数的一半
    Linkto=random.sample(Nodes,Neighbor)
    for j in Linkto:
        Net[i][j]=Net[j][i]=1                                           #节点ij的双边通路

"""
模拟传播
"""
getMessage=np.zeros(population)                               #是否接收信息
getMessageTime=np.zeros(population)                           #接收信息的时间
SumOfGot=np.zeros(epoch)                                   #接收信息总人数
SumOfFocus=np.zeros(epoch)                                 #注意力周期内人数
getMessage[0]=1
getMessageTime[0]=1


for time in range(2,epoch+2):         #共设20个周期,第一个周期为第一个节点赋值
    for node1 in range(population):
        if (getMessageTime[node1] != 0 and getMessageTime[node1] + focus >= time and getMessageTime[node1] != time):  # 要求已接收信息且在注意力周期内
            SumOfFocus[time-2]+=1
            for node2 in range(population):
                if (Net[node1, node2] == 1 and getMessageTime[node2] == 0):                  # 是否存在通路，由于连接过于稀疏，故单独一个if加速
                    if(random.random()<PropogateRate):          #根据一定概率传播
                        getMessage[node2]=1
                        getMessageTime[node2]=time
    print(time-1)
    SumOfGot[time-2]=sum(getMessage)

with open("Net1PropogateRate0.1Focus"+str(focus)+".csv",'w',encoding='utf-8',newline='')as csvfile:
    writer2 = csv.writer(csvfile, delimiter=',')
    writer2.writerow(SumOfGot)
    writer2.writerow(SumOfFocus)

plt.xlabel("Time")
plt.ylabel("Population")
plt.plot(range(epoch),SumOfGot,label='$number of knows$',color='blue')
plt.plot(range(epoch),SumOfFocus,label='$number of focus$',color='red')
plt.legend()
plt.show()