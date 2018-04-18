# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya
"""
# We use pandas library to read CSV data.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

plt.close("all")
file_dir = "./data_prices.csv"
def read_dataset(file_dir = "./dataprices.csv"):
    
    data = pd.read_csv(file_dir, sep = ',',header = None, names = None) 
    # names = None coz the file does not contain column names
    Nsamples, Ndim = data.shape   # Get the number of bits and attr
    data_np = np.array(data, dtype = float).reshape(Nsamples, Ndim)
    
    return data_np

def get_Return(price_sequence):
    R = (price_sequence[-1] - price_sequence[0])/ price_sequence[0]
    return R

def sort_and_get_order (x):
    # Sorts x in increasing order and also returns the ordered index
    x = x.flatten()  # Just in case we are given a matrix vector.
    order = range(len(x))
    x_ordered, order = zip(*sorted(zip(x, order)))
    
    return np.array(x_ordered), np.array(order)
    
# Get the prices list and its shape
prices = read_dataset(file_dir)
Nsamples, Nprices = prices.shape


## Plot sequences 
plt.figure()

for i in range (Nprices):
    plt.plot(prices[:,i], lw=3)   

plt.title('Prices')
plt.xlabel('Working Day')
plt.ylabel('Price')
plt.legend(['1','2','3','4','5'])

# Plot Dayly returns
plt.figure()
for i in range (Nprices):
    plt.plot((prices[1:,i]-prices[:Nsamples-1,i])/prices[:Nsamples-1,i] + i*0.1, lw=3)

plt.title('Dayly Returns')
plt.xlabel('Working Day')
plt.ylabel('Return')
plt.legend(['1','2','3','4','5'])

# Get the annual returns
returns = np.zeros((1,Nprices))

for i in range (Nprices):
    returns[0,i] = get_Return(prices[:,i])

# Order them and get order
r_ordered, order = sort_and_get_order(returns)

order = np.flipud(order)   # We reverse since it is in increasing order.
r_ordered = np.flipud(r_ordered)


################# USE SIMPLE GAUSSIAN PROCESS EXAMPLE ################
Y = np.matrix(prices[:,0]).T   # Nsamples x Ndim matrix
Nsamples, Ndim = Y.shape

Ytrain = Y[0:Nsamples,:]
Ytest = Y[-1,:]   # Only last sample

# The X is just index:
X = np.matrix(range(Nsamples)).T
Xtrain = X[0:Nsamples,:]

Xtest = np.matrix(range(Nsamples + 100)).T + 0.5  # Interpolation
Ytest = np.ones(Xtest.shape)

Ntest, Ndim = Xtest.shape

# Preprocess X and Y 
from sklearn import preprocessing
#scaler = preprocessing.StandardScaler().fit(Xtrain)
#Xtrain = scaler.transform(Xtrain)            
#Xtest = scaler.transform(Xtest)       

scaler = preprocessing.StandardScaler().fit(Ytrain)
Ytrain = scaler.transform(Ytrain)            
Ytest = scaler.transform(Ytest)      

print Xtrain.shape
### Get hyperparameters

sigma_0 = np.std(Ytrain)
sigma_eps = sigma_0 / np.sqrt(100)
l = 50

## Do the magic
X_1d = Xtrain
Xt_1d = Xtest
idx = np.argsort(Xt_1d,axis=0) #We sort the vector for representational purposes
Xt_1d = np.sort(Xt_1d,axis=0)
idx = np.array(idx).flatten().T
Ytest = Ytest[idx]

dist = spatial.distance.cdist(X_1d,X_1d,'euclidean')
dist_ss = spatial.distance.cdist(Xt_1d,Xt_1d,'euclidean')
dist_s = spatial.distance.cdist(Xt_1d,X_1d,'euclidean')

K = (sigma_0**2)*np.exp(-dist/l)
K_ss = (sigma_0**2)*np.exp(-dist_ss/l)
K_s = (sigma_0**2)*np.exp(-dist_s/l)
                        
m_y = K_s.dot(np.linalg.inv(K + sigma_eps**2 * np.eye(K.shape[0]))).dot((Ytrain))
v_f = K_ss - K_s.dot(np.linalg.inv(K + sigma_eps**2 * np.eye(K.shape[0]))).dot(K_s.T)
v_f_diag = np.matrix(np.diagonal(v_f)).T

L = np.linalg.cholesky(v_f+1e-10*np.eye(v_f.shape[0]))

plt.figure()
#print m_y.shape

# Generate random prediction for the test points
for iter in range(50):
    f_ast = L.dot(np.random.randn(len(Xt_1d),1)) + m_y
    plt.plot(np.array(Xt_1d)[:,0],f_ast[:,0],'c:');

# Plot real data
plt.plot(np.array(Xtrain[:,0]),Ytrain[:,0],'r',linewidth=3,label='Real Data');

plt.plot(Xt_1d[:,0],m_y[:,0],'b-',linewidth=3,label='Predictive mean');
plt.plot(np.array(Xt_1d)[:,0],np.matrix(m_y[:,0]).T+2*v_f_diag,'m--',label='Predictive mean of f $\pm$ 2std',linewidth=3);
plt.plot(np.array(Xt_1d)[:,0],np.matrix(m_y[:,0]).T-2*v_f_diag,'m--',linewidth=3);

#Plot now the posterior mean and posterior mean \pm 2 std for s (i.e., adding the noise variance)
plt.plot(np.array(Xt_1d)[:,0],np.matrix(m_y[:,0]).T+2*v_f_diag+2*sigma_eps,'m:',label='Predictive mean of s $\pm$ 2std',linewidth=3);
plt.plot(np.array(Xt_1d)[:,0],np.matrix(m_y[:,0]).T-2*v_f_diag-2*sigma_eps,'m:',linewidth=3);

plt.legend(loc='best')
plt.xlabel('x',fontsize=18);
plt.ylabel('s',fontsize=18);

