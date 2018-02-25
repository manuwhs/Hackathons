# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 15:07:01 2016

@author: montoya
"""

import pandas as pd
import numpy as np
import datetime as dt

from calendar import monthrange
from dateutil.relativedelta import relativedelta
from graph_lib import gl
import matplotlib.pylab as plt

plt.close("all")
# Difference in months between two dates
#def monthdelta(d1, d2):
#    delta = 0
#    while True:
#        mdays = monthrange(d1.year, d1.month)[1]
#        d1 += dt.timedelta(days=mdays)
#        if d1 <= d2:
#            delta += 1
#        else:
#            break
#    return delta
    
def get_dividends(Nshares, dividendValue, 
                  edate, lastDiv, # Dates of start and end
                  m_period,  
                  inflation = 0.02):  # Inflation
    # Nshares: The number of shares we hold
    # dividendValue: Estimated value of the dividend of a share
    # m_period: Each how many months we get dividends
    # edate: The date up to which we calculate the dividends
    # lastDiv: Last time we obtained dividends.
    # inflation: Yearly inflation rate.
    freq = 12/m_period  # Frequency
#    time_delta = dt.timedelta(weeks=4, days=2, hours=0,
#                          minutes=0, seconds=0)  # adds up to 365 days
#    lastDiv = lastDiv + dt.timedelta(m_period*(365.0/12))
    lastDiv = lastDiv + relativedelta(months=+m_period)
    
    ## Initilize it !
    total_dividends = 0
    t = 1 # Number of periods past
    while (lastDiv <= edate):
        div_i = dividendValue*Nshares
         # We apply the inflation
#        months_past = (sdate - lastDiv).total_seconds()/60*60*24*30
        inflation_div = np.power(1 + inflation/freq, freq*t)
        div_i = div_i/inflation_div
#        print inflation_div
        
        # While the time we get the dividend is less than the current price.
        total_dividends += div_i
        lastDiv = lastDiv + relativedelta(months=+m_period)
        t += 1
    return total_dividends

##############################################
########## BASIC LOADING #####################
##############################################

port_path = "./Danske Bank task/Anne_Portfolio.csv"
dataCSV = pd.read_csv(port_path,
                  sep = ',',  # Separation of the columns
                  index_col = 0, # First column is the index
                  header = 0) # The header is the first row

# Print index and columns
print dataCSV.index.values
#['General Electric' 'HP Inc' 'Exxon Mobil Corp' 'Danske Bank']
print dataCSV.columns.values
#['ISIN' 'Amount (No.)' 'Recent dividend payed (per share)' 'Dividend currency']
# Company names in yahoo
Companies = dataCSV.index.values

##############################################
########## Temporal Variables  ###############
##############################################
sdate = dt.date(2016,12,31) # Start date
edate = dt.date(2017,12,31) # End date
# List of the last dates we got dividends
lastDivs = [dt.date(2016,10,25), dt.date(2016,10,5),
            dt.date(2016,12,9),dt.date(2016,3,22)] 

# Period  in months of the dividends
m_periods = [3, 3, 3, 10]  # Periods of the dividends
TAX = 0.25   # TAXes on profit
USDDKK = 7.12  # Exchange rate
inflation = 0.00  # yearly inflation rate

##############################################
########## Compute Dividends   ###############
##############################################

total_div = 0
# For every company
for i in range(len(Companies)):
    comp = Companies[i]
    dividends = get_dividends(dataCSV['Amount (No.)'][comp], 
                               dataCSV['Recent dividend payed (per share)'][comp],
                                edate,lastDivs[i], m_periods[i],
                                inflation = inflation)

   # Check the currency
    if (dataCSV['Dividend currency'][comp] == "USD"):
        dividends = dividends * USDDKK
        print "%s changed currency" % comp
    
    # Apply the TAXes
    dividends = dividends * (1-TAX)
    
    total_div += dividends                            
                                  
print "The total divididends are: %0.2f" % (total_div) 
                                
estimation = 12900 * 0.23 * 4 * USDDKK + \
        3700 *0.12*4* USDDKK  + \
        1300* 0.75*4*  USDDKK + \
        9733 * 8 * 2 # We expect it twice because of casuality
                     # On January and november
estimation = estimation * (1-TAX)
print "Checking %s" % estimation

#############################################################
############## See evolution of total expected benefit #######
############################################################

nyears = 10

all_divs = []
#for j in range (1,nyears + 1):  # In 10 years time.
#    edate = sdate.replace(year = sdate.year +j)

nmonths = nyears * 12 + 1
range_months = range (1,nmonths)
for j in range_months:  # In 10 years time.
    edate = sdate + relativedelta(months=+j)
    total_div = 0
    for i in range(len(Companies)):
        comp = Companies[i]
        dividends = get_dividends(dataCSV['Amount (No.)'][comp], 
                                   dataCSV['Recent dividend payed (per share)'][comp],
                                    edate,lastDivs[i], m_periods[i],
                                    inflation = inflation)
    
       # Check the currency
        if (dataCSV['Dividend currency'][comp] == "USD"):
            dividends = dividends * USDDKK
#            print "%s changed currency" % comp
        
        # Apply the TAXes
        dividends = dividends * (1-TAX)
        
        total_div += dividends                            
    all_divs.append(total_div)

gl.subplot2grid((4,4), (0,0), rowspan=4, colspan=4)
gl.plot(range_months,all_divs, 
        legend = ["Inflation 0%"], 
        labels = ["Dividends","Months", "DKK"], nf = 0, fill =1, alpha = 0.5)
gl.set_xlim(range_months[0],range_months[-1])


if (1):
    #TAX = 0.25
    inflation = 0.02
    all_divs = []
    
    dataCSV.loc['HP Inc' , 'Amount (No.)'] += 1300 
    dataCSV.loc['Exxon Mobil Corp' ,'Amount (No.)'] -= 1000 
    
    
    #for j in range (1,nyears + 1):  # In 10 years time.
    #    edate = sdate.replace(year = sdate.year +j)
    
    nmonths = nyears * 12 + 1
    range_months = range (1,nmonths)
    for j in range_months:  # In 10 years time.
        edate = sdate + relativedelta(months=+j)
        total_div = 0
        for i in range(len(Companies)):
            comp = Companies[i]
            dividends = get_dividends(dataCSV['Amount (No.)'][comp], 
                                       dataCSV['Recent dividend payed (per share)'][comp],
                                        edate, lastDivs[i], m_periods[i],
                                        inflation = inflation)
        
           # Check the currency
            if (dataCSV['Dividend currency'][comp] == "USD"):
                dividends = dividends * USDDKK
    #            print "%s changed currency" % comp
            
            # Apply the TAXes
            dividends = dividends * (1-TAX)
            
            total_div += dividends                            
        all_divs.append(total_div)
        
    print "The total divididends are: %0.2f" % (all_divs[-1]) 
    gl.plot(range_months, all_divs, legend = ["Inflation 2%"], nf = 0, fill =1, alpha = 0.5)
    #gl.set_xlim(1,nyears)

