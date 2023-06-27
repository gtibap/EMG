#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt
import pyemgpipeline as pep


def plotChannels(channels, channelsNames, filename):
        
        time = channels[0]
        time_label = channelsNames[0]
        ## minus 1 because the first is the Time channel
        
        if len(channels)==2:
            fig, ax = plt.subplots(nrows=len(channels)-1, ncols=1)
            fig.canvas.mpl_connect('key_press_event', on_press)
            ax.plot(time, channels[1], label=channelsNames[1])
            ax.legend()
            ax.set_title(filename)
            ax.set_xlabel(time_label)
        else:
            fig, ax = plt.subplots(nrows=len(channels)-2, ncols=1, sharex=True, sharey=True)
            fig.canvas.mpl_connect('key_press_event', on_press)
            cont=0
            for ch, ch_n in zip(channels[1:-1], channelsNames[1:-1]):
                ax[cont].plot(time, ch, label=ch_n)
                ax[cont].legend()
                cont+=1
            
            ax[0].set_title(filename)
            ax[cont-1].set_xlabel(time_label)
        
        return 0

def on_press(event):
    # print('press', event.key)
    sys.stdout.flush()
    
    if event.key == 'x':
        plt.close('all')
    else:
        pass
            
    return 0
         

def main(args):
    
    flag = int(args[1])
    
    if flag==1:
        path='../data/h-ref_matlab_legacy/'
        files=['H-Reflexe.mat','H-Reflexe-1.mat']
        
    elif flag==2:
        path='../data/emg_noraxon/matlab/'
        files=['EBC040S1-Baseline1.mat','EBC040S1e1.mat','EBC040S1e2.mat','EBC040S1e3.mat', 'EBC040S1-Baseline2.mat']
        
    else:
        return 0
    
    signals_files=[]

    for filename in files:
        mat = scipy.io.loadmat(path+filename)
        sampling_rate = mat['samplingRate'][0,0]
        ## plus one to jump the time
        noChans = mat['noChans'][0,0]+1
        
        channels = np.empty((noChans, 0)).tolist()
        channelsNames = np.empty((noChans, 0)).tolist()

        for i in np.arange(noChans):
            channels[i] = mat['Data'][0,i].flatten()
            channelsNames[i] = mat['channelNames'][0][i][0]
            
        signals_files.append([channels, channelsNames])
        plotChannels(np.array(channels),np.array(channelsNames), filename)

    plt.ion()
    plt.show(block=True)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
