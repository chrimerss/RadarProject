# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 16:40:28 2019

@author: lizhi
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from furuno import nowcast_images
import dateutil
import time
from PIL import Image
from multiprocessing import Pool
import multiprocessing
import pdb
from RadarForecast_Stat_Jan25 import FUNC_LISTS
import itertools
import scipy

def moving_window(pred, obs,patch_size):
    #patch_size: tuple e.g. (5,5)
    # return patch-size matrix
    step_x = patch_size[0]
    step_y = patch_size[1]
    for x in range(1000/step_x):
        for y in range(1000/step_y):
            i+=1
            yield pred[x:x+step_x, y:y+step_y], obs[x:x+step_x, y:y+step_y],i

def read_tif_file():
    files=[]
    for tif in os.listdir("D:\\Radar Projects\\lizhi\\for LiZhi\\ModelForecast\\RadarRaw"):
        if tif[-4:]=='.tif':
            files.append(tif)
    files=np.array(files)
    return files

def gauge_based(threshold):
    inds = []
    daily_gauge = pd.read_excel('D:\\Radar Projects\\lizhi\\for LiZhi\\1440min-gauge-adjusted.xlsx')
    daily_gauge.index = daily_gauge.index.tz_localize('Asia/Ujung_Pandang').tz_convert("UTC").tz_convert(None)
    for day in daily_gauge.index:
        if daily_gauge.loc[day].mean()>threshold:
            inds.append(day)
    return inds


def read_event_meta():
    events = pd.read_excel('D:\\Radar Projects\\lizhi\\for LiZhi\\Events.xlsx')
    events['start'] = [s.replace('"','') for s in events['start']]
    events['end'] = [s.replace('"','') for s in events['end']]
    for i in range(len(events)):
        events.start[i] = pd.to_datetime(events['start'][i], format='%d/%m/%Y %H:%M').tz_localize('Asia/Ujung_Pandang').tz_convert("UTC").tz_convert(None)
        events.end[i] = pd.to_datetime(events['end'][i], format='%d/%m/%Y %H:%M').tz_localize('Asia/Ujung_Pandang').tz_convert("UTC").tz_convert(None)
# check radar date
    return events


def batch_radar(files_tot, event,cal='gauge', lead_time='0 days 01:00:00'):
    '''
    lead_time: str, 
    '''
    # detect time
    sbt_time = [dateutil.parser.parse(each.split('_')[1][:-4]) for each in files_tot]
    if cal =='event':
        events.index=events.start
        events['lead_start'] = events.start - pd.Timedelta(lead_time)
        evenst['lead_end'] = event.end - pd.Timedelta(lead_time)
        for i in range(len(events)-1):
            event = events.iloc[i+1,:]
            inds=[]
            [inds.append(j) for j in range(len(sbt_time)) if sbt_time[j]>= event.lead_start and sbt_time[j]<=event.lead_end]
        #        ind = (sbt_time>event.start) & (sbt_time<event.end)
            inds = [inds[0]-2]+[inds[0]-1]+inds
            return list(files_tot[inds])
        print('--------------event done---------------')

    elif cal=='gauge':
        inds=[]
        [inds.append(j) for j in range(len(sbt_time)) if sbt_time[j]>=event and sbt_time[j]<= event+pd.Timedelta('1 days')]
        inds = [inds[0]-2]+[inds[0]-1]+inds
        return list(files_tot[inds])
        
def Nowcast(event):
    start = time.time()
    FILE= read_tif_file()
    os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi\\ModelForecast\\RadarRaw')
    files_batch = batch_radar(FILE, event)
    for j in range(2, len(files_batch)):
        if np.sum(np.matrix(Image.open(files_batch[j-2]))/100.)>8000 and np.sum(np.matrix(Image.open(files_batch[j-1]))/100.)>8000 and\
        np.sum(np.matrix(Image.open(files_batch[j]))/100.)>8000:
            files_three = files_batch[j-2:j+1]
        #            print(files_three)
        #                pdb.set_trace()
            nowcast= nowcast_images(files_three, time_step=120, new_method=True)
            
            for timestamp, ind, pred in nowcast.nowcast(num_predicted=31):
#                obs_file = '0000_'+timestamp.strftime("%Y%m%d%H%M%S")+'.tif'
#                obs = np.asarray(Image.open(obs_file))
                # caluculate statistics 500x500 pixels
#                stats = pd.DataFrame(columns=FUNC_LISTS.keys(), index=range(4))  # calculate statistics later
#                for pred_sub, obs_sub, ind in moving_window(pred, obs, (500,500)):
#                for pred_sub, obs_sub,_ in moving_window(pred, obs, (5,5)):
                    
#                    for key in FUNC_LISTS.keys():
#                        stats[key][i] = FUNC_LISTS[key](obs_sub, pred_sub)
#                stats.to_excel(writer, sheet_name='%sminlead_'%((ind+1)*2))
                os.chdir('../RadarNowcast_60min')
#                img = Image.fromarray(pred)
                mat = scipy.sparse.csr_matrix(pred, dtype=int)
#                img.save('%s_'%(files_three[-1][:-4])+'%sminlead_'%((ind+1)*2)+timestamp.strftime("%Y%m%d%H%M%S")+'.tif')
                scipy.sparse.save_npz('%s_'%(files_three[-1][:-4])+'%sminlead_'%((ind+1)*2)+timestamp.strftime("%Y%m%d%H%M%S")+'.npz', mat)
            print('batch %s completed'%(j))
            os.chdir('../RadarRaw')
    end=time.time()
    print('----------one event done, elapsed time: %s hours-----------'%((end-start)/3600.))
#            
def main():
    events = gauge_based(10)
    pool = Pool(multiprocessing.cpu_count())
    pool.map(Nowcast, events)
    pool.close()
    
        
if __name__=='__main__':
    start=time.time()
#Nowcast(events)
    main()
    end=time.time()
    elapsed = end-start
    print('total elapsed time: %s hours'%(elapsed/3600))


#events = gauge_based(10)
#for i in batch_radar(FILE, events,cal='gauge', lead_time='0 days 01:00:00'):
#    a = Image.open(i[0])
#    b=np.matrix(a)/100.
#    print(np.sum(b))
#    
#a = Image.open(FILE[1])
#b = np.matrix(a)
#np.matrix.sum(b)
