#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tracking_emg.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy.signal import savgol_filter

def smooth_filter(arr):
    arr[:,0]=savgol_filter(arr[:,0], window_length=60, polyorder=1, mode='mirror')
    arr[:,1]=savgol_filter(arr[:,1], window_length=60, polyorder=1, mode='mirror')
    arr[:,2]=savgol_filter(arr[:,2], window_length=60, polyorder=1, mode='mirror')
    return arr

def max_and_min(arr):
        win_size = 60
        id0=0
        delta=10
        max_list=[]
        min_list=[]
        while id0 < len(arr):
            window = arr[id0:id0+win_size]
            ids_max = np.argmax(window)
            ids_min = np.argmin(window)
            print(f'max:{ids_max}')
            print(f'min:{ids_min}')
            max_list.append(ids_max+id0) 
            min_list.append(ids_min+id0) 
            id0 = id0 + delta
        
        return max_list, min_list

def main(args):
    
    filename = '../data/motive_tracking/tracking_006_s1/e1.csv'
    ## reading csv file. Header includes: Frame, Time, ... 
    df = pd.read_csv(filename, header=5)
    print(f'{df.columns}')
    print(f'{df}')
    # print(f'{df.iloc[:,6].tolist()}')
    
    ## for EBC006_s1 we selected markers on the right (droite) leg: four at the cuisse and four at the jambe
    
    ## how many missing values in the selected columns?
    print('\nMissing values:')
    print(f'CD_Marker1: {df.iloc[:,110].isnull().sum()}')
    print(f'CD_Marker2: {df.iloc[:,113].isnull().sum()}')
    print(f'CD_Marker3: {df.iloc[:,116].isnull().sum()}')
    print(f'CD_Marker4: {df.iloc[:,119].isnull().sum()}')
    print(f'JD_Marker1: {df.iloc[:,122].isnull().sum()}')
    print(f'JD_Marker2: {df.iloc[:,125].isnull().sum()}')
    print(f'JD_Marker3: {df.iloc[:,128].isnull().sum()}')
    print(f'JD_Marker4: {df.iloc[:,131].isnull().sum()}')
    print('\n')
        
    ## filling missing data
    df.iloc[:,110:113].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df.iloc[:,113:116].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df.iloc[:,116:119].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df.iloc[:,119:122].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df.iloc[:,122:125].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df.iloc[:,125:128].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df.iloc[:,128:131].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df.iloc[:,131:134].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    
    CD_Marker1 = df.iloc[:,110:113].to_numpy()
    CD_Marker2 = df.iloc[:,113:116].to_numpy()
    CD_Marker3 = df.iloc[:,116:119].to_numpy()
    CD_Marker4 = df.iloc[:,119:122].to_numpy()
    JD_Marker1 = df.iloc[:,122:125].to_numpy()
    JD_Marker2 = df.iloc[:,125:128].to_numpy()
    JD_Marker3 = df.iloc[:,128:131].to_numpy()
    JD_Marker4 = df.iloc[:,131:134].to_numpy()
    
    # fig, ax = plt.subplots()
    # ax.plot(CD_Marker1[:,1], label='original')
    
    CD_Marker1 = smooth_filter(CD_Marker1)
    CD_Marker2 = smooth_filter(CD_Marker2)
    CD_Marker3 = smooth_filter(CD_Marker3)
    CD_Marker4 = smooth_filter(CD_Marker4)
    JD_Marker1 = smooth_filter(JD_Marker1)
    JD_Marker2 = smooth_filter(JD_Marker2)
    JD_Marker3 = smooth_filter(JD_Marker3)
    JD_Marker4 = smooth_filter(JD_Marker4)
    
    # ax.plot(CD_Marker1[:,1], label='smooth')
    
    
    print(f'CD_Marker1:\n{CD_Marker1}\n shape: {CD_Marker1.shape}')
    
    ## calculation mean points for both CD markers and JD markers
    CD_center = (CD_Marker1 + CD_Marker2 + CD_Marker3 + CD_Marker4)/4
    JD_center = (JD_Marker1 + JD_Marker2 + JD_Marker3 + JD_Marker4)/4
    
    
    JCD_norm = np.linalg.norm(JD_center - CD_center, axis=1)
    
    
    ## finding maximum and minimum at each window
    max_list, min_list = max_and_min(JCD_norm)
    print(f'max and min:\n{max_list},\n{min_list}')
    
    
    
    
    # JCD_grad = np.gradient(JCD_norm)
    
    fig, ax = plt.subplots()
    ax.plot(JCD_norm, label='original')
    # ax.plot(JCD_grad, label='gradient')
    ax.legend()
    ax.set_xlim([500,1000])
    plt.show()
    
    # norm_CD_center = np.linalg.norm(CD_center,axis=1)
    # norm_JD_center = np.linalg.norm(JD_center,axis=1)
    
    
    # fig1, ax1 = plt.subplots()
    # ax1.plot(norm_JD_center, label='JD_norm')
    # ax1.plot(norm_CD_center, label='CD_norm')
    # ax1.set_xlim([500,1000])
    # ax1.legend()
    
    # color = 'tab:red'
    # ax1.set_xlabel('samples')
    # ax1.set_ylabel('JCD_norm [m]', color=color)
    # ax1.plot(JCD_norm, color=color)
    # ax1.tick_params(axis='y', labelcolor=color)

    # ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    # color = 'tab:blue'
    # ax2.set_ylabel('JCD_gradient [m/sample]', color=color)  # we already handled the x-label with ax1
    # ax2.plot(JCD_grad, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)

    # ax2.set_xlim([500,100])
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.show()
    
    
    '''    
    ## column 0 frames, column 1 time (seconds)
    frames = df.iloc[:,0].tolist()
    time = df.iloc[:,1].to_numpy()

    ## coordinates marker 1 left knee
    lmfc_x = df.iloc[:,26].to_numpy()
    lmfc_y = df.iloc[:,27].to_numpy()
    lmfc_z = df.iloc[:,28].to_numpy()
    
    ## ## coordinates marker lower left leg
    ltb2_x = df.iloc[:,41].to_numpy()
    ltb2_y = df.iloc[:,42].to_numpy()
    ltb2_z = df.iloc[:,43].to_numpy()
    
    ## coordinates marker 2 left knee
    llfc_x = df.iloc[:,44].to_numpy()
    llfc_y = df.iloc[:,45].to_numpy()
    llfc_z = df.iloc[:,46].to_numpy()
    
    ## ## coordinates marker higher left leg
    lth2_x = df.iloc[:,50].to_numpy()
    lth2_y = df.iloc[:,51].to_numpy()
    lth2_z = df.iloc[:,52].to_numpy()
    
    print(f'lmfc_x:{lmfc_x}\nlmfc_y:{lmfc_y}\nlmfc_z:{lmfc_z}\n')
    print(f'ltb2_x:{ltb2_x}\nltb2_y:{ltb2_y}\nltb2_z:{ltb2_z}\n')
    print(f'llfc_x:{llfc_x}\nllfc_y:{llfc_y}\nllfc_z:{llfc_z}\n')
    print(f'lth2_x:{lth2_x}\nlth2_y:{lth2_y}\nlth2_z:{lth2_z}\n')
    
    ## middle point between the two markers left knee
    lfc_x = (llfc_x + lmfc_x)/2
    lfc_y = (llfc_y + lmfc_y)/2
    lfc_z = (llfc_z + lmfc_z)/2
    
    ## vector c (cuisse)
    vc_x = lfc_x - lth2_x
    vc_y = lfc_y - lth2_y
    vc_z = lfc_z - lth2_z
    
    ## vector j (jambe)
    vj_x = ltb2_x - lfc_x
    vj_y = ltb2_y - lfc_y
    vj_z = ltb2_z - lfc_z
    
    ## calculate angle between vector c and vector j using dot product
    vc_dot_vj = (vc_x*vj_x)+(vc_y*vj_y)+(vc_z*vj_z)
    norm_vc = np.sqrt(vc_x**2 + vc_y**2 +vc_z**2)
    norm_vj = np.sqrt(vj_x**2 + vj_y**2 +vj_z**2)
    theta = np.arccos(vc_dot_vj/(norm_vc * norm_vj))
    
    angle = 180 - np.rad2deg(theta)
    
    ## calculate distance between 
    vjc_x = ltb2_x - lth2_x
    vjc_y = ltb2_y - lth2_y
    vjc_z = ltb2_z - lth2_z
    
    norm_vjc = np.sqrt(vjc_x**2 + vjc_y**2 + vjc_z**2)
    
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('samples')
    ax1.set_ylabel('angle [deg]', color=color)
    ax1.plot(angle, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('dist [m]', color=color)  # we already handled the x-label with ax1
    ax2.plot(norm_vjc, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    '''    
    # plt.plot(angle, label='angle [deg]')
    # plt.plot((1000*norm_vjc)-100.35, label='dist [mm]')
    # plt.show()
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
