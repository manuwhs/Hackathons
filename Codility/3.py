# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 00:46:16 2016

@author: montoya
"""

A = [2, 1, 3, 5, 4] 
A = [1, 2, 4, 3, 5] 
A = [8, 2, 6, 4, 5, 3, 12,7,1,9,10, 11,14,13] 

def solution(A):
    
    A_len = len(A)
    if (A_len == 0):
        return -1
        
    permt_indexes = [] # Indexes to store the position of the permutation points.                  
    needed_numbers = 0  # These are the numbers needed to complete the permutation
    
    last_found = A[0]
    if (A[0] == 1):
        permt_indexes.append(0)
    else:
        needed_numbers += A[0] -1   # We add the sequence of numbers needed to find before completing the permutation
            
    for i in range(1,A_len):
        if ((needed_numbers == 0) and A[i] == i + 1):  # Order in sequence
            permt_indexes.append(i)
            last_found = i + 1
        
        else:  # IF we get a number out of sequence
            # We add the needed numbers to find until we can complete the permutation
            if (A[i] > last_found):  # If the number is bigger than the last number found
                 needed_numbers += A[i] - last_found  -1
                 last_found = A[i]
            else:  
#                print needed_numbers, A[i] 
                needed_numbers -= 1
                if (needed_numbers == 0):  # If we dont need other numbers
                    permt_indexes.append(i)
                    
    print  permt_indexes
    return len(permt_indexes)

solution(A)
