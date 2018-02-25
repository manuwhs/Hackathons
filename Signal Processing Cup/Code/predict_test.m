function [ ypred_tst,P ] = predict_test(X, Y,Xtst, classifier,type)
%PREDICT_TEST Performs a prediction
% INPUTS
% X           is the matrix of training data
% Y           is the vector of labels
% Xtst        is the matrix of test data
% classifier  either knn of maxL
% type        is the K if classifier = 'knn' or 'full'/'diag'/'equal' if
% classifier = 'maxL'
% OUTPUTS
% ypred_tst   predicted labels
% P           matrix of probabilities
nG = 9;
minP = zeros (nG,1);  % With the minimum probability of every class

if (strcmp(classifier,'knn'))  % Use knn
    ypred_tst = kNN(X,Y,Xtst,type);
    ypred_tst = ypred_tst.';
    
elseif strcmp(classifier,'maxL')   %Use probabilistic approach
    
    P = zeros (length(Xtst(:,1)) ,nG);
    D = size(X,2);
    ms = zeros(nG,D);
    Cs = zeros(D,D,nG);
    
    for n=1:nG  % Calculate the probabikity of every cluster
        % Mean and cov. matrix of each class:
        ms(n,:) = mean(X(Y==n,:));
        Cs(:,:,n) = cov(X(Y==n,:));
        
    end
    
    C = mean(Cs,3);
    % Prediction
    for n=1:nG
        switch type
            case 'full' % full covariance
                sd = mvnpdf(Xtst,ms(n,:),Cs(:,:,n));
                minP(n) = min(mvnpdf(X(Y==n,:),ms(n,:),Cs(:,:,n)));
            case 'diag' % diagonal covariance
                sd = mvnpdf(Xtst,ms(n,:),diag(diag(Cs(:,:,n))));
                minP(n) = min(mvnpdf(X(Y==n,:),ms(n,:),diag(diag(Cs(:,:,n)))));
            case 'equal'% homoscedastic
                sd = mvnpdf(Xtst,ms(n,:),C);
                minP(n) = min(mvnpdf(X(Y==n,:),ms(n,:),C));
        end
        
        P(:,n) = sd ;
        
    end
    [~,ypred_tst] = max(P,[],2); % Max. likelihood criterion
    ypred_tst = ypred_tst(1);
    
end

