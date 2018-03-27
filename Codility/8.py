# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 19:57:12 2016

@author: montoya
"""

def solution(A, K):
    # write your code in Python 3.6
    N,M = len(A),len(A[0])
    switches_w_balls = [[0,0,K,"down"]]  # List of [i,j,N,direction] triplets with info of cells with balls.
    new_swb = []
    score = 0
    
    while (len(switches_w_balls) > 0):
        for switch in switches_w_balls:
            new_swb = [];
            ## Check if we stop
            
            if (switch[0] == N-1 and switch[1] == M-1 and switch[3] == "down" ):
                score +=  switch[2]
                continue;
            elif (switch[0] == N ):
                continue;
            elif (switch[1] == M ):
                continue;
                
            if (A[switch[0]][switch[1]] == -1):
                new_swb.append([switch[0]+1,switch[1],int(switch[2]/2) + switch[2]%2 ,"down"])
                new_swb.append([switch[0],switch[1]+1,int(switch[2]/2),"right"])
                if (switch[2]%2 == 1):
                    A[switch[0]][switch[1]] = - A[switch[0]][switch[1]]
                 
            elif(A[switch[0]][switch[1]] == 1):
                new_swb.append([switch[0]+1,switch[1],int(switch[2]/2),"down"])
                new_swb.append([switch[0],switch[1]+1,int(switch[2]/2) + switch[2]%2 ,"right"])
                if (switch[2]%2== 1):
                    A[switch[0]][switch[1]] = - A[switch[0]][switch[1]]
                
            elif(A[switch[0]][switch[1]] == 0):
                if (switch[3] == "down"):
                    new_swb.append([switch[0]+1,switch[1],switch[2],"down"])
                else:
                    new_swb.append([switch[0],switch[1]+1,switch[2],"right"])
            #print ("moved", switch)
        switches_w_balls = new_swb
    return score