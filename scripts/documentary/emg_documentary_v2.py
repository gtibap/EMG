import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from class_emg_filtering import Reading_EMG
from sklearn.decomposition import PCA


def markers_selection(df, mokka_ids, labels_markers):
    ## change header titles for the chosen markers
        
    columns_ids = df.columns
    print(f'columns:{columns_ids}')
    ## list to save markers columns in the csv file
    col_csv = list()
    ## selecting markers' data selected by name (id)
    for id in mokka_ids:
        print(f'id marker: {id}')
        ## finding the column of the marker's id
        col = np.argwhere(('Unlabeled:'+str(id)) == columns_ids)
        print(f'(id, col): ({id}, {col})')
        col_csv.append(col[0,0])
    ## 
    # print(f'col_csv: {col_csv}')

    ## changing header row of dataframe to read coordinates X,Y,Z
    df.columns = df.iloc[2]
    ## removing rows 0:2 means that we keep all rows starting at row 3
    df = df[3:]
    # print(f'df:\n{df}')
    ## data type to float
    df = df.astype(float)

    header = df.columns.values.tolist()
    # print(f'initial_header: {header}, {len(header)}')
    ## new header with labels for each marker

    ## replacing labels in header dataframe
    for col, labels in zip(col_csv, labels_markers):
        # print(f'col, labels: {col}, {labels}')
        header[col:col+3] = labels

    df.columns = header
    # header = df.columns
    # print(f'final_header: {df.columns}')
    # print(f'dataframe:\n{df}')

    return df

def interpolation_filter(df, label):
    df[label[0]].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df[label[1]].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    df[label[2]].interpolate(method="cubicspline", inplace=True, limit_direction='both')
    return df

def smooth_filter(arr):
    arr[:,0]=savgol_filter(arr[:,0], window_length=60, polyorder=1, mode='mirror')
    arr[:,1]=savgol_filter(arr[:,1], window_length=60, polyorder=1, mode='mirror')
    arr[:,2]=savgol_filter(arr[:,2], window_length=60, polyorder=1, mode='mirror')
    return arr

def flexion_extension_identification(df, labels_markers, sel):
    ## estimate major and minor axes of a marker with an elliptical trajectory (right lower distal)
    ## points projection to the estimated axes

    df = interpolation_filter(df,labels_markers[sel])

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


def max_and_min(df, arr, percentage_delta_time):
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

    pp_max = ids_sel_max[1:]-ids_sel_max[:-1]
    pp_min = ids_sel_min[1:]-ids_sel_min[:-1]

    # print(f'pp_max: {pp_max}\npp_min: {pp_min}')
    # print(f'median pp_max: {np.median(pp_max)}\nmedian pp_min: {np.median(pp_min)}')

    lag_time = np.median(pp_max) * percentage_delta_time / 100

    # print(f'lag time: {lag_time}')

    ids_sel_max = ids_sel_max - lag_time
    ids_sel_min = ids_sel_min - lag_time

    return ids_sel_max, ids_sel_min


def on_press(event):
        # print('press', event.key)
        sys.stdout.flush()
        
        if event.key == 'x':
            plt.close('all')
        else:
            pass
        return 0

def main(args):
    path = '../../data/documentary/' 
    filename_emg = 'emg_doc2.mat'
    filename_csv = 'frames40k_2.csv'
    
    file_channels = [1,9]
    obj_emg = Reading_EMG(path, filename_emg, file_channels)
    print(f'reading success !')
    channels_names = obj_emg.getChannelsNames()
    print(f'channels_names: {channels_names}')

    ## channels names
    # ['VLO RT, uV', 'VMO RT, uV', 'TIB.ANT. RT, uV', 'LAT. GASTRO RT, uV', 'VLO LT, uV', 'VMO LT, uV', 'TIB.ANT. LT, uV', 'LAT. GASTRO LT, uV',]
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT. GASTRO LT, uV', 'LAT. GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']
    ## plot channels
    
    time_interval = [50, 150] ## 900 seconds are 15 min
    # obj_emg.plotSignals(time_interval)

    ## filtering emg signals
    obj_emg.filteringSignals()

    obj_emg.envelopeFilter()

    list_emg = [3,1,7,5,2,0,6,4]
    list_act_emg = []

    selected_channel = 'VLO LT, uV'
    time_interval = [650, 680] ##900 seconds are 15 min
    size_sec = 15 ## seconds

    # obj_emg.plot_slidingWindow(selected_channel, time_interval, size_sec)

    obj_emg.plotEMG_filtered(selected_channel, time_interval)

    # # obj_emg.plotEnvelopedSignals(list_emg, 'title_emg', 'patient_number', 'session_name', 'session_number', list_act_emg, channels_names)

    # # obj_emg.plotEnvelopedSignals(list_emg, list_act_emg, channels_names, time_interval)
    



    # # df_data = obj_emg.getData()
    # # print(f'data:\n{df_data}')

    # ## kinematics flexion extension
    # df = pd.read_csv(path+filename_csv, header=3)
    # ## df_columns has the markers ids

    # ## column number selected marker
    # mokka_ids=[348, 914]
    # ## right lower distal (rld)
    # labels_markers = [['rlp_x','rlp_y','rlp_z'], ['rld_x','rld_y','rld_z']]

    # df = markers_selection(df, mokka_ids, labels_markers)
    # # print(f'final_header: {df.columns}')

    # selected_marker = 1
    # arr_x = flexion_extension_identification(df, labels_markers, selected_marker)

    # ## according to experimental observations, the  maximum extension happens a time delta earlier than max value of the rld in the major axis. We have calculated that the delta time is approx. 7 % of the cycle time.
    # percentage_delta_time = 7 # percentage
    # arr_time_max, arr_time_min = max_and_min(df, arr_x, percentage_delta_time)
    # # print(f'arr time:\n max: {arr_time_max}\n min: {arr_time_min}')

    # ## plotting emg with flexion extension annotations
    # obj_emg.plotSegmentedSignals(list_emg, channels_names, arr_time_max, arr_time_min, time_interval)

    # fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(7,3.5), sharex=True, sharey=True)
    # fig.canvas.mpl_connect('key_press_event', on_press)
    # sel_max = arr_time_max[0:20]
    # sel_min = arr_time_min[0:20]
    # signal_name = 'VLO LT, uV'
    # right_side = False
    # obj_emg.plotFlexionExtension(ax, sel_max, sel_min, signal_name, right_side)


    plt.show()
    return 0



if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

