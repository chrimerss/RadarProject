# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:29:00 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
from furuno import nowcast_images
import time
from PIL import Image
import os
import pandas as pd
import scipy
from tqdm import tqdm

def moving_window(pred, obs, patch_size=(5,5)):
    step_x = patch_size[0]
    step_y = patch_size[1]
    for x in range(1000/step_x):
        for y in range(1000/step_y):
            yield pred[x:x+step_x, y:y+step_y], obs[x:x+step_x, y:y+step_y], (x,y)

def read_pred(lead_time):
    '''
    lead_time: str e.g. 10minlead
    '''
    files_lists = np.asarray(os.listdir("D:\\Radar Projects\\lizhi\\for LiZhi\\ModelForecast\\RadarNowcast_60min"))
    inds=[]
    for file in files_lists:
        if file.split('_')[2]==lead_time:
            inds.append(True)
        else:
            inds.append(False)
    pred_time= [files_lists[inds][j].split('_')[-1][:-4] for j in range(len(files_lists[inds]))]
    orig_time = [files_lists[inds][j].split('_')[0][6:] for j in range(len(files_lists[inds]))]
    return files_lists[inds], pred_time, orig_time

def read_obs(files):
	exact_files = ['0000_'+files[j]+'.tif' for j in range(len(files))]
	return exact_files

# def Statistics_cal(y_true, y_pred):

# 	for key in FUNC_LISTS.keys():

def read_batch_file(files_pred, files_obs):
	#read pred
	if len(files_pred!= files_obs):
		raise ValueError("the length of predicted and observed is not consistent!")
	for i in range(len(files_pred)):
		pred = np.asaarray(Image.open(files_pred[i]))
		obs = np.asarray(Image.open(files_obs[i]))
		yield pred, obs, i

def Group_data(patch_size):
	# patch_size; tuple (5,5)
    os.chdir("D:\\Radar Projects\\lizhi\\for LiZhi\\ModelForecast\\RadarNowcast_60min")
    for x in range(patch_size[0]):
        for y in range(patch_size[1]):
#            df= pd.DataFrame(columns = [str(i)+'mislead' for i in range(2,62,2)])
            df= pd.DataFrame()
            for lead_time in tqdm(range(6,12,2)):
                lead_str = str(lead_time)+'minlead'
                pred_files, pred_times, orig_times = read_pred(lead_str)
                _df = {}
                print('Processing :%s'%(lead_str))
                for i,pred in enumerate(pred_files):
                    pred_mat = scipy.sparse.load_npz(pred).todense()
                    _df.update({orig_times[i]: pred_mat[x:x+patch_size[0], y:y+patch_size[1]].mean()/100.})
                _df = pd.Series(data=_df.values(), index=_df.keys())
#                print(len(_df))
                df = pd.concat([df, _df], axis=1, ignore_index=True)
#            df.columns=[str(i)+' min lead' for i in range(2,62,2)]
            df.to_csv('../Table/predicted-(%s,%s).csv'%(x+1,y+1))
            print("---------one patch done! --------")


def main():
	# read
    start = time.time()
    Group_data((50,50))
    end = time.time()
    elapsed = end-start
    print("elapsed time: %s"%(elapsed))

if __name__=='__main__':
	main()
