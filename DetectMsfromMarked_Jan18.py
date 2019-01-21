# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 13:11:07 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from AggregateAllScripts import RadarGauge

def count_miss(data):
    miss = {}
    for col in data:
        ind = data[col].isna()
        new = data[col][ind]
        miss.update({col:len(new)})
        
    return pd.DataFrame(miss, index=[0])

#RG = RadarGauge()
#gauge, radar = RG.read_gauge_radar_10min()

#gauge = pd.read_excel('180min-gauge-radar.xlsx', sheet_name='gauge')/10.
#radar = pd.read_excel('180min-gauge-radar.xlsx', sheet_name='radar')
#
#cleaned = pd.read_excel('180min-bias-adjusted-each.xlsx')
#missing_values=count_miss(gauge)
#cleaned_miss = count_miss(cleaned)
#
#missing_values = pd.concat([missing_values, cleaned_miss])

#writer = pd.ExcelWriter('180min-bias-adjusted-each.xlsx')
#gauge.to_excel(writer, sheet_name='original_gauge')
#cleaned.to_excel(writer, sheet_name='gauge_cleaned')
#radar.to_excel(writer, sheet_name='radar')
#description = cleaned.describe()
#description.to_excel(writer, sheet_name = 'gauge statistics')
#missing_values.to_excel(writer, sheet_name='1')
os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
original_1h = pd.read_excel('60min-gauge-radar.xlsx', sheet_name='gauge')
original_30min = pd.read_excel('30min-gauge-radar.xlsx', sheet_name='gauge')
original_10min = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='gauge')
original_180min = pd.read_excel('180min-gauge-radar.xlsx', sheet_name='gauge')
lists_ori = [original_1h, original_30min, original_10min, original_180min]

xl = pd.ExcelFile('marked-data-old.xlsx')
sheet_names = xl.sheet_names
writer = pd.ExcelWriter('MissingValues-marked-old.xlsx')
for i, sheet_name in enumerate(sheet_names):
    new = xl.parse(sheet_name)
    old = lists_ori[i]
    new_miss = count_miss(new)
    old_miss = count_miss(old)
    data = pd.concat([old_miss, new_miss])
    data.to_excel(writer, sheet_name = sheet_name)
writer.close()