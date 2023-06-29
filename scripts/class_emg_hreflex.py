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

        ## channel 0 is 'Time'
        for i in np.arange(self.n_channels):
            self.channels[i] = mat['Data'][0,i].flatten()
            self.channelsNames[i] = mat['channelNames'][0][i][0]
    
    def plotEMG(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
    
        fig, ax = plt.subplots(nrows=1, ncols=1)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        ax.plot(time, self.channels[1], label=self.channelsNames[1])
        ax.legend()
        ax.set_title(self.filename)
        ax.set_xlabel(time_label+' [s]')
        
        return 0            
    
    def plotEMG_multichannel(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]

        if self.n_channels==2:
            fig, ax = plt.subplots(nrows=1, ncols=1)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            ax.plot(time, self.channels[1], label=self.channelsNames[1])
            ax.legend()
            ax.set_title(self.filename)
            ax.set_xlabel(time_label+' [s]')
        else:
            fig, ax = plt.subplots(nrows=(self.n_channels-1), ncols=1)
            fig.canvas.mpl_connect('key_press_event', self.on_press)
            for i in np.arange(self.n_channels-1):
                ax[i].plot(time, self.channels[i+1], label=self.channelsNames[i+1])
                ax.legend()
            ax[0].set_title(self.filename)
            ax[i].set_xlabel(time_label+' [s]')
        
        return 0

    def plotPowerSpectrum(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
        
        fig, ax = plt.subplots(nrows=1, ncols=1)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        f, Pxx_spec = signal.periodogram(self.channels[1], self.sampling_rate, 'flattop', scaling='spectrum')
        ax.axes.semilogy(f, np.sqrt(Pxx_spec),label=self.channelsNames[1])
        ax.legend()
        ax.set_title(self.filename)
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('Linear spectrum [V RMS]')
            
        return 0
        
    def on_press(self, event):
        # print('press', event.key)
        sys.stdout.flush()
        
        if event.key == 'x':
            plt.close('all')
        else:
            pass
                
        return 0

