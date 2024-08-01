## kinematics
## markers names for the right and left legs
## adquisitions at active (ac), baseline (bl), and 5, 10, 15, 20, 25, and 30 minutes
## the markers are sorted according to the following order:
## [rud, rup, rlp, rld, lud, lup, llp, lld]
## each letter means:
# r: right, l: left, 
# u: upper, l: lower, 
# d: distal, p: proximal

labels_col = [['rud_x','rud_y','rud_z'],
              ['rup_x','rup_y','rup_z'], 
              ['rlp_x','rlp_y','rlp_z'], 
              ['rld_x','rld_y','rld_z'], 
              ['lud_x','lud_y','lud_z'], 
              ['lup_x','lup_y','lup_z'], 
              ['llp_x','llp_y','llp_z'], 
              ['lld_x','lld_y','lld_z'],]

VL_markers = {
    'ac':[148, 145, 135, 140, 151, 149, 152, 150],
    'bl':[124, 125, 126, 127, 128, 129, 131, 132],
    '05':[160, 158, 157, 154, 159, 164, 165, 166],
    '10':[160, 158, 157, 154, 159, 164, 165, 166],
    '15':[160, 158, 157, 154, 159, 164, 165, 166],
    '20':[123, 179, 192, 190, 175, 183, 187, 189],
    '25':[123, 179, 192, 190, 175, 183, 187, 189],
    '30':[121, 122, 123, 124, 118, 120, 117, 119],
    }

VL_emg_files = {
    'ac': 'BED CYCLING_active_assis.mat',
    'bl': 'BED CYCLING_baseline_assis.mat',
    '05': 'BED CYCLING_5min_assis.mat',
    '10': 'BED CYCLING_10min.mat',
    '15': 'BED CYCLING_15min.mat',
    '20': 'BED CYCLING_20min.mat',
    '25': 'BED CYCLING_25min_assis.mat',
    '30': 'BED CYCLING_30min_assis.mat',
}

VL_emg_channels = {
    'ac': [9,17],
    'bl': [9,17],
    '05': [9,17],
    '10': [9,17],
    '15': [9,17],
    '20': [9,17],
    '25': [1,9],
    '30': [1,9],
}

VL_c3d_files = {
    'ac': 'VL_active_assis.c3d',
    'bl': 'VL_baseline_assis.c3d',
    '05': 'VL_5min_assis.c3d',
    '10': 'VL_10min_assis.c3d',
    '15': 'VL_15min_assis.c3d',
    '20': 'VL_20min_assis.c3d',
    '25': 'VL_25min_assis.c3d',
    '30': 'VL_30min_assis.c3d',
}

VL_csv_files = {
    'ac': 'VL_active_assis.csv',
    'bl': 'VL_baseline_assis.csv',
    '05': 'VL_5min_assis.csv',
    '10': 'VL_10min_assis.csv',
    '15': 'VL_15min_assis.csv',
    '20': 'VL_20min_assis.csv',
    '25': 'VL_25min_assis.csv',
    '30': 'VL_30min_assis.csv',
}

VL_emg_names = {
    'ac': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
    'bl': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
    '05': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
    '10': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
    '15': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
    '20': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
    '25': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
    '30': ['VMO RT, uV', 'VLO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VMO LT, uV', 'VLO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV', 'Ultium EMG.Sync, On'],
}

VL_channels_sorted = {
    'ac': [1,3,7,5,0,2,6,4],
    'bl': [1,3,7,5,0,2,6,4],
    '05': [1,3,7,5,0,2,6,4],
    '10': [1,3,7,5,0,2,6,4],
    '15': [1,3,7,5,0,2,6,4],
    '20': [1,3,7,5,0,2,6,4],
    '25': [1,3,7,5,0,2,6,4],
    '30': [1,3,7,5,0,2,6,4],
}

