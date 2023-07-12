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
    
    path='../data/emg_ebc/'
    
    args = parser.parse_args()

    file_number=args.file_number

    file1 = 'ebc_'+file_number+'_s01_e3.mat'
    file2 = 'ebc_'+file_number+'_s14_e3.mat'

    files=[file1, file2] 
        
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