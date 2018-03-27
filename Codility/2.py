# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 00:31:11 2016

@author: montoya
"""

s = "caca3pLf2d93jf9j"
s = 'afA0Ba9eRt980rrrrtY7ggggggggg9aG'

def solution(s):
    S_list = list(s)
    Nchar = len(S_list)
    
    valid_pass = 0
    nchar = 0
    max_char = -1
    
    for i in range(Nchar):
        cchar = S_list[i]
        if (cchar >= '0' and cchar <= '9'):  # If it is not valid
            if (valid_pass == 1):     # Store possible pass if it was valid so far
                if (nchar > max_char):
                    max_char = nchar
                    
            valid_pass = 0 
            nchar = 0     
        else:
            nchar += 1;
            if (valid_pass == 0):  # We check if it has become a valid pass
                if (cchar >= 'A' and cchar <= 'Z'):
                    valid_pass = 1;
    
    # Last check
    if (valid_pass == 1):     # Store possible pass if it was valid so far
        if (nchar > max_char):
            max_char = nchar
            
    return max_char
    
print solution(s)

