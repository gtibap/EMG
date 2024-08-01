# import kineticstoolkit.lab as ktk
from scipy.signal import savgol_filter
import scipy.io
from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import os 

class Reading_EMG:

    def __init__(self, path, filename, ids_channels):

        self.path=''
        self.filename=[]
        self.sampling_rate=1.0
        self.n_channels=1
        self.channels=[]
        self.channelsFiltered=[]
        self.channelsEnveloped=[]
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
        # print('Header:',  mat['__header__'])
        # print('Channel Names:',  mat['channelNames'])
        
        self.sampling_rate = mat['samplingRate'][0,0]
        # print(f'sample rate: {self.sampling_rate}')
        # ## number of channels plus one to include the Time channel (channel 0)
        
        # self.n_channels = mat['noChans'][0,0]+1
        # self.n_channels = 9
        
        # print(f'self.n_channels {self.n_channels}')
        # print(f'ids_channels {ids_channels}')
        
        self.n_channels = ids_channels[1]-ids_channels[0] + 1
        
        self.channels = np.empty((self.n_channels, 0)).tolist()
        self.channelsFiltered = np.empty((self.n_channels, 0)).tolist()
        self.channelsEnveloped = np.empty((self.n_channels, 0)).tolist()
        self.channelsNames = np.empty((self.n_channels, 0)).tolist()

        ## channel 0 is the time array
        self.ch_time = mat['Data'][0, 0].flatten()
        self.ch_time_name = mat['channelNames'][0][0][0]
        # print(f'time ch: {self.ch_time[0]}, {self.ch_time[-1]}, {self.ch_time.shape}')
        
        self.df_EnvelopedSignals[self.ch_time_name] = self.ch_time
        
        i=0
        for num_ch in np.arange(ids_channels[0], ids_channels[1]+1):
            self.channels[i] = mat['Data'][0, num_ch].flatten()
            self.channelsNames[i] = mat['channelNames'][0][num_ch][0]
        
            i+=1

        # print(self.df_EnvelopedSignals)

        # print(f'channels sinc: {self.channelsNames[-1]}\n{self.channels[-1]}')
        # plt.plot(self.channels[-1])
        # plt.show()
        
        # num_ch=ids_channels[-1]+1
        # ch_switch = mat['Data'][0, num_ch].flatten()
        # name_switch = mat['channelNames'][0][num_ch][0]
        
        # print(f'channel switch: {name_switch}, {len(ch_switch)}, {ch_switch}')
        
        # print(f'channels: {len(self.channels)}, {len(self.channels[0])}, {len(self.channelsNames)}')

    def max_and_min(self, arr):
            
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


    def smooth_filter(self, arr):
        arr[:,0]=savgol_filter(arr[:,0], window_length=60, polyorder=1, mode='mirror')
        arr[:,1]=savgol_filter(arr[:,1], window_length=60, polyorder=1, mode='mirror')
        arr[:,2]=savgol_filter(arr[:,2], window_length=60, polyorder=1, mode='mirror')
        return arr



    def kinematics(self, filename, list_ids_x,):
    
        # list_filenames=['Take 2022-07-04 10.23.53 AM.csv', 'Take 2022-07-04 10.37.36 AM.csv', 'Take 2022-07-04 10.52.59 AM.csv']
        
        ## four groups of markers
        ## order: CG, JG, CD, JD
        ## JD columns, marker1:(EB:EB+3), marker2:(EE:EE+3), marker4:(EH:EH+3), Unlabeled_377:(EK:EK+3)
        ##
        # list_columns=[ [], [], [[],[],[],[131,134,137,140]]]
        
        ## calculate coordinates middle point of the markers for each body part
        ## first: open files
        # filename = path+list_filenames[record_number]
        
        print(f'reading markers file... ', end='')
        try:
            df = pd.read_csv(filename, header=5)
        except ValueError:
                print(f'error. Problem reading the file {filename}.')
                return 0
        print(f'done.')
        
        # print(f'data markers:\n{df}')
        
        ## column indexes read coordinates markers
        # list_ids_x = list_columns[record_number][3]
        # print(f'list_ids_x: {list_ids_x}')
        
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
            markers_arr[i] = self.smooth_filter(markers_arr[i])
            # ax[i].plot(markers_arr[i,:,col], label='smooth')
            # ax[i].legend()
            markers_sum += markers_arr[i]
        
        # print(f'markers_arr:\n{markers_arr}')
        
        marker_center = markers_sum / len(list_ids_x)
        
        ## finding maximums and minimums (positive and negative picks) of the X component of the marker_center
        max_list, min_list = self.max_and_min(marker_center[:,0])
        print(f'max and min:\n{max_list},\n{min_list}')
        
        sample_rate_tracking = 120 ## samples per second (Hz)
        ## time in seconds
        t_delay=0.0
        self.arr_time_max = np.array(max_list)/sample_rate_tracking - t_delay
        self.arr_time_min = np.array(min_list)/sample_rate_tracking - t_delay
        
        # for i in np.arange(3):
            # ax[i].plot(marker_center[:,i],)
        # plt.show()
        
        return 0



    def smoothingRMS(self, ch, window_size):
        ## window_size is in miliseconds
        # spm = 60 ## seconds per min
        # window_size = int(spm*self.window_min)
        ## transform window size to number of samples
        window_samples = int(self.sampling_rate * window_size*1e-3)
        # print(f'window_samples: {window_samples}')
        
        # print(f'window: {window}')
        # print(  'window size (s): ', window_size)
        ## window to average values (same weight)
        
        window = np.ones(window_samples)/(window_samples)
        ch_smoothed = np.sqrt(signal.convolve(ch**2, window, 'same'))

        # window = signal.windows.boxcar(window_samples)
        # ch_smoothed = np.rint(signal.convolve(ch, window, mode='same'))/window_samples
        
        
        return ch_smoothed
        
        
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
        
        
    # def smoothingRMS(self, window_size):
        
        # ## window size in mili-seconds
        # window_samples = np.rint(self.sampling_rate * window_size*1e-3)
        # print('sampling_rate, window_samples: ', self.sampling_rate, window_samples)
        # window = np.ones(window_samples)/float(window_samples)
        # ## we excluded 'Time' and 'Switch' channels (first and last channels)
        # self.channels_rms = np.empty((self.n_channels-2, 0)).tolist()
        # i=0
        # for ch in self.channels[1:-1]:
            # ## RMS window smoothing
            # self.channels_rms[i] = np.sqrt(np.convolve(ch**2, window, 'same'))
            # i+=1
        
        # return 0
        
    def filteringSignals(self):
        
        fc1 = 50 ## 50 Hz high pass filter
        fc2 = 500 ## 500 Hz low pass filter

        i=0
        for ch, ch_n in zip(self.channels, self.channelsNames):
            # print(f'filtering {ch_n}')
            self.channelsFiltered[i] = self.filterBandPass(ch, fc1, fc2)
            i+=1
        
        return 0


    def envelopeFilter(self):
        
        fc = 6 ## 6 Hz low pass filter
        i=0
        for ch, ch_n in zip(self.channelsFiltered, self.channelsNames):
            # print(f'filtering {ch_n}')
            self.channelsEnveloped[i] = self.filterLowPass(np.absolute(ch), fc)
            ## channelsEnveloped in a pandas DataFrame
            self.df_EnvelopedSignals[ch_n] = self.channelsEnveloped[i]
            i+=1
        
        return 0
        
    
    def flexion_extension(self, arr_time_max, arr_time_min, signal_name):
        
        fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(7,3.5), sharex=True, sharey=True)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        # df_fef = pd.DataFrame()
        df_fle = pd.DataFrame()
        df_ext = pd.DataFrame()
        ## resampling all selected segments to have same number of samples
        len_ref = 2000
        
        x_range = np.linspace(0,100,len_ref)
        df_fle['cycle']=x_range
        df_ext['cycle']=x_range
        
        ## selecting first index; first index of min distance: starting with flexion
        if arr_time_min[0] < arr_time_max[0]:
            id0=0
        else:
            id0=1
        
        i=0
        
        ## we include all cycles but without the last one because it could be incomplete
        for val0, val1, val2 in zip(arr_time_min[0:], arr_time_max[id0:], arr_time_min[1:]):
            
            t0 = self.ch_time[0] + val0  ## flexion
            t1 = self.ch_time[0] + val1  ## extension
            t2 = self.ch_time[0] + val2  ## flexion
            
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
        
        # print(f'df_ext.\n{df_ext_sel}')
        # print(f'df_fle.\n{df_fle}')
        color = 'tab:blue'
        self.plot_alpha(df_ext, color, ax[0])
        self.plot_alpha(df_fle, color, ax[1])
        
        # df_ext = df_ext.melt(id_vars=['cycle'], var_name='cols', value_name='vals')
        # df_fle = df_fle.melt(id_vars=['cycle'], var_name='cols', value_name='vals')
        # print(f'df_fef:\n{df_fef}')
        # sns.lineplot(ax=ax[0], x="cycle", y='vals', errorbar="sd", estimator='mean', data=df_fle)
        # sns.lineplot(ax=ax[1], x="cycle", y='vals', errorbar="sd", estimator='mean', data=df_ext)
        
        # ax.set_title(signal_name)
        ax[0].set_title(f'{signal_name} extension')
        ax[1].set_title(f'{signal_name} flexion')
        ax[0].set_xlabel('percent extension [%]')
        ax[1].set_xlabel('percentage flexion [%]')
        ax[0].set_ylabel('amplitude')
        ax[1].set_ylabel('amplitude')
        fig.tight_layout()
        
        # plt.savefig(f'../data/priority_patients/EBC024/figures/EBC024_cycle.png', bbox_inches='tight')
            
        return 0
    

    def plotFlexionExtension(self, ax, arr_time_max, arr_time_min, signal_name):
        
        # fig, ax = plt.subplots(nrows=1,ncols=2, figsize=(7,3.5), sharex=True, sharey=True)
        # fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        # df_fef = pd.DataFrame()
        df_ext = pd.DataFrame()
        df_fle = pd.DataFrame()
        ## resampling all selected segments to have same number of samples
        len_ref = 2400
        
        # x_range = np.linspace(0,100,len_ref)
        x_range = np.arange(len_ref)
        df_ext['cycle']=x_range
        df_fle['cycle']=x_range+len_ref
        
        
        ## selecting first index; first index of min distance: starting with flexion
        if arr_time_min[0] < arr_time_max[0]:
            id0=0
        else:
            id0=1
        
        i=0
        
        for val0, val1, val2 in zip(arr_time_min[0:], arr_time_max[id0:], arr_time_min[1:]):
            
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
            print(f'sel: {len(arr_a)}, {len(arr_b)}')
            
            arr_a = signal.resample_poly(arr_a, len_ref, len(arr_a), padtype='line')
            arr_b = signal.resample_poly(arr_b, len_ref, len(arr_b), padtype='line')
            
            # arr_r = np.concatenate([arr_a, arr_b])
            
            # print(f'sel: {len(arr_r)}\n')
            # ax.plot(arr_r)
            df_ext[i] = arr_a.flatten()
            df_fle[i] = arr_b.flatten()
            
            i=i+1
        
        # print(f'df_ext.\n{df_ext_sel}')
        # print(f'df_fle.\n{df_fle}')
        color = 'tab:blue'
        ax, pos_y1 = self.plot_alpha(df_ext, color, ax)
        ax, pos_y2 = self.plot_alpha(df_fle, color, ax)
        
        
        ## vertical lines to delimit extension and flexion
        ax.axvline(x = 0, color = 'tab:green')
        ax.axvline(x = len_ref, color = 'tab:purple')
        ax.axvline(x = 2*len_ref, color = 'tab:green')
        
        pos_x = int((1/6)*len_ref)
        # pos_y = int(35)
        ax.annotate('extension', xy=(pos_x, pos_y1),
                    color='blue',
                    bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                    )
                    
        pos_x = int((1/6)*len_ref) + len_ref
        # pos_y = int(35)
        ax.annotate('flexion', xy=(pos_x, pos_y2),
                    color='blue',
                    bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                    )
        
        
        list_xticks = np.arange(0, 2*len_ref+1, int(2*len_ref)/4)
        print(f'list_xticks: {list_xticks}')
        ax.set_xticks(list_xticks)
        ax.set_xticklabels(['9','12','3','6','9'])

        ax.set_ylim(0.5, 20.0)
        
        # df_ext = df_ext.melt(id_vars=['cycle'], var_name='cols', value_name='vals')
        # df_fle = df_fle.melt(id_vars=['cycle'], var_name='cols', value_name='vals')
        # print(f'df_fef:\n{df_fef}')
        # sns.lineplot(ax=ax[0], x="cycle", y='vals', errorbar="sd", estimator='mean', data=df_fle)
        # sns.lineplot(ax=ax[1], x="cycle", y='vals', errorbar="sd", estimator='mean', data=df_ext)
        
        # ax.set_title(signal_name)
        # ax[0].set_title(f'{signal_name} extension')
        # ax[1].set_title(f'{signal_name} flexion')
        # ax[0].set_xlabel('percent extension [%]')
        # ax[1].set_xlabel('percentage flexion [%]')
        # ax[0].set_ylabel('amplitude')
        # ax[1].set_ylabel('amplitude')
        # fig.tight_layout()
        
        # plt.savefig(f'../data/priority_patients/EBC024/figures/EBC024_cycle.png', bbox_inches='tight')
            
        return 0
        
    
        

    def plot_alpha(self, df, color, ax):
        
        x = df.iloc[:,0].tolist()
        y = df.iloc[:,1:].median(axis=1).tolist()
        ymax = df.iloc[:,1:].max(axis=1).tolist()
        ymin = df.iloc[:,1:].min(axis=1).tolist()
        alpha_fill = 0.3
        
        ax.plot(x, y, color=color)
        # ax.fill_between(x, ymax, ymin, color=color, hatch=pattern, alpha=alpha_fill, label=sel_label)
        ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill,)

        val_max = np.max(ymax)
        
        return ax, val_max
        
        

    def plotSignals(self):
        # print(f'\nids channels: {ids_channels}')
        fig, ax = plt.subplots(nrows=len(self.channels), ncols=1, sharex=True, sharey=True,)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        cont=0
        for ch, ch_n in zip(self.channels, self.channelsNames):
            ax[cont].plot(self.ch_time, ch, label=ch_n)
            ax[cont].legend()
            cont+=1

        ax[0].set_ylim([-100,100])            
        # ax[-1].set_ylim([-0.1, 1.1])    
        ax[0].set_title(self.filename)
        ax[cont-1].set_xlabel(self.ch_time_name+' [s]')

        return 0
        
    def plotSelectedSignal(self, signal_number):
        # print(f'\nids channels: {ids_channels}')
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 7))
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        # cont=0
        ch = self.channels[signal_number]
        ch_n = self.channelsNames[signal_number]
        # for ch, ch_n in zip(self.channels, self.channelsNames):
        
        # window_size=20 ## miliseconds
        # ch_s = self.smoothingRMS(ch, window_size)
        # filtered_ch = ktk.filters.butter(ch, btype="bandpass", fc=[20, 500])
        fc1 = 50 ## 20 Hz high pass filter
        fc2 = 500 ## Hz
        ch_s = self.filterBandPass(ch, fc1, fc2)
        
        id01 = (len(self.ch_time)/2 - (self.sampling_rate*2.5)).astype(int)
        id02 = (id01 + (self.sampling_rate*5)).astype(int)  

        # f1, Pxx_spec1 = signal.periodogram(ch, self.sampling_rate, 'flattop', scaling='spectrum')
        # f2, Pxx_spec2 = signal.periodogram(ch_s, self.sampling_rate, 'flattop', scaling='spectrum')
        # f1, S1 = signal.periodogram(ch[id01:id02], self.sampling_rate, scaling='density')
        # f2, S2 = signal.periodogram(ch_s[id01:id02], self.sampling_rate, scaling='density')
        
        
        (f1, S1)= scipy.signal.welch(ch[id01:id02], self.sampling_rate, nperseg=2*1024, scaling='density')
        (f2, S2)= scipy.signal.welch(ch_s[id01:id02], self.sampling_rate, nperseg=2*1024, scaling='density')

        
        ax[0][0].plot(self.ch_time, ch, label=ch_n)
        ax[0][0].legend()
        
        ax[0][1].plot(self.ch_time, ch_s, label=ch_n)
        ax[0][1].legend()
        
        # ax[1][0].axes.semilogy(f1, np.sqrt(Pxx_spec1),label=ch_n)
        # ax[1][1].axes.semilogy(f2, np.sqrt(Pxx_spec2),label=ch_n)
        # ax[1][0].axes.semilogy(f1, S1,label=ch_n)
        # ax[1][1].axes.semilogy(f2, S2,label=ch_n)
        # ax[1][0].axes.semilogy(f1, np.sqrt(S1),label=ch_n)
        # ax[1][1].axes.semilogy(f2, np.sqrt(S2),label=ch_n)
        ax[1][0].axes.plot(f1, np.sqrt(S1),label=ch_n)
        ax[1][1].axes.plot(f2, np.sqrt(S2),label=ch_n)
        ax[1][0].legend()
        ax[1][1].legend()

              
        
        ax[0][0].set_xlim([self.ch_time[id01],self.ch_time[id02]])
        ax[0][1].set_xlim([self.ch_time[id01],self.ch_time[id02]])

        ax[1][0].set_xlim([0,fc2*1.5])
        ax[1][1].set_xlim([0,fc2*1.5])
        
        amp_y = 40
        
        ax[0][0].set_ylim([-amp_y,amp_y])
        ax[0][1].set_ylim([-amp_y,amp_y])
        ax[1][0].set_ylim([10e-8, amp_y/64])
        ax[1][1].set_ylim([10e-8, amp_y/64])
        
        fig.suptitle(f'{self.filename}, bandpass filter {fc1} Hz - {fc2} Hz')
        ax[0][0].set_title(f'original')
        ax[0][1].set_title(f'filtered')
        
        ax[0][0].set_xlabel(self.ch_time_name+' [s]')
        ax[0][1].set_xlabel(self.ch_time_name+' [s]')
        
        ax[1][0].set_xlabel('frequency [Hz]')
        ax[1][1].set_xlabel('frequency [Hz]')
        
        ax[0][0].set_ylabel('magnitude')
        ax[0][1].set_ylabel('magnitude')
        ax[1][0].set_ylabel('power spectral density')
        ax[1][1].set_ylabel('power spectral density')

        return 0
        
        
    def plotFilteredSignals(self, ids_emg, title_emg, patient_number, session_name, session_number, list_act_emg, channels_names):
        
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(10, 7), sharex=True, sharey=True, squeeze=False)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        ax = ax.reshape(-1)
        
        # cont=0
        # for ch, ch_n, id_emg in zip(self.channelsFiltered, self.channelsNames, ids_emg):
        for ch, id_emg in zip(self.channelsFiltered, ids_emg):
            ax[id_emg].plot(self.ch_time, ch, label=channels_names[id_emg])
            ax[id_emg].legend()
            # cont+=1
        
        # for id_ax, ch_n in enumerate(channels_names):
            # ax[id_ax]
            # ax.legend()
                
        
        
        ## select 5 seconds range of data at the middle of the recordings
        id01 = (len(self.ch_time)/2 - (self.sampling_rate*2.5)).astype(int)
        id02 = (id01 + (self.sampling_rate*5)).astype(int)  
        
        ax[0].set_xlim([self.ch_time[id01],self.ch_time[id02]])
        ax[0].set_ylim([-100,100])
        # ax[0].set_title(self.filename)
        ax[6].set_xlabel(self.ch_time_name+' [s]')
        ax[7].set_xlabel(self.ch_time_name+' [s]')
        
        ## frame with red color means potential muscular activity
        # ax[0].tick_params(color='red',labelcolor='red')
        for id_emg in list_act_emg:
            for spine in ax[id_emg].spines.values():
                spine.set_edgecolor('tab:orange')
                spine.set_linewidth(2)
        
        ## saving plot png file
        # fig.suptitle(f'{self.filename}\n{title_emg}')
        # fig.suptitle(f'P-{patient_number} session {session_number}')
        fig.suptitle(f'P-{patient_number}')
        # plt.savefig(f'../docs/figures/feb19_2024/ebc{patient_number}{session_name}.png', bbox_inches='tight')
        
        return 0
        
        
    def plotEnvelopedSignals(self, ids_emg, title_emg, patient_number, session_name, session_number, list_act_emg, channels_names):
        
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(10, 7), sharex=True, sharey=True, squeeze=False)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        ax = ax.reshape(-1)
        
        # cont=0
        # for ch, ch_n, id_emg in zip(self.channelsFiltered, self.channelsNames, ids_emg):
        for ch_fil, ch_env, id_emg in zip(self.channelsFiltered, self.channelsEnveloped, ids_emg):
            ch_n = channels_names[id_emg]
            ax[id_emg].plot(self.ch_time, ch_fil, label=ch_n)
            ax[id_emg].plot(self.ch_time, ch_env)
            
            # self.channelsEnveloped[id_emg]
            # self.df_EnvelopedSignals[]
            
            
            ax[id_emg].legend()
            # cont+=1
        
        # for id_ax, ch_n in enumerate(channels_names):
            # ax[id_ax]
            # ax.legend()
                
        
        
        ## select 5 seconds range of data at the middle of the recordings
        id01 = (len(self.ch_time)/2 - (self.sampling_rate*2.5)).astype(int)
        id02 = (id01 + (self.sampling_rate*5)).astype(int)  
        
        ax[0].set_xlim([self.ch_time[id01],self.ch_time[id02]])
        ax[0].set_ylim([-100,100])
        # ax[0].set_title(self.filename)
        ax[6].set_xlabel(self.ch_time_name+' [s]')
        ax[7].set_xlabel(self.ch_time_name+' [s]')
        
        ## frame with red color means potential muscular activity
        # ax[0].tick_params(color='red',labelcolor='red')
        for id_emg in list_act_emg:
            for spine in ax[id_emg].spines.values():
                spine.set_edgecolor('tab:orange')
                spine.set_linewidth(2)
        
        ## saving plot png file
        # fig.suptitle(f'{self.filename}\n{title_emg}')
        # fig.suptitle(f'P-{patient_number} session {session_number}')
        fig.suptitle(f'P-{patient_number}')
        # plt.savefig(f'../docs/figures/feb19_2024/ebc{patient_number}{session_name}.png', bbox_inches='tight')
        
        return 0
    
    
    def plotEMGSession(self, ids_emg, channels_names, patient_number, session, moment, baseline):
        
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(10, 7), sharex=True, sharey=True, squeeze=False)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        ax = ax.reshape(-1)
        
        # cont=0
        # for ch, ch_n, id_emg in zip(self.channelsFiltered, self.channelsNames, ids_emg):
        for ch_fil, ch_env, id_emg in zip(self.channelsFiltered, self.channelsEnveloped, ids_emg):
            ch_n = channels_names[id_emg]
            ax[id_emg].plot(self.ch_time, ch_fil, label=ch_n)
            ax[id_emg].plot(self.ch_time, ch_env)
            
            # self.channelsEnveloped[id_emg]
            # self.df_EnvelopedSignals[]
            
            
            ax[id_emg].legend()
            # cont+=1
        
        # for id_ax, ch_n in enumerate(channels_names):
            # ax[id_ax]
            # ax.legend()
                
        
        # delta_t = (self.sampling_rate*5).astype(int)
        ## select 5 seconds range of data at the middle of the recordings
        id01 = (len(self.ch_time)/2 - (self.sampling_rate*2.5)).astype(int)
        id02 = (id01 + (self.sampling_rate*5)).astype(int)
        
        ax[0].set_xlim([self.ch_time[id01],self.ch_time[id02]])
        ax[0].set_ylim([-50,50])
        # ax[0].set_title(self.filename)
        ax[6].set_xlabel(self.ch_time_name+' [s]')
        ax[7].set_xlabel(self.ch_time_name+' [s]')
        
        if moment==0:
            if baseline:
                instant='baseline - at the beginning'
            else:
                instant='cycling - at the beginning'
                
        elif moment==1:
            instant='cycling - at the middle'
        elif moment==2:
            instant='cycling - at the end'
        else:
            instant='not defined'
        
       
        ## saving plot png file
        # fig.suptitle(f'{self.filename}\n{title_emg}')
        # fig.suptitle(f'P-{patient_number} session {session_number}')
        fig.suptitle(f'EBC{patient_number} session {session}\n{instant}')
        
        path_out=f'../docs/figures/march_12_2024/EBC{patient_number}'
        # checking if the directory
        # exist or not. 
        if not os.path.isdir(path_out): 
            # if directory is  
            # not present then create it. 
            os.makedirs(path_out) 
        
        plt.savefig(f'{path_out}/ebc{patient_number}{session}_{moment}.png', bbox_inches='tight')
        
        return 0
    
    
    
    def plotSegmentedSignals(self, ids_emg, title_emg, patient_number, session_name, session_number, list_act_emg, channels_names, arr_time_max, arr_time_min, flag):
        
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(10, 7), sharex=True, sharey=True, squeeze=False)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        ax = ax.reshape(-1)
        # ax = ax.flatten()
        
        # cont=0
        # for ch, ch_n, id_emg in zip(self.channelsFiltered, self.channelsNames, ids_emg):
        for ch, id_emg in zip(self.channelsEnveloped, ids_emg):
            ax[id_emg].plot(self.ch_time, ch, label=channels_names[id_emg])
            ax[id_emg].legend()
            
        
            ## left leg
            if id_emg % 2 == 0:
                # print(f'id_emg % 2 == 0: {id_emg}, {channels_names[id_emg]}')
                for x_val in arr_time_max:
                    p_f = ax[id_emg].axvline(x = self.ch_time[0] + x_val, color = 'tab:green', label='flexion')
                for x_val in arr_time_min:
                    p_e = ax[id_emg].axvline(x = self.ch_time[0] + x_val, color = 'tab:purple', label='extension')
            ## right leg
            else:
                # print(f'id_emg % 2 != 0: {id_emg}, {channels_names[id_emg]}')
                for x_val in arr_time_max:
                    p_e = ax[id_emg].axvline(x = self.ch_time[0] + x_val, color = 'tab:purple', label='extension')
                for x_val in arr_time_min:
                    p_f = ax[id_emg].axvline(x = self.ch_time[0] + x_val, color = 'tab:green', label='flexion')
                
            # cont+=1
        
        # handles, labels = ax.get_legend_handles_labels()
        # handles, labels = fig.gca().get_legend_handles_labels()
        # fig.legend(handles, labels, loc='upper center')
        # labels = ["flexion", "extension"] 
        # fig.legend([p_f, p_e], labels=labels, loc="upper right") 
        
        # for id_ax, ch_n in enumerate(channels_names):
            # ax[id_ax]
            # ax.legend()
                
        ## select 5 seconds range of data at the middle of the recordings
        if flag == False:
            id01 = (len(self.ch_time)/2 - (self.sampling_rate*2.5)).astype(int)
            id02 = (id01 + (self.sampling_rate*5)).astype(int)
            ax[0].set_xlim([self.ch_time[id01],self.ch_time[id02]])
        else:
            id01 = 0
            id02 = arr_time_min[10]
            ax[0].set_xlim([id01,id02])
        
        ax[0].set_ylim([-0.5,20])
        # ax[0].set_title(self.filename)
        ax[6].set_xlabel(self.ch_time_name+' [s]')
        ax[7].set_xlabel(self.ch_time_name+' [s]')
        
        # ## frame with orange color means potential muscular activity
        # for id_emg in list_act_emg:
            # for spine in ax[id_emg].spines.values():
                # spine.set_edgecolor('tab:orange')
                # spine.set_linewidth(2)
        
        
        
        ## saving plot png file
        # fig.suptitle(f'{self.filename}\n{title_emg}')
        fig.suptitle(f'P-{patient_number} session {session_number}')
        # plt.savefig(f'../docs/figures/oct02_2023/ebc{patient_number}{session_name}.png', bbox_inches='tight')
        # plt.savefig(f'../data/priority_patients/EBC024/figures/EBC024_segmented.png', bbox_inches='tight')
        
        return 0
    
        
    # def plotPowerSpectrum(self):
        
        # time = self.channels[0]
        # time_label = self.channelsNames[0]
        # ## we exclude Time channel and Swich channel (first and last channels)
        # fig, ax = plt.subplots(nrows=(self.n_channels-2), ncols=1, sharex=True, sharey=True)
        # fig.canvas.mpl_connect('key_press_event', self.on_press)
        # cont=0
        # for ch, ch_n in zip(self.channels[1:-1], self.channelsNames[1:-1]):
            # f, Pxx_spec = signal.periodogram(ch, self.sampling_rate, 'flattop', scaling='spectrum')
            # ax[cont].axes.semilogy(f, np.sqrt(Pxx_spec),label=ch_n)
            # ax[cont].legend()
            # cont+=1
        
        # ax[0].set_title('Linear spectrum [V RMS] '+self.filename)
        # ax[cont-1].set_xlabel('frequency [Hz]')
            
        # return 0
        
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
    
    def getChannels(self):
        return self.channels
        
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
        
        
    
