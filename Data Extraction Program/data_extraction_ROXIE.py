

import os, sys

from load_data import get_txt_files_in_folder 
from magnet_data import extract_magnetdata, write_magnet_file

#Works well now for retreiving data.
def main():
  
    folder = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\FRESCA raw ROXIE files\\Single Coil Horizontal'#\\Horizontal Movement'
    file_names = get_txt_files_in_folder(folder)
    #retrieves Total Inductance, Mutual Inductance matrix and B-field list
    magnetdata = extract_magnetdata(file_names, folder)
    
    
    
    horizontal = magnetdata[0:5]
  #  bottom_roll = magnetdata[5:10]
  #  horizontal = magnetdata[11:16]
   # mid_roll = magnetdata[21:26]
   # vertical = magnetdata[26:31]
   
    write_magnet_file(horizontal, \
        '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\Documents\\ROXIE\\Processed Data\\FRESCA2\\Horizontal.csv')

'''
    for i1 in angular:
        print(i1.file_name()) 

    for i2 in bottom_roll:
        print(i2.file_name())
         
    for i3 in horizontal:
        print(i3.file_name())

    print(len(mid_roll))
    for i4 in mid_roll:
        print(i4.file_name())
    print(len(vertical))
    for i5 in vertical:
        print(i5.file_name())'''


   
  #  magnetdata[1].get_B_in_QA()



if __name__ == '__main__':
    main()



