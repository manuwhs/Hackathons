function statistics=extract_features(signal)
    % Function that computes the features for the grid identification.
    % INPUTS
    % signal: Time domain signal.
    % OUTPUTS
    % statistics: Features extracted from the signal.

    %% Normalize signal
    signal = signal - ones(length(signal),1) * mean(signal);
    signal = signal/max(abs(signal));

    %% Spectrogram
    % Parameters of the spectrogram
    fs=1000; noverlap = 7500; nfft = 100000; window=  10000;

    % Obtain the spectrogrm of "signal".
    [~,F,~,P]=spectrogram(signal,window,noverlap,nfft,fs);  

    % The fourth component P contains the power spectral density, which we will use for the extraction of the ENF.
    % Range of frequencies where the maximum will be searched.
    f_range = find((F>=35) & (F<=70)); 

    [values,I]= max(P(f_range,:));  % G et the values and indices of the peak of P.
    powers = sum(P);               % Summation of all the values in P.

    % Compute the ENF. Frequency at which the maximum is located in each block
    Pspec = F(f_range(I)); 

    %Calculate the statistics of the ENF:
    statistics(1) = mean(values./powers);       % Fraction of power contained by the peak.
    statistics(2) = mean(log(values)-log(powers)); % Logarithm of the previous feature.

    statistics(3) = mean(Pspec);    % Average of the ENF in the segment
    statistics(4) = mean(log(Pspec)); % Average of the log ENF in the segment.
    statistics(5) = log(mean(Pspec)); % log Average of the ENF in the segment.

    statistics(6) = var(Pspec); % Variance of the ENF 
    statistics(7) = log(0.000000001 + var(Pspec)); % log Variance of the ENF 
    statistics(8) = var(log(0.000000001 + Pspec)); % Variance of the log ENF 
    statistics(9) = log(0.000000001 +max(Pspec)-min(Pspec)); % log Range of ENF values.

    Pspec_dif = diff(Pspec);  % Obtain the differential signal of the ENF

    statistics(10) = mean(Pspec_dif); % Average of the increments of the ENF in the segment
    statistics(11) = var(Pspec_dif); % Variance of the increments of the ENF 
    statistics(12) = log(0.000000001 + var(Pspec_dif)); % log Variance of increments of the ENF 

    statistics(13) = max(Pspec_dif)-min(Pspec_dif); % Range of increments of the ENF signal

    ac = xcorr(Pspec,2, 'coeff');
    ac2 = xcorr(log(Pspec),2, 'coeff');

    statistics(14) = ac(2);  % Autocorrelation lag = 1 of the ENF
    statistics(15) = ac(1);  % Autocorrelation lag = 2 of the ENF

    statistics(16) = ac2(2); % Autocorrelation lag = 1 of increments of the ENF
    statistics(17) = ac2(1); % Autocorrelation lag = 2 of increments of theENF

end