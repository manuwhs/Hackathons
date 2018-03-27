# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya
"""
# We use pandas library to read CSV data.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")   # Close all figures
file_dir = "./chickens.csv"
def read_dataset(file_dir = "./chickens.csv"):
    
    data = pd.read_csv(file_dir, sep = ',',header = None, names = None) 
    # names = None coz the file does not contain column names
    Nsamples, Ndim = data.shape   # Get the number of bits and attr
    data_np = np.array(data, dtype = float).reshape(Nsamples, Ndim)
    
    return data_np

# Get the prices list and its shape
data = read_dataset(file_dir)
Nsamples, dim = data.shape

weight = data[:,0]
time = data[:,1]
chick = data[:,2]
diet = data[:,3]

# Get the different number of chiquens and diets
chicks = np.unique(chick)
diets = np.unique(diet)

Nc = len(chicks)
Nd = len(diets)

# Lets split the data into the diferent diets:
diets_indx = []
for d in range (1,5):
    diets_indx.append(np.where(diet == d)[0])

# Get the diet of every chicken
chicken_diets = []
for i in range(len(diets_indx)):
    cd = np.unique(chick[diets_indx[i]])
    chicken_diets.append(cd)

diet_chick = np.zeros((1,Nc))
aux = 0
for d in range(Nd):
    for i in chicken_diets[d]:
        diet_chick[0,int(i)-1] = diets[d]

# Lets split the data into the diferent chickens:
chick_indx = []
for c in range (1,int(chick[-1]) +1):
    chick_indx.append(np.where(chick == c)[0])


""" FIRST ESTIMATOR """

# For every chicken, get the weight it got over the 21 days:
chick_in_weight = []
for c in range(len(chick_indx)):
    dw = (weight[chick_indx[c][-1]] - weight[chick_indx[c][0]])/(time[chick_indx[c][-1]] - time[chick_indx[c][0]])
    chick_in_weight.append(dw)

chick_in_weight = np.array(chick_in_weight)  # Transform to numpy array
# Now we have chick_in_weight as parameter of every chicken and diet_chick as the diet of eery chicken.
# For every class we gather all the increasing weight:


in_weighy_by_diet = []
for i in range(Nd):
    in_weighy_by_diet.append([])
    
for i in range(Nc):
    n_diet = int(diet_chick[0,i])-1
    in_weighy_by_diet[n_diet].append(chick_in_weight[i])

plt.figure()

colors = ['b','g','k','r']
for i in range (Nd):
    plt.scatter(in_weighy_by_diet[i], np.ones((1,len(in_weighy_by_diet[i])))*i, lw=3, color = colors[i])   

plt.title('Total Weight Increase of chickens')
plt.xlabel('Total Weight Increase')
plt.ylabel('Diets')
plt.legend(['1','2','3','4'])


# Get statistics of the weight increase:

averages = np.zeros((1,Nd))
for i in range (Nd):
    averages[0,i] = np.average(in_weighy_by_diet[i])

""" SECOND ESTIMATOR """

# For every chicken of every diet we get the increasing of weight over time

in_weighy_by_diet_setps = []
for i in range(Nd):
    in_weighy_by_diet_setps.append([])

for c in range(len(chick_indx)):
    for i in range(len(chick_indx[c])-1):
        dw = (weight[chick_indx[c][i+1]] - weight[chick_indx[c][i]])/(time[chick_indx[c][i+1]] - time[chick_indx[c][i]])
        n_diet = int(diet_chick[0,c])-1
        in_weighy_by_diet_setps[n_diet].append(dw)
        
plt.figure()

for i in range (Nd):
    plt.scatter(in_weighy_by_diet_setps[i], np.ones((1,len(in_weighy_by_diet_setps[i])))*i, lw=3, color = colors[i])   

plt.title('Weight Increase of chickens')
plt.xlabel('Weight Increase')
plt.ylabel('Diets')
plt.legend(['1','2','3','4'])


# Get statistics of the weight increase:

averages_steps = np.zeros((1,Nd))
for i in range (Nd):
    averages_steps[0,i] = np.average(in_weighy_by_diet_setps[i])


""" THIRD ESTIMATOR """

# For every chicken of every diet we get the increasing of weight over time

integral_weight  = []
for i in range(Nd):
    integral_weight.append([])
    
for c in range(len(chick_indx)):
    for i in range(len(chick_indx[c])-1):
        integral = (np.sum(weight[chick_indx[c][:]]) - weight[chick_indx[c][0]])/ (time[chick_indx[c][i+1]] - time[chick_indx[c][i]])
        n_diet = int(diet_chick[0,c])-1
        integral_weight[n_diet].append(integral)
        
plt.figure()
for i in range (Nd):
    plt.scatter(integral_weight[i], np.ones((1,len(integral_weight[i])))*i, lw=3, color = colors[i])   

plt.title('Integral Weight')
plt.xlabel('Integral Weight')
plt.ylabel('Diets')
plt.legend(['1','2','3','4'])


# Get statistics of the weight increase:

averages_integral = np.zeros((1,Nd))
for i in range (Nd):
    averages_integral[0,i] = np.average(integral_weight[i])




if (1):
# Graph of a typical chiquen:
# Plotear el avance del peso de una gallina
    plt.figure()
    
    chickens = [1 , 9, 15, 25, 30, 34, 45, 23]
    for c in chickens:
        plt.plot(time[chick_indx[c][:]] ,weight[chick_indx[c][:]] , lw=3)   

    plt.title('Evolution of weight of a chicken')
    plt.xlabel('time')
    plt.ylabel('weight')







