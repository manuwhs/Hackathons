# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 11:46:18 2017

@author: montoya
"""
import numpy as np
import import_folders
from graph_lib import gl

Yinf = 0.02
Nyears = 10

month_inf = np.power(1 + Yinf, 1/12.0) - 1


Return_years = []
Return_months = []

Return_years.append(1)
Return_months.append(1)


for i in range(Nyears):
    Return_years.append(Return_years[-1]*(1+Yinf))

for i in range(Nyears*12):
    Return_months.append(Return_months[-1]*(1+month_inf))
    
gl.plot(range(Nyears + 1),Return_years)
gl.plot(np.array(range(Nyears*12 + 1))/12.0,Return_months, nf = 0)

