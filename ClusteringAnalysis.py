# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:01:17 2019

@author: lizhi

This module clusters nearest stations to analyse whether the station is reliable.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from SpatialCorrelation import read_data
from SpatialCorrelation import read_dis_file
from RainfallProcessing import ind_rain_events, rain_events



def cluster_num(dis_data, nearest_num):
    '''
    This function cluter some rain gauges within the distance together
    
    Args:
        dis_data: distance for one station; pandas dataframe
        nearest_num: integer #
    Return:
        Station; list
    '''
    Stations = {}
    dis = np.asarray(dis_data)
    dis = np.sort(dis)[nearest_num]
    for ind in dis_data.index:
        if (dis_data[ind]<=dis) & (dis_data[ind]>=0):
#            Stations.append(ind)
            Stations[ind] = dis_data[ind]
    return Stations

def cluster_dis(dis_data, dis):
    '''
    This function cluter some rain gauges within the distance together
    
    Args:
        dis_data: distance for one station; pandas Series
        dis: distance for threshold m #
    Return:
        Station; list
    '''
    Stations = {}
    for ind in dis_data.index:
        if (dis_data[ind]<=dis) & (dis_data[ind]>=0):
#            Stations.append(ind)
            Stations[ind] = dis_data[ind]
    return Stations

def mul_ts_plot(rain_data):
    '''
    This function makes the comparable time series plot
    '''
    fig, ax = plt.subplots(1,1, figsize=(15,5))
    
    rain_ref = rain_data.iloc[:,0]
    non_zeros=[]
    for ind in rain_data.index:
        if (rain_data.loc[ind,:]!=0).all():
            non_zeros.append(ind)
    ax.plot(np.arange(len(rain_ref[non_zeros])),rain_ref[non_zeros], color='r')
    for col in rain_data.columns[1:]:
        #type(rain_events(rain_data[col]))
        rain_other = rain_data[col][non_zeros]
        #print(rain_other)
        ax.plot(np.arange(len(rain_other)), rain_other)
    ax.set_title(rain_data.columns[0])
    ax.legend(rain_data.columns)
    return fig
    
def mul_cum_plot(rain_data):
    '''
    This function makes the comparable cumulative plots based on the 
    clustered gauges
    Args:
        rain_data: rainfall data at clustered form(return of function 
        cluster_processing); pandas dataframe 
    Return:
        fig: matplotlib used to save
    '''
    fig, ax = plt.subplots(1,1, figsize=(15,5))
    rain_ref = rain_data.iloc[:,0]
    rain_ref_cum = np.cumsum(rain_ref)
    ax.plot(np.arange(len(rain_ref_cum)),rain_ref_cum, color='r')
    for col in rain_data.columns[1:]:
        rain_other_cum = np.cumsum((rain_data[col]))
        ax.plot(np.arange(len(rain_other_cum)), rain_other_cum)
    ax.set_title(rain_data.columns[0])
    ax.legend(rain_data.columns)
    return fig

def cluster_processing(gauge, rain_all_data, dis_data, nearest_num):
    '''
    This function further prepare clustering data in order to produce graph
    Args:
        station: station name; str
        rain_all_data: rain_all_gauges; pandas dataframe
        dis_data: distance for one stations; pandas dataframe
        nearest_num: int
    Return:
        data: dataframe including clustered stations; pandas dataframe
    '''
    data = pd.DataFrame()
    data[gauge] = rain_all_data[gauge]
    Stations = cluster(dis_data[gauge], nearest_num)
    if not Stations:
        print(f"at station {gauge} distance threshold is above the closest")
    else:
        for station in Stations:
            data[station] = rain_all_data[station]
    return data

def main():
    # Change directory
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
    rain_all_gauges, missing_events = read_data()
    dis_mat = read_dis_file('Rain_gauges.xlsx', rain_all_gauges)
    # loop to execute 
    i=0
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi\\ts_clustered')
    for col in rain_all_gauges:
        rain_data = cluster_processing(col, rain_all_gauges, dis_mat, 3)
#        fig = mul_cum_plot(rain_data)
#        fig.savefig(col+'_cum.png')
        fig = mul_ts_plot(rain_data)
        fig.savefig(col+'_ts.png')
        i+=1
        print(f"{i}/{len(rain_all_gauges.columns)} completed")
        
#if __name__ == '__main__':
#    
#    main()