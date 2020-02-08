import random
import numpy as np
import csv
import os
import matplotlib.pyplot as plt

"""
超参设定
"""
epoch=100                                                 #观察周期
BasicPropogateRate=0.2                                   #基础传播意愿
focus=2                                                  #注意力周期

InformationIntrest=(1,1,1)                               #信息内容
alpha=1

population=5000                                          #网络人数
NumberofF=2                                             #名人人数
NumberofM=3                                            #媒体数量
DenseParam1=20                                           #普通人之间
VaryParam1=3
DenseParam21=50                                          #名人与普通人
VaryParam21=2
DenseParam3=300                                          #媒体与普通人
VaryParam3=30

"""
网络搭建
"""

def InterestSamiliarity(a,b):
    return  (a[0]*b[0]+a[1]*b[1]+a[2]*b[2])/((a[0]**2+b[0]**2)**0.5+(a[1]**2+b[1]**2)**0.5+(a[2]**2+b[2]**2)**0.5)    #以余弦距离计算兴趣相似度

def RegionSamiliarity(a,b):
    return  1-((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5/(2**0.5)                                                             #以归一化后的欧式距离(已处理)计算地区相似度

class Nor:
    id=1
    interest=(0,0,0)
    region=(0,0)
    rate=0
    InitPropogateRateP1 =0.2
    InitPropogateRateP2 =0.2
    InitPropogateRateP3 =0
    InitReceiveRateP1 =1
    InitReceiveRateP2 =1
    InitReceiveRateP3 =1


    def __init__(self,NewInterest,NewRegion):
        self.interest=NewInterest
        self.region=NewRegion

    def Propogate(self,To,information):
        if To.id==1:
            self.rate=self.InitPropogateRateP1*To.InitReceiveRateP1*InterestSamiliarity(self.interest,To.interest)*RegionSamiliarity(self.region,To.region)*InterestSamiliarity(self.interest,information)*alpha
        elif To.id==2:
            self.rate = self.InitPropogateRateP2 * To.InitReceiveRateP1 * InterestSamiliarity(self.interest,To.interest) * RegionSamiliarity(self.region, To.region)*InterestSamiliarity(self.interest,information)*alpha
        elif To.id==3:
            self.rate=self.InitPropogateRateP3 * To.InitReceiveRateP1 * InterestSamiliarity(self.interest,To.interest) * RegionSamiliarity(self.region, To.region)*InterestSamiliarity(self.interest,information)*alpha
        return self.rate

class Cel:
    id=2
    interest=(0,0,0)
    region=(0,0)
    rate=0
    InitPropogateRateP1=0.2
    InitPropogateRateP2=0.2
    InitPropogateRateP3=0.2
    InitReceiveRateP1=1
    InitReceiveRateP2=1
    InitReceiveRateP3=1

    def __init__(self,NewInterest,NewRegion):
        self.interest=NewInterest
        self.region=NewRegion

    def Propogate(self,To,information):
        if To.id==1:
            self.rate=self.InitPropogateRateP1*To.InitReceiveRateP2*InterestSamiliarity(self.interest,To.interest)*RegionSamiliarity(self.region,To.region)*InterestSamiliarity(self.interest,information)*alpha
        elif To.id==2:
            self.rate = self.InitPropogateRateP2 * To.InitReceiveRateP2 * InterestSamiliarity(self.interest,To.interest) * RegionSamiliarity(self.region, To.region)*InterestSamiliarity(self.interest,information)*alpha
        elif To.id==3:
            self.rate=self.InitPropogateRateP3 * To.InitReceiveRateP2 * InterestSamiliarity(self.interest,To.interest) * RegionSamiliarity(self.region, To.region)*InterestSamiliarity(self.interest,information)*alpha
        return self.rate

class Med:
    id=3
    interest=(0,0,0)
    region=(0,0)
    rate=0
    InitPropogateRateP1 =1
    InitPropogateRateP2 =1
    InitPropogateRateP3 =0
    InitReceiveRateP1 =0
    InitReceiveRateP2 =1
    InitReceiveRateP3 =0

    def __init__(self,NewInterest,NewRegion):
        self.interest =NewInterest
        self.region = NewRegion

    def Propogate(self, To,information):
        if To.id == 1:
            self.rate = self.InitPropogateRateP1 * To.InitReceiveRateP3 * InterestSamiliarity(self.interest,To.interest) * RegionSamiliarity(self.region, To.region)*InterestSamiliarity(To.interest,information)*alpha
        elif To.id == 2:
            self.rate = self.InitPropogateRateP2 * To.InitReceiveRateP3 * InterestSamiliarity(self.interest,To.interest) * RegionSamiliarity(self.region, To.region)*InterestSamiliarity(To.interest,information)*alpha
        elif To.id == 3:
            self.rate = self.InitPropogateRateP3 * To.InitReceiveRateP3 * InterestSamiliarity(self.interest,To.interest) * RegionSamiliarity(self.region, To.region)*InterestSamiliarity(To.interest,information)*alpha
        return self.rate

Net=np.zeros([population,population])
Nodes=list(range(0,population))
random.shuffle(Nodes)
for i in range(1,population):
    Net[Nodes[i-1],Nodes[i]]=Net[Nodes[i],Nodes[i-1]]=1

NodesinClass=[]
Cele = random.sample(Nodes, NumberofF)
Medi = random.sample(Nodes, NumberofM)
for i in range(population):
    if i not in Cele and i not in Medi:
        if(i<500):
            NodesinClass.append(Nor(np.random.rand(3),tuple([0,0])))
        else:
            NodesinClass.append(Nor(np.random.rand(3),tuple([1,1])))
    elif i in Cele:
        NodesinClass.append(Cel(tuple(np.random.rand(3)),tuple(np.random.rand(2))))
    elif i in Medi:
        NodesinClass.append(Med(tuple(np.random.rand(3)),tuple(np.random.rand(2))))

for i in  Nodes:
    if i not in Medi and i not in Cele:
        Neighbor=max(1,int(random.gauss(DenseParam1/2,VaryParam1**2)))          #邻接节点数符合正态分布，由于过于稀疏，取稠密系数的一半
        Linkto=random.sample(Nodes,Neighbor)
        for j in Linkto:
            if(j not in Medi):
                Net[i][j]=Net[j][i]=1                                           #节点ij的双边通路
    elif i in Cele:                                                              #名人节点接收
        Neighbor=max(1,int(random.gauss(DenseParam21/2,VaryParam21**2)))
        Linkto = random.sample(Nodes, Neighbor)
        for j in Linkto:
            Net[i][j]=Net[j][i]=1

        #Neighbor=max(1,int(random.gauss(DenseParam22/2,VaryParam22**
        Neighbor=NumberofF
        Linkto=random.sample(Cele,Neighbor)
        for j in Linkto:
            Net[i][j]=Net[j][i]=1
        #Neighbor = max(1, int(random.gauss(DenseParam23 / 2, VaryParam23 ** 2)))

        Neighbor=NumberofM
        Linkto = random.sample(Medi, Neighbor)
        for j in Linkto:
            Net[i][j] = Net[j][i] = 1

    elif i in Medi:                                                                #媒体节点生成
        Neighbor=max(1,int(random.gauss(DenseParam3/2,VaryParam3**2)))
        Linkto = random.sample(Nodes, Neighbor)
        for j in Linkto:
            Net[i][j]=Net[j][i]=1

"""
模拟传播
"""

getMessage=np.zeros(population)                                #是否接收信息
getMessageTime=np.zeros(population)                            #接收信息的时间
SumOfGot=np.zeros(epoch)                                       #接收信息总人数
SumOfFocus=np.zeros(epoch)                                     #注意力周期内人数

start=random.sample(Cele,1)
getMessage[start]=1
getMessageTime[start]=1

for time in range(2,epoch+2):         #共设20个周期,第一个周期为第一个节点赋值
    if time in [2,4,6,8,10]:
        getMessageTime[start]=time
    for node1 in range(population):
        if (getMessageTime[node1] != 0 and getMessageTime[node1] + focus >= time and getMessageTime[node1] != time):   #要求已接收信息且在注意力周期内
            SumOfFocus[time-2]+=1
            for node2 in range(population):
                if (Net[node1, node2] == 1 and getMessage[node2] == 0 ):                                               #是否存在通路，由于连接过于稀疏，故单独一个if加速
                    if(random.random()<NodesinClass[node1].Propogate(NodesinClass[node2],InformationIntrest)):         #根据一定概率传播、接收
                        getMessage[node2]=1
                        getMessageTime[node2]=time
    print(time-1)
    SumOfGot[time-2]=sum(getMessage)

"""
数据保存与展示
"""
save_path='Net2'
if not os.path.exists(save_path):
    os.mkdir(save_path)
filepath=save_path+"/名人00到11.csv"
with open(filepath,'w',encoding='utf-8',newline='')as csvfile:
    writer2 = csv.writer(csvfile, delimiter=',')
    writer2.writerow(SumOfGot)
    writer2.writerow(SumOfFocus)

plt.xlabel("Time")
plt.ylabel("Population")
plt.plot(range(epoch),SumOfGot,label='$number of knows$',color='blue')
plt.plot(range(epoch),SumOfFocus,label='$number of focus$',color='red')
plt.legend()
plt.show()
