# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 09:40:23 2019

@author: lizhi

This module aggregates 5min rain gauge data to 10min data in order to compare 
with radar data
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from SpatialCorrelation import read_data

def aggregate(data, freq):
    '''
    This function aggregates rainfall data to any frequency you want
    Args:
        data: pandas dataframe; rainfall_all_gauges
        freq: str; frequency you want to synthesize e.g.'10min'
    Return:
        the aggregated data
    '''
    data_10min = pd.DataFrame(columns=data.columns)
    for col in data.columns:
        data_col = data[col]
        data_10min[col]=data_col.groupby(pd.Grouper(freq=freq)).agg(lambda x: np.nan if np.isnan(x).all() else x.sum())
        print(col+' is done!' )
    return data_10min


def main():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
    rain_all_gauges, missing_events = read_data()
    rain_all_gauges_10min = aggregate(rain_all_gauges, '10min')
    rain_all_gauges_10min = rain_all_gauges_10min.tz_convert(None)
    rain_all_gauges_10min.to_excel('rain_gauges_10min.xlsx')    
    rain_all_gauges_30min = aggregate(rain_all_gauges_10min, '30min')
    rain_all_gauges_30min = rain_all_gauges_30min.tz_convert(None)
    rain_all_gauges_30min.to_excel('rain_gauges_30min.xlsx')
    rain_all_gauges_1h = aggregate(rain_all_gauges_10min, '60min')
    rain_all_gauges_1h = rain_all_gauges_1h.tz_convert(None)
    rain_all_gauges_1h.to_excel('rain_gauges_60min.xlsx')
    rain_all_gauges_90min = aggregate(rain_all_gauges_10min, '90min')
    rain_all_gauges_90min = rain_all_gauges_90min.tz_convert(None)
    rain_all_gauges_90min.to_excel('rain_gauges_90min.xlsx')

#    if __name__=='__main__':
#    main()