import pywt
import sys
import argparse
from class_emg_ebc_plots import Processing_EMG
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

def plot_together(list_data, list_labels, list_sr, file_number, asia_nl):
    
    fig, ax = plt.subplots(nrows=4, ncols=2, sharey=True)
    fig.canvas.mpl_connect('key_press_event', on_press)
    
    dt = list_data[0]
    la = list_labels[0]
    
    time = dt[0]
    time_label = la[0]
    
    id01 = (len(time)/2 - (list_sr[0]*2.5)).astype(int)
    id02 = (id01 + (list_sr[0]*5)).astype(int)        
    
    cont=0
    for signal, label  in zip(dt[1:], la[1:]):
        if label == 'Noraxon Ultium.EMG 8, uV':
            label = 'VLO RT, uV'
        elif label == 'RECTUS FEM. RT, uV':
            label = 'VMO RT, uV'
        elif label == 'RECTUS FEM. LT, uV':
            label = 'VMO LT, uV'
        else:
            pass
        ax[cont][0].plot(time, signal, label=label)
        ax[cont][0].set_xlim([time[id01],time[id02]])
        ax[cont][0].legend(loc='lower right')
        cont+=1
    
    ##############################    
    dt = list_data[1]
    la = list_labels[1]
    
    time = dt[0]
    label_time = la[0]
    
    id01 = (len(time)/2 - (list_sr[0]*2.5)).astype(int)
    id02 = (id01 + (list_sr[0]*5)).astype(int)        
    
    cont=0
    for signal, label  in zip(dt[1:], la[1:]):
        if label == 'Noraxon Ultium.EMG 8, uV':
            label = 'VLO RT, uV'
        elif label == 'RECTUS FEM. RT, uV':
            label = 'VMO RT, uV'
        elif label == 'RECTUS FEM. LT, uV':
            label = 'VMO LT, uV'
        else:
            pass
        ax[cont][1].plot(time, signal, label=label)
        ax[cont][1].set_xlim([time[id01],time[id02]])
        ax[cont][1].legend(loc='lower right')
        cont+=1

    #######
    
    ax[0][0].set_ylim([-300,300])
    
    ax[0][0].set_title('day 01')
    ax[0][1].set_title('day 07')
    ax[cont-1][0].set_xlabel(time_label+' [s]')
    ax[cont-1][1].set_xlabel(time_label+' [s]') 
    
    fig.suptitle('P:'+file_number+' ASIA:'+asia_nl[0]+' NL:'+asia_nl[1], fontsize=16)  
    
    
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
    
                        
    list_files_names = {'003':['EBC003-J1.mat','EBC003-J14.mat'],
                        '004':['EBC004-S1.mat','EBC004  J13.mat'],
                        '006':['EBC 006 S1 E3.mat','EBC006 s15 e3.mat'],
                        '018':['EBC018_S3_E3.mat','EBC018_S12_e3.mat'],
                        '024':['EBC24-S4-E3.mat','EBC024S13e3.mat'],
                        '030':['EBC030_S1_E3.mat','EBC30_S14_E3.mat'],
                        '031':['EBC031_s2_e3.mat','EBC031_s14_e3.mat'],
                        '032':['EBC032_s1_e3.mat','EBC032S14e3.mat'],
                        '033':['EBC033S3e3.mat','EBC033S14e3.mat'],
                        '037':['EBC037_S2_E3.mat','EBC037S14E3.mat'],
                        '042':['EB042S730MIN.mat'],
                        '045':['EBC45-S2-25min.mat','EBC045S14e3.mat']}
    
    
    list_asia_nl = {'003':['C','C5'],
                    '004':['B','C4'],
                    '006':['A','L2'],
                    '018':['A','C2'],
                    '024':['A','T4'],
                    '030':['A','T10'],
                    '031':['B','C4'],
                    '032':['A','C3'],
                    '033':['B','T12'],
                    '037':['A','C3'],
                    '042':['A','T10'],
                    '045':['A','C6'],
                    }
    
    print(f'Dir name: {path}')
    # print(f'Selected files: {list_files_names[file_number]}')
    
    files = list_files_names[file_number]
    asia_nl = list_asia_nl[file_number]
   
        
    ## EMG early bed cycling (EBC) from .mat file (matlab file) generated by Noraxon software.
    ## Each file has several channels.
    ## We read the data in the class 'Processing_EMG'.
    ## We create an object (obj_emg) for a selected file.
    list_days=['1','14']
    
    list_objs = []
    ## read emg-signals from all recordings of a selected session
    for filename, day_number in zip(files, list_days):
        print(f'filename {filename}')
        list_objs.append(Processing_EMG(path,filename,day_number))
    ## plot emg-signals selected muscle
    list_emg_times=[]
    list_emg_signals=[]
    list_emg_names=[]
    
    list_data=[[],[]]
    list_labels=[[],[]]
    list_sr=[]
    
    i=0
    for obj_emg in list_objs:
        # print(f'obj emg: {obj_emg}')
        list_data[i], list_labels[i] = obj_emg.plotSignals(file_number)
        list_sr.append(obj_emg.getSamplingRate())
        i=+1
        # emg_time, emg_signal, emg_name = obj_emg.getSignal(num_muscle)
        # emg_time, emg_signal, emg_name = obj_emg.getSignal(muscle)
        
        # list_emg_times.append(emg_time)
        # list_emg_signals.append(emg_signal)
        # list_emg_names.append(emg_name)
    # print(list_emg_names)
    # plotEMG(list_emg_times, list_emg_signals, list_emg_names, session, file_number)
        
    # wavelet_ecg(list_emg_signals[2])

    print('sampling: ', list_sr)
    
    plot_together(list_data, list_labels, list_sr, file_number, asia_nl)

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
