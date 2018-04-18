function [ cvErr, Pfile ] = crossValidation(X, Y, Yfile, segment_file, K_fold, classifier,type)
%CROSSVALIDATION Performs cross-validation
% INPUTS
% X           is the matrix of training data (segments)
% Y           is the vector of labels
% K_fold      is the number of partitions
% classifier  either knn of maxL
% type        is the K if classifier = 'knn' or 'full'/'diag'/'equal' if
% classifier = 'maxL'
% OUTPUTS
% cvErr       prob. of error
% P           matrix of probabilities (at file level)
nG = 9;

cv = cvpartition(Yfile,'KFold',K_fold);  % Creates K-fold object
err = zeros(cv.NumTestSets,1);
err_file = zeros(cv.NumTestSets,1);
yfile = zeros(size(Yfile));
y = zeros(size(Y));
P = zeros(size(Y,1),nG);
for i = 1:cv.NumTestSets
    
    % Obtain the sets of validation and training by files
    trfileIdx = find(cv.training(i)== 1);  % Contains the index of the files for train
    valfileIdx = find(cv.test(i) == 1);     % Contains the index of the files for val
    % Now we get the samples associated to the files
    trIdx = [];
    valIdx = [];
     % Partitions so that all the segments in a file go either to the train
     % or the validation fold.
    for j = 1:cv.TrainSize(i)
        trIdx_aux = find(segment_file == trfileIdx(j));
        trIdx = [trIdx;trIdx_aux];
    end
    for j = 1:cv.TestSize(i)
        valIdx_aux = find(segment_file == valfileIdx(j));
        valIdx = [valIdx;valIdx_aux];
    end
    
    Xtrain = X(trIdx,:);
    Xval = X(valIdx,:);
    
    Ytrain = Y(trIdx,:);
    Yval = Y(valIdx,:);
    
    % Train the sistem and obtain the score of the validation
    
    if (strcmp(classifier,'knn'))  % Use knn
        ypred = kNN(Xtrain,Ytrain,Xval,type);
        ypred = ypred.';
        
    elseif strcmp(classifier,'maxL')   %Use probabilistic method
        n_val = length(Yval);
        p = zeros (n_val,nG);
        
        D = size(Xtrain,2);
        ms = zeros(nG,D);
        Cs = zeros(D,D,nG);
        
        for n=1:nG  % Calculate the probabikity of every cluster
            % Mean and cov. matrix of each class:
            ms(n,:) = mean(Xtrain(Ytrain==n,:));
            Cs(:,:,n) = cov(Xtrain(Ytrain==n,:));
        end
        
        C = mean(Cs,3);
        % Prediction
        for n=1:nG
            switch type
                case 'full' % Full cov. matrix
                    sd = mvnpdf(Xval,ms(n,:),Cs(:,:,n));
                case 'diag' % diagonal matrix 
                    sd = mvnpdf(Xval,ms(n,:),diag(diag(Cs(:,:,n))));
                case 'equal'% homoscedastic
                    sd = mvnpdf(Xval,ms(n,:),C);
            end
            p(:,n) = sd;
        end
        
    end
    [~,ypred] = max(p,[],2);
    P(valIdx,:) = p;
    y(valIdx) = ypred;
    %err(i) = sum(Yval ~= ypred)/length(ypred);
    
end
% Get file predictions
[ yfile,Pfile ] = get_file_prediction( segment_file, y, P );
% Calculate the percentaje of error
cvErr = 100 * mean(yfile~=Yfile);


