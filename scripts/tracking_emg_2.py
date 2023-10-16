#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tracking_emg.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy.signal import savgol_filter


def test_func(x, a, b, theta, offset):
    return a * np.sin(b * x + theta) + offset

def delta_mov(df, cg_rb_position, jg_rb_position):

    delta=[]
    # delta=[[],[],[]]
    # pos_cg=[[],[],[]]
    # pos_jg=[[],[],[]]
    # i=0
    for cg,jg in zip(cg_rb_position, jg_rb_position):
        # print(f'i,cg,jg: {i}, {cg}, {jg}')
        values_cg = df.iloc[:,cg].to_numpy()
        values_jg = df.iloc[:,jg].to_numpy()
        
        print(f'some nan indices: {np.isnan(values_cg).any()}, {np.isnan(values_jg).any()}')
        # print(f'values cuisse:\n{values_cg}')
        # print(f'values jambe:\n{values_jg}')
        
        # pos_cg[i]=values_cg
        # pos_jg[i]=values_jg
        # delta[i] = values_jg - values_cg
        delta.append(values_jg - values_cg) 
        # i=i+1
        
    norm_delta=np.linalg.norm(delta, axis=0)
    
    ## smoothing 
    yhat = savgol_filter(norm_delta, 30, 3) # window size 51, polynomial order 3

    # return norm_delta, yhat
    return  norm_delta, yhat


def main(args):
    
    filename = '../data/motive_tracking/tracking_061_s9/EBC061-S9_5MIN_tracking.csv'
    
    ## reading csv file. Header includes: Frame, Time, ... 
    df = pd.read_csv(filename, header=5)
    # print(f'{df.columns}')
    # print(f'{df}')
    # print(f'{df.iloc[:,6].tolist()}')
    
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
    
    
    
    
    
    
    
    
    
    
    ids=list(range(2,(23+1)*4,4))
    ## id each component of the Cuisse Gauche (cg), Rigid Body (rb)
    cg_rb_rotation= list(range(ids[0],ids[0]+4))
    cg_rb_position= list(range(ids[1],ids[1]+3))
    cg_rb1_position=list(range(ids[2],ids[2]+3))
    cg_rb2_position=list(range(ids[3],ids[3]+3))
    cg_rb3_position=list(range(ids[4],ids[4]+3))
    cg_rb4_position=list(range(ids[5],ids[5]+3))
    ## id each component of the Jambe Gauche (jg), Rigid Body (rb)
    jg_rb_rotation= list(range(ids[6],ids[6]+4))
    jg_rb_position= list(range(ids[7],ids[7]+3))
    jg_rb1_position=list(range(ids[8],ids[8]+3))
    jg_rb2_position=list(range(ids[9],ids[9]+3))
    jg_rb3_position=list(range(ids[10],ids[10]+3))
    jg_rb4_position=list(range(ids[11],ids[11]+3))
    ## id each component of the Cuisse Droite (cd), Rigid Body (rb)
    cd_rb_rotation= list(range(ids[12],ids[12]+3))
    cd_rb_position= list(range(ids[13],ids[13]+3))
    cd_rb1_position=list(range(ids[14],ids[14]+3))
    cd_rb2_position=list(range(ids[15],ids[15]+3))
    cd_rb3_position=list(range(ids[16],ids[16]+3))
    cd_rb4_position=list(range(ids[17],ids[17]+3))
    ## id each component of the Jambe Droite (jd), Rigid Body (rb)
    jd_rb_rotation= list(range(ids[18],ids[18]+3))
    jd_rb_position= list(range(ids[19],ids[19]+3))
    jd_rb1_position=list(range(ids[20],ids[20]+3))
    jd_rb2_position=list(range(ids[21],ids[21]+3))
    jd_rb3_position=list(range(ids[22],ids[22]+3))
    jd_rb4_position=list(range(ids[23],ids[23]+3))
    
    
    # pos_cg=[[],[],[]]
    # pos_jg=[[],[],[]]
    # delta=[[],[],[]]
    
    # print(f'ranges: {cg_rb_position}, {jg_rb_position}')
    # print(f'jambe gauche')
    # norm_delta_g, yhat_g = delta_mov(df, cg_rb_position, jg_rb_position)
    # print(f'droite')
    # norm_delta_d, yhat_d, norm_sub = delta_mov(df, cd_rb_position, jd_rb_position)
    # norm_delta=np.linalg.norm(norm_delta_d, axis=0)
    # norm_yhat=np.linalg.norm(yhat_d, axis=0)
    
    print(f'\nGauche\n')
   
    norm_g, smooth_g = delta_mov(df, cd_rb4_position, jd_rb1_position)
    norm_d, smooth_d = delta_mov(df, cd_rb1_position, jd_rb4_position)
    # norm_delta=np.linalg.norm(norm_delta_d, axis=0)
    # norm_yhat=np.linalg.norm(yhat_d, axis=0)
    
    # x_data=time
    # y_data=norm_delta
    
    # ampl = 0.01
    # freq = 1*2*3.1415
    # theta = 0
    # offset = 0.28
    
    # print(f'xdata:\n{x_data}')
    # print(f'ydata:\n{y_data}')
    
    # params, params_covariance = optimize.curve_fit(test_func, x_data, y_data,
                                               # p0=[ampl, freq, theta, offset])
    # print(f'params: {params}')
    
    
        
    # y_fitted = test_func(x_data, params[0], params[1], params[2], params[3])
    # print(f'fitted_fuc:\n{y_fitted}')
    
    
    fig, ax = plt.subplots()
    # ax.plot(time,norm_delta_d[0])
    # ax.plot(time,norm_delta_d[1])
    # ax.plot(time,norm_delta_d[2])
    ax.plot(time,norm_g, label='gauche')
    ax.plot(time,norm_d, label='droite')
    
    # ax.plot(time,yhat_d[0])
    # ax.plot(time,yhat_d[1])
    # ax.plot(time,yhat_d[2])
    # ax.plot(time,smooth_g, label='gauche_hat')
    # ax.plot(time,smooth_d, label='droite_hat')
    
    
    # ax.plot(time,norm_sub+0.95, label='c')
    
    
    
    # ax.plot(time,delta[0])
    # ax.plot(time,delta[1])
    # ax.plot(time,delta[2])
    
    # ax.plot(time,norm_delta_g, label='g')
    # ax.plot(time, yhat_g, label='sg')
    # ax.plot(time,norm_delta_d, label='d')
    # ax.plot(time, yhat_d, label='sd')
    
    
    ax.set_xlabel(f'time [s]')
    ax.legend()
    plt.show()
    
    
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
