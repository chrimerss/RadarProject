# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:18:53 2019

@author: lizhi

This module ultilizes object AggregateAllScripts to do everything!
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from AggregateAllScripts import RadarGauge
from RadarGauge_statistics import func_lists, statistics

#try with 1 hour data


os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
#RG = RadarGauge('D:\\Radar Projects\\lizhi\\for LiZhi')
#RG.cal_all_agg_stat() #calculate all statistics over each station output agg_all_stat_new.xlsx
#_ = RG.read_gauge_all_data() # this just initialize all needed data no need to store
#RG.plot_aggs_stat()  #this plot every statistic at each station
#adjusted_rain = pd.read_excel('10min-bias-adjusted.xlsx')
radar_1h = pd.read_excel('60min-gauge-radar.xlsx', sheet_name='radar')
radar_30min = pd.read_excel('30min-gauge-radar.xlsx', sheet_name='radar')
radar_10min = pd.read_excel('10min-gauge-radar.xlsx', sheet_name='radar')
radar_180min = pd.read_excel('180min-gauge-radar.xlsx', sheet_name='radar')
radars = [radar_1h, radar_30min, radar_10min, radar_180min]
xl = pd.ExcelFile('marked-data-old.xlsx')
sheet_names = xl.sheet_names
writer = pd.ExcelWriter('Statistics-marked-old.xlsx')
for i, sheet_name in enumerate(sheet_names):
    gauge = xl.parse(sheet_name)
    stat = statistics(gauge, radars[i], func_lists())
    stat.to_excel(writer, sheet_name=sheet_name)
writer.close()

gauge_10min = pd.read_excel('10min-bias-adjusted-each.xlsx')
func_lists = func_lists()
stats = statistics(gauge_10min[gauge_10min.index>'2018-11-14'], radar_10min[radar_10min.index>'2018-11-14'], func_lists )
func_lists['pearson'](gauge_10min['S100'][gauge_10min.index>'2018-11-14'], radar_10min['S100'][radar_10min.index>'2018-11-14'])