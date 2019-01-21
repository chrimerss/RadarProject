# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:48:19 2019

@author: lizhi

This 'test' module add all statistics to one excel file in order to
import everything into QGIS to produce map

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os

os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi')

gauge_meta = pd.read_excel('Rain_gauges.xlsx', sheet_name='Rain_gauges')
gauge_meta.station = [gauge_meta['station'][i].replace("'", '') for i in range(len(gauge_meta))]
gauge_meta.set_index('station',inplace=True)
gauge_meta = gauge_meta.sort_index()

# add loop data
xl = pd.ExcelFile('Statistics-marked-new.xlsx')
for sheet in xl.sheet_names:
    data = xl.parse(sheet).T.sort_index()
    data.columns = [f'MAE_{sheet}', f'pearson_{sheet}', f'RMSE_{sheet}', f'TVR_{sheet}', f'pos_{sheet}',f'neg_{sheet}']
    gauge_meta = pd.concat([gauge_meta, data], axis=1)

gauge_meta.to_excel('gaugePlusstat-marked.xlsx')