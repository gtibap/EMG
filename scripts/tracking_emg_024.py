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
    
    
    # path = '../data/priority_patients/kinematics/ebc024/'
    # session = ['s1/','s9/','s13/'] 
    # filename = '../data/motive_tracking/tracking_006_s1/e1.csv'
    filename = '../data/priority_patients/kinematics/ebc024/s1/Take 2022-05-06 01.48.53 PM.csv'
    filenames = ['']
    # filename_emg = '../data/motive_tracking/tracking_006_s1/ebc_006_s01_e1.mat'
    ## reading csv file. Header includes: Frame, Time, ... 
    df = pd.read_csv(filename, header=5)
    # print(f'{df.columns}')
    # print(f'{df}')
    
    ## right leg
    ## thigh markers Unlabeled 6538 and 4692
    ## leg markers Unlabeled 5461 and 5498
    
    ## csv file columns
    
    ## Unlabeled:4692 columns (DP,DQ,DR) -> [119:122]
    ## Unlabeled:6538 columns (EE,EF,EG) -> [134:137]
    
    ## Unlabeled:5461 columns (DY,DZ,EA) -> [128:131]
    ## Unlabeled:5498 columns (EB,EC,ED) -> [131:134]
    
    ## two first thigh; two last leg
    list_ids_x = [119, 134, 128, 131,]
    
    # for id_x in list_ids_x:
        # print(f'{df.iloc[:,id_x]}')
    
    ## how many missing values in the selected columns?
    print('\nMissing values before interpolation:')
    for i, id_x in enumerate(list_ids_x):
        print(f'Marker {i}: {df.iloc[:,id_x].isnull().sum()}')
    
    print('\n')
        
    ## filling missing data
    for id_x in list_ids_x:
        df.iloc[:,id_x+0].interpolate(method="cubicspline", inplace=True, limit_direction='both')
        df.iloc[:,id_x+1].interpolate(method="cubicspline", inplace=True, limit_direction='both')
        df.iloc[:,id_x+2].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    
    # fig, ax = plt.subplots(nrows=4,ncols=1)
    col=2
    ## converting selected columns to numpy arrays
    markers_arr = np.empty([len(list_ids_x), len(df), 3])
    for i, id_x in enumerate(list_ids_x):
        markers_arr[i] = df.iloc[:,id_x:id_x+3].to_numpy()
        # ax[i].plot(markers_arr[i,:,col], label='original')
        markers_arr[i] = smooth_filter(markers_arr[i])
        # ax[i].plot(markers_arr[i,:,col], label='smooth')
    
    print(f'markers_arr:\n{markers_arr}')
    # plt.show()
    
    # CD_Marker1 = df.iloc[:,110:113].to_numpy()
    # CD_Marker2 = df.iloc[:,113:116].to_numpy()
    # CD_Marker3 = df.iloc[:,116:119].to_numpy()
    # CD_Marker4 = df.iloc[:,119:122].to_numpy()
    # JD_Marker1 = df.iloc[:,122:125].to_numpy()
    # JD_Marker2 = df.iloc[:,125:128].to_numpy()
    # JD_Marker3 = df.iloc[:,128:131].to_numpy()
    # JD_Marker4 = df.iloc[:,131:134].to_numpy()
    
    # JCD_Marker = np.linalg.norm(JD_Marker3 - CD_Marker4, axis=1)
    # fig1, ax1 = plt.subplots()
    # ax1.plot(JCD_Marker, label='original')
    # ax1.legend()
    
    # fig2, ax2 = plt.subplots()
    # fig3, ax3 = plt.subplots()
    # fig4, ax4 = plt.subplots()
    # ax1.plot(CD_Marker1[:,0], label='original')
    # ax2.plot(CD_Marker1[:,1], label='original')
    # ax3.plot(CD_Marker1[:,2], label='original')
    
    ## smoothing every component (x, y, z) of the markers location
    # CD_Marker1 = smooth_filter(CD_Marker1)
    # CD_Marker2 = smooth_filter(CD_Marker2)
    # CD_Marker3 = smooth_filter(CD_Marker3)
    # CD_Marker4 = smooth_filter(CD_Marker4)
    # JD_Marker1 = smooth_filter(JD_Marker1)
    # JD_Marker2 = smooth_filter(JD_Marker2)
    # JD_Marker3 = smooth_filter(JD_Marker3)
    # JD_Marker4 = smooth_filter(JD_Marker4)
    
    # JCD_Marker = np.linalg.norm(JD_Marker3 - CD_Marker4, axis=1)
    # ax1.plot(JCD_Marker, label='filtered')
    # ax1.legend()
    
    
    # ax1.plot(CD_Marker1[:,0], label='smooth')
    # ax2.plot(CD_Marker1[:,1], label='smooth')
    # ax3.plot(CD_Marker1[:,2], label='smooth')
        
    # print(f'CD_Marker1:\n{CD_Marker1}\n shape: {CD_Marker1.shape}')
    
    ## calculating mean points for both CD markers and JD markers
    # CD_center = (CD_Marker1 + CD_Marker2 + CD_Marker3 + CD_Marker4)/4
    # JD_center = (JD_Marker1 + JD_Marker2 + JD_Marker3 + JD_Marker4)/4

    CD_center = (markers_arr[0] + markers_arr[1])/2
    JD_center = (markers_arr[2] + markers_arr[3])/2
    
    
    ## calculating distance between the two markers centers 
    JCD_norm = np.linalg.norm(JD_center - CD_center, axis=1)
    
    # fig2, ax2 = plt.subplots(nrows=1,ncols=1)
    # ax2.plot(JCD_norm, label='JCD_norm')
    # ax4.plot(JCD_norm, label='JCD_norm')
    # ax1.plot(JCD_norm, label='average')
    # ax2.legend()
    # plt.show()
    
    # print(f'jcd: {JCD_norm.shape[0]/120}')
    
    ## finding maximums and minimums (positive and negative picks) of the resultant signal
    max_list, min_list = max_and_min(JCD_norm)
    # print(f'max and min:\n{max_list},\n{min_list}')
    
    sample_rate_tracking = 120 ## samples per second (Hz)
    ## time in seconds
    t_delay=0.0
    arr_time_max = np.array(max_list)/sample_rate_tracking - t_delay
    arr_time_min = np.array(min_list)/sample_rate_tracking - t_delay
    
    ## plot signal distance
    # plot_distance(JCD_norm, max_list, min_list)
    
    #####
    ## EMG reading
    # path_kin = '../data/priority_patients/kinematics/ebc024/s1/Take 2022-05-06 01.48.53 PM.c3d'
    # path_emg = '../data/priority_patients/EBC024/EBC24-S4-E3.mat'
    path_emg = '../data/priority_patients/EBC024/'
    
    # filename = 'ebc_006_s01_e1.mat'
    filename = 'EBC24-S4-E3.mat'
    file_channels = [9,16]

    obj_emg = Reading_EMG(path_emg, filename, file_channels)
    # obj_emg.plotSignals()
    obj_emg.filteringSignals()
    obj_emg.envelopeFilter()
    
    ids_emg_plot = [7,2,4,1,6,5,0,3]
    title_emg = 'B - T5 (discharge)  -> C - L1 (12 months)'
    patient_number = '024'
    session_name='a'
    file_number=0
    act_emg=[0,1,3]
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT.GASTRO LT, uV', 'LAT.GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']
    
    # obj_emg.plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
    
    ## Arrays max and min distance between markers from the right leg. Therefore, lines in the plot are as follows: 
    ## orange: flexion; minimum distance
    ## purple: extension: maximum distance
    
    obj_emg.plotSegmentedSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names, arr_time_max, arr_time_min)
    
    ## left leg we exchange min and max
    # signal_name = 'TIB.ANT. LT, uV'
    # obj_emg.flexion_extension(arr_time_min, arr_time_max, signal_name)
    
    ## right leg we keep min and max
    # signal_name = 'VLO RT, uV'
    signal_name = 'VMO RT, uV'
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
