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
        self.empty = False
        self.fig_emg = []
        self.ax_emg = []
        self.time_angles_markers = {}
        
        self.path = path
        self.filename = filename
        
        # self.day_number = day_number
        try:
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
            self.channelsNames = mat['channelNames']
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

        except:
            print(f'Problem reading the selected file: {self.filename}')
            self.empty = True


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
        
        fc1p =  20 ## 20 Hz high pass filter to remove motion artifacts
        fc2p = 150 ## 500 Hz low pass filter 

        print(f"{fc1p}-{fc2p} Hz bandpass")

        # line power 60 Hz
        fc1s =  55 ## low limit
        fc2s =  65 ## high limit

        print(f"60 Hz notch filter")

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
            self.df_EnvelopedSignals[ch_name] = ch
        
        return 0

    ############################
    def flexion_extension(self, signal_name):

        if ' LT,' in signal_name:
            arr_time_max = self.time_angles_markers['left_max']
            arr_time_min = self.time_angles_markers['left_min']
        elif ' RT,' in signal_name:
            arr_time_max = self.time_angles_markers['right_max']
            arr_time_min = self.time_angles_markers['right_min']
        else:
            print(f"Selected signal neither left nor right")
            return 0
        
        print(f"columns:\n{self.df_EnvelopedSignals.columns}")

        fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(7,3.5), sharex=True, sharey=True)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        # df_fef = pd.DataFrame()
        df_fle = pd.DataFrame()
        df_ext = pd.DataFrame()
        ## resampling all selected segments to have same number of samples
        len_ref = 4096
        
        x_range = np.linspace(0, 0.5, len_ref)
        df_fle['cycle']=x_range
        df_ext['cycle']=x_range + 0.5
        
        print(f"x_range, df_fle['cycle'], df_ext['cycle']:\n{x_range},\n{df_fle['cycle']}\n{df_ext['cycle']}")
        
        ## selecting first index; first index of min distance: starting with flexion
        if arr_time_min[0] < arr_time_max[0]:
            id0=0
        else:
            id0=1
        
        i=0
        
        ## we include all cycles but without the last one because it could be incomplete
        for val0, val1, val2 in zip(arr_time_min[0:-1], arr_time_max[id0:-1], arr_time_min[1:]):
            
            # t0 = self.ch_time[0] + val0  ## flexion
            # t1 = self.ch_time[0] + val1  ## extension
            # t2 = self.ch_time[0] + val2  ## flexion
            t0 = val0  ## flexion
            t1 = val1  ## extension
            t2 = val2  ## flexion
            
            ## extension
            arr_a = self.df_EnvelopedSignals.loc[(self.df_EnvelopedSignals[self.ch_time_name]>=t0) & (self.df_EnvelopedSignals[self.ch_time_name]<t1), [signal_name]].to_numpy()
            
            ## flexion
            arr_b = self.df_EnvelopedSignals.loc[(self.df_EnvelopedSignals[self.ch_time_name]>=t1) & (self.df_EnvelopedSignals[self.ch_time_name]<t2), [signal_name]].to_numpy()
            
            ## VLO RT
            # arr_vlr = df_sel.iloc[:,2].to_numpy()
            # print(f'sel: {len(arr_a)}, {len(arr_b)}')
            
            arr_a = signal.resample_poly(arr_a, len_ref, len(arr_a), padtype='line')
            arr_b = signal.resample_poly(arr_b, len_ref, len(arr_b), padtype='line')
            
            # arr_r = np.concatenate([arr_a, arr_b])
            
            # print(f'sel: {len(arr_r)}\n')
            # ax.plot(arr_r)
            df_ext[i] = arr_a.flatten()
            df_fle[i] = arr_b.flatten()
            
            
            i=i+1
        
        ## concat
        df_all = pd.concat([df_fle, df_ext], ignore_index=True)
        print(f"df_all:\n{df_all}")
        # print(f'df_ext.\n{df_ext_sel}')
        # print(f'df_fle.\n{df_fle}')
        color = 'tab:blue'
        # self.plot_alpha(df_fle, color, ax[0])
        # self.plot_alpha(df_ext, color, ax[1])
        self.plot_alpha(df_all, color, ax[0])

        ax[0].set_ylim(-1,25)
        
        # df_ext = df_ext.melt(id_vars=['cycle'], var_name='cols', value_name='vals')
        # df_fle = df_fle.melt(id_vars=['cycle'], var_name='cols', value_name='vals')
        # print(f'df_fef:\n{df_fef}')
        # sns.lineplot(ax=ax[0], x="cycle", y='vals', errorbar="sd", estimator='mean', data=df_fle)
        # sns.lineplot(ax=ax[1], x="cycle", y='vals', errorbar="sd", estimator='mean', data=df_ext)
        
        # ax.set_title(signal_name)
        ax[0].set_title(f'{signal_name} flexion_extension')
        # ax[1].set_title(f'{signal_name} extension')
        ax[0].set_xlabel('flexion-extension cycle')
        # ax[1].set_xlabel('percent extension [%]')
        ax[0].set_ylabel('amplitude')
        # ax[1].set_ylabel('amplitude')
        fig.tight_layout()
        
        # plt.savefig(f'../data/priority_patients/EBC024/figures/EBC024_cycle.png', bbox_inches='tight')
            
        return 0
    
    #######################################
    def plot_alpha(self, df, color, ax):
        
        x = df.iloc[:,0].tolist()
        y = df.iloc[:,1:].median(axis=1).tolist()
        ymax = df.iloc[:,1:].max(axis=1).tolist()
        ymin = df.iloc[:,1:].min(axis=1).tolist()
        alpha_fill = 0.3
        
        ax.vlines(0.5, ymin=-1,ymax=500, colors='tab:purple', alpha=0.5, lw=0.5, linestyles='dashed')
        ax.plot(x, y, color=color)
        # ax.fill_between(x, ymax, ymin, color=color, hatch=pattern, alpha=alpha_fill, label=sel_label)
        ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill,)
        
        return ax


    ############################
    # def plotEMGSession_assis_filtered(self, channels_names, fig, ax):
    def plotEMGSession_assis_filtered(self, channels_names):
        # path, save_figs
        # # print(f"channels names: {channels_names, len(channels_names)}")        
        num_rows = len(channels_names)//2
        # num_rows = math.ceil(len(channels_names)/2)
        fig, ax = plt.subplots(nrows=num_rows, ncols=2, figsize=(10, 7), sharex=True, squeeze=False)
        # fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        # ax = ax.reshape(-1)
        
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
            # ax[-1].plot(self.ch_time, self.channels_data[in_r],color='m',label='In_R, %', alpha=0.25)
            ax[-2].legend()
            # ax[-1].legend()
        else:
            pass
        if in_l in self.channels_data:
            # ax[-2].plot(self.ch_time, self.channels_data[in_l],color='c',label='In_L, %', alpha=0.25)
            ax[-1].plot(self.ch_time, self.channels_data[in_l],color='c',label='In_L, %', alpha=1.00)
            # ax[-2].legend()
            ax[-1].legend()
        else:
            pass
    
        # ## select number of seconds range of data at the middle of the recordings
        # val1 = 5.0
        # val2 = val1*2.0
        # id01 = (len(self.ch_time)/2 - (self.sampling_rate*val1)).astype(int)
        # id02 = (id01 + (self.sampling_rate*val2)).astype(int)
        
        ## adjust x-scale for the first and for all the subplots (sharex=True)
        # ax[0].set_xlim([self.ch_time[id01],self.ch_time[id02]])

        ax[-2].set_xlabel(self.ch_time_name+' [s]')
        ax[-1].set_xlabel(self.ch_time_name+' [s]')
        
        filename = self.filename.split('.')[0]
        fig.suptitle(f'{filename}\n{self.date}')
        
        # if save_figs:
        #     ### save figures ####
        #     # path_out=f'../data/a_velo_assis/figures/figs/'
        #     path_out= path + 'figures/'
        #     # checking if the directory
        #     # exist or not. 
        #     if not os.path.isdir(path_out): 
        #         # if directory is  
        #         # not present then create it. 
        #         os.makedirs(path_out) 
            
        #     plt.savefig(f'{path_out}/{filename}.png', bbox_inches='tight')
        #     ### save figure ####
        # else:
        #     pass
        
        # return fig, ax
        self.fig_emg = fig
        self.ax_emg = ax

        return 0
    ############################

    # def plot_selected_emg(self, label):
        
    #     # fig, ax = 
    #     # ax = ax.reshape(-1)
    #     print(f"time sync: {self.arr_time_angles_max}")
    #     ymin = -500
    #     ymax =  500
        
    #     ## plot EMG signals
    #     for ch_name, ax_single in zip(self.channels_names, self.ax_emg):
    #         if (label in ch_name):
    #             ax_single.vlines(self.arr_time_angles_max,  ymin=ymin,ymax=ymax, colors='tab:purple', alpha=0.5, lw=0.5)
    #         else:
    #             pass

    #     return 0
    
    ############################
    # def plotEMGSession_assis_filtered(self, channels_names, fig, ax):
    def plot_selected_emg(self, channels_names):

        num_rows = len(channels_names)//2
        fig, ax = plt.subplots(nrows=num_rows, ncols=2, figsize=(10, 7), sharex=True, squeeze=False)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        ax = ax.reshape(-1)
        ymin = -500
        ymax =  500
        
        ## plot EMG signals
        for ch_name, ax_single in zip(channels_names, ax):
            if (ch_name in self.channels_data) and not(ch_name.startswith('Insole')):
                # print(f"plot channels filtered and enveloped")
                if (' LT,' in ch_name):
                    ax_single.vlines(self.time_angles_markers['left_max'],  ymin=ymin,ymax=ymax, colors='tab:purple', alpha=0.5, lw=0.5)
                elif (' RT,' in ch_name):
                    ax_single.vlines(self.time_angles_markers['right_max'],  ymin=ymin,ymax=ymax, colors='tab:red', alpha=0.5, lw=0.5)

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
            ax[-1].vlines(self.time_angles_markers['right_max'],  ymin=ymin,ymax=ymax, colors='tab:red', alpha=0.5, lw=0.5)
            ax[-1].plot(self.ch_time, self.channels_data[in_r],color='m',label='In_R, %', alpha=1.00)
            ax[-1].legend()
        else:
            pass
        if in_l in self.channels_data:
            ax[-2].vlines(self.time_angles_markers['left_max'],  ymin=ymin,ymax=ymax, colors='tab:purple', alpha=0.5, lw=0.5)
            ax[-2].plot(self.ch_time, self.channels_data[in_l],color='c',label='In_L, %', alpha=1.00)
            ax[-2].legend()
        else:
            pass
    
        ax[-2].set_xlabel(self.ch_time_name+' [s]')
        ax[-1].set_xlabel(self.ch_time_name+' [s]')
        
        filename = self.filename.split('.')[0]
        fig.suptitle(f'{filename}\n{self.date}')
        
        # if save_figs:
        #     ### save figures ####
        #     # path_out=f'../data/a_velo_assis/figures/figs/'
        #     path_out= path + 'figures/'
        #     # checking if the directory
        #     # exist or not. 
        #     if not os.path.isdir(path_out): 
        #         # if directory is  
        #         # not present then create it. 
        #         os.makedirs(path_out) 
            
        #     plt.savefig(f'{path_out}/{filename}.png', bbox_inches='tight')
        #     ### save figure ####
        # else:
        #     pass
        
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

    def setTimeAnglesMarkers(self, arr, label):
        self.time_angles_markers[label] = arr
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
    
    def getFilename(self):
        return self.filename
    
    ######
    def get_flag_empty(self):
        return self.empty
    
    ## we remove the last minimum because it could be incomplete
    def getFlexionTimeList(self):
        return self.arr_time_min[:-1]
    
    
    

############################

        
        
    
