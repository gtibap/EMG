#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  emg_filtering.py
#  
from class_emg_filtering import Reading_EMG
from scipy.signal import savgol_filter

import argparse
import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd



def on_press(event):
        # print('press', event.key)
        sys.stdout.flush()
        
        if event.key == 'x':
            plt.close('all')
        else:
            pass
        return 0

        
def plotSignalsSeq(ax, obj_emg, signal, arr_time_max, arr_time_min, flag_left_leg):
        
        # cont=0
        # for ch, ch_n, id_emg in zip(self.channelsFiltered, self.channelsNames, ids_emg):
        ch_fil = obj_emg.getChannelsFiltered()
        ch_env = obj_emg.getChannelsEnveloped()
        ch_name = obj_emg.getChannelsNames()
        ch_time = obj_emg.getChannelTime()
        sampling_rate = obj_emg.getSamplingRate()
        
        ax.plot(ch_time, ch_fil[signal], label=ch_name[signal])
        ax.plot(ch_time, ch_env[signal])
        ax.legend()
        
        ## left leg
        if flag_left_leg:
            for x_val in arr_time_max:
                p_f = ax.axvline(x = ch_time[0] + x_val, color = 'tab:green', label='flexion')
            for x_val in arr_time_min:
                p_e = ax.axvline(x = ch_time[0] + x_val, color = 'tab:purple', label='extension')
        ## right leg
        else:
            for x_val in arr_time_max:
                p_e = ax.axvline(x = ch_time[0] + x_val, color = 'tab:purple', label='extension')
            for x_val in arr_time_min:
                p_f = ax.axvline(x = ch_time[0] + x_val, color = 'tab:green', label='flexion')
         
        ## select 5 seconds range of data at the middle of the recordings
        id01 = (len(ch_time)/2 - (sampling_rate*2.5)).astype(int)
        id02 = (id01 + (sampling_rate*5)).astype(int)  
        
        ax.set_xlim([ch_time[id01],ch_time[id02]])
        ax.set_ylim([-100,100])
        # ax[0].set_title(self.filename)
        # ax.set_xlabel('time [s]')
        
        ## saving plot png file
        # fig.suptitle(f'{self.filename}\n{title_emg}')
        # fig.suptitle(f'P-{patient_number} session {session_number}')
        # fig.suptitle(f'P-{patient_number}')
        # plt.savefig(f'../docs/figures/feb19_2024/EBC031_session_B.png', bbox_inches='tight')
        
        return 0
    

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


def smooth_filter(arr):
    arr[:,0]=savgol_filter(arr[:,0], window_length=60, polyorder=1, mode='mirror')
    arr[:,1]=savgol_filter(arr[:,1], window_length=60, polyorder=1, mode='mirror')
    arr[:,2]=savgol_filter(arr[:,2], window_length=60, polyorder=1, mode='mirror')
    return arr


def kinematics(path, record_number,):
    
    list_filenames=['Take 2022-07-04 10.23.53 AM.csv', 'Take 2022-07-04 10.37.36 AM.csv', 'Take 2022-07-04 10.52.59 AM.csv']
    
    ## four groups of markers
    ## order: CG, JG, CD, JD
    ## JD columns, marker1:(EB:EB+3), marker2:(EE:EE+3), marker4:(EH:EH+3), Unlabeled_377:(EK:EK+3)
    ##
    list_columns=[ [], [], [[],[],[],[131,134,137,140]]]
    
    ## calculate coordinates middle point of the markers for each body part
    ## first: open files
    filename = path+list_filenames[record_number]
    
    print(f'reading markers file... ', end='')
    try:
        df = pd.read_csv(filename, header=5)
    except ValueError:
            print(f'error. Problem reading the file {filename}.')
            return 0
    print(f'done.')
    
    # print(f'data markers:\n{df}')
    
    ## column indexes read coordinates markers
    list_ids_x = list_columns[record_number][3]
    print(f'list_ids_x: {list_ids_x}')
    
    print('\nMissing values before interpolation:')
    for i, id_x in enumerate(list_ids_x):
        print(f'Marker {i}: {df.iloc[:,id_x].isnull().sum()}')
        print(f'{df.iloc[:,id_x]}')
    print('\n')
    
    ## filling missing data
    for id_x in list_ids_x:
        df.iloc[:,id_x+0].interpolate(method="cubicspline", inplace=True, limit_direction='both')
        df.iloc[:,id_x+1].interpolate(method="cubicspline", inplace=True, limit_direction='both')
        df.iloc[:,id_x+2].interpolate(method="cubicspline", inplace=True, limit_direction='both')

    # fig, ax = plt.subplots(nrows=4,ncols=1)
    # fig.canvas.mpl_connect('key_press_event', on_press)
    # col=2

    ## smoothing each component (x,y,z) of each marker
    markers_arr = np.empty([len(list_ids_x), len(df), 3])
    markers_sum = np.zeros([len(df), 3])
    
    for i, id_x in enumerate(list_ids_x):
        markers_arr[i] = df.iloc[:,id_x:id_x+3].to_numpy()
        # ax[i].plot(markers_arr[i,:,col], label='original')
        markers_arr[i] = smooth_filter(markers_arr[i])
        # ax[i].plot(markers_arr[i,:,col], label='smooth')
        # ax[i].legend()
        markers_sum += markers_arr[i]
    
    # print(f'markers_arr:\n{markers_arr}')
    
    marker_center = markers_sum / len(list_ids_x)
    
    ## finding maximums and minimums (positive and negative picks) of the X component of the marker_center
    max_list, min_list = max_and_min(marker_center[:,0])
    print(f'max and min:\n{max_list},\n{min_list}')
    
    sample_rate_tracking = 120 ## samples per second (Hz)
    ## time in seconds
    t_delay=0.0
    arr_time_max = np.array(max_list)/sample_rate_tracking - t_delay
    arr_time_min = np.array(min_list)/sample_rate_tracking - t_delay
    
    # for i in np.arange(3):
        # ax[i].plot(marker_center[:,i],)
    # plt.show()
    
    return arr_time_max, arr_time_min



def main(args):
    
    # Initialize parser
    parser = argparse.ArgumentParser(description = 'EMG filtering')

    # Adding optional argument
    parser.add_argument('-d', '--dir_name', type = str, help = "Select directory, for example: EBC031/session_b/")
    parser.add_argument('-p', '--patient_number', type = str, help = "Select file number, for example: 033")
    
    parser.add_argument('-f', '--file_number', type = str, help = "Select file number, for example: 0")
    
    parser.add_argument('-session', '--session', type = str, help = "Select session, for example: a, b, or c")
    
    parser.add_argument('-s', '--signal_number', type = str, help = "Select signal number, for example: 0")
    
    
    
    args = parser.parse_args()

    path=args.dir_name
    patient_number=args.patient_number
    file_number=int(args.file_number)
    session=args.session
    signal_number=int(args.signal_number)
    
    print(f'path and files: {path}, {patient_number}, {session}, {file_number}')
    
    path_emg = path+f'session_{session}/emg/'
    path_mov = path+f'session_{session}/mov/'
    
    # ################
    # ## kinematics
    # take_number=2
    # arr_max, arr_min = kinematics(path_mov, file_number)
    # print(f'arr_max: {arr_max}\narr_min: {arr_min}')
    
    # return 0
    
    # ## kinematics
    # ################
    
    list_files_coord = {
                        '031':['Take 2022-07-04 10.23.53 AM.csv', 'Take 2022-07-04 10.37.36 AM.csv', 'Take 2022-07-04 10.52.59 AM.csv'],
    }
    
    # order: CG=0, JG=1, CD=2, JD=3
    list_limb_select = {
                        '031':[3,3,3],
    }
    
    list_flag_leg_all = {
                        '031':[False,False,False]
    } 
        
    ## four groups of markers for each recording [usually three: 5min (e1), 15min (e2), 30min (e3)]
    ## order: CG, JG, CD, JD
    ## '031' JD columns, marker1:(EB:EB+3), marker2:(EE:EE+3), marker4:(EH:EH+3), Unlabeled_377:(EK:EK+3)
    ##
    list_id_columns = {
                        '031':[[[],[],[],[122,125,128,131]], [[],[],[],[131,134,137,140]], [[],[],[],[131,134,137,140]] ],
    }
    
    
        
    list_files_names = {
                        '031':['EBC031S7e1.mat', 'EBC031_s7e2.mat', 'EBC031S7e3.mat'],

                        }
    
    ## ids of the eight required channels: muscular signals EMG without the insole signals
    list_ids_channels = {
                         '031':[[9,16],[9,16],[9,16]],

                        }
    
    ## sorting plots to present each lead in the same place                    
    list_emg_sorted = {
                       '031':[[7,2,4,1,6,5,0,3]]*4,
                       
                        }
                        
    list_emg_titles = {
                       '031':'B - C4 (discharge)  -> D - C6 (12 months)',
                       
                       }
    
    list_session_names={0:'a',
                        1:'b',
                        2:'c',
                        }
                        
    list_activity_emg={
                       '031':[[],[],[],[]],
                       
                        }
    
    list_selected_channels={
                        '031':['VL RT, uV'],
                        }
    
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT.GASTRO LT, uV', 'LAT.GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']
    
    #################
    ### kinematics
    
    files_list_mov = list_files_coord[patient_number]
    list_columns = list_id_columns[patient_number]
    list_limb = list_limb_select[patient_number]
    list_flag_leg = list_flag_leg_all[patient_number]
    # flag_left_leg = False
    
    ### kinematics
    #################
    
    # print(f'filename main: {filename}')
    
    ##################
    ## emg
                        
    files_list_emg = list_files_names[patient_number]
    ids_channels_emg = list_ids_channels[patient_number]
    ids_emg_sorted = list_emg_sorted[patient_number]
    title_emg = list_emg_titles[patient_number]
    activity_emg = list_activity_emg[patient_number]
    list_ch_cycle = list_selected_channels[patient_number]
    
    filename = files_list_emg[file_number]
    file_channels = ids_channels_emg[file_number]
    ids_emg_plot = ids_emg_sorted[file_number]
    session_name = list_session_names[file_number]
    act_emg = activity_emg[file_number]
    name_ch_cycle = list_ch_cycle[0]
    
    
    
    # print(f'files: {files_list}')
    # print(f'channels: {ids_channels}')
    # print(f'selected file: {filename}, channels: {file_channels}')
    
    ##############################################################################
    ## canvas for the visualization plots EMG and vertical lines indicating flexion and extension
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(8, 5), sharex=True, sharey=True, squeeze=False)
    fig.canvas.mpl_connect('key_press_event', on_press)

    fig.suptitle(f'P-{patient_number} session B\n(purple: extension, green: flexion)')
    ax = ax.reshape(-1)
    ax[-1].set_xlabel('time [s]')
    ax[0].set_ylabel('E1 (5 min)')
    ax[1].set_ylabel('E2 (15 min)')
    ax[2].set_ylabel('E3 (30 min)')
    ## canvas for the visualization plots EMG and vertical lines indicating flexion and extension
    ##############################################################################
    ##############################################################################
    # ## canvas for the visualization flexion and extension
    fig01, ax01 = plt.subplots(nrows=3,ncols=1, figsize=(7,3.5), sharex=True, sharey=True)
    fig01.canvas.mpl_connect('key_press_event', on_press)
    ax01 = ax01.reshape(-1)
    
    fig01.suptitle(f'P-{patient_number} session B\n{name_ch_cycle}')
    ax01[-1].set_xlabel('circular clock (h)')
    ax01[0].set_ylabel('E1 (5 min)')
    ax01[1].set_ylabel('E2 (15 min)')
    ax01[2].set_ylabel('E3 (30 min)')
    # ## canvas for the visualization flexion and extension
    ##############################################################################
    
    
    obj_emg = [[]]*len(files_list_emg)

    i=0
    for filename_emg, file_channels_emg in zip(files_list_emg, ids_channels_emg):
        try:
            print(f'reading file: {filename_emg}, {file_channels_emg}... ', end='')
            # create object class
            # list_objs[i] = Activity_Measurements()
            # list_objs[i].openFile(path, filename)
            obj_emg[i] = Reading_EMG(path_emg, filename_emg, file_channels_emg)
            ch_names = obj_emg[i].getChannelsNames()
            print(f'names: {ch_names}')
            
            obj_emg[i].filteringSignals()
            obj_emg[i].envelopeFilter()
            
            ##################
            ## kinematics
            # list_ids_x = list_columns[record_number][3]
            filename_mov = files_list_mov[i]
            limb = list_limb[i]
            list_ids_x = list_columns[i][limb]
            flag_left_leg = list_flag_leg[i]
            
            obj_emg[i].kinematics(path_mov+filename_mov, list_ids_x,)
            arr_time_extension = obj_emg[i].getExtensionTimeList()
            arr_time_flexion = obj_emg[i].getFlexionTimeList()
            
            print(f'extension and flexion:\n{arr_time_extension}\n{arr_time_flexion}')
            # filename = path_mov+list_filenames[file_number]
            
            ## kinematics
            ##################
            
            # obj_emg[i].plotEnvelopedSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
            
            plotSignalsSeq(ax[i], obj_emg[i], signal_number, arr_time_extension, arr_time_flexion, flag_left_leg)
            # plt.savefig(f'../docs/figures/feb19_2024/EBC031_session_B.png', bbox_inches='tight')
            
            obj_emg[i].plotFlexionExtension(ax01[i], arr_time_extension, arr_time_flexion, name_ch_cycle)
            # fig01.savefig(f'../docs/figures/feb19_2024/EBC031_session_B_cycle.png', bbox_inches='tight')
            # plotFlexionExtension(ax01[i], obj_emg[i], signal_number, arr_time_extension, arr_time_flexion)
            
            # obj_emg[i].plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
            
            
            
            print(f'done.')
            
        except ValueError:
            print(f'Problem reading the file {filename}.')
        i+=1
    
    # obj_emg = Reading_EMG(path, filename, file_channels)
    # ch_names = obj_emg.getChannelsNames()
    # print(f'names: {ch_names}')
    
    # obj_emg.plotSignals()
    # obj_emg.plotSelectedSignal(signal_number)
    
    # obj_emg.filteringSignals()
    # obj_emg.plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
    
    # ## open files
    # list_objs = []
    # ## read emg-signals from all recordings of a selected session
    # for num_rec, filename in enumerate(files):
        # print(f'filename: {filename}')
        # list_objs.append(Reading_EMG(path,filename, list_ids_channels[file_number][0]))
    
    # list_objs[0].plotSignals()
    
    plt.ion()
    plt.show(block=True)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
