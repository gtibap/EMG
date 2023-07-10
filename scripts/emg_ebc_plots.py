import pywt
import sys
import argparse
from class_emg_ebc import Processing_EMG
import numpy as np
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt

def wavelet_ecg(data):
    # waveletname = 'sym8'
    waveletname = 'Haar'
    nlevel=10
    fig, axarr = plt.subplots(nrows=nlevel, ncols=1)
    for ii in np.arange(nlevel):
        (data, coeff_d) = pywt.dwt(data, waveletname)
        axarr[ii].plot(data, 'r')
    
    return 0

def on_press(event):
    # print('press', event.key)
    sys.stdout.flush()
    
    if event.key == 'x':
        plt.close('all')
    else:
        pass
            
    return 0

def plotEMG(emg_times, emg_signals, emg_names, num_session, file_number):
    num_signals = len(emg_signals)
    ## we exclude Time channel and Swich channel (first and last channels)
    fig, ax = plt.subplots(nrows=num_signals, ncols=1, sharex=True, sharey=True)
    fig.canvas.mpl_connect('key_press_event', on_press)
    cont=0
    for time, signal, name in zip(emg_times, emg_signals, emg_names):
        ax[cont].plot(time, signal, label=name)
        ax[cont].legend()
        cont+=1
    
    ax[0].set_ylim([-500,500])
    ax[0].set_title('EBC '+ file_number+' session '+str(num_session))
    ax[cont-1].set_xlabel('Time [s]')
    ax[0].set_ylabel('b1')
    ax[1].set_ylabel('e1')
    ax[2].set_ylabel('e2')
    ax[3].set_ylabel('e3')
    ax[4].set_ylabel('b2')
    
    return 0

def main():
    
    # Initialize parser
    parser = argparse.ArgumentParser(description = 'EMG visualization')

    # Adding optional argument
    parser.add_argument('-f', '--file_number', type = str, help = "Select file number, for example: 040")
    # parser.add_argument('-s', '--session', type = int, help = "Select one SESSION among: 1, 7, and 14")
    # parser.add_argument('-r','--recording', type = str, help='Select one RECORDING among: b1, e1, e2, e3, b2 (baseline1, 2min-, 15min-, and 30min-pedaling, baseline2)')
    # parser.add_argument('-m','--muscle', type = str, help='Select one MUSCLE among: grt, glt, tbart, tbalt, vlrt, vllt, vmrt, vmlt')

    path='../data/emg_ebc/'
    # path='../data/emg_noraxon/matlab/'
    # path='../data/ebc033/'
    # path='../data/ebc036/'
    ## Read arguments from command line
    args = parser.parse_args()

    # session = int(args[1]) ## [1,7,14]
    # num_file = int(args[2]) ## [0,1,2,3,4]-> (baseline_start, e1,e2,e2, baseline_end)
    
    # file_number=['040']
    # session = args.session

    # if  session == 1:
        # sn ='_s01_'
    # elif session == 7:
        # sn ='_s07_'
    # elif session == 14:
        # sn ='_s14_'
    # else:
        # print(f'The {session} session was not found.')
        # return 0
        # path='../data/emg_noraxon/matlab/s01/'
        # path='../data/ebc033/'
        # path='../data/ebc036/'
        # files=['EBC040S1-Baseline1.mat','EBC040S1e1.mat','EBC040S1e2.mat','EBC040S1e3.mat', 'EBC040S1-Baseline2.mat']

    file_number=args.file_number

    file1 = 'ebc_'+file_number+'_s01_e3.mat'
    file2 = 'ebc_'+file_number+'_s14_e3.mat'

    # f_b1 = 'ebc_'+file_number+sn+'b1.mat'
    # f_e1 = 'ebc_'+file_number+sn+'e1.mat'
    # f_e2 = 'ebc_'+file_number+sn+'e2.mat'
    # f_e3 = 'ebc_'+file_number+sn+'e3.mat'
    # f_b2 = 'ebc_'+file_number+sn+'b2.mat'
    
    files=[file1, file2] 
        
    # if session == 14 and file_number=='040':
        # path='../data/emg_noraxon/matlab/s14/'
        # files=['EBC_Bed_cycling-s14-Baseline.mat', 'EBC040_Bed_cycling-S14.mat','EBC040_Bed_cycling-s14-5min.mat','EBC040-_Bed_cycling_-s14-15m.mat','EBC040_Bed_cycling-s14-30min.mat']
        # files=['EBC_Bed_cycling-s14-Baseline.mat','EBC040_Bed_cycling-S14.mat','EBC040_Bed_cycling-s14-5min.mat','EBC040-_Bed_cycling_-s14-15m.mat','EBC040_Bed_cycling-s14-30min.mat']
        
    # else:
        # pass
        # path='../data/ebc036/'
        # files=['EBC036_S14_BASELINE1.mat','EBC036_S14_E1.mat','EBC036_S14_E2.mat', 'EBC036_S14_E3.mat','EBC036_S14_BASELINE2.mat']
        # files=['ebc_036_S6_baseline.mat','ebc_036_s6_e1.mat','ebc_036_s7_e2.mat','ebc_036_s7_e3.mat','ebc_036_s7_baseline2.mat']
        # files=['ebc_036-Baseline1.mat','ebc_036S1e1.mat','ebc_036_S2_E2.mat','ebc_036_S2_e3.mat','ebc_036_S2_Baseline2.mat']
        
    # elif session == 7:
        # path='../data/emg_noraxon/matlab/s07/'
        # path='../data/ebc033/'
        # path='../data/ebc036/'
        # files=['EBC040_S7_BASELINE1.mat','EBC040_S7_E1.mat','EBC040_S7_E2.mat','EBC040_S7_E3.mat','EBC040_S7_BASELINE.mat']
        # f_b1 = 'ebc_'+file_number+'_s07_'+'b1.mat'
        # f_e1 = 'ebc_'+file_number+'_s07_'+'e1.mat'
        # f_e2 = 'ebc_'+file_number+'_s07_'+'e2.mat'
        # f_e3 = 'ebc_'+file_number+'_s07_'+'e3.mat'
        # f_b2 = 'ebc_'+file_number+'_s07_'+'b2.mat'
        
        # files=[f_b1, f_e1, f_e2, f_e3, f_b2] 
        
    # elif session == 14:
        # path='../data/emg_noraxon/matlab/s14/'
        # files=['EBC_Bed_cycling_Baseline.mat','EBC_Bed_cycling-s14-Baseline.mat','EBC040_Bed_cycling-S14.mat','EBC040_Bed_cycling-s14-5min.mat','EBC040-_Bed_cycling_-s14-15m.mat','EBC040_Bed_cycling-s14-30min.mat']
        # path='../data/ebc033/'
        # f_b1 = 'ebc_'+file_number+'_s14_'+'b1.mat'
        # f_e1 = 'ebc_'+file_number+'_s14_'+'e1.mat'
        # f_e2 = 'ebc_'+file_number+'_s14_'+'e2.mat'
        # f_e3 = 'ebc_'+file_number+'_s14_'+'e3.mat'
        # f_b2 = 'ebc_'+file_number+'_s14_'+'b2.mat'
        
        # files=[f_b1, f_e1, f_e2, f_e3, f_b2] 
    # else:
        # print(f'The {session} session was not found.')
        # return 0
        
    # recording = args.recording
    # if recording == 'b1':
        # num_file=0
    # elif recording == 'e1':
        # num_file=1
    # elif recording == 'e2':
        # num_file=2
    # elif recording == 'e3':
        # num_file=3
    # elif recording == 'b2':
        # num_file=4
    # else:
        # pass
        # print(f'The {recording} recording was not found.')
        # return 0
        
    # muscle = args.muscle
    # if muscle == 'grt':
        # num_muscle=5
    # elif muscle == 'glt':
        # num_muscle=2
    # elif muscle == 'tbart':
        # num_muscle=0
    # elif muscle == 'tbalt':
        # num_muscle=4
    # elif muscle == 'vlrt':
        # num_muscle=7
    # elif muscle == 'vllt':
        # num_muscle=1
    # elif muscle == 'vmrt':
        # num_muscle=3
    # elif muscle == 'vmlt':
        # num_muscle=6
    # else:
        # pass
        # print(f'The {muscle} muscle was not found.')
        # return 0
    
    ## EMG early bed cycling (EBC) from .mat file (matlab file) generated by Noraxon software.
    ## Each file has several channels.
    ## We read the data in the class 'Processing_EMG'.
    ## We create an object (obj_emg) for a selected file.
    
    ## if muscle was not selected, then signals all muscles are visualized from a especific recording (b1,e1,e2,e3,b2)
    # if muscle==None:
        # ## num_file selects among b1, e1, e2,e3, b2
        # obj_emg = Processing_EMG(path,files[num_file])
        # obj_emg.plotEMG()
    # else:
    # print(f'Plot of {muscle} muscle response during the five recordings of session {session}')
    list_objs = []
    ## read emg-signals from all recordings of a selected session
    for filename in files:
        print(f'filename {filename}')
        list_objs.append(Processing_EMG(path,filename))
    ## plot emg-signals selected muscle
    list_emg_times=[]
    list_emg_signals=[]
    list_emg_names=[]
    for obj_emg in list_objs:
        obj_emg.plotSignals()
        # emg_time, emg_signal, emg_name = obj_emg.getSignal(num_muscle)
        # emg_time, emg_signal, emg_name = obj_emg.getSignal(muscle)
        
        # list_emg_times.append(emg_time)
        # list_emg_signals.append(emg_signal)
        # list_emg_names.append(emg_name)
    # print(list_emg_names)
    # plotEMG(list_emg_times, list_emg_signals, list_emg_names, session, file_number)
        
    # wavelet_ecg(list_emg_signals[2])

    plt.ion()
    plt.show(block=True)
    
    # obj_emg.plotPowerSpectrum()   
    
    ## Window size in mili-seconds (ms).
    ## Recommended values for window_size: between 50 and 100 ms.

    # ## Smoothing RMS 
    # window_size=50 # ms
    # obj_emg.smoothingRMS(window_size)
    # obj_emg.plotEMG_smoothed()

    

    
    return 0

if __name__ == '__main__':
    sys.exit(main())
