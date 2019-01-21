# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:21:44 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from multiprocessing import Pool

os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
cleaned_3h = pd.read_excel('180min-bias-adjusted-each.xlsx', sheet_name='gauge_cleaned')
original_1h = pd.read_excel('60min-gauge-radar.xlsx', sheet_name='gauge')/10.
radar_1h = pd.read_excel('60min-gauge-radar.xlsx', sheet_name='radar')
original_30min = pd.read_excel('30min-gauge-radar.xlsx', sheet_name='gauge')/10.
radar_30min = pd.read_excel('30min-gauge-radar.xlsx', sheet_name='radar')
original_10min = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='gauge')/10.
radar_10min = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='radar')
list_to_replace = [original_1h, original_30min, original_10min]
list_to_justify = [radar_1h, radar_30min, radar_10min]
for m, data in enumerate(list_to_replace):
    radar = list_to_justify[m]
    for col in data.columns:
        for i in range(len(cleaned_3h)):
            if cleaned_3h[col].isna()[i]:
                subdata = data[col][(data.index>cleaned_3h.index.shift(-3,freq='h')[i]) &
                               (data.index<=cleaned_3h.index[i])]
#                for j in range(len(subdata)):
#                    if radar[col][subdata.index][j]>0:
##                        print(data[col][subdata.index][j], radar[col][subdata.index][j])
#                        data[col][subdata.index[j]] = np.nan
                data[col][subdata.index] = np.nan
    print(f'{data} is done!')
    
def replace(data):
    for col in data.columns:
        for i in range(len(cleaned_3h)):
            if cleaned_3h[col].isna()[i]:
                subdata = data[col][(data.index>cleaned_3h.index.shift(-3,freq='h')[i]) &
                               (data.index<=cleaned_3h.index[i])]
                data[col][subdata.index] = np.nan
    print(f'{data} is done!')
    return data
name=['1h','30min', '10min']
writer = pd.ExcelWriter('marked-data-old.xlsx')
for i, data in enumerate(list_to_replace):
    data.to_excel(writer, sheet_name=name[i])
cleaned_3h.to_excel(writer, sheet_name='3h')
writer.close()