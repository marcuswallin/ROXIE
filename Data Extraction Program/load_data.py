import os
from os import listdir

def get_txt_files_in_folder(folder_name):
    
    all_files = []

    files = os.listdir(folder_name)
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if not file_extension:
            for f in get_txt_files_in_folder(folder_name +'\\' +filename):
                all_files.append(filename + '\\' + f)
        elif (file_extension == '.txt'):
            all_files.append(file)
    return all_files




