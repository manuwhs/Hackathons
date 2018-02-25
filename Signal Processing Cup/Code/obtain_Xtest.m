function [ X, segment_file] = obtain_Xtest( grids, L, folder )
    % Read Test or Practice files
    nG = length(grids); % Number of grids
    X=[];              % Statistics of the samples
    segment_file = []; % Aux. variable with the index of the file for each grid.
    
    % READING OF THE .wav FILES in Practice_dataset

    if (strcmp(folder, 'Practice'))
        wavs = dir(['Practice_dataset/*.wav']); 
        fprintf('Reading Practice Files: ');
        addpath(genpath('Practice_dataset'));
    elseif (strcmp(folder, 'Test'))
        wavs = dir(['Testing_dataset/*.wav']); 
        addpath(genpath('Testing_dataset'));
        fprintf('Reading Testing  Files: ');
    end
    
    nfiles = length(wavs);
    
    % Walk through each folder and list the files inside.
    for m = 1:nfiles  % For every .wav file in the grid
        fprintf('%i', m);
        %Read the file, which will be then divided in segments of 10 min.
        if (strcmp(folder, 'Practice'))
            PowerFiles = audioread(sprintf('Practice_dataset/Practice_%d.wav',m)); %Extract the statistics of the file.
        elseif (strcmp(folder, 'Test'))
            PowerFiles = audioread(sprintf('Testing_dataset/Test_%d.wav',m)); %Extract the statistics of the file.
        end
        n_segments=ceil(length(PowerFiles)/L); %Calculate the number of segments.
        
        for i=0:L:L*(n_segments-1) %Stop the loop just before i overcomes length(PowerFiles).
            % Extract the statistics from the segment:
            if i+L <= length(PowerFiles)
                 %Extract the statistics from the segment.
                statistics = extract_features(PowerFiles(i+1:i+L));
            else
                %Include the last segment of files non-multiple of L
                statistics = extract_features(PowerFiles(i+1:end)); 
            end
            % Store them in X
            X = [X;statistics];
            segment_file = [segment_file;m];% Contains the file of every segment
        end
    end
    fprintf('\n');
end



