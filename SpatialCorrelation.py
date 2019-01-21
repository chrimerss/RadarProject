# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:13:10 2019

This module deals with the distinguish with "good" and "bad" stations
The philosiphy behind is to fit a line of all points and for each station,
we count the # of good results, which are above the predicted line and then
rank the number of counts.

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os

def read_data():
    f = open('cleaned_data.pckl', 'rb')
    rain_all_gauges = pickle.load(f)
    f.close()
    f = open('missing_rainevents.pckl','rb')
    missing_events = pickle.load(f)
    f.close()
    for col in rain_all_gauges:
        if rain_all_gauges[col].isna().all():
            rain_all_gauges.drop(col, axis=1, inplace=True)
            missing_events.drop(col, axis=1, inplace=True)
    return rain_all_gauges, missing_events

def read_dis_file(file_name, rain_data):
    data = pd.read_excel(file_name, sheet_name='Sheet1')
    data = data.iloc[3:, 1:]
    data.columns = [s.replace("'", '') for s in data.columns]
    data['column_name'] = data.columns
    data.set_index('column_name', inplace=True)
    data = data[rain_data.columns]
    data = data.loc[data.columns,:]
    return data

def corplot(rain_data, dis_data):
    os.chdir('./spatial_plot')
    cor_mat = rain_data.corr()
    i=0
    for col in rain_data:
        x_values = dis_data[col]/10000
        y_values = cor_mat[col]
        fig, ax = plt.subplots(1,1, figsize=(15,8))
        ax.scatter(dis_data/10000., cor_mat, marker='.')
        ax.scatter(x_values, y_values, marker='.', color='r')
        ax.set_title(f"Scatter plot of {col}")
        ax.set_xlabel("Distance (10 km)")
        ax.set_ylabel("correlation")
        ax.set_xlim([0,5])
        ax.set_xticks(np.arange(0,5,0.5))
        fig.savefig(col+'.png')
        i+=1
        print(f"{i}/{len(rain_data.columns)} completed")
        
def log_transform(data):
    return np.log(data)

def model_fit(x_data, y_data):
    # this does not use
    output = np.polyfit(x_data, y_data, deg=1)
    return output

def iterative_ruleout(rain_data, dis_data):
    '''
    This function no longer use
    '''
    station_all = np.array(rain_data.columns)
    corr = rain_data.corr()
    for col in rain_data.columns:
        x = np.delete(dis_data[col].values,0)
        x_real = log_transform()
        coefs = model_fit(x_real, corr[col][1:])
        for ind, cor in enumerate(corr[col][1:]):
            y_expected = coefs[0] + coefs[1]*x_real[ind]
            if cor <y_expected:
                station_all = station_all[station_all!=col]
    return station_all

def fit_all(rain_data, dis_data):
    '''
    This function takes all correlation scatter plot in one graph and try to 
    fit a straight line to all points, stations above this line considered as 
    "good" stations
    '''
    from sklearn import linear_model
    corr = rain_data.corr()
    Y = np.ndarray.flatten(np.asarray(corr))
    X = np.ndarray.flatten(np.asarray(dis_data))
    nan_ind = np.where(pd.isnull(Y))[0]
    #print(nan_ind)
    ex_ind = list(set(np.arange(len(Y)))-set(nan_ind))
    #print(ex_ind)
    X = X[ex_ind]
    Y = Y[ex_ind]
    regr = linear_model.LinearRegression()
    X = (np.log(X[X!=0])).reshape(-1,1)
    Y = (Y[Y!=1]).reshape(-1,1)
    regr.fit(X, Y)
    Y_expected = regr.predict(X)
    return X, Y, Y_expected, regr

def plot(X, Y_train, Y_target):
    plt.figure()
    plt.scatter(X,Y_train, marker='.')
    plt.plot(X, Y_target, color='r')
    plt.show()

def main():
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi') #change the dir
    rain_all_gauges, missing_events = read_data()
    dis_mat = read_dis_file('Rain_gauges.xlsx', rain_data=rain_all_gauges)
    #corplot(rain_all_gauges, dis_mat)  if you want to plot the spatial scatter
    X,Y,Y_expected, model = fit_all(rain_all_gauges, dis_mat)
    corr = rain_all_gauges.corr()
    dic = dict(zip(corr.columns, [0]*len(corr.columns)))
    df_counts = pd.DataFrame(data=dic, index=[0])
    for col in corr.columns:
        for station in corr[col].index:
            #print(np.log(dis_mat[col][station]))
            if not (pd.isnull(np.log(dis_mat[col][station])) or np.isinf(np.log(dis_mat[col][station]))):
                y = model.predict(np.log(dis_mat[col][station]))
                if corr[col][station]>y:
                    df_counts[station]+=1
    df_counts['count'] = 'count'
    df_counts.set_index('count', inplace=True)
    new_df = df_counts.T.sort_values('count',axis=0)
    new_df.to_excel('correlation_counts.xlsx')
if __name__ == '__main__':
    main()
