load("Samples.mat");

Data_By_Year=zeros(12,29,17);    %三个坐标分别为 年份 国家 指标
for i =1:12
Data_By_Year(i,1,:)=Argentina(i,:);
Data_By_Year(i,2,:)=Brazil(i,:);
Data_By_Year(i,3,:)=Cambodia(i,:);
Data_By_Year(i,4,:)=Chad(i,:);
Data_By_Year(i,5,:)=China(i,:);
Data_By_Year(i,6,:)=Colombia(i,:);
Data_By_Year(i,7,:)=CongoDemographicRepublic(i,:);
Data_By_Year(i,8,:)=CongoRepublic(i,:);
Data_By_Year(i,9,:)=Denmark(i,:);
Data_By_Year(i,10,:)=Egypt(i,:);
Data_By_Year(i,11,:)=France(i,:);
Data_By_Year(i,12,:)=Germany(i,:);
Data_By_Year(i,13,:)=India(i,:);
Data_By_Year(i,14,:)=Italy(i,:);
Data_By_Year(i,15,:)=Japan(i,:);
Data_By_Year(i,16,:)=Laos(i,:);
Data_By_Year(i,17,:)=Madagascar(i,:);
Data_By_Year(i,18,:)=Malaysia(i,:);
Data_By_Year(i,19,:)=NewZealand(i,:);
Data_By_Year(i,20,:)=Norway(i,:);
Data_By_Year(i,21,:)=Paraguay(i,:);
Data_By_Year(i,22,:)=Philippines(i,:);
Data_By_Year(i,23,:)=Russia(i,:);
Data_By_Year(i,24,:)=Senegal(i,:);
Data_By_Year(i,25,:)=Sweden(i,:);
Data_By_Year(i,26,:)=Turkey(i,:);
Data_By_Year(i,27,:)=Uganda(i,:);
Data_By_Year(i,28,:)=UK(i,:);
Data_By_Year(i,29,:)=USA(i,:);
end 

%截取一年数据
Data_2010_0=reshape(Data_By_Year(4,:,2:16),29,15);
Data_2010=(Data_2010_0-min(Data_2010_0))./(max(Data_2010_0)-min(Data_2010_0));   %归一化

%熵权法
[EWMW,Z2_2010]=EWM(Data_2010);
AHPW=[0.0333	0.1	0.0333	0.0938	0.1563	0.0417	0.0625	0.0833	0.0283	0.0695	0.0625	0.0347	0.0692	0.0769	0.0623];

%Z用来检验AHP与EWM
Z=zeros(10,6);
for i=1:10
    Z(i,:)=Data_2010([1,2,3,4,5,11],:)*AHPW'*i/10+Data_2010([1,2,3,4,5,11],:)*EWMW'*(10-i)/10;
end

%相关性分析
DataOfChad=reshape(Data_By_Year(:,4,2:16),12,15);
Economy=DataOfChad(:,4)*0.375+DataOfChad(:,5)*0.625;
Society=DataOfChad(:,6)*0.2+DataOfChad(:,7)*0.3+DataOfChad(:,8)*0.4+DataOfChad(:,9)*0.1;
Cohesion=DataOfChad(:,10)*0.4167+DataOfChad(:,11)*0.375+DataOfChad(:,12)*0.2083;
Politic=DataOfChad(:,13)*0.3321+DataOfChad(:,14)*0.369+DataOfChad(:,15)*0.2989;
for i=1:3
temp=corrcoef(Economy,DataOfChad(:,i)');
Corel_E(i)=temp(1,2);
temp=corrcoef(Society,DataOfChad(:,i)');
Corel_S(i)=temp(1,2);
temp=corrcoef(Cohesion,DataOfChad(:,i)');
Corel_C(i)=temp(1,2);
temp=corrcoef(Politic,DataOfChad(:,i)');
Corel_P(i)=temp(1,2);
end
[Prediction,Standard]=KMEANS(Data_2010,3);

Chad2018=zeros(1,15);
for i=1:15
    Chad2018(i)=polyval(polyfit((1:11)',DataOfChad(1:11,i),2),13);
end


