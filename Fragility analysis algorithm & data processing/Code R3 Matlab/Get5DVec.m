function[ScoresVec]=Get5DVec(X)       
ScoresVec=zeros(12,29,5);

for i =1:12
    for j =1:29
        ScoresVec(i,j,1)=sum(weight(1:3).*X(i,j,2:4));          %气候评分
        ScoresVec(i,j,2)=sum(weight(4:5).*X(i,j,5:6));          %经济评分
        ScoresVec(i,j,3)=sum(weight(6:8).*X(i,j,7:9));          %社会评分
        ScoresVec(i,j,4)=sum(weight(9:11).*X(i,j,10:12));        %凝聚力评分
        ScoresVec(i,j,5)=sum(weight(12:14).*X(i,j,13:15));        %政治评分
    end 
end
