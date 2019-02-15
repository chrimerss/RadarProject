# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 16:01:48 2019

@author: lizhi
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
from PIL import Image
import scipy
from scipy import misc
import cv2


def grid2grid(x,y,x_dis, y_dis):
    return (int(x+x_dis/100.), int(y+y_dis/100.)) #distance divided by 100m per pixel

def get_dis(V, timestep):
    '''
    This function calculates the distance over some velocity, meaning each cell
    moves certain distances
    
    Args:
        V: velocity field (1000,1000,2)
        timestep: int, in seconds
    Returns:
        dis_X, dis_Y: array-like, (1000,1000)
    '''
    V_x,V_y = V[:,:,0], V[:,:,1]
    D_x, D_y = V_x*timestep, V_y*timestep
    return D_x, D_y

os.chdir('D:\\Radar Projects\\lizhi\\for LiZhi\\WindField')
#curr_img = np.matrix(Image.open('test_file.tif'))
#THRESHOLD = 0.5
#curr_img[curr_img>THRESHOLD] = 10
#curr_img[curr_img<THRESHOLD] = 0

#x,y = np.where(curr_img==1)
#sub_x = x[:100]
#sub_y = y[:100]
#
#V = np.zeros((1000,1000,2), dtype=np.float16)
#for z in range(2):
#    for x in range(0,1000,20):
#        for y in range(0,1000,20):
#            V[x:x+20,y:y+20,z] = np.random.randint(-10,10)


V = np.zeros((1000,1000,2))
V[400:500,400:420,0] = 4
V[400:500,420:550,0] = 6
V[400:500,450:570,0] = 8
V[400:500,470:500,0] = 10


V[400:420,400:500,1] = 4
V[420:450,400:500,1] = 6
V[450:470,400:500,1] = 8
V[470:500,400:500,1] = 10

curr_img = np.zeros((1000,1000))
curr_img[400:500, 400:500] = 1

#for time in range(2,62,2):
#    pred_img = np.zeros((1000,1000), dtype=np.float16)
#    D_x,D_y = get_dis(V, time*2*60)
#    for i,j in zip(x,y):
#        (trans_i, trans_j) = grid2grid(i,j,D_x[i,j], D_y[i,j])
#        if 0<=trans_i<=999 and 0<=trans_j<=999: 
#            pred_img[trans_i, trans_j] += 1
#    pred_img[pred_img<0.5] = 0
#    pred_img[pred_img>0.5] = 1
#    scipy.misc.imsave(f'pred-subgrid-{time}.png', pred_img)





def ADE_solver(curr_img,V,dx,dy,dt,nt):
    # t is recorded by seconds
#    curr_img = cv2.resize(curr_img, (nx*1000, ny*1000), interpolation=cv2.INTER_LINEAR)
    U = V[:,:,0]
    V = V[:,:,1]
#    curr_img = scipy.sparse.csr_matrix(curr_img)
#    print(U.shape, V.shape)
#    U = cv2.resize(U, (nx*1000, ny*1000), interpolation=cv2.INTER_LINEAR)
#    V = cv2.resize(V, (nx*1000, ny*1000), interpolation=cv2.INTER_LINEAR)
#    curr_rain = curr_img[curr_img!=0]
#    curr_rain = cv2.resize(curr_rain, curr_rain.shape*10, interpolation = cv2.INTER_LINEAR)
    for t in range(dt,nt*dt+dt,dt):
        pred_img = np.zeros((1000,1000))
        In = curr_img.copy()
        In[1:,1:] = curr_img[1:,1:] -U[1:,1:]*dt/dx*(curr_img[1:,1:]-curr_img[1:,0:-1]) -V[1:,1:]*dt/dy*(curr_img[1:,1:]-curr_img[0:-1,1:])
        curr_img = In
        if t%60==0:
            D_x,D_y = dx*(t/dt),dy*(t/dt)
#            print(D_x, D_y)
            x,y = np.where(In!=0)
            for (m,n) in zip(x,y):
                (trans_i, trans_j) = grid2grid(m,n,D_y,D_x)
                if 0<=trans_i<=999 and 0<=trans_j<=999: 
                    pred_img[trans_i, trans_j] = In[m,n]
            pred_img[pred_img<0.5] = 0
            pred_img[pred_img>=0.5] = 1
#            X,Y = np.where(pred_img!=0)
#            print(X[-1],Y[-1])
            scipy.misc.imsave(f'ADE-{t}.png', pred_img)
            print(int(t/60),' mins processed')
#        curr_img = pred_img
    return pred_img

            

pred = ADE_solver(curr_img,V,100,100,5,360)

#
#plt.figure()
#plt.imshow(In)


#img = cv2.resize(curr_img, fx=0.1, fy=0.1,interpolation=cv2.INTER_LINEAR)