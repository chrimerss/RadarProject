# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 09:11:21 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from sklearn.metrics import r2_score
from AggregateAllScripts import RadarGauge

RG = RadarGauge('D:\\Radar Projects\\lizhi\\for LiZhi')
gauge_10, radar_10 = RG.read_gauge_radar_10min()
#r2_score( radar_10['S100'], [radar_10['S100'].mean()]*len(radar_10))
RG.radar_gauge_ts_plot(radar_10, gauge_10)

#x,y = RG.delete_zeros_nans()
#x,y = RG.delete_zeros_nans(radar_10['S100'], gauge_10['S100'])
trace1 = go.Bar(x=x.index,
                y=x,
                name='gauge'
               )
trace2 = go.Bar(x=y.index,
                y=y,
                name='radar'
                )
data = [trace1, trace2]
layout = go.Layout(title=f'col',
            barmode='group',
            xaxis=dict(autorange=True,
                       tickmode = 'array',
                       tickvals=np.asarray(x.index),
                       ticktext=np.asarray(x.index))
        )
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename = f'col.html', auto_open=False)

df = pd.DataFrame()
df['gauge'] = x
df['radar'] = y
df.iplot(kind='bar')