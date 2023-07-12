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

    def __init__(self, path, filename, day_number):

        self.path=''
        self.filename=[]
        self.sampling_rate=1.0
        self.n_channels=1
        self.channels=[]
        self.channelsNames=[]
        
        # self.channelsRef = {0:'Tb Ant RT, uV', 1:'VL LT, uV', 2:'Gastroc LT, uV', 3:'VM RT, uV', 4:'Tb Ant LT, uV', 5:'Gastroc RT, uV', 6:'VM LT, uV', 7:'VL RT, uV'}
        self.dict_namesChannels1 ={'time':'Time',
                                'tbart':'Tb Ant RT, uV', 
                                 'vllt':'VL LT, uV', 
                                  'glt':'Gastroc LT, uV', 
                                 'vmrt':'VM RT, uV', 
                                'tbalt':'Tb Ant LT, uV',
                                  'grt':'Gastroc RT, uV', 
                                 'vmlt':'VM LT, uV', 
                                 'vlrt':'VL RT, uV'}
                                 
        self.dict_namesChannels2 = {'time':'Time',
                                     'tart':'TIB.ANT. RT, uV',
                                    'vmolt':'VMO LT, uV',
                                     'talt':'TIB.ANT. LT, uV',
                                     'lglt':'LAT. GASTRO LT, uV',
                                    'vlolt':'VLO LT, uV',
                                     'lgrt':'LAT. GASTRO RT, uV',
                                    'vlort':'VLO RT, uV',
                                    'vmort':'VMO RT, uV'}
                                    
        self.dict_namesChannels3 = {'time':'Time',
                                    'tbart':'TBA RT, uV',
                                     'vllt':'VLO LT, uV',
                                      'glt':'LAT. GASTRO LT, uV',
                                     'vmrt':'VMO RT, uV',
                                    'tbalt':'TBA LT, uV',
                                      'grt':'Noraxon Ultium.EMG 6, uV',
                                     'vmlt':'VMO LT, uV',
                                     'vlrt':'VLO RT, uV'}
    
        self.dict_namesChannels4 = {'time':'Time',
                                    'tbart':'Noraxon Ultium.EMG 1, uV',
                                     'vllt':'VLO LT, uV',
                                      'glt':'LAT. GASTRO LT, uV',
                                     'vmrt':'VMO RT, uV',
                                    'tbalt':'Noraxon Ultium.EMG 5, uV',
                                      'grt':'LAT. GASTRO RT, uV',
                                     'vmlt':'VMO LT, uV',
                                     'vlrt':'Noraxon Ultium.EMG 8, uV'}
                                     
        self.dict_namesChannels5 = {'time':'Time',
                                    'slt' :'SOLEUS LT, uV',
                                    'talt':'TIB.ANT. LT, uV',
                                    'tart':'TIB.ANT. RT, uV',
                                    'rfrt':'RECTUS FEM. RT, uV',
                                    'rflt':'RECTUS FEM. LT, uV',
                                    'srt' :'SOLEUS RT, uV',
                                    'vlrt':'VLO RT, uV',
                                    'vllt':'VLO LT, uV'}
    
    
    
        self.path = path
        self.filename = filename
        self.day_number = day_number
    
        mat = scipy.io.loadmat(self.path+self.filename)
        print(self.filename)
        print('File content:',  mat['__header__'])
        self.sampling_rate = mat['samplingRate'][0,0]
        # print(f'sample rate: {self.sampling_rate}')
        ## plus one to include the Time channel (channel 0)
        self.n_channels = mat['noChans'][0,0]+1
        # self.n_channels = 9
        
        # print(f'self.n_channels {self.n_channels}')
        
        self.channels = np.empty((self.n_channels, 0)).tolist()
        self.channelsNames = np.empty((self.n_channels, 0)).tolist()

        for i in np.arange(self.n_channels):
        # for name_ch in self.dict_namesChannels:
            self.channels[i] = mat['Data'][0,i].flatten()
            self.channelsNames[i] = mat['channelNames'][0][i][0]
        
        header = mat['__header__']
        header = header.decode('ASCII')
        header = header.split()
        self.date = header[7] +' '+header[8]+' '+header[10] 
        print(self.date)
        
        print(f'self.channelsNames {self.channelsNames}')
        
                
    
    def smoothingRMS(self, window_size):
        
        ## window size in mili-seconds
        window_samples = int(self.sampling_rate * window_size*1e-3)
        # print('sampling_rate, window_samples: ', self.sampling_rate, window_samples)
        window = np.ones(window_samples)/float(window_samples)
        ## we excluded 'Time' and 'Switch' channels (first and last channels)
        self.channels_rms = np.empty((self.n_channels-2, 0)).tolist()
        i=0
        for ch in self.channels[1:-1]:
            ## RMS window smoothing
            self.channels_rms[i] = np.sqrt(np.convolve(ch**2, window, 'same'))
            i+=1
        
        return 0


    def plotSignals(self, file_number):
        
        channels_names1=['vmrt','vlrt','vmlt','vllt']
        channels_names2=['vmort','vlort','vmolt','vlolt',]
        channels_names3=['vmrt','vlrt','vmlt','vllt']
        channels_names4=['vmrt','vlrt','vmlt','vllt']
        channels_names5=['rfrt','vlrt','rflt','vllt']
        
        if file_number == '003' or file_number == '004' or file_number == '006':
            selected_names = channels_names2
            selected_dict  = self.dict_namesChannels2
        elif file_number == '018' and self.filename=='EBC018_S3_E3.mat':
            selected_names = channels_names2
            selected_dict  = self.dict_namesChannels2
        elif file_number == '018' and self.filename=='EBC018_S12_e3.mat':
            selected_names = channels_names4
            selected_dict  = self.dict_namesChannels4
        elif file_number == '024' and self.filename=='EBC24-S4-E3.mat':
            selected_names = channels_names3
            selected_dict  = self.dict_namesChannels3
        elif (file_number == '024' and self.filename=='EBC024S13e3.mat') or file_number == '030' or file_number == '031' or file_number == '032' or file_number == '033' or file_number == '037' or file_number == '042':
            selected_names = channels_names1
            selected_dict  = self.dict_namesChannels1
        elif file_number == '045' and self.filename=='EBC45-S2-25min.mat':
            selected_names = channels_names5
            selected_dict  = self.dict_namesChannels5
        elif file_number == '045' and self.filename=='EBC045S14e3.mat':
            selected_names = channels_names2
            selected_dict  = self.dict_namesChannels2
        else:
            return 0
        
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
        
        # print(f'filename: {self.filename}')
        
        # ## we exclude Time channel and Swich channel (first and last channels)
        fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True, sharey=True)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        # name = channels_names[1]
        # channel_name = self.dict_namesChannels[name]
        # if channel_name in self.channelsNames:
            # selected_names = channels_names
            # selected_dict  = self.dict_namesChannels
        # else:
            # pass
        
        # name = channels_names2[1]
        # channel_name = self.dict_namesCannnels2[name]
        # if channel_name in self.channelsNames:
            # selected_names = channels_names2
            # selected_dict  = self.dict_namesCannnels2
        # else:
            # pass
        
        # name = channels_names3[1]
        # channel_name = self.dict_namesCannnels3[name]
        # if channel_name in self.channelsNames:
            # selected_names = channels_names3
            # selected_dict  = self.dict_namesCannnels3
        # else:
            # pass

        # name = channels_names4[1]
        # channel_name = self.dict_namesCannnels4[name]
        # if channel_name in self.channelsNames:
            # selected_names = channels_names4
            # selected_dict  = self.dict_namesCannnels4
        # else:
            # print('Channels not found.')
            # return 0
           
        list_data = []
        list_labels=[]
        list_data.append(time)
        list_labels.append(time_label)
        
        
        cont=0
        for name in selected_names:
            if name in selected_dict:
                channel_name = selected_dict[name]
                id_signal = self.channelsNames.index(channel_name)
                # print(f'channel_name and id_signal: {channel_name}, {id_signal}')
                
                ax[cont].plot(time, self.channels[id_signal], label=channel_name)
                ax[cont].legend(loc='lower right')
                cont+=1
                
                list_data.append(self.channels[id_signal])
                list_labels.append(channel_name)
                
        
        ## 5 seconds x axis
        # print('time:', self.sampling_rate, len(time), np.min(time), np.max(time))

        ## we select 5 seconds in the middle of the recordings for visualization
        id01 = (len(time)/2 - (self.sampling_rate*2.5)).astype(int)
        id02 = (id01 + (self.sampling_rate*5)).astype(int)        
        
        ax[0].set_xlim([time[id01],time[id02]])
        ax[0].set_ylim([-300,300])
        ax[0].set_title('P'+file_number+' - day '+self.day_number)
        ax[cont-1].set_xlabel(time_label+' [s]')
        
        return list_data, list_labels
        
    
    def plotEMG(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
        ## we exclude Time channel and Swich channel (first and last channels)
        fig, ax = plt.subplots(nrows=(len(self.channels)-2), ncols=1, sharex=True, sharey=True)
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        cont=0
        for ch, ch_n in zip(self.channels[1:-1], self.channelsNames[1:-1]):
            ax[cont].plot(time, ch, label=ch_n)
            ax[cont].legend()
            cont+=1
        
        ax[0].set_ylim([-500,500])
        ax[0].set_title(self.filename)
        ax[cont-1].set_xlabel(time_label+' [s]')
        
        return 0

    def plotPowerSpectrum(self):
        
        time = self.channels[0]
        time_label = self.channelsNames[0]
        ## we exclude Time channel and Swich channel (first and last channels)
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
        ## we exclude Time channel and Swich channel (first and last channels)
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
        
    def getSignal(self, muscle):
        ## channels[0] is the time
        if muscle in self.dict_namesChannels:
            channel_name = self.dict_namesChannels[muscle]
            id_signal = self.channelsNames.index(channel_name)
            
            # return self.channels[0], self.channels[num_muscle+1], self.channelsNames[num_muscle+1]
            return self.channels[0], self.channels[id_signal], self.channelsNames[id_signal]
        else:
            print(f'\n{muscle} muscle was not found.\n')
            return 0,0, muscle+' was not found'


    def getSamplingRate(self):
        return self.sampling_rate
