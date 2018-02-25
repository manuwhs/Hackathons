function [ ypred_file,Pfiles ] = get_file_prediction( segment_files, ypred, P )
%GET_FILE_PREDICTION Gets the prediction for a file given the predictions
%for segments. 
% INPUTS
% segment_files are the index that assign segments to files
% ypred  are the segment predictions
% P is a matrix Nsegment x 9 of estimated probs. p(segment | grid)
% OUTPUT
% ypred_file is the vector of prediction at file level
% Pfiles is a Nfile x 9 matrix of probabities
% 
% If 2 inputs are given, the segments predictions are assumed hard and the
% file prediction is extracted as the mode. If 3 inputs are given, we have
% information about the soft segment decisions, so a soft decoding is
% performed. 
% Files are labeled with 10 if the (1/9) sum_i p(x | grid=i) is below 1e-13 
n_files = max(segment_files);

ypred_file = zeros(n_files,1);
Pfiles = zeros(n_files,9);
for i = 1:n_files
    predicts = ypred(segment_files == i);
    uni = unique(predicts);
    suni = size(uni);
    if nargin==3
        Pfile = prod(P(segment_files == i,:),1);
        [~,ypred_file(i) ] = max(Pfile);
        Pfiles(i,:)=Pfile;
        if mean(Pfile)<exp(-50*length(predicts)/3),
            ypred_file(i)=10;
        end
    else
        if (suni(2) ==3)
            ypred_file(i) = 10;    %N
        else
            ypred_file(i) = mode(predicts);
        end
    end
end

