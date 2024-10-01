import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from class_emg_filtering import Reading_EMG
import patients_info as emg_files

def main(args):
    path_emg = '../../data/data_Xavier/emg/'
    path_kin = '../../data/data_Xavier/kinematics/'

    list_subjects = ['N1','N2','N3','N4','N5','S1','S2','S3','S4','S5','S6','S7','S8','S9','XG','XL','PT',]

    for id in list_subjects:
        folder = emg_files.subject_dir[id]
        # print(f'{id}:{folder}')
        files = emg_files.files_list[id]
        # print(f"{id}:{files['a_ac']}")


    # obj_emg = Reading_EMG(path_emg, filename_emg, file_channels)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))