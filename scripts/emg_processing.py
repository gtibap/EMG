from class_emg import Processing_EMG
import numpy as np
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt


def main(args):
    # print('EMG processing')
    
    flag = int(args[1])
    
    if flag==1:
        path='../data/h-ref_matlab_legacy/'
        files=['H-Reflexe.mat','H-Reflexe-1.mat']
        
    elif flag==2:
        path='../data/emg_noraxon/matlab/'
        files=['EBC040S1-Baseline1.mat','EBC040S1e1.mat','EBC040S1e2.mat','EBC040S1e3.mat', 'EBC040S1-Baseline2.mat']
    
    else:
        return 0

    list_objs = []
    ## read data. Each file .mat has several channels. We read data from every file in the class 'Processing_EMG'; we create an object for each file; all the created objects are in 'list_objs'
    for filename in files:
        list_objs.append(Processing_EMG(path,filename))
        
    # for obj_emg in list_objs:
        # obj_emg.plotEMG()
        # obj_emg.plotPowerSpectrum()

    num = 0

    list_objs[num].plotEMG()
    # window size in mili-seconds
    window_size=100 # ms
    list_objs[num].smoothingRMS(window_size)
    list_objs[num].plotEMG_smoothed()

    plt.ion()
    plt.show(block=True)

    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
