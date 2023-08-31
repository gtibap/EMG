# import kineticstoolkit.lab as ktk
import scipy.io
from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

class Reading_EMG:

    def __init__(self, path, filename, ids_channels):

        self.path=''
        self.filename=[]
        self.sampling_rate=1.0
        self.n_channels=1
        self.channels=[]
        self.channelsNames=[]
        
        self.path = path
        self.filename = filename
        # self.day_number = day_number
    
        mat = scipy.io.loadmat(self.path+self.filename)
        print(f'\n{self.filename}')
        # print(f'dictionary {mat}')
        print('Header:',  mat['__header__'])
        print('Channel Names:',  mat['channelNames'])
        
        self.sampling_rate = mat['samplingRate'][0,0]
        print(f'sample rate: {self.sampling_rate}')
        # ## number of channels plus one to include the Time channel (channel 0)
        
        # self.n_channels = mat['noChans'][0,0]+1
        # self.n_channels = 9
        
        # print(f'self.n_channels {self.n_channels}')
        
        self.n_channels = ids_channels[1]-ids_channels[0] + 1
        
        self.channels = np.empty((self.n_channels, 0)).tolist()
        self.channelsNames = np.empty((self.n_channels, 0)).tolist()

        ## channel 0 is the time array
        self.ch_time = mat['Data'][0, 0].flatten()
        self.ch_time_name = mat['channelNames'][0][0][0]
        # print(f'time ch: {self.ch_time.shape}')
        
        i=0
        for num_ch in np.arange(ids_channels[0], ids_channels[1]+1):
            self.channels[i] = mat['Data'][0, num_ch].flatten()
            self.channelsNames[i] = mat['channelNames'][0][num_ch][0]
            i+=1

        # print(f'channels: {len(self.channels)}, {len(self.channels[0])}, {len(self.channelsNames)}')


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
        sos = signal.butter(10, fc, btype='highpass', fs=self.sampling_rate, output='sos')
        filtered = signal.sosfilt(sos, emg)
        return filtered

    def filterLowPass(self, emg, fc):
        sos = signal.butter(10, fc, btype='lowpass', fs=self.sampling_rate, output='sos')
        filtered = signal.sosfilt(sos, emg)
        return filtered

    def filterBandPass(self, emg, fc1, fc2):
        sos = signal.butter(10, [fc1,fc2], btype='bandpass', fs=self.sampling_rate, output='sos')
        filtered = signal.sosfilt(sos, emg)
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
        

    def plotSignals(self):
        # print(f'\nids channels: {ids_channels}')
        fig, ax = plt.subplots(nrows=8, ncols=1, sharex=True, sharey=True)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        cont=0
        for ch, ch_n in zip(self.channels, self.channelsNames):
            ax[cont].plot(self.ch_time, ch, label=ch_n)
            ax[cont].legend()
            cont+=1
        
        ax[0].set_ylim([-100,100])
        ax[0].set_title(self.filename)
        ax[cont-1].set_xlabel(self.ch_time_name+' [s]')

        return 0
        
    def plotSelectedSignal(self, signal_number):
        # print(f'\nids channels: {ids_channels}')
        fig, ax = plt.subplots(nrows=2, ncols=2)
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

        ax[1][0].set_xlim([0,fc2])
        ax[1][1].set_xlim([0,fc2])
        
        amp_y = 150
        
        ax[0][0].set_ylim([-amp_y,amp_y])
        ax[0][1].set_ylim([-amp_y,amp_y])
        ax[1][0].set_ylim([10e-8, amp_y/64])
        ax[1][1].set_ylim([10e-8, amp_y/64])
        
        ax[0][0].set_title(self.filename+' (original)')
        ax[0][1].set_title(f'{self.filename} passband {fc1} Hz - {fc2} Hz')
        
        ax[0][0].set_xlabel(self.ch_time_name+' [s]')
        ax[0][1].set_xlabel(self.ch_time_name+' [s]')
        
        ax[1][0].set_xlabel('frequency [Hz]')
        ax[1][1].set_xlabel('frequency [Hz]')
        
        ax[0][0].set_ylabel('magnitude')
        ax[0][1].set_ylabel('magnitude')
        ax[1][0].set_ylabel('power spectral density')
        ax[1][1].set_ylabel('power spectral density')

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
        
        
        
    
