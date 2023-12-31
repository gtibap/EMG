from scipy import ndimage
from scipy import signal
import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pywt
import re
import sys



class Processing_EMG:

    def __init__(self, path, filename):

        self.path=''
        self.filename=[]
        self.sampling_rate=1.0
        self.n_channels=1
        self.channels=[]
        self.channelsNames=[]
    
        self.path = path
        self.filename = filename
    
        mat = scipy.io.loadmat(self.path+self.filename)
        self.sampling_rate = mat['samplingRate'][0,0]
        ## plus one to include the Time channel (channel 0)
        self.n_channels = mat['noChans'][0,0]+1
        
        self.channels = np.empty((self.n_channels, 0)).tolist()
        self.channelsNames = np.empty((self.n_channels, 0)).tolist()

        for i in np.arange(self.n_channels):
            self.channels[i] = mat['Data'][0,i].flatten()
            self.channelsNames[i] = mat['channelNames'][0][i][0]
                
    
    def smoothingRMS(self, window_size):
        
        ## window size in mili-seconds
        window_samples = int(self.sampling_rate * window_size*1e-3)
        print('sampling_rate, window_samples: ', self.sampling_rate, window_samples)
        window = np.ones(window_samples)/float(window_samples)
        
        self.channels_rms = np.empty((self.n_channels, 0)).tolist()
        
        i=0
        ## we excluded 'Time' and 'Switch' channels (first and last channels)
        for ch in self.channels[1:-1]:
            self.channels_rms[i] = np.sqrt(np.convolve(ch**2, window, 'same'))
            i+=1
        
        return 0
        
    
    def plotEMG(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
        ## minus 1 because the first is the Time channel
        
        if self.n_channels==2:
            fig, ax = plt.subplots(nrows=1, ncols=1)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            ax.plot(time, self.channels[1], label=self.channelsNames[1])
            ax.legend()
            ax.set_title(self.filename)
            ax.set_xlabel(time_label+' [s]')
        else:
            ## we exclude swich channel
            fig, ax = plt.subplots(nrows=(self.n_channels-2), ncols=1, sharex=True, sharey=True)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            cont=0
            for ch, ch_n in zip(self.channels[1:-1], self.channelsNames[1:-1]):
                ax[cont].plot(time, ch, label=ch_n)
                ax[cont].legend()
                cont+=1
            
            ax[0].set_title(self.filename)
            ax[cont-1].set_xlabel(time_label+' [s]')
        
        return 0

    def plotPowerSpectrum(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
        
        if self.n_channels==2:
            fig, ax = plt.subplots(nrows=1, ncols=1)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            
            f, Pxx_spec = signal.periodogram(self.channels[1], self.sampling_rate, 'flattop', scaling='spectrum')
            ax.axes.semilogy(f, np.sqrt(Pxx_spec),label=self.channelsNames[1])
            ax.legend()
            ax.set_title(self.filename)
            ax.set_xlabel('frequency [Hz]')
            ax.set_ylabel('Linear spectrum [V RMS]')
        else:
            fig, ax = plt.subplots(nrows=(self.n_channels-2), ncols=1, sharex=True, sharey=True)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            cont=0
            for ch, ch_n in zip(self.channels[1:-1], self.channelsNames[1:-1]):
                f, Pxx_spec = signal.periodogram(ch, self.sampling_rate, 'flattop', scaling='spectrum')
                ax[cont].axes.semilogy(f, np.sqrt(Pxx_spec),label=ch_n)
                ax[cont].legend()
                cont+=1
            
            ax[0].set_title('Linear spectrum [V RMS] '+self.filename)
            ax[cont-1].set_xlabel('frequency [Hz]')
            
        return 0
        
        
    def plotEMG_smoothed(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
        ## minus 1 because the first is the Time channel
        
        if self.n_channels==2:
            fig, ax = plt.subplots(nrows=1, ncols=1)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            ax.plot(time, self.channels_rms[0], label=self.channelsNames[1])
            ax.legend()
            ax.set_title(self.filename)
            ax.set_xlabel(time_label+' [s]')
        else:
            ## we exclude swich channel
            fig, ax = plt.subplots(nrows=(self.n_channels-2), ncols=1, sharex=True, sharey=True)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            cont=0
            for ch, ch_n in zip(self.channels_rms, self.channelsNames[1:-1]):
                ax[cont].plot(time, ch, label=ch_n)
                ax[cont].legend()
                cont+=1
            
            ax[0].set_title('smoothing RMS '+ self.filename)
            ax[cont-1].set_xlabel(time_label+' [s]')
        
        return 0
        

    def on_press(self, event):
        # print('press', event.key)
        sys.stdout.flush()
        
        if event.key == 'x':
            plt.close('all')
        else:
            pass
                
        return 0

