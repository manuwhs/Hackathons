import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import libratyWind as lW
import libraryEstimate as lE
import copy

def plot_evolution_performance(TotalPow, TotalWind, WindSpeed,Ws, Ov):
    
    ini_index = 0
    fin_index = Ws
    Total_samples = TotalPow.shape[0]
    
    power_gen = []
    while ((Total_samples - fin_index) > Ws):
        
        Pow = TotalPow[ini_index:fin_index]
        Win = TotalWind[ini_index:fin_index]

        th_power = 2300 # Whatever
        Pow,Win = lW.ultimate_cleaning(Pow,Win,10, 13, th_power)

        p0 = []
        values = lE.fit_function(Win,Pow,"cubic", p0, 0)
        Yfunc = np.poly1d(values)
        powercillo = Yfunc(WindSpeed)
        power_gen.append(powercillo)
        
        ini_index = ini_index + Ov
        fin_index = fin_index + Ov

    return power_gen


def get_params_windowed(TotalPow, TotalWind,Ws, Ov):
    
    ini_index = 0
    fin_index = Ws
    Total_samples = TotalPow.shape[0]
    
    power_gen = []
    while ((Total_samples - fin_index) > Ws):
        
        Pow = TotalPow[ini_index:fin_index]
        Win = TotalWind[ini_index:fin_index]

        th_power = 2300 # Whatever
        Pow,Win = lW.ultimate_cleaning(Pow,Win,10, 13, th_power)

        p0 = []
        values = lE.fit_function(Win,Pow,"cubic", p0, 0)

        Max_Win = max(Win)
        Min_Win = min(Win)

        power_gen.append([values,Min_Win,Max_Win])
        
        ini_index = ini_index + Ov
        fin_index = fin_index + Ov

    return power_gen