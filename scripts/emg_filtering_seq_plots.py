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
                        # '':[],
                        '001':['EBC-PATIENT 1 S7.mat'],
                        '002':['EBC-PATIENT 2-1.mat','EBC002-S1.mat'],
                        '003':['EBC003-J1.mat','EBC003-J14.mat'],
                        '004':['EBC004-S1.mat','EBC004 S6.mat','EBC004  J13.mat'],
                        # '004':['EBC004-S1.mat','EBC004 S6.mat','EBC004  J13.mat'],
                        '006':['EBC 006 S1 E3.mat','EBC 006 S8 E3.mat','EBC006 s15 e3.mat'],
                        '009':['ebc_009 _s01_e3.mat','ebc_009 _s08_e3.mat','ebc_009 _s14_e3.mat'],
                        '012':['ebc_012 _s02_e3.mat','ebc_012 _s07_e3.mat'],
                        '015':['ebc_015 _s02_e3.mat','ebc_015 _s07_e3.mat','ebc_015 _s13_e2.mat'],
                        # '018':['EBC018_S3_E3.mat','EBC018_S8_E3.mat','EBC018_S12_e3.mat'],
                        '018':['EBC018-s3-e1.mat','EBC018_S2_E2.mat','EBC018_S3_E3.mat'],
                        
                        '019':['ebc_019_s01_e3.mat','ebc_019_s10_e3.mat','ebc_019_s14_e3.mat'],
                        '022':['ebc_022_s02_e3.mat'],
                        '024':['EBC24-S4-E3.mat','EBC24_s9_E3.mat','EBC024S13e3.mat'],
                        '027':['ebc_027_s02_e3.mat','ebc_027_s07_e3.mat','ebc_027_s14_e3.mat'],
                        '028':['ebc_028_s01_e3.mat','ebc_028_s07_e3.mat','ebc_028_s14_e3.mat'],
                        '029':['ebc_029_s02_e3.mat','ebc_029_s09_e3.mat', 'ebc_029_s14_e3.mat'],
                        '030':['EBC030_S1_E3.mat','EBC030_S7_E3.mat','EBC30_S14_E3.mat'],
                        
                        # '031':['EBC031_Baseline2.mat','EBC031_baseline1.mat','EBC Bed cycling_test.mat'],
                        # '031':['EBC031_s2_e1.mat','EBC031_s2_e2.mat','EBC031_s2_e3.mat','EBC031_s2_baseline2'],
                        # '031':['EBC031_baseline1.mat','EBC031_Baseline2.mat',],
                        '031':['EBC031S7e1.mat','EBC031_s7e2.mat','EBC031S7e3.mat'],
                        # '031':['EBC031_s2_e1.mat','EBC031_s2_e2.mat','EBC031_s2_e3.mat'],
                        
                        # '031':['EBC031S7e1.mat','EBC031_s7e2.mat','EBC031S7e3.mat'],
                        # '031':['EBC031_S14_E1.mat','EBC031S14e2.mat','EBC031_s14_e3.mat'],
                        # '031':['EBC031_s2_e3.mat','EBC031S7e3.mat','EBC031_s14_e3.mat'],
                        # '032':['EBC032_s1_e3.mat','EBC032S7e3.mat','EBC032S14e3.mat'],
                        '032':['EBC032_S1_e1.mat','EBC032_S1_E2.mat','EBC032_s1_e3.mat'],
                        # '032':['EBC032_s1_e3.mat','EBC032S7e3.mat','EBC032S14e3.mat'],
                        # '032':['EBC032_s1_e3.mat','EBC032S7e3.mat','EBC032S14e3.mat'],
                        
                        '033':['EBC033S3e3.mat','EBC033_S7_E3.mat','EBC033S14e3.mat'],
                        # '037':['EBC037_S2_E3.mat','EBC037S7e3.mat','EBC037S14E3.mat'],
                        '037':['EBC037_S14_E1.mat','EBC037_S14_E2.mat','EBC037S14E3.mat'],
                        # '039':['EBC039S1E3.mat','EBC039s7e3.mat','EBC039S14e3.mat'],
                        '039':['EBC039_S2_E1.mat','ebc039S1E2.mat','EBC039S1E3.mat'],
                        # '039':['EBC039_S2_E1.mat','ebc039S1E2.mat','EBC039S1E3.mat'],
                        
                        '040':['ebc_040_s01_e3.mat','ebc_040_s07_e3.mat','ebc_040_s14_e3.mat'],
                        '042':['EB042S730MIN.mat'],
                        # '045':['EBC45-S2-25min.mat','EBC045S14e3.mat'],
                        '045':['EBC45-S2-5min.mat','EBC45-S2-30min.mat','EBC45-S2-25min.mat'],
                        '046':['ebc_046_s01_e3.mat','ebc_046_s06_e2_20min.mat','ebc_046_s13_e3.mat'],
                        '048':['ebc_048_s01_e3.mat','ebc_048_s07_e3.mat','ebc_048_s14_e3.mat'],
                        '052':['ebc_052_s01_e3.mat','ebc_052_s07_e3.mat','ebc_052_s14_e3.mat'],
                        '053':['ebc_053_s01_e3.mat','ebc_053_s07_e3.mat','ebc_053_s14_e3.mat'],
                        '054':['ebc_054_s01_e3.mat','ebc_054_s14_e3.mat'],
                        '056':['ebc_056_s01_e3.mat'],
                        '057':['ebc_057_s01_e3.mat','ebc_057_s07_e4.mat','ebc_057_s14_e4.mat'],
                        '058':['ebc_058_s01_e3.mat','ebc_058_s07_e2_25min.mat','ebc_058_s14_e2_25min.mat'],
                        '056':['ebc_056_s01_e3.mat'],
                        '059':['ebc_059_s07_e3.mat','ebc_059_s14_e3.mat'],
                        '060':['EBC060-25MIN.mat','EBC060-S14-15MIN.mat'],
                        # 'test':['test2-config1.mat','test3-config2.mat'],
                        }
    
    ## Documents/EMG/docs/figures/sep06_2023/  
                        
    ## ids of the eight required channels: muscular signals EMG without the insole signals
    list_ids_channels = {'001':[[9,16]]*1,
                         '002':[[9,16]]*2,
                         '003':[[9,16]]*2,
                         '004':[[9,16]]*3,
                         '006':[[9,16]]*3,
                         '009':[[9,16]]*3,
                         '012':[[9,16]]*2,
                         '015':[[9,16]]*3,
                         '018':[[9,16],[9,16],[9,16],[1,8]],
                         '019':[[9,16]]*3,
                         '022':[[9,16]],
                         '024':[[9,16]]*3,
                         '027':[[9,16]]*3,
                         '028':[[9,16]]*3,
                         '029':[[9,16]]*3,
                         '030':[[9,16],[1,8],[1,8]],
                         
                         # '031':[[1,8],[1,8],[1,8],[1,8]],
                         '031':[[9,16],[9,16],[9,16]],
                         # '031':[[1,8],[9,16],[1,8]],
                         # '031':[[9,16],[9,16],[9,16]],
                         # '032':[[9,16],[1,8],[1,8]],
                         '032':[[9,16],[9,16],[9,16]],
                         '033':[[1,8]]*3,
                         '037':[[1,8]]*3,
                         '039':[[1,8]]*3,
                         '040':[[1,8]]*3,
                         '042':[[1,8]],
                         '045':[[9,16]]*3,
                         '046':[[9,16]]*3,
                         '048':[[1,8]]*3,
                         '052':[[1,8]]*3,
                         '053':[[1,8]]*3,
                         '054':[[1,8]]*2,
                         '056':[[9,16]],
                         '057':[[9,16]]*3,
                         '058':[[9,16]]*3,
                         '059':[[9,16]]*2,
                         '060':[[9,16]]*2,
                        }
    
    ## sorting plots to present each lead in the same place                    
    list_emg_sorted = {'001':[[7,0,6,4,2,5,3]]*1,
                       '002':[[7,0,6,4,2,5,3]]*2,
                       '003':[[5,7,3,0,6,4,2,1]]*2,
                       '004':[[5,7,3,0,6,4,2,1]]*3,
                       '006':[[5,7,3,0,6,4,2,1]]*3,
                       '015':[[5,7,3,0,6,4,2,1],[5,7,3,0,6,4,2,1],[5,7,3,0,4,2,1,6]],
                       '018':[[7,2,4,1,6,5,0,3]]*3,
                       '024':[[7,2,4,1,6,5,0,3]]*3,
                       '027':[[7,2,4,1,6,5,0,3]]*3,
                       '030':[[7,2,4,1,6,5,0,3]]*3,
                       '031':[[7,2,4,1,6,5,0,3]]*4,
                       '032':[[7,2,4,1,6,5,0,3]]*3,
                       '033':[[7,2,4,1,6,5,0,3]]*3,
                       '037':[[7,2,4,1,6,5,0,3],[7,2,4,1,6,5,0,3],[2,4,1,6,5,0,3]],
                       '039':[[7,2,4,1,6,5,0,3]]*3,
                       '042':[[0,6,5,7,2,4,3,1]],
                       '045':[[4,6,7,1,0,5,3,2],[5,3,7,1,4,0,6,2]],
                       '048':[[5,3,7,1,4,0,6,2],[6,2,0,4,7,3,1,5],[7,5,3,1,2,0,6,4]],
                       '052':[[2,4,0,6,3,1,5,7]]*3,
                       '053':[[2,4,0,6,3,1,5,7]]*3,
                       '054':[[2,4,0,6,3,1,5,7]]*2,
                       '058':[[2,4,0,6,3,1,5,7]]*3,
                       '056':[[7,5,1,3,6,4,0,2]],
                       '059':[[7,5,1,3,6,4,0,2]]*2,
                       '060':[[7,5,1,3,6,4,0,2]]*2,
                       
                       '':[],
                        }
                        
    list_emg_titles = {'001':'A - T10 (discharge) -> B - T11 (12 months)',
                       '004':'B - C4 (discharge)  -> B - C4 (6 months)',
                       '006':'A - L2 (6 weeks)    -> B - L2 (12 months)',
                       '015':'? - ? -> ? - ?',
                       '018':'B - C4 (3 months)   -> A - C4 (6 months)',
                       '024':'B - T5 (discharge)  -> C - L1 (12 months)',
                       '027':'? - ? -> ? - ?',
                       '030':'A - T10 (discharge) -> A - T11 (6 months)',
                       '031':'B - C4 (discharge)  -> D - C6 (12 months)',
                       '032':'C - C4 (discharge)  -> D - C7 (12 months)',
                       '033':'B - T12 (post-op.)  -> C - L1 (12 months)',
                       '037':'A - C4 (discharge)  -> B - C6 (12 months)',
                       '039':'A - C4 (discharge)  -> A - C2 (9 months)',
                       '042':'A - T10 (discharge) -> A - T10 (6 months)',
                       '045':'A - C6 (discharge)  -> A - C7 (6 months)',
                       '048':'? - ? -> ? - ?',
                       '060':'? - ? -> ? - ?',
                       }
    
    list_session_names={0:'a',
                        1:'b',
                        2:'c',
                        3:'d',
                        }
                        
    list_activity_emg={'001':[[3]],
                       '004':[[1,6],[],[0,1]],
                       '006':[[0,1,2,3,5,6,7],[0,1,2,3,4,6,7],[0,1,2,3,4,6,7]],
                       '015':[[0],[0,1,2,3,4,6,7],[0,1,4,5,]],
                       '018':[[0],[0,1,2,4],[0,2,3,7]],
                       '024':[[0,1,3],[0,1],[0,2,3,4]],
                       '027':[[2,],[],[]],
                       '030':[[1],[4,5],[5]],
                       # '031':[[4],[2,3,4],[]],
                       '031':[[],[],[],[]],
                       '032':[[0,1,4,5],[1],[0,7]],
                       '033':[[],[],[1,4]],
                       '037':[[],[],[0]],
                       '039':[[],[],[]],
                       '042':[[0,1,2,5,6,7]],
                       '045':[[0,1,3,6],[]],
                       '048':[[1],[0,1,5,6,7],[1,3]],
                       '060':[[],[],[]],
                        }
    
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT.GASTRO LT, uV', 'LAT.GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']
                        
    files_list = list_files_names[patient_number]
    ids_channels = list_ids_channels[patient_number]
    ids_emg_sorted = list_emg_sorted[patient_number]
    title_emg = list_emg_titles[patient_number]
    activity_emg = list_activity_emg[patient_number]
    
    filename = files_list[file_number]
    file_channels = ids_channels[file_number]
    ids_emg_plot = ids_emg_sorted[file_number]
    session_name = list_session_names[file_number]
    act_emg = activity_emg[file_number]
    
    
    # print(f'files: {files_list}')
    # print(f'channels: {ids_channels}')
    # print(f'selected file: {filename}, channels: {file_channels}')
    
    
    
    
    obj_emg = [[]]*len(files_list)

    i=0
    for filename, file_channels in zip(files_list, ids_channels):
        try:
            print(f'reading file: {filename}, {file_channels}... ', end='')
            # create object class
            # list_objs[i] = Activity_Measurements()
            # list_objs[i].openFile(path, filename)
            obj_emg[i] = Reading_EMG(path, filename, file_channels)
            ch_names = obj_emg[i].getChannelsNames()
            print(f'names: {ch_names}')
            
            obj_emg[i].filteringSignals()
            obj_emg[i].envelopeFilter()
            obj_emg[i].plotEnvelopedSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
            
            # obj_emg[i].plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
            
            print(f'done.')
            
        except ValueError:
            print(f'Problem reading the file {filename}.')
        i+=1
    
    # obj_emg = Reading_EMG(path, filename, file_channels)
    # ch_names = obj_emg.getChannelsNames()
    # print(f'names: {ch_names}')
    
    # obj_emg.plotSignals()
    # obj_emg.plotSelectedSignal(signal_number)
    
    # obj_emg.filteringSignals()
    # obj_emg.plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
    
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
