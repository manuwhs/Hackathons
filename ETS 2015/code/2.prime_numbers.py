# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:33:12 2015

@author: montoya
"""
# We use pandas library to read CSV data.
import numpy as np

N_ini = 0000
N_fin = 9999

def get_primes(n_ini, n_fin):
    
    # Get the prime numbers using sieves, n_fin > 6
    
    sieve = np.ones(n_fin/3 + (n_fin%6==2), dtype=np.bool)
    sieve[0] = False
    for i in xrange(int(n_fin**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[      ((k*k)/3)      ::2*k] = False
            sieve[(k*k+4*k-2*k*(i&1))/3::2*k] = False
            
    all_primes = np.r_[2,3,((3*np.nonzero(sieve)[0]+1)|1)]
    primes_subset = all_primes[np.where(all_primes > n_ini)]
    return primes_subset
    
primes = get_primes(N_ini, N_fin)

# Since the distance between firts and last number is 6660, this constraints 
# the first number of the series to be lower than 9999 - 6660 = 3339
# The last number does not change so it does not matter but at least it cannot
# be 2 or 5.

# We can apply the following constraints !!
# abc can only change to another 2 permutation sets:
#  - abc, bca, cab   [1]
#  - abc, cab, bca   [2]
# b and c have to overflow 9 in any of the two permutations  and a cannot overflow 9 so:
#  - a < 4 and (b > 3, c > 6) or  (c > 3, b > 6)

"""
Also, we can derive the constraint for [1]   abc, bca, cab 
    a = (c + 3) % 10
    c = (b + 3 + I[c + 3 > 9]) % 10 
    b = a + 3 + I[b + 3 > 9]
    
    b = (a + 3) % 10
    a = (c + 3 + I[a + 3 > 9]) % 10 
    c = b + 3 + I[c + 3 > 9]

Since a < 4 -> We have that a + 3 < 9 so we change equations to:
    a = (c + 3) % 10
    c = (b + 3 + I[c + 3 > 9]) % 10 
    b = a + 3 + I[b + 3 > 9]
    
    b = (a + 3)
    a = (c + 3) % 10 
    c = b + 3 + I[c + 3 > 9]

Since b = a + 3, we have I[b + 3 > 9] = 0, so b < 7
    a = (c + 3) % 10
    c = (b + 3 + I[c + 3 > 9]) % 10 
    b = a + 3 
    
    b = (a + 3)
    a = (c + 3) % 10 
    c = b + 3 + I[c + 3 > 9]

We use the 2 equations of c:
    c = (a + 6 + I[c + 3 > 9]) % 10 
    c = a + 6 + I[c + 3 > 9]
    
So:
    c = a + 6 + I[c + 3 > 9]

Since c > 6:
    c = a + 6 + 1 = a + 7
    
So we end up with the solution:

 a < 4, b = a + 3, c = a + 7

We just have to check if this numbers are in the prime numbers,
for example we have the tuples:

(037,370,703)... (148,481,814)... BINGO !!

"""


"""
Also, we can derive the constraint for [2] abc, cab, bca
    b = (c + 3) % 10
    a = (b + 3 + I[c + 3 > 9]) % 10 
    c = a + 3 + I[b + 3 > 9]
    
    a = (b + 3) % 10
    c = (a + 3 + I[b + 3 > 9]) % 10 
    b = c + 3 + I[a + 3 > 9]

Since a < 4 -> We have that a + 3 < 9 so we change equations to:
    b = (c + 3)
    a = (b + 3 + I[c + 3 > 9]) % 10 
    c = a + 3 + I[b + 3 > 9]
    
    a = (b + 3) % 10
    c = (a + 3 + I[b + 3 > 9]) % 10 
    b = c + 3 

Since b = c + 3, we have I[c + 3 > 9] = 0, so c < 7

    b = (c + 3)
    a = (b + 3) % 10 
    c = a + 3 + I[b + 3 > 9]
    
    a = (b + 3) % 10
    c = (a + 3 + I[b + 3 > 9]) % 10 
    b = c + 3 
    
Since a < 4 and b > 7, we hav that I[b + 3 > 9] = 1 so:

    c = a + 4
    

So we end up with the solution:

 a < 4, b = c + 3, c = a + 4

We just have to check if this numbers are in the prime numbers,
for example we have the tuples:

074,407,740, 185,518,851.....

"""

## Code to generate possible tuples: 

tuples = []

for a in range (0,4):
    tuples.append([a,a+3,a+7])
    tuples.append([a,a+7,a+4])

# So, there are only 8 possible stating values:

starts = []
for t in tuples:
    start = t[0]*100 + t[1]*10 + t[2]
    starts.append(start)
    
# Get rid of the last number to check ocurrences of the start
primes_3f = np.array(primes/10,dtype = int)
    
# Check that the starts are in the prime number and also its permutations:
Results = []
for s in starts:
    idx = np.where(primes_3f == s)[0] # Ge the index of ocurrences of the start for the 3 first ones.

    if (idx.size != 0):  # If there exist
        
        for i in idx:  # For each possible start, find if there exists the tuple
            init_number = primes[i]
            valid = 1
            for n in range (1,3):
                if (np.where(primes == init_number + 3330*n)[0].size == 0):
                    valid = 0
                    break
            if (valid == 1):
                Results.append(init_number)
                
## Get the final tuples:

for r in Results:
    resu = [r, r + 3330, r + 6660]
    print resu
                
