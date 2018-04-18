import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import libratyWind as lW
import copy

########### LOGISTIC 4 Variables #######
def logistic4(x, A, B, C, D):
    """4PL lgoistic equation."""
    return ((A-D)/(1.0+((x/C)**B))) + D

def residuals_logistic4(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C,D = p
    err = y-logistic4(x, A, B, C, D)
    return err

def peval_logistic4(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)

########### Cubic  Variables #######

def saturated_cubic(x, Offset,Linear, Threshold, Saturation):
        
        Y = copy.copy(x)
        Nsamples = Y.shape[0]
        for i in range(Nsamples):
            Y[i] = Y[i]*Linear + Offset
    
            if (Y[i] > Threshold):
                Y[i] = Saturation
            else: 
                Y[i] = Y[i]**3
        
        return Y


#def saturated_cubic(x, Offset,Linear, Threshold, Saturation):
#        x = x*Linear + np.ones((1,x.shape[0]))*Offset
##        print x.shape
##        Y = copy.copy(x)
#        
##        Index = np.argwhere(x > Threshold)
##        Y[Index] = np.argwhere(x > Threshold)
#        x = x**3
##        print x.shape
#        x = x.T
#        Index = np.argwhere(x > Threshold**3)
##        print len(Index)
#        x[Index,0] = np.ones((len(Index),1))*Saturation
##        print x[Index]
##        print x.shape
#        return x.flatten()

def residuals_saturated_cubic(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B,C, D = p
    err = y - saturated_cubic(x, A, B, C, D)
    return err

def peval_saturated_cubic(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C, D = p
    return saturated_cubic(x, A, B, C, D)
    



def cubic(x, Offset,Linear):
        x = x*Linear + np.ones((1,x.shape[0]))*Offset
        x = x**3
        return x.flatten()

def residuals_cubic(p, y, x):
    """Deviations of data from fitted 4PL curve"""
    A,B = p
    err = y - cubic(x, A, B)
    return err

def peval_cubic(x, p):
    """Evaluated value at x with current parameters."""
    A,B = p
    return cubic(x, A, B)
    
import scipy.optimize as optimization


p0 = [1,1]
p0 = [0,1]
# 4logistic  
# saturated_cubic cubic

def fit_function(X,Y,func, p0, plotting = 0):
    if (func ==  "logistic4"):
        plsq = leastsq(residuals_logistic4, p0, args=(Y, X))
        
        sigma = [1]*len(p0)
        opt =  optimization.curve_fit(residuals_logistic4, X, Y, p0, sigma)
    elif (func ==  "saturated_cubic"):
        plsq = leastsq(residuals_saturated_cubic, p0, args=(Y, X))
        
        sigma = [100]*X.shape[0]
#        print sigma
        opt =  optimization.curve_fit(saturated_cubic, X, Y, p0, sigma)
        print opt
    elif (func ==  "cubic"):
#        plsq = leastsq(residuals_cubic, p0, args=(Y, X))
        k = 8
        plsq = np.polyfit(X, Y, k)
     
        
    if (plotting == 1):
    ### PLOT THE ESTIMATED FUNCTION WITH THE DATA
        Max_Pow = max(X)
        Min_Pow = min(X)
        Nbins = 100
        x_grid = np.linspace(Min_Pow, Max_Pow, Nbins)
    
        if (func ==  "4logistic4"):
            Yfunc = peval_logistic4(x_grid,plsq[0])
        elif (func ==  "saturated_cubic"):
            Yfunc = peval_saturated_cubic(x_grid,plsq[0])
        elif (func ==  "cubic"):
    #        Yfunc = peval_cubic(x_grid,plsq[0])
            Yfunc = np.poly1d(plsq)
            Yfunc = Yfunc(x_grid)
        
        lW.scatter_graph(X,Y,labels = ["Estimation of Curve", 
            "Wind Speed ", 
            "Power Turbine", "Data_Points"], new_fig = 1, color = [0.13,0.33,0.47])
        
        lW.plot_graph(x_grid,
                         Yfunc,
                            labels = ["Estimate func"], new_fig = 0, color = "k")

    return np.poly1d(plsq)
    
from scipy import interpolate

def interpolate_func(X,Y,func, p0, plotting = 0):
    
    print "-----------------"
    print X.shape, Y.shape
    
    if (func ==  "cubic"):
#        finterp = interpolate.interp1d(X.flatten(), Y.flatten())
        finterp = interpolate.UnivariateSpline(X,Y, k = 1)
#        finterp = interpolate.InterpolatedUnivariateSpline(X,Y, k = 1)
    
#        finterp.set_smoothing_factor(0.1)
#        print finterp
    if (plotting == 1):
    ### PLOT THE ESTIMATED FUNCTION WITH THE DATA
        Max_Pow = max(X)
        Min_Pow = min(X)
        Nbins = 100
        x_grid = np.linspace(Min_Pow, Max_Pow, Nbins)
    
        if (func ==  "cubic"):
    #        Yfunc = peval_cubic(x_grid,plsq[0])
            Yfunc = finterp(x_grid)
            print Yfunc
        
        lW.scatter_graph(X,Y,labels = ["Estimation of Curve", 
        "Wind Speed w0", 
        "Power Turbine 0", "Data_Points"], new_fig = 1)
        
        lW.plot_graph(x_grid,
                         Yfunc,
                            labels = ["Estimate func"], new_fig = 0)
    return finterp


