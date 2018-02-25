
"""
ValueError: DateFormatter found a value of x=0, which is an illegal date.  This usually occurs because you have not informed the axis that it is plotting dates, e.g., with ax.xaxis_date()
"""
""" BASIC USAGE OF THE CLASS"""
# Change main directory to the main folder and import folders
### THIS CLASS DOES NOT DO MUCH, A QUICK WAY TO AFFECT ALL THE TIMESERIES
## OF THE SYMBOL IN A CERTAIN MANNER, like loading, or interval.
## It also contains info about the Symbol Itself that might be relevant.
import os
os.chdir("../../")
import import_folders
# Classical Libraries
import copy as copy
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
# Own graphical library
from graph_lib import gl 
# Data Structures Data
import CSymbol as CSy
import CPortfolio as CPfl
# Import functions independent of DataStructure
import utilities_lib as ul

plt.close("all")
######## SELECT DATASET, SYMBOLS AND PERIODS ########
source = "Yahoo" # Hanseatic  FxPro GCI Yahoo
[storage_folder, info_folder, 
 updates_folder] = ul.get_foldersData(source = source)
################## Date info ###################
sdate_str = "01-01-2010"
edate_str = "21-12-2016"
sdate = dt.datetime.strptime(sdate_str, "%d-%m-%Y")
edate = dt.datetime.strptime(edate_str, "%d-%m-%Y")

####### SELECT SYMBOLS AND PERIODS #################
symbols =  ["GE", "HPQ","XOM","DANSKE.CO"]
periods = [43200]  # 1440  43200
period1 = periods[0]
####### LOAD SYMBOLS AND SET Properties   ###################
Cartera = CPfl.Portfolio(symbols, periods)   # Set the symbols and periods to load
# Download if needed.
#Cartera.update_symbols_csv_yahoo(sdate_str,edate_str,storage_folder)    # Load the symbols and periods
Cartera.load_symbols_csv(storage_folder)    # Load the symbols and periods
## SET THINGS FOR ALL OF THEM
Cartera.set_interval(sdate,edate)
Cartera.set_seriesNames(["Close"])

#######################################################
############# DANSKE BANK Stuff ###################
######################################################

timeDataObjs = Cartera.get_timeDataObj(period1)
Nsym = len(timeDataObjs)
gl.init_figure()

#ax1.xaxis_date()

i = 0
for tdo in timeDataObjs:
    gl.subplot2grid((Nsym,4), (i,0), rowspan=1, colspan=4)
    gl.tradingPV(tdo, color_mode = 1, fontsize = 15)
    i = i + 1
    ax = gl.get_axes()[-1]

all_axes = gl.get_axes()
for i in range(len(all_axes)-2):
    ax = all_axes[i]
    plt.setp(ax.get_xticklabels(), visible=False)
    
#plt.setp(ax.get_xticklabels(), visible=True)
plt.suptitle("Danske Bank",color='k', fontsize = 20)
plt.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)
#gl.savefig("./pene.png", dpi = 200)



dividends_calculation = 1
if (dividends_calculation == 1):
    m_periods = [3, 3, 3, 10] 
    values = [0.23,0.12,0.75,8]
    prices = Cartera.get_timeSeries(period1)[-1,:]
    
    Yield_dividend = np.divide(values,prices) * 12 / np.array(m_periods)
    print Cartera.symbol_names