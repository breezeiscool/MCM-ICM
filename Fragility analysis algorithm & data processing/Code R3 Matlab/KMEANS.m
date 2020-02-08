function [Prediction,Centers ] = KMEANS(data, k_value)
% 功能：实现K-means算法的聚类功能；
%data:      matrix of size M×N,representing M samples,N dimensions
%k_value:   number of classes
%output:    an M*1 Vector, representing class index

%Select center；
data_num = size(data, 1);    
center = data(randperm(data_num, k_value)', :);

%用于计数迭代次数：
iteration = 0;
while 1
    %calculate distance & sort
    distance =Distance(data,center);
    [~, index] = sort(distance, 2, 'ascend');

    %new center:
    center_new = zeros(k_value, size(data, 2));
    for i = 1:k_value
        data_for_one_class = data(index(:, 1) == i, :);   %only the closest one is needed         
        center_new(i,:) = mean(data_for_one_class, 1);    
    end
   
    iteration = iteration + 1;
    disp(iteration);
    
    if center_new == center
        break;
    end
    center = center_new;
end

Centers=center;
Prediction=index(:,1);
    
end
