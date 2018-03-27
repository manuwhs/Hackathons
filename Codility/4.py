# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:34:15 2016

@author: montoya
"""

#A = [1, 3, 5, 3, 4] 
#A = [1,2,3,4,8,5,6,7]
#A = [1, 3, 5, 3, 4] 
#A = [1,2,3,5,4,8]
#A = [1,2,2,8,4,5]
A = [1, 5, 3, 3, 7] 

def solution(A):
    A_len = len(A)
    
    miss_flag = 0;  # flag if there is a nonordered number
    miss_indx = -1;
    
    if (A_len == 0):
        return -1
    
    for i in range(0,A_len-1):
        if (A[i+1] < A[i]):   # If there is an decreasing number
            # We have to swap it with other decreasing number and it must lay between A[i-1] and A[i+1]
            
            if (miss_flag == 2):  # If there has been a missplacement already
                return False
                
            elif (miss_flag == 0):  # If there has not been a missplacement yet
                if (i == A_len-1):  # Corner 
                    return True
                    
#                if (A[i+2]):
                miss_indx = i;
                miss_flag = 1;       # There has been a missplacement
                print miss_indx
                
            elif(miss_flag == 1):  # If there has been a missplacement
                print "Checking swap"
                # If we can replace the previous number with this one
                if ((A[miss_indx-1] <= A[i+1]) and ( A[miss_indx +1] >= A[i+1])):
                    # If it fits in the first place
                    if ((A[miss_indx] >= A[i]) and (A[miss_indx] <= A[i+2])):
                        # WSwap is possible:
                        miss_flag = 2; # There has already been a possible swap
                        print "Swap!"
                    else:
                        return False
                else:
                    return False
                    
    if (miss_flag == 1):  # If we couldnt find a swap
        return False
        
    return True
            
        
print solution(A)