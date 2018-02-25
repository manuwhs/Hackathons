function t_test=kNN(Xtrain,Ytrain,Xeval,k)
%INPUTS: training and evaluation data & number of neighbors k to be considered.
%OUTPUT: vector with the tag of the training file.

for i=1:size(Xeval,1)
    [~, positions]=sort(dist(Xtrain,Xeval(i,:)')); %Sort in ascending order the distances between training and evaluation data.
    neighbors_tags = Ytrain(positions(1:k)); %Obtain the tags of the k-nearest-neighbors (k first elements of "position").
    
    uni = unique(neighbors_tags);
    suni = size(uni);
    if (suni(2) == k)
        t_test(i) = 10;    %N
    else
        t_test(i) = mode(neighbors_tags); %Choose the most repeated tag.

    end

end
