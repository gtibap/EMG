#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tracking_emg.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy.signal import savgol_filter
import scipy.io
from class_emg_filtering import Reading_EMG

def smooth_filter(arr):
    arr[:,0]=savgol_filter(arr[:,0], window_length=60, polyorder=1, mode='mirror')
    arr[:,1]=savgol_filter(arr[:,1], window_length=60, polyorder=1, mode='mirror')
    arr[:,2]=savgol_filter(arr[:,2], window_length=60, polyorder=1, mode='mirror')
    return arr

def max_and_min(arr):
        
    max_list=[]
    min_list=[]
    win_size = 60
    delta=10
    id0=0
    
    while id0 < len(arr):
        window = arr[id0:id0+win_size]
        ids_max = np.argmax(window)
        ids_min = np.argmin(window)
        
        max_list.append(ids_max+id0) 
        min_list.append(ids_min+id0) 
        id0 = id0 + delta
    
    ids_max, max_counts = np.unique(max_list, return_counts=True)
    ids_min, min_counts = np.unique(min_list, return_counts=True)
    
    # print(f'max:\n{ids_max}, {max_counts}')
    # print(f'min:\n{ids_min}, {min_counts}')
    
    ## ids occurrences greater than 1
    sel_max = np.argwhere(max_counts > 1).reshape(1,-1)
    sel_min = np.argwhere(min_counts > 1).reshape(1,-1)
    
    # print(f'indices max: {sel_max}')
    # print(f'indices min: {sel_min}')
    
    ids_sel_max = ids_max[sel_max[0]]
    ids_sel_min = ids_min[sel_min[0]]
    
    # print(f'values max: {ids_sel_max}')
    # print(f'values min: {ids_sel_min}')

    return ids_sel_max, ids_sel_min


def plot_distance(JCD_norm, max_list, min_list):
    
    fig, ax = plt.subplots()
    ax.plot(JCD_norm, label='distance markers right leg')
    # ax.plot(JCD_grad, label='gradient')
    # only one line may be specified; full height
    for x_val in max_list:
        ax.axvline(x = x_val, color = 'tab:purple')
        
    for x_val in min_list:
        ax.axvline(x = x_val, color = 'tab:orange')
    
    ax.legend()
    # ax.set_xlim([500,1000])
    # plt.show()
    
    return 0
    
##################
## auxiliar plots
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
## auxiliar plots               
##################

def main(args):
    
    filename = '../data/motive_tracking/tracking_006_s1/e1.csv'
    # filename_emg = '../data/motive_tracking/tracking_006_s1/ebc_006_s01_e1.mat'
    ## reading csv file. Header includes: Frame, Time, ... 
    df = pd.read_csv(filename, header=5)
    # print(f'{df.columns}')
    # print(f'{df}')
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
    
    ## converting selected columns to numpy arrays
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
    
    ## smoothing every component (x, y, z) of the markers location
    CD_Marker1 = smooth_filter(CD_Marker1)
    CD_Marker2 = smooth_filter(CD_Marker2)
    CD_Marker3 = smooth_filter(CD_Marker3)
    CD_Marker4 = smooth_filter(CD_Marker4)
    JD_Marker1 = smooth_filter(JD_Marker1)
    JD_Marker2 = smooth_filter(JD_Marker2)
    JD_Marker3 = smooth_filter(JD_Marker3)
    JD_Marker4 = smooth_filter(JD_Marker4)
    
    # ax.plot(CD_Marker1[:,1], label='smooth')
        
    # print(f'CD_Marker1:\n{CD_Marker1}\n shape: {CD_Marker1.shape}')
    
    ## calculating mean points for both CD markers and JD markers
    CD_center = (CD_Marker1 + CD_Marker2 + CD_Marker3 + CD_Marker4)/4
    JD_center = (JD_Marker1 + JD_Marker2 + JD_Marker3 + JD_Marker4)/4
    ## calculating distance between the two markers centers 
    JCD_norm = np.linalg.norm(JD_center - CD_center, axis=1)
    
    # print(f'jcd: {JCD_norm.shape[0]/120}')
    
    ## finding maximums and minimums (positive and negative picks) of the resultant signal
    max_list, min_list = max_and_min(JCD_norm)
    # print(f'max and min:\n{max_list},\n{min_list}')
    
    sample_rate_tracking = 120 ## samples per second (Hz)
    ## time in seconds
    arr_time_max = np.array(max_list)/sample_rate_tracking - 0.1
    arr_time_min = np.array(min_list)/sample_rate_tracking - 0.1
    
    ## plot signal distance
    # plot_distance(JCD_norm, max_list, min_list)
    
    #####
    ## EMG reading
    path = '../data/motive_tracking/tracking_006_s1/' 
    filename = 'ebc_006_s01_e1.mat'
    file_channels = [9,16]

    obj_emg = Reading_EMG(path, filename, file_channels)
    # obj_emg.plotSignals()
    obj_emg.filteringSignals()
    obj_emg.envelopeFilter()
    
    ids_emg_plot = [5,7,3,0,6,4,2,1]
    title_emg = 'A - L2 (6 weeks)    -> B - L2 (12 months)'
    patient_number = '006'
    session_name='a'
    file_number=0
    act_emg=[0,1,2,3,5,6,7]
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT.GASTRO LT, uV', 'LAT.GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']
    
    # obj_emg.plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
    
    obj_emg.plotSegmentedSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names, arr_time_max, arr_time_min)
    
    signal_name = 'TIB.ANT. LT, uV'
    obj_emg.flexion_extension(arr_time_min, arr_time_max, signal_name)
    
    signal_name = 'VLO RT, uV'
    obj_emg.flexion_extension(arr_time_max, arr_time_min, signal_name)
    
    
    
    # obj_emg.plotSegmentedSignals()
    
    # mat = scipy.io.loadmat(filename_emg)
    # print(mat)
    # print('Header:',  mat['__header__'])
    # print('Channel Names:',  mat['channelNames'])
    
    # sampling_rate = mat['samplingRate'][0,0]
    # print(f'sample rate: {sampling_rate}')
    
    # num_ch=17
    # print(mat['channelNames'][0][num_ch][0])
    # channel_switch = mat['Data'][0, num_ch].flatten()
    
    # print(f'switch:{channel_switch.shape[0]/4000}')
    
    # fig, ax = plt.subplots()
    # ax.plot(channel_switch, label='switch')
    plt.show()
    
    
    
   
    
    
    
    
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
