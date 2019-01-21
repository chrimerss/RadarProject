# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 12:03:09 2019

@author: lizhi

This module calculates the statistics of radar and gauge data based on 10min
and daily rainfall. It also saves the excel file of both completed cleaned data
format for further uses.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from SpatialCorrelation import read_data
from RainGauge_agg_10min import aggregate
from GaugeStatistics import concatenate_period
from RadarGauges_plot import read_radar
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import scipy

def MAE(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred)

def pearson_r(y_true, y_pred):
    return scipy.stats.pearsonr(y_true, y_pred)[0]

def RMSE(y_true, y_pred):
    return mean_squared_error(y_true, y_pred)**.5

def TVR(y_true, y_pred):
    val = [y_true[i]/y_pred[i] for i in range(len(y_true)) if y_pred[i]!=0]
    return np.average(val)

def count_both(radar, gauge):
    count=0
    for i in range(len(radar)):
        if (radar[i]==0 and gauge[i]==0) | (radar[i]!=0 and gauge[i]!=0):
            count+=1
    return count

def count_or(radar, gauge):
    count=0
    for i in range(len(radar)):
        if (radar[i]==0 and gauge[i]!=0) | (radar[i]!=0 and gauge[i]==0):
            count+=1
    return count

def statistics(gauge, radar, func_lists):
    stat = pd.DataFrame(columns=gauge.columns, index=func_lists.keys())
    for i, col in enumerate(gauge.columns):
        for key, func in func_lists.items():
            if (gauge[col].isnull().all() ==True) | (radar[col].isnull().all() ==True):
                print(f"Empty data in {col}")
            else:
                common = (gauge[col].isna()) | (radar[col].isna())
#                print(common)
                x = gauge[col][~common]
                y = radar[col][~common]
                stat[col][key] = func(x, y)
        
        print(f'{i}/{len(gauge.columns)} completed!')
    return stat

def tens(func_lists, writer):
    '''
    this function deals with 10-min aggregation data
    '''
    radar_data = read_radar('radar_data.xlsx')
    radar_data = concatenate_period(radar_data)
    rain_all_gauges, missing_events = read_data()
    rain_all_gauges_10min = concatenate_period(aggregate(rain_all_gauges, '10min'))/10.
    rain_all_gauges_10min = rain_all_gauges_10min.loc[radar_data.index,:]
    data = statistics(rain_all_gauges_10min, radar_data, func_lists)
    radar_data.index = radar_data.index.tz_localize(None)
    rain_all_gauges_10min.index = rain_all_gauges_10min.index.tz_localize(None)
    rain_all_gauges_10min.to_excel(writer, sheet_name='Gauges10min')
    radar_data.to_excel(writer, sheet_name='Radar10min')
    return data

def daily(func_lists, writer):
    '''
    this function deals with daily aggregated data
    This one needs reparation
    '''
    radar_data = pd.read_excel('radar_data.xlsx', sheet_name='daily_radar', skip_rows=1)
    radar_data.columns = radar_data.iloc[0,:]
    radar_data.columns = [s.replace("'",'') for s in radar_data.columns]
    radar_data = radar_data.iloc[1:,:]
    radar_data = concatenate_period(radar_data)
    
    gauge_data = pd.read_excel('Daily_Monthly_Gauges_new.xlsx', sheet_name='daily')/10.
    gauge_data = gauge_data.loc[radar_data.index,:]
    data = statistics(gauge_data, radar_data, func_lists)
    radar_data.index = radar_data.index.tz_localize(None)
    gauge_data.index = gauge_data.index.tz_localize(None) #to convert to None because excel connot deal with time zone
    radar_data.to_excel(writer, sheet_name='RadarDaily')
    gauge_data.to_excel(writer, sheet_name='GaugeDaily')
    return data

def func_lists():
    func_lists = {'MAE': MAE,
                  'pearson': pearson_r,
                  'RMSE': RMSE,
                  'TVR': TVR,
                  'pos_cor': count_both,
                  'neg_cor': count_or}
    return func_lists

def main():
    func_lists = {'MAE': MAE,
                  'pearson': pearson_r,
                  'RMSE': RMSE,
                  'TVR': TVR,
                  'pos_cor': count_both,
                  'neg_cor': count_or}
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')    
    writer_data = pd.ExcelWriter("Radar_Gauge_all_10andDaily.xlsx")
    data = tens(func_lists, writer_data)
    writer = pd.ExcelWriter('RadarGaugeStatistics.xlsx')
    data.to_excel(writer, sheet_name='10min')
    data = daily(func_lists, writer_data)
    data.to_excel(writer, sheet_name='daily')
    
#if __name__ == '__main__':
#    data = main()