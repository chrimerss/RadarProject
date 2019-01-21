# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 14:26:18 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from GaugeStatistics import concatenate_period
from SpatialCorrelation import read_data
from RadarGauges_plot import read_radar

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
        data_10min[col]=data_col.groupby(pd.Grouper(freq=freq)).agg(lambda x: np.nan if pd.isnull(x).all() else x.sum())
        print(col+' is done!' )
    return data_10min

def main():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')   
    f = open('cleaned_data.pckl', 'rb')
    rain_all_gauges = pickle.load(f)
    f.close()
    radar_data = read_radar('radar_data.xlsx')
    
    aggs = ['180min']
    
    for agg in aggs:
        writer=pd.ExcelWriter(f'{agg}-gauge-radar.xlsx')
        gauge = aggregate(rain_all_gauges, agg)
        if agg!='10min':
            radar = aggregate(radar_data, agg)
        gauge=concatenate_period(gauge)
        radar = concatenate_period(radar)
        gauge = gauge.loc[radar.index,:]
        radar.to_excel(writer, sheet_name='radar')
        gauge.to_excel(writer, sheet_name='gauge')
        print(f"{agg} is done!")
    writer.close()

if __name__ == '__main__':
    main()
