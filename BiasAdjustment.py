# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 08:45:24 2019

@author: lizhi

This module works as bias adjustment to drop those periods that there is rainfall
in its nearest station (2km) during heavy events based on daily time scale

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from AggregateAllScripts import RadarGauge
from SpatialCorrelation import read_dis_file
from ClusteringAnalysis import cluster_dis

def read_events_from_web():
    event = pd.read_excel('Events.xlsx')
    event.set_index('event count', inplace=True)
    start = [s.replace('"','') for s in event.start]
    end = [s.replace('"','') for s in event.end]
    start = pd.to_datetime(start, format='%d/%m/%Y %H:%M')
    end = pd.to_datetime(end, format='%d/%m/%Y %H:%M')
    event.start = start
    event.end = end
    return event

def select_ind(data, event):
    ind=[]
    for time in data.index:
        if (time>=event.start) & (time<=event.end):
            ind.append(time)
    return data.loc[ind, :]

def read_dis(gauge):
    return read_dis_file('Rain_gauges.xlsx', gauge)

def cluster(dis_data, dis):
    return cluster_dis(dis_data, dis)

def justify(cluster, data, threshold_rain, threshold_to_replace):
    # threshold_rain takes the threshold to determine a heavy rainfall events
    # threshold_to_replace is the value under which to be replaced
    data = data.loc[:, cluster.keys()]
    for time in data.index:
        if (data.loc[time,:]>threshold_rain).any():
            col = data.loc[time,:]<threshold_to_replace
            data.loc[time, col] = data.loc[time, col].mask(data.loc[time, col]<threshold_to_replace)
    return data

def event_process(gauge, dis, threshold_rain, threshold_to_replace):
    events = read_events_from_web()
    for i in range(len(events)):
        event = events.iloc[i,:]
        gauge_event = select_ind(gauge, event)
        dis_mat = read_dis(gauge)
        for col in gauge.columns:
            stations = cluster_dis(dis_mat[col], dis)
#            if not stations:
#                dis += 1000
#                stations = cluster_dis(dis_mat[col], dis)
            gauge_near = gauge_event.loc[:, stations.keys()]
            gauge_near = justify(stations, gauge_near, threshold_rain, threshold_to_replace)
            gauge_event.loc[gauge_near.index, gauge_near.columns] = gauge_near
            gauge.loc[gauge_near.index, gauge_near.columns] = gauge_near
        print(f'event {i+1}  done!')
    return gauge

def each_process(gauge, radar, dis, threshold_rain, threshold_to_replace):
    for i in range(len(gauge)):
        dis_mat = read_dis(gauge)
        gauge_event = gauge.iloc[i,:]
        for col in gauge.columns:
            stations = cluster_dis(dis_mat[col], dis)
#            if not stations:
#                dis += 1000
#                stations = cluster_dis(dis_mat[col], dis)
            gauge_near = gauge_event[stations.keys()]
            if ((gauge_near>threshold_rain).any()) & (radar[col][i]>threshold_to_replace):
                gauge_near = gauge_near.mask(gauge_near<threshold_to_replace)
                gauge_event[gauge_near.index] = gauge_near
                gauge.iloc[i, :][stations.keys()] = gauge_near
        print(f'event {i+1}/{len(gauge)}  done!')
    return gauge

def main():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
    gauge = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='gauge')/10.
    radar = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='radar')
#    gauge = event_process(gauge, 3000, 3, 0.1)
    gauge = each_process(gauge, radar, 3000, 5, 0.5)
    gauge.to_excel('10min-bias-adjusted-each.xlsx')
    

if __name__ == '__main__':
    main()