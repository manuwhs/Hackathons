import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

def matlab2datetime(matlab_datenum):
    day = dt.datetime.fromordinal(int(matlab_datenum))
    dayfrac = dt.timedelta(days=matlab_datenum%1) - dt.timedelta(days = 366)
    return day + dayfrac


def get_Data(Data_list, t_i, p1 = "ActWind", p2 = "value"):  #   "time"
    # "ActWind" "ActPower"    "value" "time"
    Data1 = Data_list[0][p1][0][t_i][0,0][p2]
    Data2 = Data_list[1][p1][0][t_i][0,0][p2]
    
    total_Data = np.concatenate((Data1,Data2),axis = 0)
    
    
    return total_Data

def get_Time(Data_list, i = 0):
    Time =  get_Data(Data_list,i,"ActPower","time")
    TimeGood = [matlab2datetime(tim[0]) for tim in Time]
    return TimeGood


def scatter_graph(x,y,labels = [],new_fig = 1, color = None):
    y = np.array(y)
#    print y.shape
#    print x.shape
    if (new_fig == 1):
        fig = plt.figure()  # figsize = [w,h]
        
    if (x == []): # If x is empty
        print "X was empty"
        y_shape = y.shape
        x = np.array(range(y_shape[0]))
        
    print x.shape, y.shape
        # TODO for some reason doesnt let me print matrix so convert to list
    
    if (color == None):
        color = np.random.uniform(0,1,(1,3))
        
    plt.scatter(x.tolist(),y.tolist(), 
                color = color, 
                lw = 3,
                alpha = 0.4)

    if (new_fig == 1):  # We put the general labels and the label of the points
#        plt.title(labels[0])
#        plt.xlabel(labels[1])
#        plt.ylabel(labels[2])
        
        scatter_graph.aux_label = []  # Labels to accumulate
        
        fig.suptitle(labels[0], fontsize=20)
        plt.xlabel(labels[1], fontsize=20)
        plt.ylabel(labels[2], fontsize=20)

        if (len(labels) > 3 ):

            ## Self variable for storing the labels
            scatter_graph.aux_label.append(labels[3])
            plt.legend( scatter_graph.aux_label, loc=2)
    else:
        if(len(labels) > 0):
            (scatter_graph.aux_label).extend(labels)
            plt.legend(scatter_graph.aux_label, loc=2)
        
    plt.grid()
    plt.show()
    
    return plt

def plot_graph(x,y,labels,new_fig = 1, color = None):
    y = np.array(y)
    lw = 3
    loc = 1
#    print y.shape
#    print x.shape
    if (new_fig == 1):
        fig = plt.figure()  # figsize = [w,h]
        
    if (x == []): # If x is empty
#        print "X was empty"
        y_shape = y.shape
        x = np.array(range(y_shape[0]))
        
#    print x.shape, y.shape
        # TODO for some reason doesnt let me print matrix so convert to list

    if (color == None):

        plt.plot(x.tolist(),y.tolist(), 
                    lw =lw)
    else:
        plt.plot(x.tolist(),y.tolist(), color = color,
                    lw =lw)
    
#    plt.fill_between(x.tolist(),y.tolist(), alpha = 0.3)    
        
    if (new_fig == 1):  # We put the general labels and the label of the points
#        plt.title(labels[0])
#        plt.xlabel(labels[1])
#        plt.ylabel(labels[2])
        
        fig.suptitle(labels[0], fontsize=20)
        plt.xlabel(labels[1], fontsize=20)
        plt.ylabel(labels[2], fontsize=20)
        scatter_graph.aux_label = []
        
        if (len(labels) > 3 ):
            plt.legend(labels[1])
            ## Self variable for storing the labels
            scatter_graph.aux_label.append(labels[3], loc=loc)
            
    else:
        if(len(labels) > 0):
            (scatter_graph.aux_label).extend(labels)
            plt.legend(scatter_graph.aux_label, loc=loc)
        
    plt.grid()
    plt.show()
    
    return plt



### Removes the NAN and values below a threshold
def clean_data(X, threshold = 10):
    threshold= 10
    ########## NAN Removing ############
    # Get the nan index and delete them
    Nan_index = np.argwhere(np.isnan(X))
    # [Data_est.pop(i) for i in sorted(Nan_index,reverse=True)] # Inline
    X = np.delete(X,Nan_index)
    
    ####### Zeros removing  #########
    Miss_index = np.argwhere(X < threshold)
    X = np.delete(X,Miss_index)

    return X

### Removes the NAN and values below a threshold
def clean_data_PowWin(Pow,Win, threshold = 1):
    ########## NAN Removing ############
    # Get the nan index and delete them
    Nan_index_Pow = np.argwhere(np.isnan(Pow))
    Pow = np.delete(Pow,Nan_index_Pow)
    Win = np.delete(Win,Nan_index_Pow)
    
    Nan_index_Win = np.argwhere(np.isnan(Win))
    Pow = np.delete(Pow,Nan_index_Win)
    Win = np.delete(Win,Nan_index_Win)
    ####### Zeros removing  from power #########
    Miss_index = np.argwhere(Pow < threshold)
    Pow = np.delete(Pow,Miss_index)
    Win = np.delete(Win,Miss_index)

    return Pow,Win
    
    
def ultimate_cleaning (Pow,Win,th_0sPow, th_wind, th_power):
    Pow,Win = clean_data_PowWin(Pow,Win,th_0sPow)

    #### Remove too high power (We want to remove saturation)
#    thr = get_upper_threshold(Pow)
#    Index = np.argwhere(Pow > thr)
#    Pow = np.delete(Pow,Index)
#    Win = np.delete(Win,Index)
    
    Index = np.argwhere(Win > th_wind)
    Pow = np.delete(Pow,Index)
    Win = np.delete(Win,Index)
    
    return Pow,Win
    
from sklearn.neighbors import KernelDensity
def kde_sklearn(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scikit-learn"""
    kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
    kde_skl.fit(x[:, np.newaxis])
    # score_samples() returns the log-likelihood of the samples
    log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
    return np.exp(log_pdf)



## Get histogram
Nbins = 100

def get_upper_threshold(Power):
    Max_Power = max(Power)
    threshold = Max_Power * 0.85
    return threshold


def get_histogram(X, Nbins = 100, bandwidth = 0.2, labels = [], threshold = 1):
    ## Clean the data !!

    X = clean_data(X)
    Max_Pow = max(X)
    Min_Pow = min(X)

    x_grid = np.linspace(Min_Pow, Max_Pow, Nbins)
    
    estimation = kde_sklearn(X.flatten(), 
                             x_grid.flatten(), 
                            bandwidth=bandwidth)
    
    plot_graph(x_grid,
               estimation,
               labels = labels, 
                 new_fig = 1)
    
    return estimation
    
import matplotlib
matplotlib.rc('xtick', labelsize=13) 
matplotlib.rc('ytick', labelsize=13)

def price_volume_graph(date,price,volume,labels,new_fig = 1):
    """ This function plots the volume and price all together with different scales
    so that they can be seen properly """
    
    if (new_fig == 1):
        fig = plt.figure(figsize = [6,8])
        
    if (date == []): # If x is empty
        price_shape = price.shape
        date = np.array(range(price_shape[0]))
        
    price = np.array(price)
    volume = np.array(volume)
    
    # Define axis to plot price
    ax_price = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)  
    ax_price.plot(date,price, color = "b", lw = 3, label = labels[3][0]) 
    
    ### X axis date properties, just to be seen clearly
    for label in ax_price.xaxis.get_ticklabels():
            label.set_rotation(45)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    
    
    # Define axis to plot volume
    ax_volume = ax_price.twinx()  # Copy ax_volume with the "x" 
    ax_volume.bar(date, volume, width = 0.025,facecolor= "g",alpha=.5)
    

    
    if (len(labels) >3 ):
        ax_price.set_ylabel("Price DKK per KWh",fontsize=20)
        ax_volume.set_ylabel("Power Production",fontsize=20)
#        plt.legend(labels[3])
        
    fig.suptitle("Price graph", fontsize=20)
    plt.xlabel("Time", fontsize=20)
#    plt.ylabel(labels[2], fontsize=20)
        
#    plt.ylabel(labels[2])
    plt.subplots_adjust(bottom=.15)  # Done to view the dates nicely
    
    plt.grid()
    plt.show()