""" USE OF WIDGETS """ 
# Change main directory to the main folder and import folders
import os
os.chdir("../")
import import_folders
# Classical Libraries
import datetime as dt
import numpy as np
import copy as copy
from func import *
# Own graphical library
from graph_lib import gl
import matplotlib.pyplot as plt
# Import functions independent of DataStructure
import utilities_lib as ul
import pandas as pd
plt.close("all") # Close all previous Windows
import indicators_lib as intl

load = 0
plotting_zones = 0
spot_hired_analysis = 0

if (load):
    file1 = "Michael Schat-Holm - RainMaking output (Final).csv"
    file2 = "DFDS order data.csv"
    df = pd.read_csv("./RainMaking/" + file1, sep = ";",index_col = 0, 
                      dtype = {"TrackingTime":dt.datetime})
    df.index = ul.str_to_datetime (df.index.tolist())
    keys = df.keys()
    df = df.dropna(how='any', thresh=None, subset=keys, inplace=False)

#    df.reset_index(inplace=True)
    Nsamples, Ndim = df.shape
    
    # Now we separate the datafrate into different ones, one per Administration
    df_list = []
    orgcol = "OrganizationName"   # "OrganizationCode"
    DifferenOC = np.unique(df[orgcol])
    
    droplist = [3,9,11,13]
    for dropi in droplist:
        df = df[df[orgcol] != DifferenOC[dropi]]
    DifferenOC = np.unique(df[orgcol])
    
    for i in range(DifferenOC.size):
        OC = DifferenOC[i]
        print "Doing %i"%(i)
        subset = df.loc[df[orgcol] == OC][["Latitude(DDD.dddd)",
        "Longitude(DDD.dddd)","EquipmentOwnership","TrackingTimeOrder",
        "OperationalStatus","EquipmentItemId","LocationCity","TrackingAction", "LocationCountryName"]]
        subset.sort_index(inplace = True, ascending = True)
#        subset.reset_index(inplace=True)
        # TODO: preprocess coordinates
        ####### Compute the IDLE #####################
        subset["IDLE"] = False
        Ns,Nd = subset.shape
#        for j in range(Ns):
        idx = pd.IndexSlice
        mask1 = subset['TrackingTimeOrder'] > 0
        mask2 = subset['OperationalStatus'] == "Empty"
        mask = mask1 & mask2
        subset["IDLE"][mask] = True
#            if (subset["TrackingTimeOrder"][j] > 0):
#                if (subset["OperationalStatus"][j]  == "Empty"):
#                    subset["IDLE"][j] = True
        subset["Date"] = subset.index.date
        df_list.append(subset)
#lattitud1 = df["Latitude(DDD.dddd)"][0]
#longitud1 = df["Longitude(DDD.dddd)"][0]
#OrgC1 = df["OrganizationCode"][0] 
#df.ix[0]

#############################################################
# Plot the different Organization zones.
if plotting_zones:
    plot_flag = 1
    for iCO in range(5):
        subset = df_list[iCO]
        OC = DifferenOC[iCO]
        Ns,Nd = subset.shape
        List_of_points= []
        for i in range(Ns):
            lattitud1 = subset["Latitude(DDD.dddd)"][i]
            longitud1 = subset["Longitude(DDD.dddd)"][i]
            List_of_points.append(get_XYcoordinates(lattitud1,longitud1))
        
        List_of_points = np.array(List_of_points)
        gl.scatter(List_of_points[:,0], List_of_points[:,1], 
                   nf = plot_flag, legend = [OC], alpha = 0.8)
        plot_flag = 0
#######################################################################
#################################################################v
## "EquipmentOwnership"
## TrackingTimeOrder. If bigger than 0, it is iddle and we can use it
## It also has to be empty OperationalStatus.

#df["TrackingTimeOrder"]

if (spot_hired_analysis):

    ####### Administration sharing !! #####################
    # For a given region, we detect a Spot hired, and we see from the IDLE 
    # trails arround if we could use them.
    
#    df_list[1]["EquipmentOwnership"] == "Spot hired"
    # Copenhagen = 2
    
    region_to_optimize = df_list[2]
    spot_hired = region_to_optimize[region_to_optimize["EquipmentOwnership"] == "Spot hired"]
    different_spot_hired = np.unique(spot_hired["EquipmentItemId"])
    print spot_hired.shape, different_spot_hired.shape
    
    for soID in different_spot_hired:
        print soID, spot_hired[spot_hired["EquipmentItemId"] == soID].shape, np.sum((spot_hired[spot_hired["EquipmentItemId"] == soID])["IDLE"] == True) 
#        print spot_hired[spot_hired["EquipmentItemId"] == soID].index
    Ns,Nd = spot_hired.shape
    
    for i in range(Ns): # For each spor hired
        for j in range(1):  # Search in the other regions
            healing_region = df_list[j]
            edate = spot_hired.index[i].date()
#            print edate
            sdate = edate # - dt.timedelta(days=1)
            filtered_time = filter_pd_by_date(healing_region,sdate, edate)
            possible_IDLE = filtered_time[filtered_time["IDLE"] == True]
            Npos,Ndim= possible_IDLE.shape
            
            distances = []
            for k in range(Npos): # For every possible healing trial
                distances.append(get_distance(possible_IDLE["Latitude(DDD.dddd)"][k],
                            possible_IDLE["Longitude(DDD.dddd)"][k],spot_hired["Latitude(DDD.dddd)"][i],spot_hired["Longitude(DDD.dddd)"][i]))
            distances = np.array(sorted(distances))
            print edate, spot_hired["EquipmentItemId"][i], spot_hired["OperationalStatus"][i],  spot_hired["LocationCity"][i]
            # Many registy on the same day, different city, it is just that they move.
#            print possible_IDLE.shape
#            print distances[0:10]
IDLE_time_analysis = 0
if (IDLE_time_analysis):
    # We consider IDLE for a day, if in any of the registers of the day, it is IDLE
    Nregion = DifferenOC.size
    IDLE_prop = []
#    gl.set_subplots(Nregion/2,1)
    #### PLOT 1

    for j in range(Nregion):    #Nregion
        print "F %i"%j
        region_to_optimize = df_list[j]
        days = np.unique(region_to_optimize.index.date)
        
        N_IDLE = []
        N_trucks  = []
        
        for day in days:
            registers_day = region_to_optimize[region_to_optimize["Date"] == day]
            different_trailers = np.unique(registers_day["EquipmentItemId"])
            N_trucks.append(different_trailers.size)
            N_IDLE.append(0)
            for trailerid in different_trailers:
                if (np.mean((registers_day[registers_day["EquipmentItemId"] == trailerid])["IDLE"]) == 1):
                    N_IDLE[-1] = N_IDLE[-1] + 1
#        gl.step(days, N_IDLE, legend = ["IDLE Trailers"], alpha = 0.5, fill = 1, labels = ["Usage of Trailers","",DifferenOC[j]])
#        gl.step(days, N_trucks, legend = ["Total Trailers"], nf = 0, alpha = 0.5, fill = 1)
    #    
        propor_IDLE = np.sum(N_IDLE)/float(np.sum(N_trucks))
        IDLE_prop.append(propor_IDLE)
        
        
#    gl.subplots_adjust(left=.09, bottom=.10, right=.90, top=.95, wspace=.20, hspace=0)

#        caca = ["d","df","d","$","f"]
    gl.bar(DifferenOC.tolist(), IDLE_prop, labels = ["Proportion of IDLE Trailers","","Proportion"])   # DifferenOC.tolist()
        #TODO: Gang number 99403034 29103929
Nregion = DifferenOC.size


precompute_trailers_IDLE = 0
if (precompute_trailers_IDLE):
    total_days_onhire = 0
    total_onhire = 0
    list_IDLE = []
    Nregion = DifferenOC.size
    list_IDLE_Regions = []   # Nregions x Ndays x Trailers that are IDLE the whole day bitch
    list_days = []   # Nregions x Ndays 
    list_OSH_Regions = []
    for j in range(Nregion):    #Nregion
        print "F %i"%j
        
        list_IDLE_Regions.append([])
        list_OSH_Regions.append([])
        list_days.append([])
        region_to_optimize = df_list[j]
        days = np.unique(region_to_optimize.index.date)
        
        N_IDLE = []
        N_trucks  = []
        
        for day in days:
            registers_day = region_to_optimize[region_to_optimize["Date"] == day]
            different_trailers = np.unique(registers_day["EquipmentItemId"])
            list_IDLE_Regions[-1].append([])
            list_OSH_Regions[-1].append([])
            list_days[-1].append(day)
            for trailerid in different_trailers:
                specfic_trailer = registers_day[registers_day["EquipmentItemId"] == trailerid]
                if (np.mean(specfic_trailer["IDLE"]) == 1): # Get the iddle ones
                    list_IDLE_Regions[-1][-1].append(specfic_trailer.ix[0])
                    continue
                if (np.sum(specfic_trailer["EquipmentOwnership"] == "Spot hired")): # Get the onspot
                    list_OSH_Regions[-1][-1].append(specfic_trailer.ix[0])
                    total_days_onhire += 1
                    
reasinging_IDLE = 0
if (reasinging_IDLE):
    region_i = 0
    for day_i in range(len(list_days[region_i])): # For each day 
    
        for hired_trailer in list_OSH_Regions[region_i][day_i]: # For each trailer hired
            distances = []
            autos = []
            for regions_IDLE_i in range(len(list_IDLE_Regions)):   # For each other region
                 for IDLE_trailer in list_IDLE_Regions[regions_IDLE_i][day_i]: # For each IDLE trial that day in that region
                     distance = get_distance(IDLE_trailer["Latitude(DDD.dddd)"],
                                IDLE_trailer["Longitude(DDD.dddd)"],
                                hired_trailer["Latitude(DDD.dddd)"],
                                hired_trailer["Longitude(DDD.dddd)"])
                     distances.append(distance)
                     autos.append(IDLE_trailer["EquipmentItemId"])
                     
            distances = np.array(sorted(distances))
            autos = np.array(autos)
            print distances[0:10]
            print autos[0:10]
if (0):
    
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from datetime import datetime
    # miller projection
    map = Basemap(projection='mill',lon_0=180)
    # plot coastlines, draw label meridians and parallels.
    map.drawcoastlines()
    map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
    map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
    # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='coral',lake_color='aqua')
    # shade the night areas, with alpha transparency so the
    # map shows through. Use current time in UTC.
    date = datetime.utcnow()
    CS=map.nightshade(date)
    plt.title('Day/Night Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))
    plt.show()


cacacaca = 1
if (cacacaca):
    # For each trailer, we compute the distance Collection -> Delivery
    # And the other distances, and then We will compute how much distance is used right.
    prop_dist = []
    prop_time = []
    for ir in range(Nregion):
        print "%i"%(ir)

        region_to_optimize = df_list[ir]
        different_IDs = np.unique(region_to_optimize["EquipmentItemId"])
    #    print spot_hired.shape, different_spot_hired.shape
        
        distance_delivery = 0
        distance_bad = 0
        total_distance = 0
        time_delivery = 0
        time_bad = 0
        for soID in different_IDs:
            delivering_flag = 0
            rows_trailer = region_to_optimize[region_to_optimize["EquipmentItemId"] == soID]
            # Now we find the collection 
            Ns,Nd = rows_trailer.shape
            
#            if (rows_trailer["TrackingAction"][0] == "Collection"):
#                    delivering_flag = 1
#                    
#            for j in range(Ns -1):
#                if (rows_trailer["TrackingAction"][j+1] == "Collection"):
#                    delivering_flag = 1
#                    
#                if (rows_trailer["TrackingAction"][j+1] == "Delivery"):
#                    delivering_flag = 0
                
            if (rows_trailer["OperationalStatus"][0] == "Loaded"):
                    delivering_flag = 1
                    
            for j in range(Ns -1):
                if (rows_trailer["OperationalStatus"][j] == "Empty"):
                    delivering_flag = 1
                    
                if (rows_trailer["OperationalStatus"][j] == "Loaded"):
                    delivering_flag = 0
                
                distance = get_distance(rows_trailer["Latitude(DDD.dddd)"][j+1],
                                    rows_trailer["Longitude(DDD.dddd)"][j+1],
                                    rows_trailer["Latitude(DDD.dddd)"][j],
                                    rows_trailer["Longitude(DDD.dddd)"][j])
                timedelta = (rows_trailer.index[j+1] - rows_trailer.index[j]).total_seconds()/1e100
                if (delivering_flag):
                    distance_delivery += distance
                    if (distance > 1):
                        time_delivery += timedelta
                else:
                    distance_bad += distance
                    if (distance > 1):
                        time_bad += timedelta
                total_distance += distance
                
        proportion = distance_bad/float(distance_delivery + distance_bad)
        print proportion
        prop_dist.append(proportion)
     
        proportion = time_bad/(time_delivery + time_bad)
        print proportion
        prop_time.append(proportion)
        
    gl.bar(DifferenOC.tolist(), prop_time, labels =["Time transporting Empty Trailers ","","Proportion"], alpha = 0.8, color = "r")   # DifferenOC.tolist()
    gl.bar(DifferenOC.tolist(), prop_dist,labels =["Distance transporting Empty Trailers","","Proportion"], alpha = 0.8, color = "g")


cacacaca2 = 0
if (cacacaca2):
    # For each trailer, we compute the distance Collection -> Delivery
    # And the other distances, and then We will compute how much distance is used right.
    prop_dist = []
    prop_time = []
    colors = ["r","b"]
    for ir in range(1,2):
        print "%i"%(ir)

        region_to_optimize = df_list[ir]
        different_IDs = np.unique(region_to_optimize["EquipmentItemId"])
    #    print spot_hired.shape, different_spot_hired.shape
        
        distance_delivery = 0
        distance_bad = 0
        
        time_delivery = 0
        time_bad = 0
        for soID in different_IDs:
            delivering_flag = 0
            rows_trailer = region_to_optimize[region_to_optimize["EquipmentItemId"] == soID]
            # Now we find the collection 
            Ns,Nd = rows_trailer.shape
            
#            if (rows_trailer["TrackingAction"][0] == "Collection"):
#                    delivering_flag = 1
#            
#            prev_coordinates = get_XYcoordinates(rows_trailer["Latitude(DDD.dddd)"][0],
#                                                              rows_trailer["Longitude(DDD.dddd)"][0])
#            for j in range(Ns -1):
#                if (rows_trailer["TrackingAction"][j+1] == "Collection"):
#                    delivering_flag = 1
#                    
#                if (rows_trailer["TrackingAction"][j+1] == "Delivery"):
#                    delivering_flag = 0
#                
#                new_coordinates = get_XYcoordinates(rows_trailer["Latitude(DDD.dddd)"][j+1],
#                                                              rows_trailer["Longitude(DDD.dddd)"][j+1])

            
            prev_coordinates = get_XYcoordinates(rows_trailer["Latitude(DDD.dddd)"][0],
                                                              rows_trailer["Longitude(DDD.dddd)"][0])
            for j in range(Ns -1):
                if (rows_trailer["OperationalStatus"][j] == "Empty"):
                    delivering_flag = 1
                    
                if (rows_trailer["OperationalStatus"][j] == "Loaded"):
                    delivering_flag = 0
                
                new_coordinates = get_XYcoordinates(rows_trailer["Latitude(DDD.dddd)"][j+1],
                                                              rows_trailer["Longitude(DDD.dddd)"][j+1])
 
                color = colors[delivering_flag]
                
                x_points = [prev_coordinates[0],new_coordinates[0] ]
                y_points =  [prev_coordinates[1],new_coordinates[1] ]
                
                prev_coordinates = copy.deepcopy(new_coordinates)
                gl.plot(x_points, y_points, color =color, nf = 0)
            break
        break
    

cacacaca3 = 0
if (cacacaca3):
    # For each trailer, we compute the distance Collection -> Delivery
    # And the other distances, and then We will compute how much distance is used right.
    prop_dist = []
    prop_time = []
    colors = ["r","b"]
    Country_day = []  # Ncountry x days
    days_list = []  # Ncountry x days day
    for ir in range(1,2):
        print "%i"%(ir)

        region_to_optimize = df_list[ir]
        different_contries = np.unique(region_to_optimize["LocationCountryName"])
        days = np.unique(region_to_optimize["Date"])
        Country_day.append([])
        days_list.append([])
        for soID in different_contries:
            Country_day[-1].append([])
            days_list[-1].append([])
            rows_trailer = region_to_optimize[region_to_optimize["LocationCountryName"] == soID]
            # Now we find the collection 
            Ns,Nd = rows_trailer.shape
#            print rows_trailer.shape
            for day in days:
                Country_day[-1][-1].append(0)
                days_list[-1][-1].append(day)
#                print rows_trailer.shape
                rows_trailer2 = rows_trailer[rows_trailer["Date"] == day]
#                print rows_trailer.shape
                rows_trailer2 = rows_trailer2[rows_trailer2["TrackingAction"] == "Delivery"]
                Country_day[-1][-1][-1] += rows_trailer2.shape[0]

    for k in range(len(days_list[0])):
        week_mean = intl.get_SMA(ul.fnp(Country_day[0][k]), 7)
        gl.plot(days_list[0][k],week_mean, nf = 0, legend = [different_contries[k]])