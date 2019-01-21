# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 08:41:21 2019

@author: lizhi

This module calculates the statistics of rain gauges in the period of Nov. to Dec
according to the monthly sum and daily sum

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from SpatialCorrelation import read_data
from SpatialCorrelation import read_dis_file
from RainfallProcessing import ind_rain_events, rain_events

def concatenate_period(rain_gauge):
    # concatenate the period excluding JAN.
    return rain_gauge[rain_gauge.index.year<2019]

def daily_sum(data, writer):
    '''
    aggregate the dataframe into daily basis
    Args:
        data: pandas dataframe; rain gauge data only include Dec and Nov
        writer: pd.to_excel writer
    Return:
        data: pandas dataframe, the index is tuple like (11,1); first is month
    '''
    data = data.groupby([data.index.month, data.index.day]).agg('sum')
    ind = pd.date_range(start='2018-11-01',end='2018-12-31', freq='D')
    data.index= ind
    data.to_excel(writer, sheet_name='daily')
    return data

def monthly_sum(data, writer):
    '''
    aggregate the dataframe into monthly basis
    Args:
        data: pandas dataframe; rain gauge data only include Dec and Nov
        writer: pd.to_excel writer
    Return:
        data: pandas dataframe
    '''
    data = data.groupby(data.index.month).agg('sum')
    data.to_excel(writer, sheet_name='monthly')
    return data

def main():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')
    rain_all_gauges, missing_events = read_data()
    rain_data = concatenate_period(rain_all_gauges)
    writer = pd.ExcelWriter('Daily_Monthly_Gauges_new.xlsx')
    daily = daily_sum(rain_data, writer)
    monthly = monthly_sum(rain_data, writer)
    
if __name__ == '__main__':
    main()

