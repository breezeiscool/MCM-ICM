function[W,Z2]=EWM(X)        %XΪ3ά
Sample_Num=size(X,1);
Indicator_Num=size(X,2);

P=X./sum(X,1);
temp=P.*log(P);
temp(P==0)=0;

D=-sum(temp,1)/log(Sample_Num);

W=(1-D)/(Indicator_Num-sum(D));

Z2=X*W';
