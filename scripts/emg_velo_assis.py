import argparse
from class_emg_assis import Reading_EMG_Assis
import matplotlib.pyplot as plt
import sys

from selected_channels_names import list_selected_channels
from files_names_emg import list_files_names

def main(args):

    print(f"velo assis emg data")
    
    # Initialize parser
    parser = argparse.ArgumentParser(description = 'EMG filtering')

    # Adding optional argument
    parser.add_argument('-d', '--dir_name', type = str, help = "Select directory, for example: ../data/a_velo_assis/")
    parser.add_argument('-p', '--patient_id', type = str, help = "Select file number, for example: as01")
    parser.add_argument('-s', '--session', type = int, help = "Select session (0,1,2), for example: 0")
    
    args = parser.parse_args()

    path_emg=args.dir_name+f'{args.patient_id}/'
    patient_id=args.patient_id
    session=args.session
    
    print(f'path and files: {path_emg}, {patient_id}, {session}')

    list_session_names={0:'a', 1:'b', 2:'c', 3:'d',}

    channel_names = list_selected_channels[patient_id][int(session)]

    files_names = list_files_names[patient_id][int(session)]

    sn = list_session_names[int(session)]

    # print(f'files: {files_names}')
    # print(f'list channels: {list_channels}')
    # print(f'channels-sorted: {ids_emg_sorted}')
    
    # print(f'selected file: {filename}, channels: {file_channels}')
    obj_emg = [[]]*len(files_names)
    
    path_emg = path_emg+f'session_{sn}/'
    
    i=0
    for filename_emg in files_names:
        try:
            print(f'reading file: {filename_emg}, ... \n', end='')
            # create object class
            obj_emg[i] = Reading_EMG_Assis(path_emg, filename_emg, channel_names)
            
            obj_emg[i].filteringSignals_assis(channel_names,)
            obj_emg[i].envelopeFilter_assis()
            obj_emg[i].plotEMGSession_assis_filtered(channel_names,)
            
            print(f'done.')
            
        except ValueError:
            print(f'Problem reading the selected files.')
        i+=1

    plt.ion()
    plt.show(block=True)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

