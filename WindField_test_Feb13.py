# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:47:44 2019

@author: lizhi

The methods of avoiding split and merge are including:
    
    scenario 1 (Benchmark):
        Maintain wind vector during forecast for sub-domains
        function: scenario_1(num_blocks)
    scenario 2:
        Moving wind vector along with events
    scenario 3:
        Combination of scenario 1 and 2
    scenario 4:
        Sum pixels when merging and Split for partition
    scenario 5:
        Substitute merged pixels with the maximum and maintain the split
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from scipy.ndimage import shift
from PIL import Image
import cv2
from numba import jit
import imageio
import datetime
import scipy

os.chdir('../for LiZhi/WindField')

def grid2grid(x,y,x_dis, y_dis):
    return (int(x+x_dis/100.), int(y+y_dis/100.)) #distance divided by 100m per pixel

def get_V(velocity_vector):
    '''
    This function returns the velocity field.
    
    Args:
    
        
    Returns:
        V_x, V_yb: array-like, (1000,1000), m/s
        
    '''
#    V_x,V_y = np.random.randint(-10, 10, (1000,1000)),np.random.randint(-10, 10, (1000,1000))
    return V_x, V_y

def get_dis(V, num_pred):
    '''
    This function calculates the distance over some velocity, meaning each cell
    moves certain distances
    
    Args:
        num_pred: int; indicates the predicted minutes ahead
    Returns:
        dis_X, dis_Y: array-like, (1000,1000)
    
    '''
    V_x,V_y = V[:,:,0], V[:,:,1]
    D_x, D_y = V_x*num_pred*2*60, V_y*num_pred*2*60
    return D_x, D_y

def Pred_img(curr_img, V , num_pred):
    '''
    This function predicts the number of images
    
    Args:
        curr_img: takes the current timestamp image, array-like (1000,1000), thresholded
        num_pred: see in get_dis
    
    Returns:
        img: predicted image
    '''
    #Initialize the pred_img:
    pred_img = np.zeros((curr_img.shape), np.int8) #binary image
    D_x, D_y = get_dis(V, num_pred)
    x,y = np.where(curr_img==1)
    for i,j in zip(x,y):
        (trans_i, trans_j) = grid2grid(i,j,D_x[i,j], D_y[i,j])
        if 0<=trans_i<=999 and 0<=trans_j<=999: 
            pred_img[trans_i, trans_j] = 1

    return pred_img

@jit(nopython=True, parallel=True)
def _matrix_synthesize(V, num_blocks):
    x,y,z = V.shape
    block_size= int(x/num_blocks)
    for m in range(z):
        for i in range(0,1000,num_blocks):
            for j in range(0,1000,num_blocks):
                V[i:i+block_size-1, j:(j+block_size-1),m] = V[i:i+block_size-1, j:(j+block_size-1),m].mean()
    return V

def scenario_1(curr_img, V, num_blocks, num_pred=None):
    '''
    This function correspondes to the first scenario see description above,
    one parameter needs to be specified is number of blocks which means the number of
    sub-domains want to use. Alternatively, if it is left with blank, then the system automatically
    determines how many blocks to use. The philosophy behind is first to locate the cloud, 
    '''
    V = _matrix_synthesize(V, num_blocks)
    pred_img = Pred_img(curr_img, V, num_pred)
#    scipy.misc.imsave(f'pred-{i}.png', pred_img)        
    return pred_img, V


#def make_gif():
#    images=[]
#    for image in scenario_1(curr_img, V, num_blocks):
#        images.append(imageio.imread(Image.fromarray(image)))
#    output_file = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
#    imageio.mimsave(output_file, images, duration=2)
    
num_blocks=20


V = np.random.randint(-10, 10, (1000,1000,2))



img = np.matrix(Image.open('test_file.tif'))
THRESHOLD = 0.5
curr_img = np.zeros(img.shape, dtype=np.int8)
curr_img[img>THRESHOLD] = 1
curr_img[img<THRESHOLD] = 0
next_img, Wind = scenario_1(curr_img, V, 20, 2)


fig = plt.figure()
plt.subplot(121)
plt.imshow(curr_img)
ax = plt.gca();
ax.grid()
plt.subplot(122)
plt.imshow(next_img)
ax = plt.gca();
ax.grid()
