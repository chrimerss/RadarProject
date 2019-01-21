# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 16:49:47 2019

@author: lizhi
"""

import rasterio
import numpy as np
import os


band = np.zeros((1000,1000,9))
os.chdir(r"D:\Radar Projects\Scripts\RadarImageExtract\2018 01 01 - 5 min rainfall\PhiDp_Changi")
with rasterio.open("dP0056_20180907090200.tif") as rst:
    print(rst.width, rst.height)
    print(rst.crs)
    print(rst.count)
    print(type(rst))
    band = rst.read()
    
band_trans = band.transpose(1,2,0)
print(type(band_trans))