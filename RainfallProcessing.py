# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 14:21:32 2019

@author: lizhi
"""

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing as mp
import pickle
import matplotlib.dates as mdates

def ind_rain_events(data_col):
    '''
    This function returns the index of rainfall event
    '''
    start_lists=[]
    end_lists = []
    for ind in range(len(data_col.values)-1):
        if ((data_col.values[ind])==0 and (data_col.values[ind+1])!=0) & (data_col.values[ind]!= np.nan and data_col.values[ind+1]!= np.nan):
            start_lists.append(ind)
            #print(index_lists)
    for ind in range(len(data_col.values)-1):
        if (data_col.values[ind]!=0 and data_col.values[ind+1]==0)& (data_col.values[ind]!= np.nan and data_col.values[ind+1]!= np.nan):
            end_lists.append(ind)    
    #for i in range(len(index_lists)-1):
        #end= [j  for j in range(index_lists[i], index_lists[i+1]) if data_col.values[j]==0]
        #new_data[col] = new_data[col].append(data[col][index_lists[i]-10: index_lists[i+1]],ignore_index=True)
#    for i in range(len(start_lists)-1):
#        if start_lists[i+1]-end_lists[i]>10:
#            start_lists[i+1] = start_lists[i+1]-10
#        elif start_lists[i+1]-end_lists[i]>5:
#            start_lists[i+1] = start_lists[i+1]-5
#        elif start_lists[i+1]-end_lists[i]>5:
#            start_lists[i+1] = start_lists[i+1]-1
    if len(start_lists)>len(end_lists):
        start_lists = start_lists[:-1]
    elif len(start_lists)<len(end_lists):
        end_lists = end_lists[:-1]
    events = [np.arange(start_lists[i], end_lists[i]) for i in range(len(start_lists))]
    return events

def rain_events(rain_data_col):
    if len(ind_rain_events(rain_data_col))!=0:
        events = np.concatenate(ind_rain_events(rain_data_col))
        rain_data_col = rain_data_col[events]
    return rain_data_col

def ts_plot(data):
    '''
    This function takes the pandas data frame as input, output the time series plot of each rain gauge
    '''
    # change the directory
    os.chdir('./TimeSeriesPlots')
    i=0
    for col in data.columns:
        event_data = rain_events(data[col])
        event_data.dropna(axis=0,inplace=True)
        i+=1
        if event_data.isnull().all() ==True:
            print("data set with all nans")
        else:
            fig, ax = plt.subplots(1,1,figsize=(15,5))
            ax.bar(event_data.index, event_data.values, width=0.2)
            ax.set_title(f"{col}")
            ax.set_xlabel("Time Series")
            ax.set_ylabel("Rainfall  (mm/5min)")
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.savefig(col+'.png')
            plt.close(fig)
            print(f"{i}/{len(data.columns)} processing")

def data_cleaning(data):
    '''
    This function takes raw rainfall data and return cleaned data
    '''
    data = data.iloc[1:289,:] # get rid of the first empty row and last sum line
    data.replace('-', np.nan, inplace=True) # replace missing values with nan
    data.set_index(data.iloc[:,0], inplace=True)
    data=data.iloc[:,1:]
    return data

def detect_missing(data_col):
    '''
    This function detects the missing values in the data frame; parallely process
    arg: rain_gauge
    '''
    count = data_col.isna().sum()
    percentage = count/len(data_col)*100
    return count, percentage

def miss_bar_plot(data, name):
    '''
    This function takes the missing data frame to produce the barplot of missing values
    Args: data, pandas dataframe
          name, either 'missing counts' or 'missing percentage'
    '''
    if name == 'missing counts':
        fig, ax = plt.subplots(2,1,figsize=(25,13))
        ax[0].bar(data.index[:41],data['missing counts'].values[:41])
        ax[0].set_title('The missing values counts')
        ax[0].set_xlabel('Stations')
        ax[0].set_ylabel('# missing counts')
        ax[1].bar(data.index[41:], data['missing counts'].values[41:])
        ax[1].set_title('The missing values counts')
        ax[1].set_xlabel('Stations')
        ax[1].set_ylabel('# missing counts')
        ax.tight_layout()
                      
    if name == 'missing percentage':
        fig, ax = plt.subplots(2,1,figsize=(25,13))
        ax[0].bar(data.index[:41],data['missing percentage (%)'].values[:41])
        ax[0].set_title('The missing values percentage')
        ax[0].set_xlabel('Stations')
        ax[0].set_ylabel('missing percentage (%)')
        ax[1].bar(data.index[41:],data['missing percentage (%)'].values[41:])
        ax[1].set_title('The missing values percentage')
        ax[1].set_xlabel('Stations')
        ax[1].set_ylabel('missing percentage (%)')        

def main():
    os.chdir("D:\\Radar Projects\\lizhi\\for LiZhi")
    folders = ['2018-11', '2018-12', '2019-01']
    First =True
    for folder in folders:
        os.chdir(f"./{folder}")
        # Read excel data
        i=0
        for rainfall_data in os.listdir():
            if First:
                df = pd.read_excel(rainfall_data)
                df = data_cleaning(df)
                First=False
            else:
                _df = data_cleaning(pd.read_excel(rainfall_data))
                df = df.append(_df)
            i+=1
            print(f"{i}/{len(os.listdir())} completed")
        print(f"{folder} completed")
        os.chdir('../')
    return df

if __name__=='__main__':
    rain_all_gauges = main()
    #create a time range from given gauge data
    time_range = pd.date_range('2018-11-01','2019-01-06',freq='5T')[:-1]
    rain_all_gauges.set_index(time_range,inplace=True)
   
    #plot time series 
    #pool = mp.Pool(processes=4)
    #pool.apply(ts_plot, [rain_all_gauges])
    #ts_plot(rain_all_gauges)
    # detect number of missing values
  #  missing_values = pd.DataFrame(columns= rain_all_gauges.columns)
  #  a,b = pool.apply(detect_missing, [rain_all_gauges])
  #  missing_values = missing_values.append([a,b], ignore_index=True)
  #  missing_values['header'] = ['missing counts', 'missing percentage (%)']
  #  missing_values.set_index('header', inplace=True)
  #  missing_values_T = missing_values.T
   # miss_bar_plot(missing_values_T, 'missing counts')
   # miss_bar_plot(missing_values_T, 'missing percentage')
   # f = open('cleaned_data.pckl', 'wb')
   # pickle.dump(rain_all_gauges, f)
   # f.close()
    
    
    #ts_plot(rain_all_gauges)
    


