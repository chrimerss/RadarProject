# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:10:37 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from BiasAdjustment import read_events_from_web, read_dis
from ClusteringAnalysis import cluster_num
from AggregateAllScripts import RadarGauge
import plotly
import plotly.graph_objs as go

def data_clean(gauge, radar, station):
    '''
    gauge: gauge data for certain time resolution
    radar: radar data for certain time resolution, these two should be consistent
    station: str e.g. 'S100'
    '''
    dis_data = read_dis(gauge)
    dis_data_clustered = dis_data[station]
    Stations = cluster_num(dis_data_clustered,2)
    gauge = gauge.loc[:, Stations.keys()]
    bls=[]
    for ind in range(len(gauge)):
        if gauge.iloc[ind,:].sum()==0 and radar[station][ind]==0:
            bls.append(False)
        else:
            bls.append(True)
    
    gauge = gauge[bls]
    radar = radar[bls]
    return gauge, radar, Stations

def plot(gauge, radar, events, station, Stations):
    gauge_event_based = pd.DataFrame()
    radar_event_based = pd.DataFrame()
    for ind in range(len(events)):
        _gauge = gauge[(gauge.index>events.start.values[ind]) & (gauge.index<events.end.values[ind])]
        _radar = radar[(radar.index>events.start.values[ind]) & (radar.index<events.end.values[ind])]
        gauge_event_based = pd.concat([gauge_event_based, _gauge])
        radar_event_based = pd.concat([radar_event_based, _radar])
#    gauge = gauge[(gauge.index>event.start) & (gauge.index<event.end)]
#    radar = radar[(radar.index>event.start) & (radar.index<event.end)]
    
#    print(gauge_event_based.index)
    trace=[]
    for col in gauge.columns:
        trace.append(go.Bar(x=np.arange(len(gauge_event_based)),
                        y=gauge_event_based[col],
                        name=f'gauge {col}-{round((Stations[col])/1000)} km'))
    trace.append(go.Bar(x=np.arange(len(gauge_event_based)),
                    y = radar_event_based[station],
                    name='radar'))
    
    layout = go.Layout(title=f'{station}',
                barmode='group',
                xaxis=dict(tickmode='array',
#                           type='date',
                           tickvals=np.arange(len(gauge_event_based)),
                           ticktext=np.array(gauge_event_based.index.strftime('%m-%d %H h')))
            )
    fig = go.Figure(data=trace, layout=layout)
    os.chdir('./ts-plot-event-new')
    plotly.offline.plot(fig, filename = f'{station}-event.html', auto_open=False)
    os.chdir('../')

def main():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
    gauge = pd.read_excel('60min-bias-adjusted.xlsx')
    radar = pd.read_excel('60min-gauge-radar.xlsx', sheet_name='radar')
    bad_stations = pd.read_excel('bad_gauges.xlsx')['Field1']
#RG = RadarGauge('D:\\Radar Projects\\lizhi\\for LiZhi')
#gauge, radar = RG.read_gauge_radar_10min()
    events = read_events_from_web()
    for station in bad_stations:
        gauge_event, radar_event, Stations = data_clean(gauge, radar, station)
        plot(gauge_event,radar_event, events, station, Stations)
        
if __name__ =='__main__':
    main()


#event=events.iloc[1,:]

#gauge = gauge[(gauge.index>event.start) & (gauge.index<event.end)]
#radar = radar[(radar.index>event.start) & (radar.index<event.end)]

