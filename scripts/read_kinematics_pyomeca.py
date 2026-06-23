import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
# import pyomeca
from pyomeca import Markers


from class_emg_filtering import Reading_EMG
# import markers_list as recordings
from markersets_names import markersets_dict

class Leg_kinematics:
    ######
    def __init__(self, path_filename, labels_markers, label_side):
        self.df = pd.DataFrame()
        self.path_filename = path_filename
        self.markers_labels = labels_markers
        self.markers_side = label_side
        self.markers_arr = Markers.from_c3d(path_filename, usecols=labels_markers)
        self.df['time'] = self.markers_arr.time.to_numpy()

        ch_list = ['a','b','c']
        for ch_label, marker_label in zip(ch_list, labels_markers):
            self.df[ch_label+'_x'] = self.markers_arr.sel(axis='x', channel=marker_label,).to_numpy()
            self.df[ch_label+'_y'] = self.markers_arr.sel(axis='y', channel=marker_label,).to_numpy()
            self.df[ch_label+'_z'] = self.markers_arr.sel(axis='z', channel=marker_label,).to_numpy()

        self.interpolation_filter(ch_list)
        self.smooth_filter(ch_list)
        self.angles_rad = self.angle_between_three_markers()
        self.angles_deg = np.rad2deg(self.angles_rad)
        self.arr_time_angles_max, self.arr_time_angles_min = self.get_time_max_and_min_angles()

    ######
    def interpolation_filter(self, ch_list):
        for ch in ch_list:
            self.df[ch+'_x'] = self.df[ch+'_x'].interpolate(method="cubicspline", limit_direction='both')
            self.df[ch+'_y'] = self.df[ch+'_y'].interpolate(method="cubicspline", limit_direction='both')
            self.df[ch+'_z'] = self.df[ch+'_z'].interpolate(method="cubicspline", limit_direction='both')
        return 0
    
    #####
    def smooth_filter(self, ch_list):
        for ch in ch_list:
            self.df[ch+'_x']=savgol_filter(self.df[ch+'_x'].to_numpy(), window_length=10, polyorder=2, mode='mirror')
            self.df[ch+'_y']=savgol_filter(self.df[ch+'_y'].to_numpy(), window_length=10, polyorder=2, mode='mirror')
            self.df[ch+'_z']=savgol_filter(self.df[ch+'_z'].to_numpy(), window_length=10, polyorder=2, mode='mirror')
        return 0
    
    #####
    def angle_between_three_markers(self):
        ## taking data from dataframe to numpy array
        a_vector = self.df[['a_x','a_y','a_z']].to_numpy()
        b_vector = self.df[['b_x','b_y','b_z']].to_numpy()
        c_vector = self.df[['c_x','c_y','c_z']].to_numpy()

        # print(f"a_vector:\n{a_vector}")
        # print(f"b_vector:\n{b_vector}")
        # print(f"c_vector:\n{c_vector}")

        ab_vector = a_vector - b_vector
        cb_vector = c_vector - b_vector

        ang_rad = self.get_angles(ab_vector, cb_vector)
        return ang_rad

    #####
    def get_angles(self, arr_a, arr_b):
        # arr_a = get_vector_section(df, side+'ud', side+'up')
        # arr_b = get_vector_section(df, side+'ld', side+'lp')
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
    
    ######
    def get_time_max_and_min_angles(self):
        max_list=[]
        min_list=[]
        win_size = 60
        delta = 10
        id0 = 0

        arr = self.angles_deg
        
        while id0 < len(arr):
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

        ## from samples' number to time
        arr_time = self.df['time'].to_numpy()
        t_sel_max = arr_time[ids_sel_max]
        t_sel_min = arr_time[ids_sel_min]

        return t_sel_max, t_sel_min

    ######
    def get_df(self):
        return self.df
    
    ######
    def get_time(self):
        return self.df.time.to_numpy()
    
    ######
    def get_angles_rad(self):
        return self.angles_rad
    
    ######
    def get_angles_deg(self):
        return self.angles_deg
    
    ######
    def get_arr_time_angles_max(self):
        return self.arr_time_angles_max
    
    ######
    def get_arr_time_angles_min(self):
        return self.arr_time_angles_min





# def max_and_min(arr):
        
#     max_list=[]
#     min_list=[]
#     win_size = 60
#     delta=10
#     id0=0
    
#     while id0 < len(arr):
#         window = arr[id0:id0+win_size]
#         ids_max = np.argmax(window)
#         ids_min = np.argmin(window)
        
#         max_list.append(ids_max+id0) 
#         min_list.append(ids_min+id0) 
#         id0 = id0 + delta
    
#     ids_max, max_counts = np.unique(max_list, return_counts=True)
#     ids_min, min_counts = np.unique(min_list, return_counts=True)
    
#     # print(f'max:\n{ids_max}, {max_counts}')
#     # print(f'min:\n{ids_min}, {min_counts}')
    
#     ## ids occurrences greater than 1
#     sel_max = np.argwhere(max_counts > 1).reshape(1,-1)
#     sel_min = np.argwhere(min_counts > 1).reshape(1,-1)
    
#     # print(f'indices max: {sel_max}')
#     # print(f'indices min: {sel_min}')
    
#     ids_sel_max = ids_max[sel_max[0]]
#     ids_sel_min = ids_min[sel_min[0]]
    
#     # print(f'values max: {ids_sel_max}')
#     # print(f'values min: {ids_sel_min}')

#     return ids_sel_max, ids_sel_min


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
 
def main(args):


    # data_path = "../tests/data/markers_analogs.c3d"
    data_path = args[1]

    markers_right_list = markersets_dict['abc005']['right']
    markers_left_list  = markersets_dict['abc005']['left']

    obj_right = Leg_kinematics(data_path, markers_right_list, 'right')
    obj_left  = Leg_kinematics(data_path,  markers_left_list,  'left')

    arr_time_max_extension_right = obj_right.get_arr_time_angles_max()
    arr_time_max_extension_left  = obj_left.get_arr_time_angles_max()

    # #################
    # ## visualization
    # fig, ax = plt.subplots(2, 1, sharex=True)
    # ax = ax.flatten()
    # ymin =  80
    # ymax = 130
    # # ax[0].vlines(ts_sel_max, ymin=100,ymax=150, colors='tab:green', alpha=0.5, lw=0.5)
    # ax[0].vlines(arr_time_max_extension_right, ymin=ymin,ymax=ymax, colors='tab:purple', alpha=0.5, lw=0.5)
    # ax[1].vlines(arr_time_max_extension_left,  ymin=ymin,ymax=ymax, colors='tab:purple', alpha=0.5, lw=0.5)

    # ax[0].plot(obj_right.get_time(), obj_right.get_angles_deg())
    # ax[1].plot(obj_left.get_time(),  obj_left.get_angles_deg())

    # ax[0].set_ylim([ymin,ymax])
    # ax[1].set_ylim([ymin,ymax])
    # ## visualization
    # #################
    
    ###############
    ## EMG reading
    



    plt.show(block=True)
    return 0


    # data = markers_right.sel(axis='x', channel='Markerset_001:Marker_001', ).plot.line(x='time')
    # data_x = markers_right.sel(axis='x', channel='right_leg:Marker_001',)
    # data_right_ch1 = markers_right.sel(channel='right_leg:Marker_001', )

    df = pd.DataFrame()
    df['time'] = markers_right.time.to_numpy()

    ch_list = ['a','b','c']
    
    for ch_label, marker_label in zip(ch_list, markers_right_list):
        df[ch_label+'_x'] = markers_right.sel(axis='x', channel=marker_label,).to_numpy()
        df[ch_label+'_y'] = markers_right.sel(axis='y', channel=marker_label,).to_numpy()
        df[ch_label+'_z'] = markers_right.sel(axis='z', channel=marker_label,).to_numpy()

    # print(f"df:\n{df}")

    # fig, ax = plt.subplots(3, 3, sharex=True)
    # ax = ax.flatten()

    # id=0
    # for ch_label in ch_list:
    #     ax[id+0].plot(df['time'], df[ch_label+'_x'], )
    #     ax[id+1].plot(df['time'], df[ch_label+'_y'], )
    #     ax[id+2].plot(df['time'], df[ch_label+'_z'], )
    #     id+=3

    df = interpolation_filter(df, ch_list)
    df = smooth_filter(df, ch_list)

    print(f"df:\n{df}")

    ###############
    ## taking data from dataframe to numpy array
    a_vector = df[['a_x','a_y','a_z']].to_numpy()
    b_vector = df[['b_x','b_y','b_z']].to_numpy()
    c_vector = df[['c_x','c_y','c_z']].to_numpy()

    # print(f"a_vector:\n{a_vector}")
    # print(f"b_vector:\n{b_vector}")
    # print(f"c_vector:\n{c_vector}")

    ab_vector = a_vector - b_vector
    cb_vector = c_vector - b_vector

    ang_rad = get_angles(ab_vector, cb_vector)
    
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax = ax.flatten()
    ax[0].plot(df['time'], np.rad2deg(ang_rad))
    

    # print(f"ab_vector:\n{ab_vector}")
    # print(f"cb_vector:\n{cb_vector}")




    # #############
    # ## a-b, c-b
    # df = vector_diff(df,'a','b')
    # df = vector_diff(df,'c','b')



    # def vector_diff(df, label_1,label_2):
    #     df[label_1+label_2+'_x'] = df[label_1+'_x'] - df[label_2+'_x']
    #     df[label_1+label_2+'_y'] = df[label_1+'_y'] - df[label_2+'_y']
    #     df[label_1+label_2+'_z'] = df[label_1+'_z'] - df[label_2+'_z']
    #     return df



    # id=0
    # for ch_label in ch_list:
    #     ax[id+0].plot(df['time'], df[ch_label+'f_x'], )
    #     ax[id+1].plot(df['time'], df[ch_label+'f_y'], )
    #     ax[id+2].plot(df['time'], df[ch_label+'f_z'], )
    #     id+=3

    #####
    ## dot product between two vectors to calculate the angle between them


    # fig, ax = plt.subplots(3, 3, sharex=True)
    # ax = ax.flatten()

    # id=0
    # for ch_label in ch_list:
    #     ax[id+0].plot(df['time'], df[ch_label+'_x'], df['time'], df[ch_label+'f_x'], )
    #     ax[id+1].plot(df['time'], df[ch_label+'_y'], df['time'], df[ch_label+'f_y'], )
    #     ax[id+2].plot(df['time'], df[ch_label+'_z'], df['time'], df[ch_label+'f_z'], )
    #     id+=3
    
    # print(f"data_x:\n{data_x}")
    # print(f"data_x:\n{data_x.to_numpy()}")
    # print(f"dataframe:\n {data_right_ch1.to_dataframe()}")
    # print(f"markers_right.attrs:\n{markers_right.attrs}")

    # data_time = markers_right.sel(axis='x', channel='Markerset_001:Marker_001',)
    # data_time = markers_right.time.to_numpy()
    # print(f"time:\n{data_time}")
    
    # print(f"time:\n{data_time.time.to_numpy()}")

    # markers_null_values = markers_right.sel(axis="x").isnull()
    # print(f"There are {markers_null_values.sum().values} missing values")

    # markers_null_values.sum(dim="time").to_series().nlargest(5).plot.barh()
    # markers_null_values.sum("channel").cumsum("time").plot()

    # markers_without_null = markers_right.interpolate_na(dim="time", method="cubic")

    plt.show(block=True)

    return 0

    path = '../data/VL/' 
    filename_csv = 'VL_active_assis_labels.csv'


    # filename = '../data/VL/VL_active_assis_labels.csv'
    # filename_emg = '../data/motive_tracking/tracking_006_s1/ebc_006_s01_e1.mat'

    # c3d_files = recordings.VL_c3d_files
    # print(f'c3d files:\n{type(c3d_files)}, \n{c3d_files}')
    # print(f"c3d active: {c3d_files['ac']}")

    # csv_files = recordings.VL_csv_files
    # print(f'csv files:\n{type(csv_files)}, \n{csv_files}')
    # print(f"csv active: {csv_files['ac']}")
    
    # r = c3d.Reader(open(path+c3d_files['ac'], 'rb'))
    # print(f'header: {r.header}')
    
    # for i, points, analog in r.read_frames():
    #     print('frame {}: point {}, analog {}'.format(i, points.shape, analog.shape))


    # reading csv file. Header includes: Frame, Time, ... 
    df = pd.read_csv(path+filename_csv, header=6)
    
    # df = pd.read_csv(path+csv_files['ac'], header=2)
    # print(f'header 3:\n{df.head()}')
    # print(f'{df.columns}')

    # columns_names = df.columns
    # id = np.argwhere(columns_names=='Unlabeled:140')
    # print(f'id = {id}')


    # df = pd.read_csv(path+csv_files['ac'], header=5)
    # print(f'header 6:\n{df.head()}')
    # print(f'{df.columns}')

    
    # print(f'{df}')
    # print(f'{df.iloc[:,6].tolist()}')
    
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

    ## finding location of maximums and minimums (positive and negative picks) of the angles' vector to identify the sample' number for max. flexion and max. extension for each leg. Maximum values 
    ids_max_r, ids_min_r = max_and_min(ang_r)
    ids_max_l, ids_min_l = max_and_min(ang_l)
    
    sample_rate_tracking = 120 ## samples per second (Hz)
    ## time in seconds
    t_delay=0.0
    arr_time_max = np.array(ids_max_r)/sample_rate_tracking - t_delay
    arr_time_min = np.array(ids_min_r)/sample_rate_tracking - t_delay
    # print(f'max and min:\n{max_list},\n{min_list}')

    # plot_angles(ang_r, ids_max_r, ids_min_r)
    # plot_angles(ang_l, ids_max_l, ids_min_l)

    ## synchonization between kinematics and EMG
    ## first reading EMG
    filename_emg = 'BED CYCLING_active_assis.mat'
    file_channels = [9,17]

    obj_emg = Reading_EMG(path, filename_emg, file_channels)
    obj_emg.plotSignals()
    
    obj_emg.filteringSignals()
    obj_emg.envelopeFilter()

    # ids_emg_plot = [5,7,3,0,6,4,2,1]
    ids_emg_plot = [1,3,7,5,0,2,6,4]
    title_emg = 'A - L2 (6 weeks)    -> B - L2 (12 months)'
    patient_number = '006'
    session_name='a'
    file_number=0
    act_emg=[0,1,2,3,5,6,7]
    channels_names = ['VMO LT, uV', 'VMO RT, uV', 'VLO LT, uV', 'VLO RT, uV', 'LAT.GASTRO LT, uV', 'LAT.GASTRO RT, uV', 'TIB.ANT. LT, uV', 'TIB.ANT. RT, uV']
    
    # obj_emg.plotFilteredSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names)
    
    obj_emg.plotSegmentedSignals(ids_emg_plot, title_emg, patient_number,session_name, file_number+1, act_emg, channels_names, arr_time_max, arr_time_min)
    
    plt.show()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))