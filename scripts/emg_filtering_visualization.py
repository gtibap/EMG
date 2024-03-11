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
    
    # parser.add_argument('-f', '--file_number', type = str, help = "Select file number, for example: 0")
    
    parser.add_argument('-s', '--session', type = int, help = "Select session (0,1,2), for example: 0")
    
    args = parser.parse_args()

    path_emg=args.dir_name+f'EBC{args.patient_number}/'
    patient_number=args.patient_number
    session=args.session
    # file_number=int(args.file_number)
    # signal_number=int(args.signal_number)
    
    
    # print(f'path and files: {path}, {patient_number}, {file_number}')
    print(f'path and files: {path_emg}, {patient_number}, {session}')
    
    list_files_names = {
                        ## no baseline
                        '002':[['EBC_PATIENT_2.mat'],
                        ['EBC_PATIENT_2_1.mat'],
                        ['EBC002_S1.mat'],],
                        
                        ## no baseline
                        '003':[['EBC003-J1.mat'],
                        ['EBC003-S7.1.mat','EBC003-S7.2.mat'],
                        ['EBC003-J14.mat'],],
                        
                        ## no baseline
                        '004':[['EBC004_S1.mat'],
                        ['EBC004_S6.mat'],
                        ['EBC_Bed_cycling.mat','EBC004_J13.mat'],],
                        
                        ## no baseline
                        '005':[['EBC Bed cycling.mat'],
                        ['ebc test.mat','EBC005 S7.mat'],
                        ['EBC Bed cycling-3.mat','EBC 15min.mat'],],
                        
                        ## no baseline
                        '006':[['EBC006 S1 E1.mat','EBC006 S1 E2.mat','EBC 006 S1 E3.mat'],
                        ['EBC 006 S8 E1.mat','EBC 006 S8 E2.mat','EBC 006 S8 E3.mat'],
                        ['EBC006 s15 E1.mat','EBC006 s15 E2.mat','EBC006 s15 e3.mat'],],
                        
                        ## no baseline
                        '007':[['ebc_007 _s01_e1.mat','ebc_007 _s01_e2.mat','ebc_007 _s01_e3.mat'],
                        ['ebc_007 _s07_e1.mat','ebc_007 _s07_e2.mat','ebc_007 _s07_e3.mat'],
                        ['ebc_007 _s14_e1.mat','ebc_007 _s14_e2.mat','ebc_007 _s14_e3.mat'],],
                        
                        ## no baseline
                        '008':[['ebc_008 _s01_e1.mat','ebc_008 _s01_e2.mat','ebc_008 _s01_e3.mat'],
                        ['ebc_008 _s07_e1.mat','ebc_008 _s07_e2.mat',],
                        ['ebc_008 _s14_e1.mat','ebc_008 _s14_e2.mat','ebc_008 _s14_e3_OK.mat'],],
                        
                        ## no baseline
                        '009':[['ebc_009 _s01_e1.mat','ebc_009 _s01_e2.mat','ebc_009 _s01_e3.mat'],
                        ['ebc_009 _s08_e1.mat','ebc_009 _s08_e2.mat','ebc_009 _s08_e3.mat'],
                        ['ebc_009 _s14_e1.mat','ebc_009 _s14_e2.mat','ebc_009 _s14_e3.mat'],],
                        
                        ## no baseline
                        '010':[['ebc_010 _s08_e1.mat','ebc_010 _s08_e2.mat','ebc_010 _s08_e3.mat'],
                        [],
                        [],],
                        
                        ## no baseline
                        '011':[['ebc_011 _s02_e1.mat','ebc_011 _s02_e2.mat','ebc_011 _s02_e3.mat'],
                        ['ebc_011 _s07_e1.mat','ebc_011 _s07_e2.mat','ebc_011 _s07_e3.mat'],
                        ['ebc_011 _s14_e1.mat','ebc_011 _s14_e2-1.mat','ebc_011 _s14_e3.mat'],],
                        
                        ## no baseline
                        '012':[['ebc_012_s02_b1.mat','ebc_012_s02_e1.mat','ebc_012_s02_e3.mat'],
                        ['ebc_012_s07_e1.mat','ebc_012_s07_e2.mat','ebc_012_s07_e3.mat'],],
                        
                        ## no baseline
                        '013':[['ebc_013 _s03_e1.mat','ebc_013 _s03_e2.mat','ebc_013 _s03_e3.mat'],
                        ['EBC013_crank_C_1.mat','EBC013_crank_L_1.mat','EBC013_crank_TC_1.mat'],
                        [],],
                        
                        ## no baseline
                        '014':[['ebc_014 _s01_e1.mat','ebc_014 _s01_e2.mat','ebc_014 _s01_e3.mat'],
                        ['ebc_014 _s07_e1.mat','ebc_014 _s07_e2.mat','ebc_014 _s07_e3.mat'],
                        ['ebc_014 _s14_e1.mat','ebc_014 _s14_e2.mat','ebc_014 _s14_e3.mat'],],
                        
                        ## no baseline
                        '015':[['ebc_015 _s02_e1.mat','ebc_015 _s02_e2.mat','ebc_015 _s02_e3.mat'],
                        ['ebc_015 _s07_e1.mat','ebc_015 _s07_e2.mat','ebc_015 _s07_e3.mat'],
                        ['ebc_015 _s13_e1.mat','ebc_015 _s13_e2.mat'],],
                        
                        ## no baseline
                        '016':[['ebc_016 _s01_e1.mat','ebc_016 _s01_e2.mat','ebc_016 _s01_e3.mat'],
                        ['ebc_016 _s07_e1.mat','ebc_016 _s07_e2.mat','ebc_016 _s07_e3.mat'],
                        [],],
                        
                        ## no baseline
                        '017':[['ebc_017 _s01_e1.mat'],
                        ['ebc_017_s07_e1.mat','ebc_017_s07_e2.mat','ebc_017_s07_e3.mat'],
                        ['ebc_017_s14_e1.mat','ebc_017_s14_e2.mat','ebc_017_s14_e3.mat'],],
                        
                        ## no baseline
                        '018':[['EBC018-s3-e1.mat','EBC018_S2_E2.mat','EBC018_S3_E3.mat'],
                        ['ebc018_S8_e1.mat','EBC018_s8_e2.mat','EBC018_S8_E3.mat'],
                        ['EBC018_S12_e1.mat','EBC018_S12_E2.mat','EBC018_S12_e3.mat'],],
                        
                        ## no baseline
                        '019':[['ebc_019_s01_e1-1.mat','ebc_019_s01_e2.mat','ebc_019_s01_e3.mat'],
                        ['ebc_019_s10_e1.mat','ebc_019_s10_e2.mat','ebc_019_s10_e3.mat'],
                        ['ebc_019_s14_e1.mat','ebc_019_s14_e2.mat','ebc_019_s14_e3.mat'],], #ebc_019_s14_e1.mat
                        
                        ## no baseline
                        '020':[['ebc_020_s01_e1.mat','ebc_020_s01_e2.mat',],
                        [],
                        [],],

                        ## no baseline
                        '022':[['ebc_022_s02_e1.mat','ebc_022_s02_e2-2-20min.mat','ebc_022_s02_e3.mat'],],
                        
                        ## baseline
                        '023':[['ebc_023_s03_b1.mat','ebc_023_s03_e2.mat','ebc_023_s03_e3.mat'], #ebc_023_s03_e1.mat
                        ['ebc_023_s08_b1.mat','ebc_023_s08_e2.mat','ebc_023_s08_e3.mat'],#ebc_023_s08_e1.mat
                        [],],#EBC24_S14_E1.mat 'EBC24 BASELINE 1.mat','EBC24-S14-E2.mat','ebc24_S14-E3.mat'
                        
                        ## baseline
                        '024':[['EBC24-S4_BASELINE.mat','EBC024-S4-E2.mat','EBC24-S4-E3.mat'],
                        ['EBC24_S9_baseline1.mat','EBC24-S9-e2.mat','EBC24_s9_E3.mat'],
                        ['EBC024S13e1.mat','EBC024S13e2.mat','EBC024S13e3.mat'],],
                        
                        ## baseline
                        '025':[['ebc_025_s03_e1.mat','ebc_025_s03_e2.mat','ebc_025_s03_e3.mat'],
                        ['ebc_025_s08_b1.mat','ebc_025_s08_e2.mat','ebc_025_s08_e3.mat'],
                        ['ebc_025_s15_b1.mat','ebc_025_s15_e1.mat','ebc_025_s15_e3.mat'],],
                        
                        ## no baseline
                        '026':[['ebc_026_s01_e1.mat','ebc_026_s01_e2.mat','ebc_026_s01_e3.mat'],#'ebc_026_s01_b2.mat'
                        [],
                        [],],
                        
                        ## baseline
                        '027':[['ebc_027_s02_b1.mat','ebc_027_s02_e2.mat','ebc_027_s02_e3.mat'],
                        ['ebc_027_s07_b1.mat','ebc_027_s07_e2.mat','ebc_027_s07_e3.mat'],
                        ['ebc_027_s14_b1.mat','ebc_027_s14_e2.mat','ebc_027_s14_e3.mat'],],
                        
                        ## baseline
                        '028':[['ebc_028_s01_b1.mat','ebc_028_s01_e2.mat','ebc_028_s01_e3.mat'],
                        ['ebc_028_s07_b1.mat','ebc_028_s07_e2.mat','ebc_028_s07_e3.mat'],
                        ['ebc_028_s14_b1.mat','ebc_028_s14_e2.mat','ebc_028_s14_e3.mat'],],
                        
                        ## no baseline
                        '029':[['ebc_029_s02_b1.mat','ebc_029_s02_e2.mat','ebc_029_s02_e3.mat'],
                        ['ebc_029_s09_b1.mat','ebc_029_s09_e2.mat','ebc_029_s09_e3.mat'],
                        ['ebc_029_s14_b1.mat','ebc_029_s14_e2.mat','ebc_029_s14_e3.mat'],],
                        
                        ## baseline
                        '030':[['EBC030_S1_BASELINE1.mat','EBC030_S1_E2.mat','EBC030_S1_E3.mat'],
                        ['EBC030_S7_BASELINE1.mat','EBC030_S7_E2.mat','EBC030_S7_E3.mat'],
                        ['EBC030_S14_BASELINE.mat','EBC030_s14_e2.mat','EBC30_S14_E3.mat'],],
                        
                        '031':[
                        ## session a, no baseline
                        ['EBC031_s2_e1.mat','EBC031_s2_e2.mat','EBC031_s2_e3.mat'],
                        ## session b, yes baseline
                        ['EBC031_baseline1.mat', 'EBC031_s7e2.mat', 'EBC031S7e3.mat' ],
                        ## session c, yes baseline but the bike moved a bit during the recording
                        ['EBC031_S14_BASELINE1.mat', 'EBC031S14e2.mat', 'EBC031_s14_e3.mat'],
                        ],
                        
                        # EBC032_s1_baseline1.mat                     
                        '032':[
                        ## session a, yes, baseline but with pedaling at the end of the recording 
                        ['EBC032_s1_baseline1.mat','EBC032_S1_E2.mat','EBC032_s1_e3.mat'],
                        ## session b, yes, baseline
                        ['EBC032S7-Baseline1.mat','EBC032S7e1.mat','EBC032S7e3.mat'], #'EBC032S7e2.mat'
                        ## session c, yes, baseline
                        ['EBC032-Baseline1.mat','EBC032S14e1.mat','EBC032S14e3.mat'], #'EBC032S14e2.mat'
                        ],
                        
                        ## no baseline
                        '033':[['EBC033S3-Baseline.mat','EBC033S3e2.mat','EBC033S3e3.mat'],
                        ['EBC033_S7_BASELINE1.mat','EBC033_S7_E2.mat','EBC033_S7_E3.mat'],
                        ['EBC033S14-Baseline1.mat','EBC033S14e2.mat','EBC033S14e3.mat'],],
                        
                        ## no baseline
                        '036':[['ebc_036_s02_b1.mat','ebc_036_s02_e2.mat','ebc_036_s02_e3.mat'],
                        ['ebc_036_s06_b1.mat','ebc_036_s06_e2.mat','ebc_036_s06_e3.mat'],
                        ['ebc_036_s14_b1.mat','ebc_036_s14_e2.mat','ebc_036_s14_e3.mat'],],
                        
                        '037':[
                        ## session a, 
                        ['EBC37_S1_BASELINE1.mat','EBC037_S2_E1.mat','EBC037_S2_E3.mat'], #'EBC037_S2_E2.mat'
                        ## session b,
                        ['EBC037S7-Baseline1.mat','EBC037S7e1.mat','EBC037S7e3.mat'], #'EBC037S7e2.mat'
                        ## session c,
                        ['EBC037_S14_BASELINE1.mat','EBC037_S14_E1.mat','EBC037S14E3.mat'], #'EBC037_S14_E2.mat'
                        ],
                        
                        '039':[
                        ## session a
                        ['EBC039_BASELINE1.mat','EBC039_S2_E1.mat','EBC039S1E3.mat'],#'ebc039S1E2.mat',
                        ## session b
                        ['EBC039S7-baseline1.mat','EBC039s7e1.mat','EBC039s7e3.mat'],#'EBC039s7e2.mat'
                        ## session c
                        ['EBC039S14-Baseline1.mat','EBC039S14e1.mat','EBC039S14e3.mat'],#'EBC039S14e2.mat'
                        ],
                        
                        
                        '040':[
                        ['ebc_040_s01_b1.mat','ebc_040_s01_e1.mat','ebc_040_s01_e3.mat'],#'ebc_040_s01_e2.mat',
                        ['ebc_040_s07_b1.mat','ebc_040_s07_e1.mat','ebc_040_s07_e3.mat'],#'ebc_040_s07_e2.mat',
                        ## session c, no baseline
                        ['ebc_040_s14_b1.mat','ebc_040_s14_e1.mat','ebc_040_s14_e3.mat'],#'ebc_040_s14_e2.mat',
                        ],
                        
                        ## no baseline
                        '042':[['ebc_042_s01_b1.mat','TEST2.mat','TEST-1.mat'],
                        ['EBC042_S7_BASELINE.mat','EBC042S715MIN.mat','EB042S730MIN.mat'],
                        [],],
                        
                        '045':[
                        ## session a, no baseline
                        ['EBC45-S2-5min.mat','EBC45-S2-15min.mat','EBC45-S2-25min.mat'],#'EBC45-S2-Baseline.mat'
                        ## session b, yes baseline
                        ['EBC045S14Baseline1.mat','EBC045S14e1.mat','EBC045S14e3.mat'],#'EBC045S14e2.mat',
                        ],
                        
                        ## no baseline
                        '046':[['ebc_046_s01_b1.mat','ebc_046_s01_e2.mat','ebc_046_s01_e3.mat'],
                        ['ebc_046_s06_b1.mat','ebc_046_s06_e2.mat','ebc_046_s06_e2_20min.mat'],
                        ['ebc_046_s13_b1.mat','ebc_046_s13_e2.mat','ebc_046_s13_e3.mat'],],
                        
                        '048':[
                        ## session a, no baseline
                        ['ebc_048_s01_b1.mat','ebc_048_s01_e1.mat','ebc_048_s01_e3.mat'],#ebc_048_s01_e2.mat
                        ## session b, no baseline
                        ['ebc_048_s07_b1.mat','ebc_048_s07_e1.mat','ebc_048_s07_e3.mat'],#ebc_048_s07_e2.mat
                        ## session c, yes baseline
                        ['ebc_048_s14_b1.mat','ebc_048_s14_e1.mat','ebc_048_s14_e3.mat'],#ebc_048_s14_e2.mat,
                        ],
                        
                        ## baseline
                        '049':[['ebc_049_s01_e1.mat','ebc_049_s01_e2.mat','ebc_049_s01_e3.mat'],#ebc_049_s01_b1.mat
                        ['ebc_049_s05_b1.mat','ebc_049_s05_e2.mat','ebc_049_s05_e3.mat'],
                        ['ebc_049_s14_b1.mat','ebc_049_s14_e2.mat','ebc_049_s14_e3.mat'],],

                        ## no baseline
                        '050':[['ebc_050_s01_e1.mat','ebc_050_s01_e2.mat','ebc_050_s01_e3.mat'],#ebc_050_s01_b1.mat
                        ['ebc_050_s07_e1.mat','ebc_050_s07_e2.mat','ebc_050_s07_e3.mat'],#ebc_050_s07_b1.mat
                        ['ebc_050_s14_b1.mat','ebc_050_s14_e2.mat','ebc_050_s14_e3.mat'],],
                        
                        ## no baseline
                        '051':[['ebc_051_s01_b1.mat','ebc_051_s01_e2.mat','ebc_051_s01_e2_20min.mat'],
                        ['ebc_051_s07_e1.mat','ebc_051_s07_e4.mat','ebc_051_s07_e9.mat'],
                        ['ebc_051_s14_e1.mat','ebc_051_s14_e5.mat','ebc_051_s14_e11.mat'],],

                        '052':[
                        ## session a, yes baseline
                        ['ebc_052_s01_b1.mat','ebc_052_s01_e1.mat','ebc_052_s01_e3.mat'],#'ebc_052_s01_e2.mat',
                        ['ebc_052_s07_b1.mat','ebc_052_s07_e2.mat','ebc_052_s07_e3.mat'],#'ebc_052_s07_e2_25min.mat',
                        ## session c, no baseline
                        ['ebc_052_s14_e1.mat','ebc_052_s14_e2.mat','ebc_052_s14_e2_25min.mat'],
                        ],
                        
                        ## no baseline
                        '053':[['ebc_053_s01_b1.mat','ebc_053_s01_e2.mat','ebc_053_s01_e3.mat'],
                        ['ebc_053_s07_b1.mat','ebc_053_s07_e2.mat','ebc_053_s07_e3.mat'],
                        ['ebc_053_s14_b1.mat','ebc_053_s14_e2.mat','ebc_053_s14_e3.mat'],],
                        
                        ## no baseline
                        '054':[['ebc_054_s01_b1.mat','ebc_054_s01_e2.mat','ebc_054_s01_e3.mat'],
                        [],
                        ['ebc_054_s14_b1.mat','ebc_054_s14_e2.mat','ebc_054_s14_e3.mat'],],
                        
                        '055':[
                        ['ebc_055_s01_b1.mat','ebc_055_s01_e1.mat','ebc_055_s01_e3.mat'],#'ebc_055_s01_e2.mat',
                        ['ebc_055_s07_b1.mat','ebc_055_s07_e1.mat','ebc_055_s07_e3.mat'],#'ebc_055_s07_e2.mat'
                        ['ebc_055_s14_b1.mat','ebc_055_s14_e1.mat','ebc_055_s14_e3.mat'],#'ebc_055_s14_e2.mat',
                        ],
                        
                        ## no baseline
                        '056':[['ebc_056_s01_b1.mat','ebc_056_s01_e2.mat','ebc_056_s01_e3.mat'],
                        [],
                        [],],
                        
                        '057':[
                        ['ebc_057_s01_b1.mat','ebc_057_s01_e1.mat','ebc_057_s01_e3.mat'],#'ebc_057_s01_e2.mat',
                        ['ebc_057_s07_b1.mat','ebc_057_s07_e1.mat','ebc_057_s07_e4.mat'],#'ebc_057_s07_e2.mat',
                        ['ebc_057_s14_b1.mat','ebc_057_s14_e1.mat','ebc_057_s14_e4.mat'],#'ebc_057_s14_e2.mat',
                        ],
                        
                        ## no baseline
                        '058':[['ebc_058_s01_b1.mat','ebc_058_s01_e2.mat','ebc_058_s01_e3.mat'],
                        ['ebc_058_s07_b1.mat','ebc_058_s07_e2.mat','ebc_058_s07_e2_25min.mat'],
                        ['ebc_058_s14_b1.mat','ebc_058_s14_e2.mat','ebc_058_s14_e2_25min.mat'],],
                        
                        ## no baseline
                        '059':[['EBC059-Baseline1.mat','EBC059S1-Baseline2.mat',],
                        ['ebc_059_s07_b1.mat','ebc_059_s07_e2.mat','ebc_059_s07_e3.mat'],
                        ['ebc_059_s14_e1.mat','ebc_059_s14_e2.mat','ebc_059_s14_e3.mat'],],
                        
                        '060':[
                        ['EBC060-TEST.mat','EBC060-TEST2.mat','EBC060-TEST3.mat'],
                        ['EBC060_BASELINE.mat','EBC060-5MIN.mat','EBC060-25MIN.mat'],#'EBC060-15MIN.mat',
                        ['EBC060-S14-BASELINE.mat','EBC060-S14-5MIN.mat','EBC060-S14-15MIN.mat'],#'EBC060-S14-10MIN.mat',
                        ],
                        
                        ## no baseline
                        '061':[['EBC061_BASELINE.mat','EBC061_S1_10 min.mat','EBC061_S1_30 min.mat'],
                        ['EBC061-S9_BASELINE.mat','EBC061-S9_10MIN.mat','EBC061-S9_30MIN.mat'],
                        ['EBC061-S14_BASELINE.mat','EBC061-S14_10MIN.mat','EBC061-S14_25MIN.mat'],],
                        
                        ## no baseline
                        '062':[['A_EBC Bed cycling_PRINCIPAL_baseline1.mat','ebc_62_s1_e2.mat','ebc_62_s1_e4.mat'],
                        ['EBC062-S3_BASELINE-1.mat','EBC062-S3_15MIN.mat','EBC062-S3_25MIN.mat'],
                        ['EBC062-S7_BASELINE-1.mat','EBC062-S7_15MIN.mat','EBC062-S7_25MIN.mat'],],
                        
                        ## no baseline
                        '063':[['EBC_063_S01_B1.mat','EBC_063_S01_E1.mat','EBC_063_S01_E2.mat'],
                        ['EBC063-S7_BASELINE.mat','EBC063-S7_15MIN_V4.mat','EBC063-S7_30MIN_V2.mat'],
                        ['EBC_063_S14_B1.mat','EBC_063_S14_E2.mat','EBC_063_S14_E3.mat'],],
                        
                        ## no baseline
                        '065':[['EBC065_S2_BASELINE.mat','EBC065_S2_10MIN.mat','EBC065_S2_25MIN.mat'],
                        ['EBC065_S3_BASELINE.mat','EBC065_S3_10MIN.mat','EBC065_S3_25MIN.mat'],
                        [],],
                        
                        ## no baseline
                        '066':[['EBC066_S1_BASELINE.mat','EBC066_S1_10MIN.mat','EBC066_S1_25MIN.mat'],
                        [],
                        [],],
                        
                        }
    
    
    ## non-baseline=False, baseline present=True; for each session (a,b,c)
    list_baseline = {
                        '002':[False, False, False],
                        '003':[False, False, False],
                        '004':[False, False, False],
                        '005':[False, True, False],
                        '006':[False, False, False],
                        '007':[False, False, False],
                        '008':[False, False, False],
                        '009':[False, False, False],
                        '010':[False, False, False],
                        '011':[False, False, False],
                        '012':[False, False, False],
                        '013':[False, False, False],
                        '014':[False, False, False],
                        '015':[False, False, False],
                        '016':[False, False, False],
                        '017':[False, False, False],
                        '018':[False, False, False],
                        '019':[False, False, False],
                        '020':[False, False, False],
                        '022':[False],
                        '023':[True, True, True],
                        '024':[True, True, False],
                        '025':[False, True, True],
                        '026':[False, False, False],
                        '027':[True, True, True],
                        '028':[True, True, True],
                        '029':[True, True, True],
                        '030':[True, True, True],
                        '031':[False, True, True],
                        '032':[True, True, True],
                        '033':[True, True, True],
                        '036':[True, True, True],
                        '037':[True, True, True],
                        '039':[True, True, True],
                        '040':[True, True, False],
                        '042':[True, False, False],
                        '045':[False, True],
                        '046':[True, True, True],
                        '048':[False, False, True],
                        '049':[False, True, True],
                        '050':[False, False, True],
                        '051':[True, True, False],
                        '052':[True, True, False],
                        '053':[True, True, False],
                        '054':[True, True, False],
                        '055':[True, True, True],
                        '056':[True, True, False],
                        '057':[True, True, True],
                        '058':[True, True, False],
                        '059':[True, True, False],
                        '060':[True, True, True],
                        '061':[True, True, True],
                        '062':[True, True, True],
                        '063':[True, True, True],
                        '065':[True, True, True],
                        '066':[True, True, True],
                    }
    # print(f'list_files_names {list_files_names[patient_number]}')
    # print(f'selected files {list_files_names[patient_number][session]}')
    
    
    ## Documents/EMG/docs/figures/sep06_2023/  
                        
    ## ids of the eight required channels: muscular signals EMG without the insole signals
    list_ids_channels = {
                         # '001':[[9,16]]*1,
                         # '002':[[9,16]]*2,
                         # '003':[[9,16]]*2,
                         # '004':[[9,16]]*3,
                         # '006':[[9,16]]*3,
                         # '009':[[9,16]]*3,
                         # '012':[[9,16]]*2,
                         # '015':[[9,16]]*3,
                         # '018':[[9,16],[9,16],[1,8]],
                         # '019':[[9,16]]*3,
                         # '022':[[9,16]],
                         # '024':[[9,16]]*3,
                         # '027':[[9,16]]*3,
                         # '028':[[9,16]]*3,
                         # '029':[[9,16]]*3,
                         # '030':[[9,16],[1,8],[1,8]],
                         
                         '002':[[[9,16]]*1,
                         [[9,16]]*1,
                         [[9,16]]*1,],
                         
                         '003':[[[9,16]]*1,
                         [[9,16]]*2,
                         [[9,16]]*1,],
                         
                         '004':[[[9,16]]*1,
                         [[9,16]]*1,
                         [[9,16]]*2,],
                         
                         '005':[[[9,16]]*1,
                         [[9,16]]*2,
                         [[9,16]]*2,],
                         
                         '006':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '007':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '008':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '009':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '010':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '011':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '012':[[[9,16]]*3,
                         [[9,16],[9,16],[1,8]],],
                         
                         '013':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '014':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16],[9,16],[1,8]],],
                         
                         '015':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '016':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '017':[[[9,16]]*3,
                         [[9,16],[9,16],[1,8]],
                         [[9,16]]*3,],
                         
                         '018':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16],[9,16],[1,8]],],
                         
                         '019':[[[9,16],[1,5],[1,5]],
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '020':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '022':[[[1,8]]*3,],
                         
                         '023':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '024':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '025':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[1,8],[1,8],[1,8]],],
                         
                         '026':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '027':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '028':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '029':[[[1,8]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '030':[[[9,16]]*3,
                         [[9,16],[1,8],[1,8]],
                         [[1,8]]*3,],
                         
                         '031':[[[1,8]]*3,
                         [[9,16]]*3,
                         [[1,8]]*3,],
                         
                         '032':[[[9,16]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '033':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '036':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[9,16]]*3,],
                         
                         '037':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '039':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '040':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '042':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '045':[[[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '046':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[9,16],[1,8],[1,8]],],
                         
                         '048':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '049':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '050':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '051':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '052':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '053':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '054':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '055':[[[1,8]]*3,
                         [[1,8]]*3,
                         [[1,8]]*3,],
                         
                         '056':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '057':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '058':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '059':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '060':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '061':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '062':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '063':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '065':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         '066':[[[9,16]]*3,
                         [[9,16]]*3,
                         [[9,16]]*3,],
                         
                         # '033':[[1,8]]*3,
                         # '037':[[1,8]]*3,
                         # '039':[[1,8]]*3,
                         # '040':[[1,8]]*3,
                         # '042':[[1,8]],
                         # '045':[[9,16]]*2,
                         # '046':[[9,16]]*3,
                         # '048':[[1,8]]*3,
                         # '052':[[1,8]]*3,
                         # '053':[[1,8]]*3,
                         # '054':[[1,8]]*2,
                         # '056':[[9,16]],
                         # '057':[[9,16]]*3,
                         # '058':[[9,16]]*3,
                         # '059':[[9,16]]*2,
                         # '060':[[9,16]]*2,
                        }
    
    ## sorting plots to present each lead in the same place                    
    list_emg_sorted = {
                       # '001':[[7,0,6,4,2,5,3]]*1,
                       # '002':[[7,0,6,4,2,5,3]]*2,
                       # '003':[[5,7,3,0,6,4,2,1]]*2,
                       # '004':[[5,7,3,0,6,4,2,1]]*3,
                       # '006':[[5,7,3,0,6,4,2,1]]*3,
                       # '015':[[5,7,3,0,6,4,2,1],[5,7,3,0,6,4,2,1],[5,7,3,0,4,2,1,6]],
                       # '018':[[7,2,4,1,6,5,0,3]]*3,
                       # '024':[[7,2,4,1,6,5,0,3]]*3,
                       # '027':[[7,2,4,1,6,5,0,3]]*3,
                       # '030':[[7,2,4,1,6,5,0,3]]*3,
                       
                       '002':[[[7,0,6,4,2,5,3]]*1,
                       [[7,0,6,4,2,5,3]]*1,
                       [[7,0,6,4,2,5,3]]*1,],
                       
                       '003':[[[5,7,3,0,6,4,2,1]]*1,
                       [[5,7,3,0,6,4,2,1]]*2,
                       [[5,7,3,0,6,4,2,1]]*1,],
                       
                       '004':[[[5,7,3,0,6,4,2,1]]*1,
                       [[5,7,3,0,6,4,2,1]]*1,
                       [[5,7,3,0,6,4,2,1]]*2,],
                       
                       '005':[[[5,7,3,0,6,4,2,1]]*1,
                       [[5,7,3,0,6,4,2,1]]*2,
                       [[5,7,3,0,6,4,2,1]]*2,],
                       
                       '006':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '007':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '008':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '009':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '010':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '011':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '012':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '013':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '014':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '015':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '016':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '017':[[[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,
                       [[5,7,3,0,6,4,2,1]]*3,],
                       
                       '018':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '019':[[[7,2,4,1,6,5,0,3],[2,4,1,5,0],[2,4,1,5,0]],
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '020':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '022':[[[7,2,4,1,6,5,0,3]]*3,],
                       
                       '023':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '024':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '025':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '026':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '027':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '028':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '029':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '030':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '031':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '032':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '033':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '036':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '037':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3],[7,2,4,1,6,5,0,3],[2,4,1,6,5,0,3,7]],],
                       
                       '039':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '040':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '042':[[[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,
                       [[7,2,4,1,6,5,0,3]]*3,],
                       
                       '045':[[[4,6,7,1,0,5,3,2]]*3,
                       [[5,3,7,1,4,0,6,2]]*3,],
                       
                       '046':[[[5,3,7,1,4,0,6,2]]*3,
                       [[5,3,7,1,4,0,6,2]]*3,
                       [[5,3,7,1,4,0,6,2]]*3,],
                       
                       '048':[[[5,3,7,1,4,0,6,2]]*3,
                       [[6,2,0,4,7,3,1,5]]*3,
                       [[7,5,3,1,2,0,6,4]]*3,],
                       
                       '049':[[[6,2,0,4,7,3,1,5]]*3,
                       [[3,7,5,1,2,6,0,4]]*3,
                       [[4,6,0,2,7,1,3,5]]*3,],
                       
                       '050':[[[2,0,6,4,1,7,5,3]]*3,
                       [[7,5,3,1,0,2,4,6]]*3,
                       [[0,2,6,4,1,7,5,3]]*3,],
                       
                       '051':[[[5,3,7,1,4,0,6,2]]*3,
                       [[6,2,0,4,7,3,1,5]]*3,
                       [[7,5,3,1,2,0,6,4]]*3,],
                       
                       '052':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '053':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '054':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '055':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '056':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '057':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '058':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '059':[[[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,
                       [[2,4,0,6,3,1,5,7]]*3,],
                       
                       '060':[[[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,],
                       
                       '061':[[[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,],
                       
                       '062':[[[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,],
                       
                       '063':[[[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,],
                       
                       '065':[[[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,],
                       
                       '066':[[[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,
                       [[7,5,1,3,6,4,0,2]]*3,],
                       
                       # '033':[[7,2,4,1,6,5,0,3]]*3,
                       # '037':[[7,2,4,1,6,5,0,3],[7,2,4,1,6,5,0,3],[2,4,1,6,5,0,3]],
                       # '039':[[7,2,4,1,6,5,0,3]]*3,
                       # '042':[[0,6,5,7,2,4,3,1]],
                       # '045':[[4,6,7,1,0,5,3,2],[5,3,7,1,4,0,6,2]],
                       # '048':[[5,3,7,1,4,0,6,2],[6,2,0,4,7,3,1,5],[7,5,3,1,2,0,6,4]],
                       # '052':[[2,4,0,6,3,1,5,7]]*3,
                       # '053':[[2,4,0,6,3,1,5,7]]*3,
                       # '054':[[2,4,0,6,3,1,5,7]]*2,
                       # '058':[[2,4,0,6,3,1,5,7]]*3,
                       # '056':[[7,5,1,3,6,4,0,2]],
                       # '059':[[7,5,1,3,6,4,0,2]]*2,
                       # '060':[[7,5,1,3,6,4,0,2]]*2,
                       
                       '':[],
                        }
                        
    
    list_session_names={0:'a',
                        1:'b',
                        2:'c'
                        }
                        
    
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT.GASTRO LT, uV', 'LAT.GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']
                        
    files_names = list_files_names[patient_number][session]
    list_channels = list_ids_channels[patient_number][session]
    ids_emg_sorted = list_emg_sorted[patient_number][session]
    baseline = list_baseline[patient_number][session]
    sn = list_session_names[session]
    
    
    # print(f'ids_channels: {ids_channels}')
    
    # title_emg = list_emg_titles[patient_number]
    # activity_emg = list_activity_emg[patient_number]
    
    # filename = files[file_number]
    # file_channels = ids_channels[file_number]
    # ids_emg_plot = ids_emg_sorted[file_number]
    # session_name = list_session_names[file_number]
    # act_emg = activity_emg[file_number]
    
    
    print(f'files: {files_names}')
    print(f'channels: {list_channels}')
    print(f'sorted: {ids_emg_sorted}')
    
    # print(f'selected file: {filename}, channels: {file_channels}')
    obj_emg = [[]]*len(files_names)
    
    path_emg = path_emg+f'session_{sn}/emg/'
    
    i=0
    for filename_emg, ids_channels, emg_sorted in zip(files_names, list_channels, ids_emg_sorted):
        try:
            print(f'reading file: {filename_emg}, ... ', end='')
            # create object class
            # list_objs[i] = Activity_Measurements()
            # list_objs[i].openFile(path, filename)
            obj_emg[i] = Reading_EMG(path_emg, filename_emg, ids_channels)
            ch_names = obj_emg[i].getChannelsNames()
            print(f'names: {ch_names}')
            
            obj_emg[i].filteringSignals()
            obj_emg[i].envelopeFilter()
            obj_emg[i].plotEMGSession(emg_sorted, channels_names, patient_number, sn, i, baseline)
            
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
