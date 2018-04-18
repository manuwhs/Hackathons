
#import os
#os.chdir("../../")
#import import_folders
#
### Import standard libraries
## Import libraries
#
#from graph_lib import gl

import queue
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
folder = "./data/"
filenames = ["d_metropolis.in"] #  "a_example.in", "b_should_be_easy.in", "c_no_hurry.in" , "d_metropolis.in", "e_high_bonus.in"];


 ####### GENERATE THE OUTPUT ##########
def generate_output(list_vehicles, file_name):
    """
    format of list_vehicles = [[0], [2, 1]]
    """
    
    archivo = open("./output_" + file_name + ".txt","w")

    for i in range(len(list_vehicles)):
        archivo.write(str(len(list_vehicles[i])) + " ")
        
        for j in range(len(list_vehicles[i])):
            archivo.write(str(list_vehicles[i][j]) + " ")
        archivo.write("\n")
        
    archivo.close()

    # Compute distances
def sort_and_get_order (x, reverse = True ):
    # Sorts x in increasing order and also returns the ordered index
    x = x.flatten()  # Just in case we are given a matrix vector.
    order = range(len(x))
    
    if (reverse == True):
        x = -x
        
    x_ordered, order = zip(*sorted(zip(x, order)))
    
    if (reverse == True):
        x_ordered = -np.array(x_ordered)
        
    return np.array(x_ordered), np.array(order)

#def assign_car()
if(1):
    for filename in filenames:
    
        ####### READ THE INPUT ##########
        df = pd.read_csv(folder + filename, sep = ' ', header = None, names = ["a", "b", "x", "y","s","f"]) # header = None, names = None 
        rows, columns, vehicles, rides, bonus, steps = df.ix[0]
        
        ## Remove firsr line
        df = df.ix[1:]
        
        # Sort by finalizig time
        df = df.sort_values(['f'], ascending=[1])
    
        if (1):
           ## Data structure for solutions
            vehicles_rides_list = []
            for i in range(vehicles):
                vehicles_rides_list.append([])
            
            ## Data structure for the state of the cars:
            vehicles_state = []
            for i in range(vehicles):
                vehicles_state.append([0,0])  # [final_x, final_y, time when it finishes job]
            
            ### while there are more rides to assign
            final_time_queue = queue.PriorityQueue()
            for i in range(vehicles):
                final_time_queue.put([0,i])  # [final_x, final_y, time when it finishes job]
            
            
            
            TOTAL_SCORE = 0
            
            while(df.shape[0] > 0):
                
                if (df.shape[0]%100 == 0):
                    print ("Rides left", df.shape[0])
                    
                finalized_time, next_idle_vehicle = final_time_queue.get()
    #            print ("Vehicle: ", next_idle_vehicle)
    #            print ("Current_time_finalized_job: ", finalized_time)
    #            print ("Position: ", vehicles_state[next_idle_vehicle])
                ## Now we assign the next task by computing the score of the next 100 rides and selecting one
                Ncaca = 10000
                a,b,x,y,s,f = np.array(df.iloc[0:Ncaca]["a"]) , np.array(df.iloc[0:Ncaca]["b"]), np.array(df.iloc[0:Ncaca]["x"]) ,np.array(df.iloc[0:Ncaca]["y"]) ,np.array(df.iloc[0:Ncaca]["s"]) ,np.array(df.iloc[0:Ncaca]["f"]) 
            
                scores = np.zeros(a.shape)
                distance_start = np.abs(vehicles_state[next_idle_vehicle][0] - a) + np.abs(vehicles_state[next_idle_vehicle][1] - b)
                distance_end = np.abs(x - a) + np.abs(y - b)
                    
                total_distance = distance_start + distance_end;
                
                
                scores[np.where(finalized_time + total_distance < f)] += distance_end[np.where(finalized_time + total_distance < f)];
                scores[np.where(distance_start + finalized_time < s)] += bonus;
                

                idle_time = np.max([np.abs(distance_start), s - finalized_time], axis = 0)
            #    print (idle_time, distance_start, distance_end,  s - current_time)
                finish_time = finalized_time + idle_time + distance_end;
    
        
                    
    #            print ("Possible Scores: ", scores)
    #            print ("Reward Scores: ",  scores_good)
    #            print ("Idle Scores: ", scores_idle)
                ## Todo 
                
                bias = int(np.random.uniform(0,min([5,scores.size])))
                ordered_score, order = sort_and_get_order(scores - idle_time)
                indx = order[bias]
 
    #            print ("Selected Index: ", indx)
    #            print (  df.iloc[indx])
                ## Put the car in the queue again
                final_time_queue.put([finish_time[indx],next_idle_vehicle])   # finish_time   # df.iloc[indx]["f"]
                
                # Put the ride in the output file 
                vehicles_rides_list[next_idle_vehicle].append(df.index[indx]-1)
        
                
                TOTAL_SCORE += scores[indx] # TODO
                
                        # Update positon of car
                vehicles_state[next_idle_vehicle] = df.iloc[indx]["x"], df.iloc[indx]["y"]
                
                ## Removing the ride
                # df.remove(indx)
                df.drop(df.index[indx], inplace=True)

        print ("Score: ", TOTAL_SCORE)
        generate_output(vehicles_rides_list, filename)


    
    
    