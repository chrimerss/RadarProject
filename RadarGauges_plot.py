# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 08:39:06 2019

@author: lizhi

This module compares the radar data and rain gauge data based on some statistics

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from SpatialCorrelation import read_data
from RainGauge_agg_10min import aggregate
from GaugeStatistics import concatenate_period
import matplotlib.dates as mdates

def read_radar(file_name):
    data = pd.read_excel(file_name, sheet_name='10min_radar')
    data.columns = data.iloc[0,:]
    data.columns = [s.replace("'",'') for s in data.columns]
    data = data.iloc[1:,:]
    data.index = [data.index[i][1] for i in range(len(data))]
    return data

def plot_10min_ts(gauge, radar):
    '''
    This function plots every station on a 10-min based time series
    '''
    y_data = pd.DataFrame()
    gauge=gauge.loc[radar.index,:] # to make them in the same time stamp
    for i,col in enumerate(gauge.columns):
        if (gauge[col].isnull().all() ==True) | (radar[col].isnull().all() ==True):
            print("data set with all nans")
        else:
            y_data['gauge'] = gauge[col]/10.
            y_data['radar'] = radar[col]
            ind = [y_data.index[i] for i in range(len(y_data)) if (y_data.gauge[i]!=0) &(y_data.radar[i]!=0)]
            y_data = y_data.loc[ind,:]
            if (y_data.gauge.isnull().all() ==True) | (y_data.radar.isnull().all() ==True):
                print(f"Empty data in {col}")
            else:
                fig, ax = plt.subplots(1,1, figsize=(20,5))
                ax = y_data.plot.bar()
                ax.figure.set_size_inches(20,10)
                ax.set_title(col)
                ax.set_xlabel('Time series')
                ax.set_ylabel('Rainfall  (mm/10min)')
                ax.figure.savefig(f'{col}-10-min-ts.png')
                print(f"{i}/ {len(gauge.columns)} completed")
        
def plot_10min_acc(gauge, radar):
    y_data = pd.DataFrame()
    gauge=gauge.loc[radar.index,:]
    for i, col in enumerate(gauge.columns):
        if (gauge[col].isnull().all() ==True) | (radar[col].isnull().all() ==True):
            print("data set with all nans")
        else:
            y_data['gauge_acc'] = (gauge[col]/10.).cumsum()
            y_data['radar_acc'] = (radar[col]).cumsum()
            fig, ax = plt.subplots(1,1, figsize=(20,10))
            ax.plot(range(len(y_data)), y_data.gauge_acc, color='r')
            ax.plot(range(len(y_data)), y_data.radar_acc, color='b')
            ax.legend(y_data.columns)
            print(f"{i}/ {len(gauge.columns)} completed")
            ax.set_xlabel('Time series')
            ax.set_title(col)
            ax.set_ylabel('Rainfall  (mm/10min)')
            fig.savefig(f'{col}-10-min-acc.png')
    return None

def main():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')    
    radar_data = read_radar('radar_data.xlsx')
    radar_data = concatenate_period(radar_data)
    rain_all_gauges, missing_events = read_data()
    rain_all_gauges_10min = concatenate_period(aggregate(rain_all_gauges, '10min'))
    rain_all_gauges_10min.index = rain_all_gauges_10min.index.tz_localize('Asia/Ujung_Pandang')
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi\\10-min-radar-gauge-ts')
    plot_10min_ts(rain_all_gauges_10min, radar_data)
    plot_10min_acc(rain_all_gauges_10min, radar_data)
#    
#if __name__ =='__main__':
#    main()
