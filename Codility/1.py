# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 23:55:22 2016

@author: montoya
"""


def sum_list (lista):
    n = 0;
    if (lista == []):
        return 0;
        
    for i in lista:
        n += i
    
    return n
    
def solution(A):
    A_len = len(A)
    if (A_len == 0):
        return -1
        
    equi_list = []  # list of equilibriums
    
    total_A = sum_list(A)
    print "Hola!"
    print total_A

    left = 0 
    right = total_A - A[0]
    
    if (left == right):
        equi_list.append(0)
        return 0
        
    for i in range(1,A_len):
        left += A[i-1] 
        right -= A[i]   
        
        if (left == right):
            equi_list.append(i)
            return equi_list[0]
            
    if (equi_list == []):
        return -1
        
    print equi_list
    return equi_list
    
prime = [500, 1, -2, -1, 2]
secon = [-1, 3, -4, 5, 1, -6, 2, 1]
solution(prime)