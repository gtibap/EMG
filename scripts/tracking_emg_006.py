#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tracking_emg.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy.signal import savgol_filter


def main(args):
    
    filename = '../data/motive_tracking/tracking_006_s1/e1.csv'
    ## reading csv file. Header includes: Frame, Time, ... 
    df = pd.read_csv(filename, header=5)
    print(f'{df.columns}')
    print(f'{df}')
    # print(f'{df.iloc[:,6].tolist()}')
    
    ## for EBC006_s1 we selected markers on the right (droite) leg: four at the cuisse and four at the jambe
    
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
    
    
    print(f'CD_Marker1:\n{CD_Marker1}\n shape: {CD_Marker1.shape}')
    
    
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
