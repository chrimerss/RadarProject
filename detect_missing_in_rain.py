# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 09:59:41 2019

@author: lizhi

This module calculates the portion of missing data in a rainfall event.
"""

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def read_dis_file(file_name, rain_data):
    data = pd.read_excel(file_name, sheet_name='Sheet1')
    data = data.iloc[3:, 1:]
    data.columns = [s.replace("'", '') for s in data.columns]
    data['column_name'] = data.columns
    data.set_index('column_name', inplace=True)
    data = data[rain_data.columns]
    data = data.loc[data.columns,:]
    return data

def detect_rain_events(rain_data, dis_data, nearest_dis):
    '''
    This function takes dataframe to produce the station and number
    of missing values during rainfall events
    Args:
        rain_data: rain_all_gauges; pandas dataframe
        dis_data: distance_mat; pandas dataframe
        nearest_dis: the threshold distance between two stations; int
    return:
        dic: dictionary, further convert to pandas dataframe
    '''
    dic={}
    for ind, col in enumerate(dis_data.columns):
        if nearest_dis>dis_data[col].values.any()>0:
            stations = dis_data[col][(dis_data[col]>0) & 
                               (nearest_dis>dis_data[col])].index
            #print(stations)
        if not stations.any():
            print(f"No nearest stations at {col}")
        else:
            for station in stations:
                missing_events = rain_data[rain_data[col].isna()==True].index
                max_num = 0
                missing_counts_rain=0
                for event in missing_events:
                    if rain_data[station][event]>0:
                        missing_counts_rain+=1
                if missing_counts_rain>max_num:
                    max_num = missing_counts_rain
        dic.update({col: max_num})
        print("The # of missing values",max_num)
    return dic

def main():
    os.chdir("D:\\Radar Projects\\lizhi\\for LiZhi")
    f = open('cleaned_data.pckl','rb') #read cleaned rainfall data
    rain_all_gauges = pickle.load(f)
    f.close()
    distance_mat = read_dis_file('Rain_gauges.xlsx', rain_data=rain_all_gauges)
    missing = detect_rain_events(rain_all_gauges, distance_mat, 5000)
    missing = pd.DataFrame(missing, index=[0])
    f = open('missing_rainevents.pckl', 'wb')
    pickle.dump(missing, f)
    f.close()


if __name__=='__main__':
    main()