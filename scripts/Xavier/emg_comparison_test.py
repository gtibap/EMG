import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from class_emg_filtering import Reading_EMG
import markers_list as recordings
from sklearn.decomposition import PCA

def max_and_min_2(df, arr):
    ## identifying maximums and minimums in the x coordinate to identify periods of flexion and extension
    ## flexion goes from a maximum to a minimum; extension from a minimum to a maximun
        
    max_list=[]
    min_list=[]
    win_size = 60
    delta=10
    id0=0
    
    while (id0+win_size) <= len(arr):
        window = arr[id0:id0+win_size]
        ids_max = np.argmax(window)
        ids_min = np.argmin(window)
        
        max_list.append(ids_max+id0) 
        min_list.append(ids_min+id0) 
        id0 = id0 + delta
    
    ids_max, max_counts = np.unique(max_list, return_counts=True)
    ids_min, min_counts = np.unique(min_list, return_counts=True)
    
    # print(f'max:\n{ids_max}, {max_counts}')
    # print(f'min:\n{ids_min}, {min_counts}')
    
    ## ids occurrences greater than 1
    sel_max = np.argwhere(max_counts > 1).reshape(1,-1)
    sel_min = np.argwhere(min_counts > 1).reshape(1,-1)
    
    # print(f'indices max: {sel_max}')
    # print(f'indices min: {sel_min}')
    
    ids_sel_max = ids_max[sel_max[0]]
    ids_sel_min = ids_min[sel_min[0]]
    
    # print(f'values max: {ids_sel_max}')
    # print(f'values min: {ids_sel_min}')

    ids_sel_max = df.loc[ids_sel_max]['Time'].to_numpy()
    # print(f'max_time: {ids_sel_max}')

    ids_sel_min = df.loc[ids_sel_min]['Time'].to_numpy()
    # print(f'min_time: {ids_sel_min}')

    return ids_sel_max, ids_sel_min


def interpolation_filter_2(df, label):
    df[label[0]].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df[label[1]].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df[label[2]].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    return df

def flexion_extension_identification(df, labels_markers, sel):
    ## estimate major and minor axes of a marker with an elliptical trajectory (right lower distal)
    ## points projection to the estimated axes

    df = interpolation_filter_2(df,labels_markers[sel])

    arr_marker = df.loc[:][labels_markers[sel]].to_numpy()
    print(f'coord. marker:\n{arr_marker}')

    arr_marker = smooth_filter(arr_marker)

    ## estimating principal axes data distribution
    pca = PCA(n_components=2)
    pca.fit(arr_marker)
    print(f'components:\n{pca.components_}')
    print(f'mean:\n{pca.mean_}')
    # print(f'explained variance: {pca.explained_variance_}')

    ## first step: marker's points minus their center (pca mean)
    arr_marker = arr_marker - pca.mean_
    print(f'coord. marker:\n{arr_marker}')

    ## second step: coordinates projection to the principal axes using dot product
    arr_marker = np.matmul(arr_marker, pca.components_.T)
    print(f'coord. marker:\n{arr_marker}')

    # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 7), sharex=True, sharey=True, squeeze=False)
    # fig.canvas.mpl_connect('key_press_event', on_press)
    # ax = ax.reshape(-1)
    # ax[0].plot(arr_marker[:,0])
    # ax[1].plot(arr_marker[:,1])

    return arr_marker[:,0]


def get_t_delay(obj_emg):

    channels_names = obj_emg.getChannelsNames()
    sync_name = 'Ultium EMG.Sync, On'

    id_synch = np.argwhere(np.char.equal(channels_names, sync_name))[0,0]
    print(f'id synch: {id_synch}')

    emg_channels = obj_emg.getChannels()
    synch_channel = emg_channels[id_synch]
    time_channel = obj_emg.getChannelTime()

    print(f'channel synch: {synch_channel}')
    print(f'channel time: {time_channel}')
    fig, ax = plt.subplots()
    ax.plot(time_channel, synch_channel, label='synch channel')

    ## first sample of synch equal to 1
    if synch_channel[0] == 1:
        t_delay = 0.0 
    else:
        arr = (synch_channel[:-1] != synch_channel[1:]) & (synch_channel[:-1] == 0)
        id = np.argmax(arr)
        sr = obj_emg.getSamplingRate()
        t_delay = id / sr

    return t_delay
    

def interpolation_filter(df, col):
    df[col+'_x'].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df[col+'_y'].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df[col+'_z'].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    return df

def smooth_filter(arr):
    arr[:,0]=savgol_filter(arr[:,0], window_length=60, polyorder=1, mode='mirror')
    arr[:,1]=savgol_filter(arr[:,1], window_length=60, polyorder=1, mode='mirror')
    arr[:,2]=savgol_filter(arr[:,2], window_length=60, polyorder=1, mode='mirror')
    return arr

def get_vector_section(df, distal, proxim):
    ## Get vector from each leg section. The function filter the data and calculates vectors for each frame
    ## parameters are: dataframe, and lables of distal and proximal markers respectively

    ## preprocessing two steps. One: complete missing data. Two: filtering to smooth signals
    ## filling missing data
    df = interpolation_filter(df, distal)
    df = interpolation_filter(df, proxim)

    ## taking data from dataframe to numpy array
    arr_distal = df[[distal+'_x',distal+'_y',distal+'_z']].to_numpy()
    arr_proxim = df[[proxim+'_x',proxim+'_y',proxim+'_z']].to_numpy()

    ## smoothing every component (x, y, z) of the markers location
    arr_distal = smooth_filter(arr_distal)
    arr_proxim = smooth_filter(arr_proxim)

    ## vector upper side right leg. The vector direction goes from the proximal to distal points
    arr_out = arr_distal - arr_proxim

    return arr_out

def get_angles(df, side):

    arr_a = get_vector_section(df, side+'ud', side+'up')
    arr_b = get_vector_section(df, side+'ld', side+'lp')
    ## To estimate the bend knee angle at each frame, we based our calculations on the dot product
    # calculate vectors' magnitude
    mag_a = np.linalg.norm(arr_a, axis=1)
    mag_b = np.linalg.norm(arr_b, axis=1)
    # vectors' normalization 
    arr_a_norm =  np.divide(arr_a, np.reshape(mag_a,(-1,1)))
    arr_b_norm =  np.divide(arr_b, np.reshape(mag_b,(-1,1)))
    # applying dot product
    arr_dot = np.diag(np.matmul(arr_a_norm, arr_b_norm.T) )
    # applying arccos() to calculate angles between vectors (in radians)
    angles_rad = np.arccos(arr_dot)

    return angles_rad

def max_and_min(arr):
        
    max_list=[]
    min_list=[]
    win_size = 60
    delta=10
    id0=0
    
    while (id0+win_size) <= len(arr):
        window = arr[id0:id0+win_size]
        ids_max = np.argmax(window)
        ids_min = np.argmin(window)
        
        max_list.append(ids_max+id0) 
        min_list.append(ids_min+id0) 
        id0 = id0 + delta
    
    ids_max, max_counts = np.unique(max_list, return_counts=True)
    ids_min, min_counts = np.unique(min_list, return_counts=True)
    
    # print(f'max:\n{ids_max}, {max_counts}')
    # print(f'min:\n{ids_min}, {min_counts}')
    
    ## ids occurrences greater than 1
    sel_max = np.argwhere(max_counts > 1).reshape(1,-1)
    sel_min = np.argwhere(min_counts > 1).reshape(1,-1)
    
    # print(f'indices max: {sel_max}')
    # print(f'indices min: {sel_min}')
    
    ids_sel_max = ids_max[sel_max[0]]
    ids_sel_min = ids_min[sel_min[0]]
    
    # print(f'values max: {ids_sel_max}')
    # print(f'values min: {ids_sel_min}')

    return ids_sel_max, ids_sel_min


def plot_angles(arr, max_list, min_list):
    
    fig, ax = plt.subplots()
    ax.plot(arr, label='angle knee')
    # ax.plot(JCD_grad, label='gradient')
    # only one line may be specified; full height
    for x_val in max_list:
        ax.axvline(x = x_val, color = 'tab:purple')
        
    for x_val in min_list:
        ax.axvline(x = x_val, color = 'tab:orange')
    
    ax.legend()
    # ax.set_xlim([500,1000])
    # plt.show()
   
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

    # plt.ion()  # turning interactive mode on

    path = '../../data/VL/' 
    # filename_csv = 'VL_active_assis_labels.csv'
    # filename = '../data/VL/VL_active_assis_labels.csv'
    # filename_emg = '../data/motive_tracking/tracking_006_s1/ebc_006_s01_e1.mat'

    ## selecting recording: active: 'ac', baseline: 'bl', and '05', '10','15','20','25', and'30' minutes
    # sel_rec = '30'
    sel_rec = args[1]
    print(f'selection: {sel_rec}')

    ## read markers ids (names) that were observed in Mokka from the c3d file and recorded in markers_list.py
    mokka_ids =  recordings.VL_markers
    # print(f'csv files:\n{type(csv_files)}, \n{csv_files}')
    # print(f"csv active: {csv_files['ac']}")
    # print(f'marker num: {mokka_ids}')
    print(f"markers {sel_rec}: {mokka_ids[sel_rec]}")

    ## read markers coordinates from csv files
    csv_files = recordings.VL_csv_files
    df = pd.read_csv(path+csv_files[sel_rec], header=2)
    # print(f'header :\n{df.head()}')
    # print(f'{df.columns}')
    # print(f'df:\n{df}')

    ## associating markers ids (Mokka) with markers coordinates (csv)
    ## df_columns has the markers ids
    columns_ids = df.columns
    ## list to save markers columns in the csv file
    col_csv = list()
    ## selecting markers' data selected by name (id)
    for id in mokka_ids[sel_rec]:
        # print(f'id marker: {id}')
        ## finding the column of the marker's id
        col = np.argwhere(('Unlabeled:'+str(id)) == columns_ids)
        print(f'(id, col): ({id}, {col})')
        col_csv.append(col[0,0])
    ## 
    print(f'col_csv: {col_csv}')

    ## changing header row of dataframe to read coordinates X,Y,Z
    df.columns = df.iloc[2]
    ## removing rows 0:2 means that we keep all rows starting at row 3
    df = df[3:]
    # print(f'df:\n{df}')
    ## data type to float
    df = df.astype(float)

    header = df.columns.values.tolist()
    print(f'initial_header: {header}, {len(header)}')
    ## new header with labels for each marker
    labels_markers = recordings.labels_col
    ## replacing labels in header dataframe
    for col, labels in zip(col_csv, labels_markers):
        # print(f'col, labels: {col}, {labels}')
        header[col:col+3] = labels

    df.columns = header
    # header = df.columns
    print(f'final_header: {df.columns}')
    print(f'dataframe:\n{df}')

    # df_coord_marker = df.iloc[:, col_csv[0]:col_csv[0]+3].to_numpy().astype(float)
    # print(f"df_coord_marker {mokka_ids['ac'][0]}:\n{df_coord_marker}")

    # for col in col_csv:
    #     df = interpolation_filter(df, col)
    #     ## taking data from dataframe to numpy array
    #     arr_marker = df.iloc[:,col:col+3].to_numpy().astype(float)
    #     ## smoothing every component (x, y, z) of the markers location
    #     arr_marker = smooth_filter(arr_marker)

        ## vector upper side right leg. The vector direction goes from the proximal to distal points
        # arr_out = arr_distal - arr_proxim

    ## markers for VL active assis. Distal and proximal are defined taking the knee as a reference
    ## left leg. Markers above the knee:  151 (left upper distal  [lud]), 149 (left upper proximal  [lup])
    ## left leg. Markers below the knee:  150 (left lower distal  [lld]), 152 (left lower proximal  [llp])
    ## right leg. Markers above the knee: 148 (right upper distal [rud]), 145 (right upper proximal [rup])
    ## right leg. Markers below the knee: 140 (right lower distal [rld]), 135 (right lower proximal [rlp])

    ## angles knee bending right leg
    ang_r = get_angles(df,'r')
    ## angles knee bending left leg
    ang_l = get_angles(df,'l')

    plt.plot(np.rad2deg(ang_r))
    plt.plot(np.rad2deg(ang_l))

    # plt.show()
    # return 0


    ## finding location of maximums and minimums (positive and negative picks) of the angles' vector to identify the sample' number for max. flexion and max. extension for each leg. Maximum values 
    ids_max_r, ids_min_r = max_and_min(ang_r)
    ids_max_l, ids_min_l = max_and_min(ang_l)
    
    ## reading emg signals

    # emg_files = recordings.VL_emg_files
    ## first reading EMG
    # filename_emg = 'BED CYCLING_active_assis.mat'
    # filename_emg = emg_files[sel_rec]
    filename_emg = recordings.VL_emg_files[sel_rec]

    # sel_channels = recordings.VL_emg_channels[sel_rec]
    # file_channels = [1,9]
    # file_channels = sel_channels[sel_rec]
    file_channels = recordings.VL_emg_channels[sel_rec]
    print(f'file channels: {file_channels}')

    obj_emg = Reading_EMG(path, filename_emg, file_channels)
    
    print (f'channels: {obj_emg.getChannelsNames()}')

    ## synchonization between kinematics and EMG

    sample_rate_tracking = 120 ## samples per second (Hz)
    ## time in seconds
    # t_delay=0.0
    # t_delay = get_t_delay(obj_emg)
    # print(f't_delay: {t_delay}')

    time_channel = obj_emg.getChannelTime()

    arr_time_max = np.array(ids_max_r)/sample_rate_tracking
    arr_time_min = np.array(ids_min_r)/sample_rate_tracking
    # arr_time_max = np.array(ids_max_r)/sample_rate_tracking - time_channel[0]
    # arr_time_min = np.array(ids_min_r)/sample_rate_tracking - time_channel[0]
    # arr_time_max = np.array(ids_max_r)/sample_rate_tracking + t_delay
    # arr_time_min = np.array(ids_min_r)/sample_rate_tracking + t_delay
    # print(f'max and min:\n{max_list},\n{min_list}')

    print(f'arr_time_max: {arr_time_max}')
    print(f'arr_time_min: {arr_time_min}')

    # plot_angles(ang_r, ids_max_r, ids_min_r)
    # plot_angles(ang_l, ids_max_l, ids_min_l)


    obj_emg.plotSignals()
    
    obj_emg.filteringSignals()

    obj_emg.envelopeFilter()

    # ids_emg_plot = [5,7,3,0,6,4,2,1]
    # ids_emg_plot = [1,3,7,5,0,2,6,4]
    ids_emg_plot = recordings.VL_channels_sorted[sel_rec]

    title_emg = 'A - L2 (6 weeks)    -> B - L2 (12 months)'
    patient_number = '006'
    session_name='a'
    file_number=0
    act_emg=[0,1,2,3,4,5,6,7]
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT.GASTRO LT, uV', 'LAT.GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']

    # channels_names = recordings.VL_emg_names[sel_rec]
    # obj_emg.plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
    
    signal_name = 'VLO RT, uV'

    num_cycles = len(arr_time_min)
    if num_cycles > 10:
        obj_emg.plotSegmentedSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names, arr_time_max, arr_time_min, True)

        fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(7,3.5), sharex=True, sharey=True)
        fig.canvas.mpl_connect('key_press_event', on_press)
        sel_max = arr_time_max[0:10]
        sel_min = arr_time_min[0:10]
        obj_emg.plotFlexionExtension(ax, sel_max, sel_min, signal_name)
    else:
        obj_emg.plotSegmentedSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names, arr_time_max, arr_time_min, False)
  
    ################
    # ### testing
    # labels_markers = [['rlp_x','rlp_y','rlp_z'], ['rld_x','rld_y','rld_z']]

    # selected_marker = 1
    # arr_x = flexion_extension_identification(df, labels_markers, selected_marker)

    # arr_time_max2, arr_time_min2 = max_and_min_2(df, arr_x)
    # # print(f'arr time:\n max: {arr_time_max}\n min: {arr_time_min}')

    # fig2, ax2 = plt.subplots(nrows=2,ncols=1, figsize=(7,3.5), sharex=True, sharey=True)
    # fig2.canvas.mpl_connect('key_press_event', on_press)

    # for x_val,x_val2 in zip(arr_time_max,arr_time_max2):
    #     p_f = ax2[0].axvline(x = x_val, color = 'tab:green', label='flexion')
    #     p_f = ax2[1].axvline(x = x_val2, color = 'tab:green', label='flexion')
    # for x_val,x_val2 in zip(arr_time_min,arr_time_min2):
    #     p_e = ax2[0].axvline(x = x_val, color = 'tab:purple', label='extension')
    #     p_e = ax2[1].axvline(x = x_val2, color = 'tab:purple', label='extension')

    # # print(f'arr_time_max: {arr_time_max}')
    # pp_max = arr_time_max[1:]-arr_time_max[:-1]
    # pp_max2 = arr_time_max2[1:]-arr_time_max2[:-1]

    # pp_min = arr_time_min[1:]-arr_time_min[:-1]
    # pp_min2 = arr_time_min2[1:]-arr_time_min2[:-1]
    
    # print(f'pp_max:\n{pp_max}\n{pp_max2}')
    # print(f'pp_min:\n{pp_min}\n{pp_min2}')

    # median_pp_max = np.median(pp_max)
    # median_pp_max2 = np.median(pp_max2)
    # median_pp_min = np.median(pp_min)
    # median_pp_min2 = np.median(pp_min2)
    
    # print(f'medians: {median_pp_max}, {median_pp_max2}, {median_pp_min}, {median_pp_min2}')

    # # print(f'len arr_max: {len(arr_time_max)}, {len(arr_time_max2)}')
    # # print(f'len arr_min: {len(arr_time_min)}, {len(arr_time_min2)}')

    # print(f'diff max: {arr_time_max2 - arr_time_max}')
    # print(f'diff min: {arr_time_min2 - arr_time_min}')


    # median_delta_max =  np.median(arr_time_max2 - arr_time_max)
    # median_delta_min =  np.median(arr_time_min2 - arr_time_min)

    # print(f'deltas: {median_delta_max},{median_delta_min}')
    # print(f'ratio {median_delta_max/median_pp_max}, {median_delta_min/median_pp_min}')

    # ## plotting emg with flexion extension annotations
    # # obj_emg.plotSegmentedSignals(list_emg, channels_names, arr_time_max, arr_time_min, time_interval)

    # ### testing
    # ###############


    plt.show()


    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))