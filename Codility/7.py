def solution(P):
    # write your code in Python 3.6
    ## Number of total circles
    Ntotal = len(P)*(len(P) +1)/2
    N_white = 0
    Nconsecutive_false = 0
    for i in range(len(P)):
        if(P[i] == False):
            Nconsecutive_false +=1
        else:  # True
           if(Nconsecutive_false > 0):
               N_white += Nconsecutive_false*(Nconsecutive_false +1)/2
               Nconsecutive_false = 0;
    if (P[-1] == False):
        N_white += Nconsecutive_false*(Nconsecutive_false +1)/2
        
    if (Ntotal - N_white > 1000000000):
        return 1000000000
    else: 
        return int(Ntotal - N_white)