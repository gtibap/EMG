# import kineticstoolkit.lab as ktk
from scipy.signal import savgol_filter
import scipy.io
from scipy import signal
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import ast
import os 

class Reading_EMG_Assis:

    def __init__(self, path, filename, channel_names):

        self.path=''
        self.filename=[]
        self.sampling_rate=1.0
        self.n_channels=1
        self.channels=[]
        self.channelsFiltered=[]
        self.channelsEnveloped={}
        self.channelsNames=[]
        self.arr_time_max=[]
        self.arr_time_min=[]
        self.df_EnvelopedSignals = pd.DataFrame()
        
        
        self.path = path
        self.filename = filename
        
        # self.day_number = day_number
    
        mat = scipy.io.loadmat(self.path+self.filename)
        # print(f'\n{self.filename}')
        # print(f'dictionary {mat}')
        header = mat['__header__']
        # print(f"Header:\n{header}")
        # print(f"Header type :\n{type(header)}")
        header = list(header.decode('utf-8'))
        # print(f"{''.join(header[-35:])}")

        ## recording date and time for plots headers
        self.date = "Recorded" + ''.join(header[-28:])

        # print(f"mat:\n{mat}")
        print(f"Channel Names:\n{mat['channelNames']}")
        # print(f"type ch: {type(mat['channelNames'])}")
        # print(f"len ch [0]: {len(mat['channelNames'][0])}")
        # print(f"ch [0][0]: {mat['channelNames'][0][0]}")
        # print(f"len (ch [0][0]): {len(mat['channelNames'][0][0])}")
        # print(f"ch [0][0][0]: {mat['channelNames'][0][0][0]}")

        ## finding id's of selected channels from all the recorded data
        ## scanning all the recorded channels
        self.channels_ids = {}

        for id in np.arange(len(mat['channelNames'][0])):
            ## comparing with selected channels
            print(f"{id}: {mat['channelNames'][0][id][0]}")
            if mat['channelNames'][0][id][0] in channel_names:
                # print(f"{id}: {mat['channelNames'][0][id][0]}")
                self.channels_ids[mat['channelNames'][0][id][0]]=id
            else:
                pass
        print(f"channels ids:\n{self.channels_ids}")
        
        self.sampling_rate = mat['samplingRate'][0,0]
        # print(f'sample rate: {self.sampling_rate}')

        ## reservate memory space for data channels
        self.n_channels = len(self.channels_ids)
        
        self.channels_data = {}

        ## channel 0 is the time array
        self.ch_time = mat['Data'][0, 0].flatten()
        self.ch_time_name = mat['channelNames'][0][0][0]
        # print(f'time ch: {self.ch_time[0]}, {self.ch_time[-1]}, {self.ch_time.shape}')
        
        self.df_EnvelopedSignals[self.ch_time_name] = self.ch_time
        
        for ch_name in self.channels_ids:
            # print(f"ch_name: {ch_name}")
            id = self.channels_ids[ch_name]
            self.channels_data[ch_name] = mat['Data'][0, id].flatten()
        
        


    def filterHighPass(self, emg, fc):
        sos = signal.butter(3, fc, btype='highpass', fs=self.sampling_rate, output='sos')
        filtered = signal.sosfiltfilt(sos, emg)
        # scipy.signal.sosfiltfilt
        return filtered

    def filterLowPass(self, emg, fc):
        sos = signal.butter(3, fc, btype='lowpass', fs=self.sampling_rate, output='sos')
        filtered = signal.sosfiltfilt(sos, emg)
        return filtered

    def filterBandPass(self, emg, fc1, fc2):
        sos = signal.butter(3, [fc1,fc2], btype='bandpass', fs=self.sampling_rate, output='sos')
        # filtered = signal.sosfilt(sos, emg)
        filtered = signal.sosfiltfilt(sos, emg)
        return filtered
    
    def filterBandStop(self, emg, fc1, fc2):
        sos = signal.butter(3, [fc1,fc2], btype='bandstop', fs=self.sampling_rate, output='sos')
        # filtered = signal.sosfilt(sos, emg)
        filtered = signal.sosfiltfilt(sos, emg)
        return filtered
        
        
    def filteringSignals_assis(self, channel_names):
        
        print(f"band pass and band stop filters")
        
        fc1p =  10 ## 20 Hz high pass filter to remove motion artifacts
        fc2p = 150 ## 500 Hz low pass filter 

        # line power 60 Hz
        fc1s =  55 ## low limit
        fc2s =  65 ## high limit

        self.channelsFiltered = {}
        for ch_name in channel_names:
            if (ch_name in self.channels_data) and not(ch_name.startswith('Insole')):
                # print(f'filtering {ch_n}')
                ch = self.channels_data[ch_name]
                ch = self.filterBandPass(ch, fc1p, fc2p)
                ch = self.filterBandStop(ch, fc1s, fc2s)
                self.channelsFiltered[ch_name] = ch
            else:
                pass
        
        return 0

    
    def envelopeFilter_assis(self):
        
        fc = 6 ## 6 Hz low pass filter

        self.channelsEnveloped = {}
        for ch_name in self.channelsFiltered:
            # print(f'filtering {ch_n}')
            ch = self.channelsFiltered[ch_name]
            ch = self.filterLowPass(np.absolute(ch), fc)
            self.channelsEnveloped[ch_name] = ch
        
        return 0
        
    

    ############################
    def plotEMGSession_assis_filtered(self, channels_names,):

        # print(f"channels names: {channels_names, len(channels_names)}")        
        num_rows = len(channels_names)//2
        # num_rows = math.ceil(len(channels_names)/2)
        fig, ax = plt.subplots(nrows=num_rows, ncols=2, figsize=(10, 7), sharex=True, squeeze=False)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        ax = ax.reshape(-1)
        
        ## plot EMG signals
        for ch_name, ax_single in zip(channels_names, ax):
            if (ch_name in self.channels_data) and not(ch_name.startswith('Insole')):
                # print(f"plot channels filtered and enveloped")
                ax_single.plot(self.ch_time, self.channelsFiltered[ch_name], label=ch_name, alpha=0.5)
                ax_single.plot(self.ch_time, self.channelsEnveloped[ch_name], alpha=1.0, lw=2.5)
                ax_single.legend()
            else:
                ## selected channel was not recorded
                ax_single.plot(self.ch_time, np.zeros(len(self.ch_time)), alpha=0.2)

            ## different y-scale for EMG and plantar pressure
            if ch_name.startswith('Insole'):
                ax_single.set_ylim([0,100])
            else:
                ax_single.set_ylim([-50,50])
                
        
        ## plot Insole curves (left and right) together
        ## in the last row of subplots
        in_r = 'Insole.Total RT, %'
        in_l = 'Insole.Total LT, %'
        if in_r in self.channels_data:
            ax[-2].plot(self.ch_time, self.channels_data[in_r],color='m',label='In_R, %', alpha=1.00)
            ax[-1].plot(self.ch_time, self.channels_data[in_r],color='m',label='In_R, %', alpha=0.25)
            ax[-2].legend()
            ax[-1].legend()
        else:
            pass
        if in_l in self.channels_data:
            ax[-2].plot(self.ch_time, self.channels_data[in_l],color='c',label='In_L, %', alpha=0.25)
            ax[-1].plot(self.ch_time, self.channels_data[in_l],color='c',label='In_L, %', alpha=1.00)
            ax[-2].legend()
            ax[-1].legend()
        else:
            pass
    
        ## select number of seconds range of data at the middle of the recordings
        val1 = 5.0
        val2 = val1*2.0
        id01 = (len(self.ch_time)/2 - (self.sampling_rate*val1)).astype(int)
        id02 = (id01 + (self.sampling_rate*val2)).astype(int)
        
        ## adjust x-scale for the first and for all the subplots (sharex=True)
        # ax[0].set_xlim([self.ch_time[id01],self.ch_time[id02]])

        ax[-2].set_xlabel(self.ch_time_name+' [s]')
        ax[-1].set_xlabel(self.ch_time_name+' [s]')
        
        filename = self.filename.split('.')[0]
        fig.suptitle(f'{filename}\n{self.date}')
        
        # ### save figure ####
        # path_out=f'../data/a_velo_assis/figures/figs/'
        # # checking if the directory
        # # exist or not. 
        # if not os.path.isdir(path_out): 
        #     # if directory is  
        #     # not present then create it. 
        #     os.makedirs(path_out) 
        
        # plt.savefig(f'{path_out}/{filename}.png', bbox_inches='tight')
        # ### save figure ####
        
        return 0
    ############################

       
    def on_press(self, event):
        # print('press', event.key)
        sys.stdout.flush()
        
        if event.key == 'x':
            plt.close('all')
        else:
            pass
        return 0
        
    def getChannelsNames(self):
        return self.channelsNames
        
    def getChannelsFiltered(self):
        return self.channelsFiltered
        
    def getChannelsEnveloped(self):
        return self.channelsEnveloped
    
    def getChannelTime(self):
        return self.ch_time
        
    def getSamplingRate(self):
        return self.sampling_rate

    ## we remove the last maximum because it could be incomplete
    def getExtensionTimeList(self):
        return self.arr_time_max[:-1]
    
    ## we remove the last minimum because it could be incomplete
    def getFlexionTimeList(self):
        return self.arr_time_min[:-1]
        
        
    
