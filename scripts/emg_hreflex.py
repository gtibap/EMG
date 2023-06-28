from class_emg_hreflex import Processing_EMG
import numpy as np
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt


def main(args):
    # print('EMG processing')
    
    path='../data/h-ref_matlab_legacy/'
    files=['H-Reflexe.mat','H-Reflexe-1.mat']

    num_file = int(args[1])

    ## read data. Each file .mat has several channels. We read data from every file in the class 'Processing_EMG'; we create an object for a selected file (num_file)
    
    obj_emg = Processing_EMG(path,files[num_file])
    
    # ## window size in mili-seconds
    window_size=5 # ms    
    obj_emg.smoothingRMS(window_size)
    
    numChannels=obj_emg.n_channels
    for num in np.arange(numChannels-1):
        obj_emg.plotEMG_smoothed(num)

    plt.ion()
    plt.show(block=True)


    # print('selected channel out of the recordings.')
    # print(f'Max. number of channels, n={self.n_channels-1} ([0,n-1])')

    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
