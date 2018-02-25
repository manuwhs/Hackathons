# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 01:31:58 2015

@author: montoya
"""

#################################################
############ HEADING FOR WORKING ################
#################################################

import scipy.io
import gc
import libratyWind as lW
import libraryEstimate as lE
import libraryThings as lT


import numpy as np 

loading = 0
if (loading == 1):
    
    Data1 = scipy.io.loadmat("./BigData_2000_2014_20161029.mat")
    Data1 = Data1["out"]
    ActPower = Data1["ActPower"][0]
    ActWind = Data1["ActWind"][0]

    Data2 = scipy.io.loadmat("./BigData_2014_2020_20161029.mat")
    Data2 = Data2["out"]
    
    Data_list = [Data1, Data2]
    Time = lW.get_Time(Data_list)
    gc.collect()
    


#Time[800] == dt.datetime(2008, 12, 31, 2, 10)

import pandas as pd
import datetime as dt
load_price = 0
if (load_price == 1):
    price_path = "./market-data-prices.csv"
    dataCSV = pd.read_csv(price_path, sep = ',') # header = None, names = None  dtype = {'phone':int}
    Nsamples, Ndim = dataCSV.shape   # Get the number of bits and attr

    dataCSV = pd.read_csv(price_path,
        sep = ',', dtype = {"Date":dt.datetime})
    

    ## Deal with dates !!
    dates_price = dt.datetime.strptime(dataCSV["Date"][0] + " " + str(dataCSV["Hour"][0]) , "%d/%m/%Y %H")
    dates_price = []
    for i in range (Nsamples):
        dates_price.append(dt.datetime.strptime(dataCSV["Date"][i] + " " + str(dataCSV["Hour"][i]-1) , "%d/%m/%Y %H"))
    
price_stuff = 1
if (price_stuff == 1):
    ## GEt the keys !!
    keys_pricesCSV = dataCSV.keys()
    #       u'Date', u'Hour', u'DK-West',
    #       u'DK-West: Price for balancing power - down regulation',
    #       u'DK-West: Price for balancing power - up regulation'],
       
    graph_labels  = ["Market Price and Production","DKK per KW", "Time"]
    graph_labels_2 = ["24-h market prices","DKK per KW", "Time", "DK-West"]
    
    main_price = dataCSV["DK-West"][-24:]
    main_time = dates_price[-24:]
    
    nn = 10000
    production = lW.get_Data(Data_list,5,"ActPower","value")[nn:(nn + 24)]

    #lW.plot_graph([],[],
    #             labels = graph_labels, new_fig = 1, color = "k")
    #             
    #lW.plot_graph(np.array(main_time),main_price, labels = ["DK-West"], 
    #              new_fig = 0, color = "k")
        
    lW.price_volume_graph(main_time,
                          main_price,
                          production,graph_labels_2)
                          
                          
load_logging = 0
if (load_logging == 1):
    
    AlarmPath = "./alarmLog.csv"
    ## It tells the correpndence index - ID
    count_ID = [1, 2, 3, 4, 5, 6, 7, 
                10, 11, 12, 13, 14, 15, 16, 
                19, 20, 21, 22, 23, 24, 25,
                28, 29, 30, 31, 32, 33, 34,
                37, 38, 39, 40, 41, 42, 43, 
                46, 47, 48, 49, 50, 51, 52,
                55, 56, 57, 58, 59, 60, 61]
                
    count_ID = np.array(count_ID)
    # Correspondence between ID and index
    ID_index = dict()
    for i in range(len(count_ID)):
        ID_index[count_ID[i]] = i
        
        
    dataCSVAlarm = pd.read_csv(AlarmPath,   
        sep = ';', dtype = {"On":dt.datetime, "Off":dt.datetime})
    
    pene_time = pd.to_datetime(dataCSVAlarm["On"],   # It is in np64 for some reason
                               format="%m/%d/%Y %H:%M:%S",utc = True)
#    dataCSVAlarm["Off"] = pd.to_datetime(dataCSVAlarm["Off"], format="%m/%d/%Y %H:%M:%S")
    
    Nsamples, Ndim = dataCSVAlarm.shape
    print dataCSVAlarm["WTG ID"][2]  # They are already date time
    print dataCSVAlarm["On"][2]
    print dataCSVAlarm["Off"][2]
    
    ### Get the index of errors for every turbine
    
    Ntur = 49
    
    log_turbines_index = [] # 49
    for i in range(Ntur):
        log_turbines_index.append([])
        
    for i in range (Nsamples):
        ID = ID_index[dataCSVAlarm["WTG ID"][i]]
        date = dataCSVAlarm["On"][i]
        penee =  pene_time[i]
##        if (type(date) == type("fuck you")):
##            print date
#        date = dt.datetime.strptime(date,"%m/%d/%Y %H:%M:%S")
#        dataCSVAlarm["On"][i] = date
        if (penee >= dt.datetime(2010,1,1) and penee <= dt.datetime(2017,1,1)):
            err = dataCSVAlarm["Description"][i]
            err_words = err.split()
            if ("stop" in err_words):
                log_turbines_index[ID].append(i)
            elif ("Stopped" in err_words):
                log_turbines_index[ID].append(i)
    
    print "Lenghts errors" 
    for i in range(Ntur):
         print len(log_turbines_index[i])
# caca = get_Data(Data_list, 0, "ActWind", "value")
    
###### UNDERSTANDING THE DATA ACCESIBILITY #########

understanding = 0
if (understanding == 1):
    NTurbines = ActPower.shape[0]
    keys = ["time","value","max","min"]
    
    for i in range (49):
        Turbine_1_Nsamples = lW.get_Data(Data_list,i,"ActPower","value").shape[0]
        Turbine_2_Nsamples = lW.get_Data(Data_list,i,"ActWind","value").shape[0]
        print Turbine_1_Nsamples, Turbine_2_Nsamples
    
    n_t = 2
#    Nsaux = 40000
    Turbine_ActPower = lW.get_Data(Data_list,n_t,"ActPower","value")
    Turbine_ActWind = lW.get_Data(Data_list,n_t,"ActWind","value")
    
#    Turbine_1_ActPower = ActPower[0][0,0]["value"][1:Nsaux]
#    Turbine_1_ActWind = ActWind[0][0,0]["value"][1:Nsaux]

    lW.scatter_graph(Turbine_ActWind,Turbine_ActPower,
                     labels = ["Power Wind Turbine " + str(n_t),
                     "Wind Speed w"+ str(n_t) + "(m/s)", "Power Turbine "+ str(n_t) + "(MW/h)",
                     "T"+ str(n_t)], new_fig = 1, color = "k")

###### PLOTTING DIFFERENT TURBINES #########

plotting_several = 0
if (plotting_several == 1):
    Ntur = 5
    
    Nsaux = 3000
    
    labels = ["Power Wind for several turbines ",
         "Wind Speed w " + "(m/s)", 
         "Power Turbine " + "(MW/h)"]
                     
    lW.scatter_graph([],[],labels = labels, new_fig = 1)
    
    colors = ["k","g","b", "y", "r"]
    
    turbines = [5, 2, 28, 25, 47 ]
    aux = 0
    Ndis = 20000
    for i in turbines:
#    for i in range(Ntur):
        
        Turbine_ActPower = lW.get_Data(Data_list,i,"ActPower","value")[Ndis*aux:(Nsaux+ Ndis*aux)]
        Turbine_ActWind = lW.get_Data(Data_list,i,"ActWind","value")[Ndis*aux:(Nsaux+ Ndis*aux)]
        Turbine_ActPower, Turbine_ActWind = lW.clean_data_PowWin(Turbine_ActPower,Turbine_ActWind)
    
        lW.scatter_graph(Turbine_ActWind,
                         Turbine_ActPower,
                         labels = ["T" + str(i)], new_fig = 0, color = colors[aux])
        aux = aux + 1

#print ActPower[1:20]

############## ESTIMATING THE FUNCTION ####################


estimating = 0


def get_std(funcInt, Pow, Win):
    Predicted_Pow = funcInt(Win)
    return np.std(Predicted_Pow- Pow)
    
if (estimating == 1):
    i = 4
    Nsaux = -1
    Noffset = 0
    TotalPow = lW.get_Data(Data_list,i,"ActPower","value")[Noffset:(Noffset + Nsaux)]
    TotalWind = lW.get_Data(Data_list,i,"ActWind","value")[Noffset:(Noffset + Nsaux)]
    
    Pow,Win = lW.ultimate_cleaning(TotalPow,TotalWind,10, 15, 5)
    Index = np.argwhere(Pow > 2300)
    Pow = np.delete(Pow,Index)
    Win = np.delete(Win,Index)
    
    p0 = []
    func = "cubic"
#    funcInt = lE.interpolate_func(Win,Pow,func, p0, plotting = 1)
    funcInt = lE.fit_function(Win,Pow,func, p0, plotting = 0)
    
    
    Nsaux = 1000
    Noffset = 500
    
    ########### Do the prediction for all datapoints #########
    
    Predicted_Pow = funcInt(Win)
    Index = np.argwhere(abs(Pow -Predicted_Pow) > 700)
    Pow = np.delete(Pow,Index)
    Predicted_Pow = np.delete(Predicted_Pow,Index)
    
    std_Pred = np.std(Predicted_Pow- Pow)
    
    legend = ["Prediction all points", "Actual Power", "Estimated Power"]
    lW.scatter_graph(Pow,
                     Predicted_Pow, 
                    labels = legend,
                    color = "k",
                    new_fig = 1)
                    
    lW.plot_graph(Pow,Pow, labels = ["Ideal"],new_fig = 0)  
    print np.std(Predicted_Pow- Pow)
    
    ###### Windowed prediction #######
    
    legend = ["Prediction all points", "Actual Power", "Estimated Power"]
    lW.plot_graph([],[], 
                    labels = legend, 
                    new_fig = 1)
    total_std = 0
    Nroe = 35
    ntu = 3
    for i in range(Nroe):
        print "$$$$$$$$$$$$"
        TotalPow = lW.get_Data(Data_list,ntu,"ActPower","value")[Noffset*i:(Noffset*i + Nsaux)]
        TotalWind = lW.get_Data(Data_list,ntu,"ActWind","value")[Noffset*i:(Noffset*i + Nsaux)]
        
        Pow,Win = lW.ultimate_cleaning(TotalPow,TotalWind,10, 15, 5)
        
        p0 = []
        func = "cubic"
    #    funcInt = lE.interpolate_func(Win,Pow,func, p0, plotting = 1)
        funcInt = lE.fit_function(Win,Pow,func, p0, plotting = 0)
        Predicted_Pow = funcInt(Win)
        std_Pred = np.std(Predicted_Pow- Pow)
            
        ########### Do the prediction for all datapoints #########
        lW.scatter_graph(Pow,
                         Predicted_Pow, 
                        labels = [], 
                        new_fig = 0)
        
        total_std = total_std + std_Pred
        
    lW.plot_graph(np.array(range(4,2500)),np.array(range(4,2500)), labels = ["Ideal"],new_fig = 0,color= "b")  
    total_std = total_std/Nroe
    print total_std
        
############# KERNEL BASED ESTIMATION  ###################
hist = 0
if (hist == 1):
    Nsaux = -1
    Data_est = ActPower[2][0,0]["value"][1:Nsaux]
    Data_est = ActWind[2][0,0]["value"][1:Nsaux]
    
    labels =  ["Probability Density Distribution", 
               "Wind Speed",
               "PDF of Wind",]
                         
    lW.get_histogram(X = Data_est, 
                     Nbins = 200, 
                     bandwidth = 0.5, 
                     labels = labels, 
                     threshold = 1)   

############# Function BASED ESTIMATION  ###################

evolution_shit = 0;
if (evolution_shit == 1):
    Nini = 0
    Ntur = 49
    WindSpeed = 8
    Ws = 10000
    Ov = 1000
    

    lW.plot_graph([],[],labels = ["Production decay ", 
                            "Time", 
                            "Power Production"], new_fig = 1)
                        
#Time = lW.get_Time(Data_list)
                        
    worst_slopes = [31,27,39, 20, 48] 
    worst_slopes = [31,27] 
    best_slopes = [2,14,19,21,25]
#    worst_slopes = [31] 
    all_slopes = []
    
    data_PT = []   # Data [Init_P, End_P, Init_T, End_T]
#    for i in range(Nini,Nini + Ntur):
    
    aux_t = 0
    for i in worst_slopes:
        
#        print i
        TotalPow = lW.get_Data(Data_list,i,"ActPower","value")
        TotalWind = lW.get_Data(Data_list,i,"ActWind","value")
        vals = lT.plot_evolution_performance(TotalPow, TotalWind,WindSpeed, Ws, Ov)
        
        ## Get the time for the graph
        Nvals = len(vals)
        Times_aux = []
        for j in range(Nvals):
            Times_aux.append(Time[Ws + j*Ov])
        Times_aux = np.array(Times_aux)
        
        ## Getting the downtrend:
        x_grid = range(len(Times_aux))
        z = np.polyfit(x_grid, vals, 1)
        p = np.poly1d(z)
        
        all_slopes.append(z[0])
        data_PT.append([p(x_grid)[0],p(x_grid)[-1],Times_aux[0],Times_aux[-1] ])
        print z[0]
        
        
        colors =["k","b"]
        decays = ["1.31%", "1.30%"]
        if (z[0] < 300):  # Only plot the ones that are positive slope
            color =colors[aux_t]   #np.random.uniform(0,1,(1,3))[0]
            lW.plot_graph(Times_aux,
                          np.array(p(x_grid)),
                          labels = ["T" + str(i) + " decay: " + decays[aux_t]], new_fig = 0, color = color)


            lW.plot_graph(Times_aux,
                          vals,
                          labels = [], new_fig = 0, color = color)

#            errors_times = dataCSVAlarm["On"][log_turbines_index[i]]
            
#            errors_times = errors_times[20:22].values
#            errors_times = errors_times.values
#            for k in range(len(errors_times)):
                
#                ts = (errors_times[k] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
#                day = dt.datetime.fromordinal(int(ts))
#                dayfrac = dt.timedelta(days=ts%1) - dt.timedelta(days = 366)
#                errors_times[k] = day + dayfrac
    
#                errors_times[k] =  dt.utcfromtimestamp(ts)
#                pene = dt.datetime(2000,1,1)
#                errors_times[k] = errors_times[k].astype(type(dt.datetime))
#                errors_times[k] = errors_times[k].date()
#                print errors_times[k]
#            errors_times = dt.datetime.utcfromtimestamp(errors_times/1e9)
            
            
            # Scatther the mistaqies !!
#            lW.scatter_graph(np.array(errors_times),
#                             np.ones((len(errors_times),1))* (700 + 10*aux_t), 
#                            labels = [], 
#                            new_fig = 0,  color = color)
            aux_t += 1
            
    all_slopes = np.array(all_slopes)
    orders = np.argmin(all_slopes)
    ## Calculate the slope in % per year
#    slopes_worst_values = all_slopes[worst_slopes]
    data_PT[0][3]- data_PT[0][2]
    powe_decay = []
    for i in range (len(data_PT)):
        percentaje_lost = 100*(data_PT[i][1] - data_PT[i][0])/data_PT[i][0]
        per_year = 365*percentaje_lost / (data_PT[0][3].date()- data_PT[0][2].date()).days
        
        powe_decay.append(per_year)
#    slopes_worst_values = 
    ## Def 
#    print all_slopes[orders[0:15]]

evolution_shit_2 = 0;
if (evolution_shit_2 == 1):
    Ntur = 20
    i = 39
    Ws = 15000

    Nbins = 100
    
    # vals = lT.plot_evolution_performance(TotalPow, TotalWind, Ws, Ov)
    TotalPow = lW.get_Data(Data_list,i,"ActPower","value")
    TotalWind = lW.get_Data(Data_list,i,"ActWind","value")
    
    ## Plot all the points
#    Treated_Pow, Treated_Wind = lW.ultimate_cleaning(TotalPow,TotalWind,10, 13, 0 )
#    lW.scatter_graph(Treated_Wind,Treated_Pow,labels = ["Evolution of Power ", 
#                            "Time", 
#                            "Power with 8 mps wind"], new_fig = 1)
##    
#    Time = lW.get_Time(Data_list)

    Ov = 365*24*6*2
#    Ov = 100000
    
    Ndes = 1800
    TotalPow = lW.get_Data(Data_list,i,"ActPower","value")[Ndes:]
    TotalWind = lW.get_Data(Data_list,i,"ActWind","value")[Ndes:]
    Time_i = lW.get_Time(Data_list,i)[Ndes:]
    vals = lT.get_params_windowed(TotalPow, TotalWind, Ws, Ov)
    
    Nsamples, Ndim = TotalPow.shape
    

    lW.plot_graph([],[],labels = ["Evolution of Power to Wind curve ", 
                            "Wind", 
                            "Power"], new_fig = 1)
    k = 0
    for vales in vals: # For every set of param
#        print vales
#        print vales[1], vales[2]
        x_grid = np.linspace(vales[1], vales[2], Nbins)
        
        Yfunc = np.poly1d(vales[0])
        powercillo = Yfunc(x_grid)
        
        ## Get the time for the graph
        Nvals = len(vals)
        Times_aux = []
        for j in range(Nvals):
            Times_aux.append(Time_i[Ws + j*Ov])
        Times_aux = np.array(Times_aux)
        
        color = [0 +0.7*(1/float(Nvals))*k]*3
        lW.plot_graph(x_grid,
                      powercillo,
                      labels = ["" + str(Times_aux[k].date())], 
                      new_fig = 0)
        
        k += 1;


