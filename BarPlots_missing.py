# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:34:03 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os

os.chdir("D:\\Radar Projects\\lizhi\\for LiZhi")
f = open('cleaned_data.pckl', 'rb')
rain_all_gauges = pickle.load(f)
f.close()
f = open('missing_rainevents.pckl','rb')
missing_events = pickle.load(f)
f.close()

def Barplot(rain_data, missing_data):
    '''
    This function plots the missing data in a bar plot
    '''
    
    missing_all = pd.DataFrame(columns=rain_data.columns)
    missing_values = rain_data.isna().sum()
    missing_all = missing_all.append(missing_values, ignore_index=True)
    for col in rain_data.columns:
        if missing_all[col].values==0:
            missing_all.drop(col, axis=1, inplace=True)
            missing_data.drop(col, axis=1, inplace=True)
            print(len(missing_all.columns))
    fig, ax = plt.subplots(2,1,figsize=(25,13))
    ax[0].bar(rain_data.columns[:41],missing_all.iloc[0,:41])
    ax[0].bar(rain_data.columns[:41],missing_data.iloc[0,:41])
    ax[0].set_title('The missing values counts')
    ax[0].set_xlabel('Stations')
    ax[0].set_ylabel('# missing counts')
    ax[0].legend(('missing values in total', 'missing values in rain events'))
    ax[1].bar(rain_data.columns[41:],missing_all.iloc[0,41:])
    ax[1].bar(rain_data.columns[41:],missing_data.iloc[0,41:])    
    ax[1].set_title('The missing values counts')
    ax[1].set_xlabel('Stations')
    ax[1].set_ylabel('# missing counts')
    ax[1].legend(('missing values in total', 'missing values in rain events'))
    
    return missing_all

a = Barplot(rain_all_gauges, missing_events)