import argparse
from class_emg_assis import Reading_EMG_Assis
import matplotlib.pyplot as plt
import sys
import os
import numpy as np

from selected_channels_names import list_selected_channels
from files_names_emg import list_files_names
from read_kinematics_pyomeca import Leg_kinematics
# import markers_list as recordings
from markersets_names import markersets_dict


############################
def plot_EMG_kinematics(self, obj_emg, obj_kin_left, obj_kin_right, channels_names, path, save_figs):

    # # print(f"channels names: {channels_names, len(channels_names)}")        
    # num_rows = len(channels_names)//2
    # # num_rows = math.ceil(len(channels_names)/2)
    # fig, ax = plt.subplots(nrows=num_rows, ncols=2, figsize=(10, 7), sharex=True, squeeze=False)
    # fig.canvas.mpl_connect('key_press_event', self.on_press)
    
    # ax = ax.reshape(-1)
    
    ## plot EMG signals
    for ch_name, ax_single in zip(channels_names, ax):
        if (ch_name in self.channels_data) and not(ch_name.startswith('Insole')):
            # print(f"plot channels filtered and enveloped")
            ax_single.plot(self.ch_time, self.channelsFiltered[ch_name], label=ch_name, alpha=0.5)
            ax_single.plot(self.ch_time, self.channelsEnveloped[ch_name], alpha=1.0, lw=2.5)
            ax_single.legend()
        else:
            ## selected channel was not recorded
            ax_single.plot(self.ch_time, np.zeros(len(self.ch_time)), alpha=0.2)

        ## different y-scale for EMG and plantar pressure
        if ch_name.startswith('Insole'):
            ax_single.set_ylim([0,100])
        else:
            ax_single.set_ylim([-50,50])
            
    
    ## plot Insole curves (left and right) together
    ## in the last row of subplots
    in_r = 'Insole.Total RT, %'
    in_l = 'Insole.Total LT, %'
    if in_r in self.channels_data:
        ax[-2].plot(self.ch_time, self.channels_data[in_r],color='m',label='In_R, %', alpha=1.00)
        ax[-1].plot(self.ch_time, self.channels_data[in_r],color='m',label='In_R, %', alpha=0.25)
        ax[-2].legend()
        ax[-1].legend()
    else:
        pass
    if in_l in self.channels_data:
        ax[-2].plot(self.ch_time, self.channels_data[in_l],color='c',label='In_L, %', alpha=0.25)
        ax[-1].plot(self.ch_time, self.channels_data[in_l],color='c',label='In_L, %', alpha=1.00)
        ax[-2].legend()
        ax[-1].legend()
    else:
        pass

    ## select number of seconds range of data at the middle of the recordings
    val1 = 5.0
    val2 = val1*2.0
    id01 = (len(self.ch_time)/2 - (self.sampling_rate*val1)).astype(int)
    id02 = (id01 + (self.sampling_rate*val2)).astype(int)
    
    ## adjust x-scale for the first and for all the subplots (sharex=True)
    # ax[0].set_xlim([self.ch_time[id01],self.ch_time[id02]])

    ax[-2].set_xlabel(self.ch_time_name+' [s]')
    ax[-1].set_xlabel(self.ch_time_name+' [s]')
    
    filename = self.filename.split('.')[0]
    fig.suptitle(f'{filename}\n{self.date}')
    
    # if save_figs:
    #     ### save figures ####
    #     # path_out=f'../data/a_velo_assis/figures/figs/'
    #     path_out= path + 'figures/'
    #     # checking if the directory
    #     # exist or not. 
    #     if not os.path.isdir(path_out): 
    #         # if directory is  
    #         # not present then create it. 
    #         os.makedirs(path_out) 
        
    #     plt.savefig(f'{path_out}/{filename}.png', bbox_inches='tight')
    #     ### save figure ####
    # else:
    #     pass
    
    return 0
############################


def main(args):

    print(f"velo assis emg data")
    list_session_names={0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g',}
    # Initialize parser
    parser = argparse.ArgumentParser(description = 'EMG filtering')

    # Adding optional argument
    parser.add_argument('-d', '--dir_name', type = str, help = "Select directory, for example: ../data/a_velo_assis/")
    parser.add_argument('-p', '--patient_id', type = str, help = "Select file number, for example: as01")
    parser.add_argument('-s', '--session', type = int, help = "Select session (0,1,2), for example: 0")
    
    args = parser.parse_args()
    session=args.session
    sn = list_session_names[int(session)]
    path_ses = args.dir_name+f'{args.patient_id}/'+f'session_{sn}/'
    path_emg = path_ses+'emg_data/'
    path_kin = path_ses+'kin_data/'
    patient_id=args.patient_id
    
    print(f'path and files: {path_ses}, {patient_id}, {session}')

    channel_names = list_selected_channels[patient_id][int(session)]

    files_names_emg = list_files_names[patient_id]['emg_'+str(session)]
    files_names_kin = list_files_names[patient_id]['kin_'+str(session)]

    print(f'files:\nemg: {files_names_emg}\nkin: {files_names_kin}')

    # print(f'list channels: {list_channels}')
    # print(f'channels-sorted: {ids_emg_sorted}')
    
    # print(f'selected file: {filename}, channels: {file_channels}')
    obj_emg_list = [[]]*len(files_names_emg)
    obj_kin_left  = [[]]*len(files_names_kin)
    obj_kin_right = [[]]*len(files_names_kin)
    

    #############################
    # print(f"channels names: {channels_names, len(channels_names)}")        
    num_rows = len(channel_names)//2
    # num_rows = math.ceil(len(channels_names)/2)
    # fig.canvas.mpl_connect('key_press_event', self.on_press)
    fig_list = []
    ax_list = []
        
    #############################
    ## EMG
    save_fig = False
    i=0
    for filename_emg in files_names_emg:
        # fig, ax = plt.subplots(nrows=num_rows, ncols=2, figsize=(10, 7), sharex=True, squeeze=False)
        # ax = ax.flatten()

        print(f'reading file: {filename_emg}, ... \n', end='')
        # create object class
        obj_emg_list[i] = Reading_EMG_Assis(path_emg, filename_emg, channel_names)
        
        if obj_emg_list[i].get_flag_empty()==False:
            obj_emg_list[i].filteringSignals_assis(channel_names,)
            obj_emg_list[i].envelopeFilter_assis()
            # obj_emg_list[i].plotEMGSession_assis_filtered(channel_names)
            # fig, ax = obj_emg[i].plotEMGSession_assis_filtered(channel_names, fig, ax)
            # obj_emg[i].plotEMGSession_assis_filtered(channel_names, path_emg, save_fig)

        else:
            print(f"empty obj {filename_emg}")
        
        print(f'done.')

        # fig_list.append(fig)
        # ax_list.append(ax)

        i+=1
    ## EMG
    #############################

    #############################
    ## Kinematics
    arr_time_max_extension_right = [[]]*len(files_names_kin)
    arr_time_max_extension_left  = [[]]*len(files_names_kin)

    markers_right_list = markersets_dict[patient_id]['right']
    markers_left_list  = markersets_dict[patient_id]['left']
    
    i=0
    for filename_kin in files_names_kin:

        print(f'reading file:  {filename_kin}, ... \n', end='')
        print(f'initials file: {filename_kin[:5]}, ... \n', end='')
        ## the initials 5 characters define the time of data collection, i.e. 00min, 05min, 10min,...
        ## we compare those initials to the initials of the emg filenames to pair them
        initials_kin_filename = filename_kin[:5]

        # create object class
        obj_kin_left[i]  = Leg_kinematics(path_kin, filename_kin, markers_left_list,  'left')
        obj_kin_right[i] = Leg_kinematics(path_kin, filename_kin, markers_right_list, 'right')

        markers_time_left_max  = obj_kin_left[i].get_time_angles_max()
        markers_time_left_min  = obj_kin_left[i].get_time_angles_min()
        markers_time_right_max = obj_kin_right[i].get_time_angles_max()
        markers_time_right_min = obj_kin_right[i].get_time_angles_min()

        for obj_emg in obj_emg_list:
            if (initials_kin_filename in obj_emg.getFilename()):
                obj_emg.setTimeAnglesMarkers(markers_time_left_max, 'left_max')
                obj_emg.setTimeAnglesMarkers(markers_time_left_min, 'left_min')
                obj_emg.setTimeAnglesMarkers(markers_time_right_max, 'right_max')
                obj_emg.setTimeAnglesMarkers(markers_time_right_min, 'right_min')
                break

                # obj_emg.plot_vlines(arr_markers_time,' LT,')

                # fig_list[i], ax_list[i] = obj_kin_left[i].plot_sync_kinematics(channel_names, fig_list[i], ax_list[i], ' LT,')
            
            
            # fig_list[i], ax_list[i] = obj_kin_right[i].plot_sync_kinematics(channel_names, fig_list[i], ax_list[i], ' RT,')
            # arr_time_max_extension_right[i] = obj_kin_left[i].get_arr_time_angles_max()
            # arr_time_max_extension_left[i]  = obj_kin_right[i].get_arr_time_angles_max()
            # print(f"{filename_kin} angles right:\n{arr_time_max_extension_right[i]}")
            print(f'done.')
        else:
            print(f"empty obj {filename_kin}")

        i+=1

    ## Kinematics
    #############################
    ## visualization emg + kinematics landmarks (time extension max.)

    # a = obj_emg_list[-1].getFilename()
    # b = obj_emg_list[-1].getChannelsNames()
    # c = obj_emg_list[-1].get_flag_empty()
    # print(f"{a}\n{b}\n{c}")

    obj_emg_list[-1].plot_selected_emg(channel_names)
    obj_emg_list[-1].flexion_extension('VMO RT, uV')

    # plot_EMG_kinematics(obj_emg, obj_kin_left, obj_kin_right, channel_names, path_ses, save_fig)

    # if save_figs:
    #         ### save figures ####
    #         # path_out=f'../data/a_velo_assis/figures/figs/'
    #         path_out= path + 'figures/'
    #         # checking if the directory
    #         # exist or not. 
    #         if not os.path.isdir(path_out): 
    #             # if directory is  
    #             # not present then create it. 
    #             os.makedirs(path_out) 
            
    #         plt.savefig(f'{path_out}/{filename}.png', bbox_inches='tight')
    #         ### save figure ####
    #     else:
    #         pass
    
    plt.ion()
    plt.show(block=True)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

