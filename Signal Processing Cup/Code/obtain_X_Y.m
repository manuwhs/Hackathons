function [ X, Y ,Yfile, segment_file] = obtain_X_Y( grids, L, power_audio)

	% This function reads the data por Training 
    nG = length(grids); % Number of grids
    nfiles = zeros(1,nG); % Counter of files per grid
    
    X=[]; 
    Y=[]; 
    
    segment_file = [];  % Aux. variable with the index of the file for each grid. 
    Yfile = [];         % Aux. variable with the class of every file
    n_files = 0;        % Number of files read
    
    %% READING OF THE .wav FILES 
    if (power_audio == 0)  % We read power
        fprintf('Reading Power Files');
        folder = 'Power_recordings';
    else
        fprintf('Reading Audio Files');
        folder = 'Audio_recordings';
    end
    for n=1:nG   % For every grid type 
    
        %Walk through each folder and list the files inside.
        wavs = dir(['TrainingGrids/Grid_',grids{n},'/',folder,'/*.wav']); 
        nfiles(n) = length(wavs);
        for m = 1:length(wavs)  % For every .wav file in the grid
            n_files = n_files + 1;
            %Read the file, which will be then divided in segments of 10 min.
            PowerFiles=audioread(char(wavs(m).name)); 

            %Include the last segment from files non-multiples of 10 min (C8, E10, F1 & I11):
            g = length(PowerFiles);
            n_segments = ceil(length(PowerFiles)/L); %Calculate the number of segments.
            for i=0:L:L*(n_segments-1) %Stop the loop just before i overcomes length(PowerFiles).
                if i+L <= length(PowerFiles)
                    %Extract the statistics from the segment.
                    statistics = extract_features(PowerFiles(i+1:i+L)); 
                else
                    %Include the last segment of files non-multiple of L
                    statistics = extract_features(PowerFiles(i+1:end));
                end
                % Store them in X
                X = [X;statistics];
                Y = [Y; n];
                segment_file = [segment_file;n_files];% Contains the file of every segment
            end
            Yfile = [Yfile; n];   % Contains the class of every file
        end
        fprintf(' %s', grids{n});
    end
    fprintf('\n');
    
