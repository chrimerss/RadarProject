# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 08:41:00 2019

@author: lizhi

This module aggregates all functions used in this task
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from SpatialCorrelation import read_data
from SpatialCorrelation import read_dis_file
from EventsSelect import read_gauge_radar_data, read_gauge_radar_day, statistics_cal_station,eventselect, statistics_cal_event
from RadarGauge_statistics import func_lists, statistics, tens, daily
import plotly
import plotly.graph_objs as go
from ClusteringAnalysis import cluster_num
from multiprocessing import Pool

class RadarGauge:
    def __init__(self, chdir):
        self.chdir = chdir
        self.gauge_all = None
        self.col_names = None
        os.chdir(self.chdir)
        
    def read_gauge_all_data(self):
        gauge,_ = read_data()
        self.col_names = gauge.columns
        self.gauge_all = gauge
        return gauge
        
    def read_dis_data(self, file_name):
        dis_data = read_dis_file(file_name, self.gauge_all)
        return dis_data
        
    def read_gauge_radar_10min(self):
        gauge = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='gauge')/10.
        radar = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='radar')
        return gauge, radar
    
    def read_gauge_radar_daily(self):
        gauge, radar = read_gauge_radar_day()
        return gauge, radar
    
    def read_gauge_radar_event(self):
        gauge, radar, ind = eventselect()
        return gauge, radar, ind
    
    def statistics_10min(self, writer):
        return tens(func_lists(), writer)

    def statistics_day(self, writer):
        return daily(func_lists(), writer)
    
    def statistics_station(self, writer):
        return statistics_cal_station(writer)

    def data_agg(self, data, freq):
        data_10min = pd.DataFrame(columns=data.columns)
        for col in data.columns:
            data_col = data[col]
            data_10min[col]=data_col.groupby(pd.Grouper(freq=freq)).agg(lambda x: np.nan if np.isnan(x).all() else x.sum())
            print(col+' is done!' )
        return data_10min
    
    def delete_zeros_nans(self,x, y):
        if len(x) != len(y):
            raise ValueError("The length of x and y does not match")
        inds=[]
        for i in range(len(x)):
            if (x[i]==0 and y[i]==0) | (x[i]==np.nan and y[i]==np.nan):
                inds.append(False)
            else:
                inds.append(True)
#        print(inds)
        return x[inds], y[inds]
    
    def radar_gauge_ts_plot(self, radar, gauge):
        for col in gauge.columns:
            gauge_col, radar_col = self.delete_zeros_nans(gauge[col], radar[col])
            print(len(gauge_col), len(radar_col))
            trace1 = go.Bar(x=gauge_col.index,
                            y=gauge_col,
                            name='gauge')
            trace2 = go.Bar(x=radar_col.index,
                            y=radar_col,
                            name='radar')
            data = [trace1, trace2]
            layout = go.Layout(title=f'{col}',
                barmode='group'
            )
            fig = go.Figure(data=data, layout=layout)
            plotly.offline.plot(fig, filename = f'{col}.html', auto_open=False)
    
    def cal_all_agg_stat(self):
        aggs = np.arange(60, 1500, 60)
        aggs = np.r_[10,30,aggs]
        aggs = [str(i)+'min' for i in aggs]
#        aggs = ['30min', '60min', '120min', '180min', '240min', '300min']
        gauge_10min, radar_10min = self.read_gauge_radar_10min()
        writer = pd.ExcelWriter('agg_all_stat_new.xlsx')
        for agg in aggs:
            if agg=='10min':
                stat = statistics(gauge_10min, radar_10min, func_lists()).T
                stat.to_excel(writer, sheet_name=f'{agg}')
            else:
                gauge, radar = self.data_agg(gauge_10min, freq=agg), self.data_agg(radar_10min, freq=agg)
                stat = statistics(gauge, radar, func_lists()).T
                stat.to_excel(writer, sheet_name=f'{agg}')
                print(f'{agg} completed')
        
    def plot_all_agg(self):
        aggs = ['30min', '60min', '120min', '180min', '240min', '300min']
        gauge_10min, radar_10min = self.read_gauge_radar_10min()
        for i, agg in enumerate(aggs):
            os.mkdir(f'./{agg}')
            os.chdir(f'./{agg}')
            gauge, radar = self.data_agg(gauge_10min, freq=agg), self.data_agg(radar_10min, freq=agg)
            self.radar_gauge_ts_plot(radar, gauge)
            os.chdir('../')
            print(f'{i}/{len(aggs)}')
    
    def single_stat(self, metric):
        # This function returns the particular one metric for each station
        xl = pd.ExcelFile('agg_all_stat_new.xlsx')
        sheet_names = xl.sheet_names
        if not self.col_names.any():
            raise ValueError("you havenot initiated column names yet!")
        stat = pd.DataFrame(index=sheet_names, columns=self.col_names)
        for sheet_name in sheet_names:
            stats = xl.parse(sheet_name).T
            stat.loc[sheet_name, :] = stats.loc[metric, :]
        return stat
    
    
    def plot_aggs_stat(self):
        # This function plots the all aggregated statistics 
        # x: aggregated time;
        # y: particular metrics
        list_func = func_lists()
        dis_mat = read_dis_file('Rain_gauges.xlsx', self.gauge_all)
        for col in self.gauge_all.columns:
            for key in list_func.keys():
                df = self.single_stat(key)
                Stations = cluster_num(dis_mat[col], 5)
                df_new = df.loc[:,Stations.keys()]
                trace=[]
                for col2 in df_new.columns:
                    trace.append(go.Scatter(x=df_new.index,
                                            y=df_new[col2],
                                            name=str(col2)+'   '+str(round(Stations[col2]/1000))+'km'))
                layout = go.Layout(title=f'{col}-{key}')
                fig = go.Figure(data=trace, layout=layout)
                os.chdir('./metrics-analysis')
                plotly.offline.plot(fig, filename = f'{col}-{key}.html', auto_open=False)
                os.chdir('../')
    
    def parallel_com(self, func, args):
        pool = Pool(4)
        f = pool.apply(func,args)
        return f
    

RG = RadarGauge('D:\\Radar Projects\\lizhi\\for LiZhi')
##RG.cal_all_agg_stat() #calculate all statistics over each station output agg_all_stat_new.xlsx
_ = RG.read_gauge_all_data() # this just initialize all needed data no need to store
RG.plot_aggs_stat()  #this plot every statistic at each station