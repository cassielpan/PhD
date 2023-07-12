import json
import os

  
path_to_json = '' 
json_files_a = []
# get all paths to the detail json files
for root, dirs, files in os.walk(path_to_json):
    for f in files:
        if f.endswith('_jobhistory.json'):      #Check for .json exten
            json_files_a.append(os.path.join(root, f))    #append full path to file

json_files = []
# get all paths to the detail json files
for root, dirs, files in os.walk(path_to_json):
    for f in files:
        if f.endswith('_detail.json'):      #Check for .json exten
            json_files.append(os.path.join(root, f))    #append full path to file


# import all detail json files to python
history_json_all = []
#id_list = []
for json_file in json_files:
    with open(json_file) as myfile:
        data = json.load(myfile)
        #data=myfile.read() 
        history_json_all.append(data)
        #id_list.append(userid)
#aaa = list(set(id_list)) #check repetitions

detail_json_all = []
#id_list = []
for json_file in json_files:
    with open(json_file) as myfile:
        data = json.load(myfile)
        #data=myfile.read() 
        detail_json_all.append(data)
        #id_list.append(userid)
  
      
#to add ciphertext to job history  
history_json_all_new = []
a = 0
for i in history_json_all:
    i["cipher"] = json_files_a[a].rsplit('/', 1)[1].rsplit('_', 1)[0]
    a += 1
    history_json_all_new.append(i)

        
    
    
    
    
    
    
    
    
    
    
        

        