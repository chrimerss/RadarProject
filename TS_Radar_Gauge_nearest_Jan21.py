# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 08:52:46 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from MakeExcelFile import aggregate
import plotly
import plotly.graph_objs as go
from BiasAdjustment import read_events_from_web, read_dis
from ClusteringAnalysis import cluster_num

gauge_3h = pd.read_excel('180min-bias-adjusted-each.xlsx')
# aggregate to daily time series
gauge_daily = aggregate(gauge_3h, '1440min')
radar_daily = pd.read_excel("1440min-gauge-radar.xlsx", sheet_name='radar')
bad_stations = pd.read_excel('bad_gauges.xlsx')['Field1']



os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
for station in bad_stations:
    dis_data = read_dis(gauge_daily)
    dis_data_clustered = dis_data[station]
    Stations = cluster_num(dis_data_clustered,2)
    gauge = gauge_daily.loc[:, Stations.keys()]
    df_bias = pd.DataFrame(columns = Stations.keys())
    trace = []
    for col in Stations.keys():
        df_bias[col] = radar_daily[col] - gauge_daily[col]
        trace.append(go.Bar(x=df_bias.index.strftime('%Y-%m-%d'),
                            y=df_bias[col],
                            name=f'{col} {round(Stations[col])/1000} km'))
    layout = go.Layout(title=f'{station}'
            )
    os.chdir('./bias-daily-plot-clustered') 
    fig = go.Figure(data=trace, layout=layout)
    plotly.offline.plot(fig, filename = f'{station}.html', auto_open=False)
    
        
    gauge = gauge.loc[:, Stations.keys()]
    trace=go.Bar(x=df_bias.index.strftime('%Y-%m-%d'),
                    y=df_bias[col],
                    )
    os.chdir('../')
    

    
    
