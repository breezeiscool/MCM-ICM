function [dist]=Distance(data,center)
dist=zeros(29,3);
for i =1:3
    dist(:,i)=sqrt(sum((data-center(i,:)).^2,2));
end