#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 13:31:39 2023

@author: zixin.pan
"""
import os



path_to_json = '' 
json_files = []
# get all paths to the detail json files
for root, dirs, files in os.walk(path_to_json):
    for f in files:
        if f.endswith('_details.json'):      #Check for .json exten
            json_files.append(os.path.join(root, f))    #append full path to file
files_all = []           
for i in json_files:
    a = i.rsplit('/', 1)[1].rsplit('_', 1)[0]
    files_all.append(a)
    
    

sam_list = list(set(files_all)) 
