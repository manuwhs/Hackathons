import numpy as np
from math import sin, cos, sqrt, atan2, radians

def get_XYcoordinates(latti,longi):
    lon1 = 0
    lat1 = 0
    if (type(latti) == type("f")):
        latti = float(latti.replace(",","."))
    if (type(longi) == type("f")):
        longi = float(longi.replace(",","."))

    dx = (longi-lon1)*40000*np.cos((lat1+latti)*np.pi/360)/360
    dy = (lat1-latti)*40000/360
    return [dx,dy]

def filter_pd_by_date(df,sdate, edate):
    dates = df.index.date
    time_mask = (dates >= sdate) & (dates <= edate)
    # This one is a list of indexes that we want to use
    # Based on "iloc" in pandas
    time_mask = np.argwhere(time_mask).T[0]
    # Lets 
    new = df.ix[time_mask]
    return new

def get_distance(lat1,lon1,lat2,lon2):
    if (type(lat1) == type("f")):
        lat1 = float(lat1.replace(",","."))
    if (type(lon1) == type("f")):
        lon1 = float(lon1.replace(",","."))
        
    if (type(lat2) == type("f")):
        lat2 = float(lat2.replace(",","."))
    if (type(lon2) == type("f")):
        lon2 = float(lon2.replace(",","."))
    # approximate radius of earth in km
    R = 6373.0
#    print [lat1, lon1,lat2,lon2]
    
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * atan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    return distance
    
    # Example of selecting a range of dates
#    sdate_str = "01-02-2017"
#    edate_str = "05-02-2017"
#    sdate = dt.datetime.strptime(sdate_str, "%d-%m-%Y").date()
#    edate = dt.datetime.strptime(edate_str, "%d-%m-%Y").date()
#    
    # Lets 
#    new = filter_pd_by_date(df_list[0],sdate, edate) 