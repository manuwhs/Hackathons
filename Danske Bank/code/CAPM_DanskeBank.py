""" BASIC USE OF THE LIBRARY FOR INTRODUCTORY ANALYSIS """
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
import CPortfolio as CPfl
import CCAPM as CCAPM

# Import functions independent of DataStructure
import utilities_lib as ul

plt.close("all")

##########################################################
############### CAPM model !!! ######################
##########################################################
## Load the porfolio in the CAPM model
periods = [43200]   # 43200 1440
source = "Yahoo" # Hanseatic  FxPro GCI Yahoo
[storage_folder, info_folder, 
 updates_folder] = ul.get_foldersData(source = source)
 
#symbols = ["XAUUSD", "XAGUSD", "NYMEX.CL"]
symbols =  ["GE", "HPQ","XOM"]
#symbols = ["Mad.ELE","Mad.ENAG","Mad.ENC","Mad.EZE","Mad.FER","Mad.GAM"]
#symbols = ["USA.JPM","USA.KO","USA.LLY","USA.MCD","USA.MMM","USA.MO","USA.MON",
#           "USA.MRK","USA.OXY","USA.PEP","USA.PFE"]
################## Date info ###################
sdate_str = "01-01-2010"
edate_str = "01-12-2016"
sdate = dt.datetime.strptime(sdate_str, "%d-%m-%Y")
edate = dt.datetime.strptime(edate_str, "%d-%m-%Y")

####### LOAD SYMBOLS AND SET Properties   ###################
Cartera = CPfl.Portfolio(symbols, periods)   # Set the symbols and periods to load
Cartera.load_symbols_csv(storage_folder)

########## Set the CAPM model object ##########
CAPMillo = CCAPM.CAPM(Cartera, periods[0])
CAPMillo.set_allocation([])  # Initial allocation of the porfolio
CAPMillo.set_Rf(0.0)  # Risk-free rate
CAPMillo.set_seriesNames(["Close"])  # Adj Close 
CAPMillo.set_index('XAUUSD')  # Set the index commodity

CAPMillo.pf.set_interval(sdate,edate)

########## FILLING THE DATA ##########
print "Filling Data"
CAPMillo.pf.fill_data()
print "Data Filled"

dates = CAPMillo.pf.symbols[symbols[0]].TDs[periods[0]].dates
rand_alloc_Danske = 1
if (rand_alloc_Danske == 1):
#    gl.set_subplots(2,1)
    Nalloc = 10000
    # Get the efficient frontier where we cannot borrow or lend money
    alloc = CAPMillo.get_random_allocations(Nalloc, short = "no", mode = "gaussian")
    CAPMillo.scatter_allocations(alloc, alpha = 0.8, nf = 1, legend = ["Markovitz alloc"])
    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Markowitz")
    CAPMillo.plot_allocations(portfolios, legend = ["Markowitz Eff"], nf = 0)
    CAPMillo.scatter_allocations(np.eye(CAPMillo.Nsym), 
            legend = ["Assets"], nf = 0, alpha = 1.0, lw = 5)
    
#    alloc = CAPMillo.get_random_allocations(Nalloc, short = "yes", mode = "gaussian")
#    CAPMillo.scatter_allocations(alloc, alpha = 0.8, legend = ["Normal alloc"])
#    optimal, portfolios = CAPMillo.efficient_frontier(kind = "Tangent", max_exp = 100.0)
#    CAPMillo.plot_allocations(portfolios, legend = ["Normal Eff"], nf = 0)
#    CAPMillo.scatter_allocations(np.eye(CAPMillo.Nsym), 
#            legend = ["Assets"], nf = 0, alpha = 1.0, lw = 5)

    # CAPMillo.pf.symbols.keys()
    ret, std = CAPMillo.compute_allocations(np.eye(CAPMillo.Nsym))
    for label, x, y in zip(CAPMillo.pf.symbol_names,std, ret):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.8),
            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
    
    ## Compute market line and optimal portfolio
    ret, risk = CAPMillo.compute_allocations(portfolios)
    SR = np.divide(ret, risk)
    inde = np.argmax(SR)
    optimal = portfolios[inde]

    ret, risk = CAPMillo.compute_allocations([optimal,optimal])
    gl.plot([0, 2*risk[0]],[0, 2*ret[0]],
                legend = ["Mkt Line Rf: 0.0% "],
                nf = 0,loc = 2)
                
    CAPMillo.scatter_allocations([optimal,optimal], 
            legend = ["Optimal"], nf = 0, alpha = 1.0, lw = 5)
