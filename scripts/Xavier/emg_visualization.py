import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from class_emg_filtering import Reading_EMG
import patients_info as emg_files

def main(args):
    path_emg = '../../data/data_Xavier/emg/'
    path_kin = '../../data/data_Xavier/kinematics/'

    subjects_list = ['N1','N2','N3','N4','N5','S1','S2','S3','S4','S5','S6','S7','S8','S9','XG','XL','PT',]
    files_subjects={
        'N1':['a_ac','a_bl','a_05','a_10','a_15','a_20','a_25','c_bl','c_05','c_10','c_15','c_20','c_25',],
        'N2':['a_bl','a_05','a_10','a_15','a_20','a_25','c_bl','c_05','c_10','c_15','c_20','c_25','c_30',],
        'N3':['a_bl','a_05','a_10','a_15','a_25','a_bl2','c_bl','c_05','c_10','c_15','c_20','c_25','c_bl2',],
        'N4':[],
        'N5':['a_ac','a_bl','a_05','a_10','a_15','a_20','a_25','a_30',],
        'S1':['a_bl','a_05','c_bl','c_01','c_05','c_10','c_15','c_20','c_25','c_30',],
        'S2':['a_bl','a_05','a_10','c_bl','c_05','c_10','c_15a',],
        'S3':['a_bl','a_01','a_05','a_14','a_15','a_20','a_25','a_28','a_29','c_bl','c_01','c_05sa','c_10','c_10_1','c_15','c_18a','c_20','c_25',],
        'S4':['a_bl','a_01','a_05','a_10','a_10_1','a_15','a_18a','a_20','a_25','a_29','a_bl','a_05','a_15','a_20','a_25','a_29a',],
        'S5':['a_bl','a_01','a_05','a_10','a_15','a_20','c_bl','c_01','c_05','c_10','c_15','c_20',],
        'S6':['a_bl','a_07','a_10','a_15','a_20','a_25','a_29','c_bl','c_02','c_05','c_10','c_15','c_20','c_25','c_29',],
        'S7':['a_bl','a_05','a_10','a_15','a_20','a_25','a_29','c_bl','c_05','c_10','c_15','c_20','c_25','c_29',],
        'S8':['a_bl','a_05','a_10','a_15','a_20','a_25','a_29','c_bl','c_05','c_10','c_15','c_20','c_25','c_29',],
        'S9':['a_bl','a_01','a_05','a_10','a_15','a_20','a_25','a_29a',],
        'XG':['a_bl','a_05','a_10','a_20','a_30',],
        'XL':['a_bl','a_05','a_10','a_15','a_20','a_25','a_30',],
        'PT':['a_bl','a_05','a_10','a_15','a_20','a_25','a_29','c_bl','c_02','c_05','c_10','c_15','c_20a','c_25',],
    }

    for id in subjects_list:
        folder = emg_files.subject_dir[id]
        # print(f'{id}:{folder}')
        files = emg_files.files_list[id]
        # print(f"{id}:{files['a_ac']}")


    # obj_emg = Reading_EMG(path_emg, filename_emg, file_channels)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))