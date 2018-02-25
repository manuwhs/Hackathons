clear all; 
%% PARAMETERS
% Add the training files to Matlab & declare variables and vectors to be used

addpath(genpath('TrainingGrids'));

L = 200000;                 % Length of the segments to be analized as samples.
grids = {'A','B','C','D','E','F','G','H','I'};  % Grid classes
nG = length(grids);            % Number of grids

% Flags for controlling execution 
READ_train_F = 1;       % Read training Data
CrossValidation_F = 1;  % Perform CrossValidation

READ_practice_F = 1;                % Read Practice Data
Train_Practice_classifier_F = 1;    % Obtain Practice Output

READ_test_F = 1;                % Read Test Data
Train_Test_classifier_F = 1;    % Obtain Test Output

var_sel = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]; % All possible features

var_sel_A = [3,6,8,11];    % Features selected for audio
classifier_A = 'maxL';  % Classifier selected for audio
type_A = 'equal';       % Type of maxL algorithm selected for audio

K_N = 3;                % K of the knn
var_sel_P = [1:3,6,8,11];     % Features selected for Power
classifier_P = 'maxL';           % Classifier selected for Power
type_P = 'full';                % Type of maxL algorithm selected for Power


%% READING THE TRAINIG DATA 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (READ_train_F == 1)
    [X_Pt, Y_P, Yfile_P, segment_file_P] = obtain_X_Y(grids,L, 0);
    [X_At, Y_A, Yfile_A, segment_file_A] = obtain_X_Y(grids,L, 1);
    
    % Normalize data Power
    m_P = mean(X_Pt);
    s_P = std(X_Pt);
    X_Pt = (X_Pt - ones(size(X_Pt,1),1)*m_P)./(ones(size(X_Pt,1),1)*s_P);

    % Normalize data Audio
    m_A = mean(X_At);
    s_A = std(X_At);
    X_At = (X_At - ones(size(X_At,1),1)*m_A)./(ones(size(X_At,1),1)*s_A);
    
end

% Perform variable selection
X_A = X_At(:,var_sel_A);
X_P = X_Pt(:,var_sel_P);

% Get Threshold for A/P detection
threshold = (min(m_P(1)) + max(m_A(1)))/2; 


%% K-FOLD CROSS-VALIDATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (CrossValidation_F == 1)
    nCV = 10;   % Number of iterations to get average 
    
    cvErr = 0;
    K_fold = 5;
    for n_i = 1:10
        cvErr = cvErr + crossValidation(X_P, Y_P, Yfile_P,segment_file_P, K_fold, classifier_P,type_P);
    end
    cvErr = cvErr/nCV;
    fprintf('Validation accuracy of Segments Power %f\n',100-cvErr );
    
    cvErr = 0;
    K_fold = 2;
    for n_i = 1:10
        cvErr = cvErr +crossValidation(X_A, Y_A, Yfile_A,segment_file_A, K_fold, classifier_A,type_A);
    end
    cvErr = cvErr/nCV;
    fprintf('Validation accuracy of Segments Audio %f\n',100-cvErr );
end

%% Read the Practice data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (READ_practice_F == 1)
    [Xprac, segment_file_prac] = obtain_Xtest(grids,L, 'Practice');
end

nPrac = length(Xprac);  % Number of test samples

%% TRAIN FINAL CLASSIFIER AND OUTPUT PRACTICE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% NOW WE ARE GONNA TRAIN THE CLASSIFIER WITH the crossvalidated parameters
% with all the samples and output the class of the test samples

if (Train_Practice_classifier_F == 1)
    ypred_prac = [];
    P = [];
        for t = 1:nPrac   % For every test sample
            tsample = Xprac(t,:);

            if (tsample(1) < threshold)    % Check if it is audio or power
                % Normalize and perform variable selection for Audio
                tsample = (tsample - ones(size(tsample,1),1)*m_A)./(ones(size(tsample,1),1)*s_A);
                tsample = tsample(var_sel_A);
                [tpred,p] = predict_test(X_A, Y_A, tsample, classifier_A, type_A);
                ypred_prac = [ypred_prac, tpred];
            else
                % Normalize and perform variable selection for Power
                tsample = (tsample - ones(size(tsample,1),1)*m_P)./(ones(size(tsample,1),1)*s_P);
                tsample = tsample(var_sel_P);
                [tpred,p] = predict_test(X_P, Y_P, tsample, classifier_P, type_P);
                ypred_prac = [ypred_prac, tpred];
            end
            P = [P;p];
        end
    [ypred_file_prac,Pfile]  = get_file_prediction( segment_file_prac, ypred_prac,P );
    nPrac_files = length(ypred_file_prac);
        
    ypred_letters_prac = {};  % Output letters for Practice
    grids = {'A','B','C','D','E','F','G','H','I', 'N'};  % Grids with the N option
    
    for i = 1:nPrac_files  % For every practive file
        ypred_letters_prac{i} =  grids {ypred_file_prac(i)};
    end

    % CREATE OUTPUT FILE
    fileID = fopen('output_practice.txt','w');
    for i = 1:nPrac_files
        fprintf(fileID,'%c',ypred_letters_prac{i});
    end
    fclose(fileID);
    
end

%% Read the Test data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (READ_test_F == 1)
    [Xtst, segment_file_tst] = obtain_Xtest(grids,L, 'Test');
end

nTst = length(Xtst);  % Number of test samples

%% TRAIN FINAL CLASSIFIER AND OUTPUT TEST
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (Train_Test_classifier_F == 1)
    ypred_tst = [];
    P = [];
        for t = 1:nTst   % For every test sample
            tsample = Xtst(t,:);

            if (tsample(1) < threshold)    % Check if it is audio or power
                % Normalize and perform variable selection for Audio
                tsample = (tsample - ones(size(tsample,1),1)*m_A)./(ones(size(tsample,1),1)*s_A);
                tsample = tsample(var_sel_A);
                [tpred,p] = predict_test(X_A, Y_A, tsample, classifier_A, type_A);
                ypred_tst = [ypred_tst, tpred];
            else
                % Normalize and perform variable selection for Power
                tsample = (tsample - ones(size(tsample,1),1)*m_P)./(ones(size(tsample,1),1)*s_P);
                tsample = tsample(var_sel_P);
                [tpred,p] = predict_test(X_P, Y_P, tsample, classifier_P, type_P);
                ypred_tst = [ypred_tst, tpred];
            end
            P = [P;p];
        end
    [ypred_file_tst,Pfile]  = get_file_prediction( segment_file_tst, ypred_tst,P);
    nTst_files = length(ypred_file_tst);
        
    ypred_letters_tst = {};  % Output letters for Practice
    grids = {'A','B','C','D','E','F','G','H','I', 'N'};  % Grids with the N option
    
    for i = 1:nTst_files  % For every practive file
        ypred_letters_tst{i} =  grids {ypred_file_tst(i)};
    end

    %% CREATE OUTPUT FILE
    fileID = fopen('output_test.txt','w');
    for i = 1:nTst_files
        fprintf(fileID,'%c',ypred_letters_tst{i});
    end
    fclose(fileID);

    Test_Out = [];
    Practice_Out = [];   % Get practice output as String
    for i = 1:nTst_files
        Test_Out = [Test_Out, ypred_letters_tst{i}];
    end

    fprintf('Test Output \n%s\n', Test_Out  );
    
end

