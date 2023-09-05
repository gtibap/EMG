#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  emg_filtering.py
#  

import argparse
from class_emg_filtering import Reading_EMG
import matplotlib.pyplot as plt
import sys

def main(args):
    
    # Initialize parser
    parser = argparse.ArgumentParser(description = 'EMG filtering')

    # Adding optional argument
    parser.add_argument('-d', '--dir_name', type = str, help = "Select directory, for example: EBC032/EBC033/")
    parser.add_argument('-p', '--patient_number', type = str, help = "Select file number, for example: 033")
    
    parser.add_argument('-f', '--file_number', type = str, help = "Select file number, for example: 0")
    
    parser.add_argument('-s', '--signal_number', type = str, help = "Select signal number, for example: 0")
    
    args = parser.parse_args()

    path=args.dir_name
    patient_number=args.patient_number
    file_number=int(args.file_number)
    signal_number=int(args.signal_number)
    
    print(f'path and files: {path}, {patient_number}, {file_number}')
    
    list_files_names = { # '003':['EBC003-J1.mat','EBC003-S7.1.mat','EBC003-S7.2.mat','EBC003-J14.mat'],
                        # '037':['EBC37_S1_BASELINE1.mat','EBC037_S2_BASELINE2.mat', 'EBC037_S2_E1.mat','EBC037_S2_E2.mat','EBC037_S2_E3.mat', 'EBC037S7-Baseline1.mat','EBC037S7e1.mat','EBC037S7e2.mat','EBC037S7e3.mat','EBC037_S14_BASELINE1.mat','EBC037_S14_BASELINE2.mat','EBC037_S14_E1.mat','EBC037_S14_E2.mat','EBC039S14E2.mat','EBC037S14E3.mat'],
                        '':[],
                        '001':['EBC-PATIENT 2-1.mat','EBC-PATIENT 1 S7.mat'],
                        '003':['EBC003-J1.mat','EBC003-J14.mat'],
                        '004':['EBC004-S1.mat','EBC004 S6.mat','EBC004  J13.mat'],
                        '006':['EBC 006 S1 E3.mat','EBC006 s15 e3.mat'],
                        '009':['ebc_009 _s01_e3.mat','ebc_009 _s08_e3.mat','ebc_009 _s14_e3.mat'],
                        '012':['ebc_012 _s02_e3.mat','ebc_012 _s07_e3.mat'],
                        '018':['EBC018_S3_E3.mat','EBC018_S8_E3.mat','EBC018_S12_e3.mat'],
                        '019':['ebc_019_s01_e3.mat','ebc_019_s10_e3.mat','ebc_019_s14_e3.mat'],
                        '022':['ebc_022_s02_e3.mat'],
                        '024':['EBC24-S4-E3.mat','EBC24_s9_E3.mat','EBC024S13e3.mat'],
                        '027':['ebc_027_s02_e3.mat','ebc_027_s07_e3.mat','ebc_027_s14_e3.mat'],
                        '028':['ebc_028_s01_e3.mat','ebc_028_s07_e3.mat','ebc_028_s14_e3.mat'],
                        '029':['ebc_029_s02_e3.mat','ebc_029_s09_e3.mat', 'ebc_029_s14_e3.mat'],
                        '030':['EBC030_S1_E3.mat','EBC030_S7_E3.mat','EBC30_S14_E3.mat'],
                        '031':['EBC031_s2_e3.mat','EBC031S7e3.mat','EBC031_s14_e3.mat'],
                        '032':['EBC032_s1_e3.mat','EBC032S7e3.mat','EBC032S14e3.mat'],
                        '033':['EBC033S3e3.mat','EBC033_S7_E3.mat','EBC033S14e3.mat'],
                        '037':['EBC037_S2_E3.mat','EBC037S14E3.mat'],
                        # '042':['EB042S730MIN.mat'],
                        '045':['EBC45-S2-25min.mat','EBC045S14e3.mat'],
                        # 'test':['test2-config1.mat','test3-config2.mat'],
                        }
    
      
                        
    ## ids of the eight required channels: muscular signals EMG without the insole signals
    list_ids_channels = {'001':[[9,16]]*2,
                         '003':[[9,16]]*4,
                         '006':[[9,16]]*2,
                         '004':[[9,16]]*3,
                         '006':[[9,16]]*2,
                         '018':[[9,16],[9,16],[1,8]],
                         '024':[[9,16]]*3,
                         '030':[[9,16],[1,8],[1,8]],
                         '031':[[1,8],[9,16],[1,8]],
                         '032':[[9,16],[1,8],[1,8]],
                         '033':[[1,8]]*2,
                         '037':[[1,8]]*2,
                         '042':[[1,8]]*2,
                         '045':[[9,16]]*2,
                        }
                        
    
                        
    files = list_files_names[patient_number]
    ids_channels = list_ids_channels[patient_number]
    
    filename = files[file_number]
    file_channels = ids_channels[file_number]
    
    print(f'files: {files}')
    print(f'channels: {ids_channels}')
    
    print(f'selected file: {filename}, channels: {file_channels}')
    
    obj_emg = Reading_EMG(path, filename, file_channels)
    ch_names = obj_emg.getChannelsNames()
    print(f'names: {ch_names}')
    
    obj_emg.plotSignals()
    obj_emg.plotSelectedSignal(signal_number)
    
    # ## open files
    # list_objs = []
    # ## read emg-signals from all recordings of a selected session
    # for num_rec, filename in enumerate(files):
        # print(f'filename: {filename}')
        # list_objs.append(Reading_EMG(path,filename, list_ids_channels[file_number][0]))
    
    # list_objs[0].plotSignals()
    
    plt.ion()
    plt.show(block=True)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
