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
    parser.add_argument('-d', '--dir_name', type = str, help = "Select directory, for example: EBC032/EBC033/")
    parser.add_argument('-f', '--file_number', type = str, help = "Select file number, for example: 040")
    
    
    
    args = parser.parse_args()

    path=args.dir_name
    file_number=args.file_number
    
                        
    list_files_names = {'001':['EBC-PATIENT 1 S7.mat'],
                        '002':['EBC-PATIENT 2.mat','EBC-PATIENT 2-1.mat'],
                        '003':['EBC003-J1.mat','EBC003-S7.1.mat','EBC003-S7.2.mat','EBC003-J14.mat'],
                        '004':['EBC004-S1.mat','EBC004 S6.mat','EBC004  J13.mat'],
                        '006':['EBC006 S1 E1.mat','EBC006 S1 E2.mat','EBC 006 S1 E3.mat','EBC 006 S8 E1.mat','EBC 006 S8 E2.mat','EBC 006 S8 E3.mat','EBC006 s15 E1.mat','EBC006 s15 E2.mat','EBC006 s15 e3.mat'],
                        '018':['EBC018_S2_E2.mat','EBC018-s3-e1.mat','EBC018_S3_E3.mat','ebc018_S8_e1.mat','EBC018_s8_e1-2.mat','EBC 018_s8_e2.mat','EBC018_S8_E3.mat','EBC018_S12_e1.mat','EBC018_S12_E2.mat','EBC018_s12_e2_.mat','EBC018_s12_E2-3.mat','EBC018_S12_e3.mat'],
                        '024':['EBC24-S4_BASELINE.mat','EBC024-S4-E1.mat','EBC024-S4-E2.mat','EBC24-S4-E3.mat','EBC24_S9_baseline1.mat','EBC24-S9-e2.mat','EBC24_s9_E3.mat','EBC24-S4-BASELINE2.mat','EBC24_S9_baseline 2.mat','EBC24-s9_e1.mat','EBC024S13e1.mat','EBC024S13e2.mat','EBC024S13e3.mat'],
                        '030':['EBC030_S1_BASELINE1.mat','EBC030_S1_E1.mat','EBC030_S1_E2.mat','EBC030_S1_E3.mat','EBC030_S1_BASELINE2.mat','EBC030_S7_BASELINE1.mat','EBC030_S7_E1.mat','EBC030_S7_E2.mat','EBC030_S7_E3.mat','EBC030_S7_BASELINE2.mat','EBC030_S14_BASELINE.mat','EBC030_S14_E1.mat','EBC030_s14_e2.mat','EBC30_S14_E3.mat','EBC030_S14_BASELINE2.mat'],
                        '031':['EBC031_s2_baseline2.mat','EBC031_s2_e1.mat','EBC031_s2_e2.mat','EBC031_s2_e3.mat','EBC031S7e1.mat','EBC031_s7e2.mat','EBC031S7e3.mat','EBC031_S14_BASELINE1.mat','EBC031_S14_E1.mat','EBC031S14e2.mat','EBC031_s14_e3.mat','EBC031_s14_baseline2.mat'],
                        '032':['EBC032_s1_baseline1.mat','EBC032_S1_e1.mat','EBC032_S1_E2.mat','EBC032_s1_e3.mat','EBC032_s1_baseline2.mat','EBC032S7-Baseline1.mat','EBC032S7e1.mat','EBC032S7e2.mat','EBC032S7e3.mat','EBC032S7-Baseline2.mat','EBC032S14e1.mat','EBC032S14e2.mat','EBC032S14e3.mat','EBC032S14-baseline2.mat'],
                        '033':['EBC033S3-Baseline.mat','EBC033S3e1.mat','EBC033S3e2.mat','EBC033S3e3.mat','EBC033_S7_BASELINE1.mat','EBC033_S7_e1.mat','EBC033_S7_E2.mat','EBC033_S7_E3.mat','ebc033_s7_baseline2.mat','EBC033S14-Baseline1.mat','EBC033S14e1.mat','EBC033S14e2.mat','EBC033S14e3.mat'],
                        '037':['EBC037_S2_BASELINE2.mat','EBC037_S2_E1.mat','EBC037_S2_E2.mat','EBC037_S2_E3.mat','EBC037S7-Baseline1.mat','EBC037S7e1.mat','EBC037S7e2.mat','EBC037S7e3.mat','EBC037_S14_BASELINE1.mat','EBC037_S14_E1.mat','EBC037_S14_E2.mat','EBC037S14E3.mat','EBC037_S14_BASELINE2.mat'],
                        '042':['EBC042_S7_BASELINE.mat','EBC042S75MIN.mat','EBC042S715MIN.mat','EB042S730MIN.mat','EBC042S7BASELINE2.mat'],
                        '045':['EBC45-S2-Baseline.mat','EBC45-S2-1min.mat','EBC45-S2-5min.mat','EBC45-S2-15min.mat','EBC45-S2-25min.mat','EBC45-S2-30min.mat']}
    
    print(f'Dir name: {path}')
    # print(f'Selected files: {list_files_names[file_number]}')
    
    files = list_files_names[file_number]
   
        
    ## EMG early bed cycling (EBC) from .mat file (matlab file) generated by Noraxon software.
    ## Each file has several channels.
    ## We read the data in the class 'Processing_EMG'.
    ## We create an object (obj_emg) for a selected file.
    
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
        # print(f'obj emg: {obj_emg}')
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
