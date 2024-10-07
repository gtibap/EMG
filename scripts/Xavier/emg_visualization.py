import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from class_emg_filtering import Reading_EMG
import patients_info as emg_files

def main(args):
    path_emg = '../../data/data_Xavier/emg/'
    path_out = '../../data/data_Xavier/emg/figures/'
    path_kin = '../../data/data_Xavier/kinematics/'

    # subjects_list = ['N1','N2','N3','N4','N5','S1','S2','S3','S4','S5','S6','S7','S8','S9','XG','XL','PT',]
    # files_subjects={
    #     'N1':['a_ac','a_bl','a_05','a_10','a_15','a_20','a_25','c_bl','c_05','c_10','c_15','c_20','c_25',],
    #     'N2':['a_bl','a_05','a_10','a_15','a_20','a_25','c_bl','c_05','c_10','c_15','c_20','c_25','c_30',],
    #     'N3':['a_bl','a_05','a_10','a_15','a_25','a_bl2','c_bl','c_05','c_10','c_15','c_20','c_25','c_bl2',],
    #     'N4':[],
    #     'N5':['a_ac','a_bl','a_05','a_10','a_15','a_20','a_25','a_30',],
    #     'S1':['a_bl','a_05','c_bl','c_01','c_05','c_10','c_15','c_20','c_25','c_30',],
    #     'S2':['a_bl','a_05','a_10','c_bl','c_05','c_10','c_15a',],
    #     'S3':['a_bl','a_01','a_05','a_14','a_15','a_20','a_25','a_28','a_29','c_bl','c_01','c_05sa','c_10','c_10_1','c_15','c_18a','c_20','c_25',],
    #     'S4':['a_bl','a_01','a_05','a_10','a_10_1','a_15','a_18a','a_20','a_25','a_29','a_bl','a_05','a_15','a_20','a_25','a_29a',],
    #     'S5':['a_bl','a_01','a_05','a_10','a_15','a_20','c_bl','c_01','c_05','c_10','c_15','c_20',],
    #     'S6':['a_bl','a_07','a_10','a_15','a_20','a_25','a_29','c_bl','c_02','c_05','c_10','c_15','c_20','c_25','c_29',],
    #     'S7':['a_bl','a_05','a_10','a_15','a_20','a_25','a_29','c_bl','c_05','c_10','c_15','c_20','c_25','c_29',],
    #     'S8':['a_bl','a_05','a_10','a_15','a_20','a_25','a_29','c_bl','c_05','c_10','c_15','c_20','c_25','c_29',],
    #     'S9':['a_bl','a_01','a_05','a_10','a_15','a_20','a_25','a_29a',],
    #     'XG':['a_bl','a_05','a_10','a_20','a_30',],
    #     'XL':['a_bl','a_05','a_10','a_15','a_20','a_25','a_30',],
    #     'PT':['a_bl','a_05','a_10','a_15','a_20','a_25','a_29','c_bl','c_02','c_05','c_10','c_15','c_20a','c_25',],
    # }

    subjects_list = ['S2','S3','S4','S9',]
    files_subjects={
        'S2':['a_bl','a_05','a_10','c_bl','c_05','c_10','c_15a',],
        'S3':['a_bl','a_01','a_05','a_14','a_15','a_20','a_25','a_28','a_29','c_bl','c_01','c_05sa','c_10','c_10_1','c_15','c_18a','c_20','c_25',],
        'S4':['a_bl','a_01','a_05','a_10','a_10_1','a_15','a_18a','a_20','a_25','a_29','a_bl','a_05','a_15','a_20','a_25','a_29a',],
        'S9':['a_bl','a_01','a_05','a_10','a_15','a_20','a_25','a_29a',],
        }


    # for id in subjects_list:
    #     folder = emg_files.subject_dir[id]+'/'
    #     # print(f'{folder}')
    #     files = emg_files.files_list[id]

    #     for idx in files_subjects[id]:
    #         print(f"{folder+files[idx]}")
    #     print(f'\n')
        # folder+files[idx]
        # id_list = files_subjects[id]
        # files

    # open file emg signals
    ## selection patient and section of emg data recording
    id_patient = 'S2'   ## patient S1

    sections_list = ['a_bl','a_05','a_10',]
    # sections_list = ['c_bl','c_05','c_10','c_15a',]

    # section = 'c_15a' # 'c_15a' -> couché 15min active, 'a_bl' -> assis baseline 
    # ids_emg = [3,1,5,2,0,4]

    folder = emg_files.subject_dir[id_patient]+'/'
    files = emg_files.files_list[id_patient]
    idx_channels = emg_files.files_channels[id_patient]
    chx_order = emg_files.signals_order[id_patient]
    fig_titles = emg_files.signals_title[id_patient]
    files_png = emg_files.filenames_figures[id_patient]

    for section in sections_list:

        filename = folder + files[section]
        channels = idx_channels[section]
        ids_emg = chx_order[section]
        title = fig_titles[section]
        out_filename = files_png[section]

        out_filename = path_out + out_filename
        
        print(f'filename: {filename}')
        print(f'channels: {channels}')
        print(f'ids_emg: {ids_emg}')

        ## reading emg data
        obj_emg = Reading_EMG(path_emg, filename, channels)
        channels_names = obj_emg.getChannelsNames()
        print(f'channels_names: {channels_names}')

        obj_emg.filteringSignals()
        obj_emg.envelopeFilter()

        # obj_emg.plotSignals()
        obj_emg.plotSignalsFiltered()
        obj_emg.plotSignalsFiltered_ordered(ids_emg, title, out_filename)
    
    
    plt.show()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))