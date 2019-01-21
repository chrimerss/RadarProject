# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:05:35 2019

@author: lizhi

This module selects the particular event based on the radar website
returns the statistics of radar data and gauge data.

Main issue: the time zone for the radar data and gauge data and event data/solved

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from RadarGauge_statistics import statistics, func_lists

def read_gauge_radar_data():
    # This function returns 10-min both gauge and radar data in the excel file
    gauge = pd.read_excel('Radar_Gauge_all_10andDaily.xlsx','Gauges10min')
    radar = pd.read_excel('Radar_Gauge_all_10andDaily.xlsx', 'Radar10min')
    return gauge, radar

def read_gauge_radar_day():
    gauge = pd.read_excel('Radar_Gauge_all_10andDaily.xlsx','GaugeDaily')
    radar = pd.read_excel('Radar_Gauge_all_10andDaily.xlsx', 'RadarDaily')
    return gauge, radar

def read_event_meta():
    events = pd.read_excel('Events.xlsx')
    events['start'] = [s.replace('"','') for s in events['start']]
    events['end'] = [s.replace('"','') for s in events['end']]
    for i in range(len(events)):
        if isinstance(events['start'][i],str):
            events['start'][i] = pd.to_datetime(events['start'][i], format='%d/%m/%Y %H:%M').tz_localize('Asia/Ujung_Pandang')
            events['end'][i] = pd.to_datetime(events['end'][i], format='%d/%m/%Y %H:%M').tz_localize('Asia/Ujung_Pandang')

    return events

def eventselect():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
    gauge, radar = read_gauge_radar_data()
    gauge.index = gauge.index.tz_localize('Asia/Ujung_Pandang')
    radar.index = radar.index.tz_localize('UTC').tz_convert('Asia/Ujung_Pandang')
    events = read_event_meta()
    start, end = events['start'], events['end']
    ind = [(gauge.index>start[i])&(gauge.index<end[i]) for i in range(len(events))]
    return gauge, radar, ind

def statistics_cal_station(writer):
    '''
    for station based statistics, concatenate all events together to calculate one value
    '''
    func_list = func_lists()
    gauge, radar, inds = eventselect()
    gauge_station = pd.DataFrame()
    radar_station = pd.DataFrame()
    for i, ind in enumerate(inds):
        _gauge_station = gauge[ind]
        _radar_station = radar[ind]
        gauge_station = gauge_station.append(_gauge_station, ignore_index=True)
        radar_station = radar_station.append(_radar_station, ignore_index=True)
    stat_station = statistics(gauge_station, radar_station, func_list)
    stat_station.to_excel(writer, sheet_name='station')
    return stat_station

def statistics_cal_event(writer):
    '''
    for event based statistics, concatenate all stations in one event
    '''
    func_list = func_lists()
    gauge, radar, inds = eventselect()
    col_names = [f'event{i+1}' for i in range(len(inds))]
    stats = pd.DataFrame(columns= col_names,index=func_list.keys())
    col = gauge.columns
    radar = radar.loc[:,col]
    for i, ind in enumerate(inds):
        _gauge_event = gauge[ind]
        _radar_event = radar[ind]
        for key, func in func_list.items():
            stats[f'event{i+1}'][key] = func(_gauge_event.agg('sum',axis=1), _radar_event.agg('sum', axis=1))
    stats.to_excel(writer, sheet_name='event')
    return stats

def main():
    writer = pd.ExcelWriter("Station_Event_based_stat.xlsx")
    sts = statistics_cal_station(writer)
    sts = statistics_cal_event(writer)
if __name__ =='__main__':
    main()

