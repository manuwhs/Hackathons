# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 17:55:45 2016

@author: montoya
"""

def case_just_1(A, first_1): # Tells if it is winnable for just 1 1 and what to do
   A_len = len(A)
   if (first_1 > 0 and first_1 < A_len - 1):  # If the one is not in the extremes
        
        # If there are more than 1 0s at any side, we can sustrac them.
        # Actually we sustract them, if it is even, we are fucked
        N_0s_left = first_1
        N_0s_right = A_len - 1 - first_1
        
        if (N_0s_left > 1) and (N_0s_right > 1):
            if ((N_0s_left + N_0s_right)%2) == 0:  # Even number, we die
                return "NO SOLUTION"
            else:
                if (N_0s_left % 2):
                    return str(0) +"," + str(first_1-3)
                else:
                    return str(first_1+1) +"," + str(A_len-1 - 2)
                    
        elif (N_0s_left == 1 and N_0s_right > 1):
            return str(first_1 + 1) +"," + str(A_len - 2)  # We leave it like 010
            
        elif (N_0s_right == 1 and N_0s_left > 1):
             return str(0) +"," + str(first_1 -2)  # We leave it like 010
        
        elif (N_0s_right == 1 and N_0s_left == 1):
            return "NO SOLUTION"
   else:    # In the case the 1 is in the extremes

        if (first_1 == 0):
            return str(1) +"," + str(A_len - 1)
        else:
            return str(0) +"," + str(A_len - 2)

    
def solution(A):
    # odd numbers must be removed by pairs
    # You can also choose to remove just an even number of an even number and a pair of integers

    # Mmm in the first move you should remove everything you can and leave the situation 
    #  010 or 1  or ...
    # You remove all the 1s possible and play also with the 0s in the boundaries of the 1s

    
    
    # Transform A into bit array
    A_bin = []
    A_len = len(A)
    for i in range (A_len):
        A_bin.append(A[i]%2)
    
    A = A_bin # Substitution
    
#    print A
    first_1 = -1;
    # Find first position of 1. There has to be an even number of 1s, otherwise you can win in the first move
    for i in range(A_len):
        if(A[i] == 1):
            first_1 = i
            break;
            
    if (first_1 == -1): # No 1s found 
        return [0,A_len - 1]   # We remove everything
        
    # Find the position of the one before the last 1.
    antepel_1 = -1;
    
    penul = 0;
    for i in range(A_len):
        if(A[A_len -1-i] == 1):
            if (penul == 0):
                penul = 1
                last_1 = i
            else:
                antepel_1 = i
                break
    
    if (antepel_1 == -1):  # If there is only 1 one !!
        return case_just_1(A, first_1)
        
    else:
        """ We have to remove them so that the left scenario makes them dead"""
        # We have to leave anything but 0100 or 01
        # 0s left and right after removing the 1s 
        # Remove the inbetween
        
        
        N_0s_left = first_1     # Extra 0s we can put either way to win
        N_0s_right = last_1 - antepel_1 - 1
        
        A_final = A_bin[0:first_1]
        A_final.extend(A_bin[antepel_1 + 1:])
        
        resul = case_just_1(A_final, last_1);  # If the other can win
        
        if (resul == "NO SOLUTION"):  # We already won
            if (N_0s_left % 2):
                return str(1) +"," + str(antepel_1)
            else:
                return str(0) +"," + str(antepel_1)
                
        else:  # We can add 0s to left or right to try to win
            # We can add an odd number of 1s to right or left 
            if (N_0s_left >= 1):
                if (N_0s_left % 2):
                    return str(0) +"," + str(antepel_1)
                else:
                    return str(1) +"," + str(antepel_1)
                    
            elif (N_0s_right >= 1):
                    return str(first_1) +"," + str(antepel_1 + 1)
            else:
                return "NO SOLUTION"
            
A = [4, 5, 3, 7, 2] 

#A = [2,5,4]

print solution(A)