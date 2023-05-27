#!/usr/bin/env python
# coding: utf-8


import os
import re
import numpy as np
import glob
import sys
import pathlib
from pathlib import Path
####class no_newlist_found(Exception)

################################# Take user input for camera and filter info  (filter need obsolete).

print('\n' + "Camera name case sensitive, enter in format: WFC3ir, WFC3uvis, WFCP2, etc")
camera_name = input("Enter camera name: ") 
#print('\n' + "Filter name is NOT case sensitive")
#filter_name = input("Enter filter name: ")

filter_name = os.listdir('/store/skysurf/' + camera_name.lower())


for f in filter_name:
    
    print('\n')
    
    path_start = os.path.join('/store/skysurf/' + camera_name.lower() + '/' + f + '/')


################################# Find newlist files and isolate only the most recent version which will be the highest numbered newlist file
################################# will then use this most recent newlist file to compare to fits files in /data or /new_data directory.
    newlist_file_list = []
    is_newlist = "newlist_" + camera_name
    newlist_path = os.listdir(path_start)
    for i in newlist_path:
        if is_newlist in i:
            newlist_file_list.append(i)
        else:
            pass
    if len(newlist_file_list) == 0:
        print("No newlist file in filter " + f)
        pass
    max = 0
    for i in newlist_file_list:
        newlist_number = int(re.search('newlist_' + camera_name + '(\d*)', i).group(1))
        max = newlist_number if newlist_number > max else max
    newlist_max = str(max)
    if max == 0:
        newlist = 'newlist_' + camera_name + '_' + f + '.txt'
    else:
        newlist = 'newlist_' + camera_name + newlist_max + '_' + f + '.txt'
        

#################################### Check where fits files are located, some filters have this as /data some as /new_data
#################################### will print an error message if neither is found and exit.
    
    fits_files1 = []
    fits_files2 = []
    
    if os.path.isdir(path_start + 'data'):
        print("Found /data for " + f)
        path = os.path.join(path_start + 'data')
        fits_files1 = os.listdir(path)
        if os.path.isdir(path_start + 'new_data'):
            print("Found /new_data for " + f)
            path1 = os.path.join(path_start + 'new_data')
            fits_files2 = os.listdir(path1)
            
    elif os.path.isdir(path_start + 'new_data'):
        print("Found /new_data for " + f)
        path = os.path.join(path_start + 'new_data')
        fits_files1 = os.listdir(path)
        
    else:
        print("ERROR: Could not locate fits files in /data or /new_data subfolders for filter." + f)
        print("Please check name of subfolder fits files are located, rename to /data or /new_data and restart.")
        continue

################################### create list of fits files from directory to compare to newlist file
    fits_files = fits_files1 + fits_files2
    is_fits_file = ".fits.gz"
    output_file_name = 'newlist_' + camera_name + newlist_max + '_' + f + '_missing_image_list.txt'
    output_file_path = os.path.join(path_start, output_file_name)

    
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    if os.path.exists(duplicate_file_path):
        os.remove(duplicate_file_path)
    
    output_file = open(output_file_path, 'w')
    final_fit_list = []    
    for i in fits_files:
        if is_fits_file in i:
            head, sep, tail = i.partition('_')
            final_fit_list.append(head)
        else:
            pass

################################### comparison of the two files, writes missing files to output file, if no missing files found
################################### using the no_match flag, will write "No missing files" to the output file. Closes files when done.
    try:
        file1 = open(os.path.join(path_start + newlist), 'r')
        newlist_lines = file1.read()
        no_match = 0
        for i in final_fit_list:
            if i in newlist_lines:
                pass
            else:
                output_file.write(i + '\n')
                no_match += 1 
            duplicate = 0
        if no_match == 0:
            output_file.write("No missing files")
        file1.close()
        output_file.close()
        
        print("Completed. Missing files will be listed in: " + '\n' + output_file_path)
    except FileNotFoundError as e:
        pass

print('\n \n' + "The following filters completed: ")
print(*filter_name, sep = ", ")


# In[ ]:




