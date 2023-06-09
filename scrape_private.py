import os
import json
import requests
import pandas as pd

def get_private_job_overview(id):
    cookies = {}

    headers = {}

    data = {}

    response = requests.post()
    json_response = response.json()
    return json_response

# get project details
def get_private_job_details(seo_url):
    import requests

    headers = {}

    params = {}

    response = requests.get()
    json_response = response.json()
    return json_response

# get client info
def get_client_info(user_id):
    headers = {}

    params = {}

    response = requests.get()
    json_response = response.json()
    return json_response

# get bidders
def get_bidders(id):
    headers = {}

    params = { }
    url = '' + str(id) + '/bids'
    response = requests.get(url, params=params, headers=headers)
    json_response = response.json()
    return json_response



# get details for all private jobs
path_to_json = '' 
json_files = []

# get all paths to the private projects
for root, dirs, files in os.walk(path_to_json):
    for f in files:
        if f.endswith('_private.json'):      #Check for .json exten
            json_files.append(os.path.join(root, f))    #append full path to file

# import all private projects to python
private_projects_all = []
for json_file in json_files:
    with open(json_file) as myfile:
        data = json.load(myfile)
        #data=myfile.read() 
        private_projects_all.append(data)
        
# extract project id of all private projects
project_id_list = []
for li in range(0, len(private_projects_all)):
            project_id = private_projects_all[li]
            try:
                project_id = project_id[0]['project_id']
                project_id_list.append(project_id)
            except:
                pass



# get the url of each project 
print("private jobs in total: " + str(len(project_id_list)))
a = 0
for id in project_id_list:
    private_jobs = {}
    a += 1
    print("scraping NO." + str(a) + ":" + str(id))
    private_job_overview = get_private_job_overview(id)
    private_job_overview = private_job_overview['aaData']
    try:
        seo_url = private_job_overview[0][21].split('/')[2:]
        seo_url = '/'.join(seo_url)
        #get details
        private_job_details = get_private_job_details(seo_url)
        private_job_details = private_job_details['result']
    except:
        private_job_details = "none"
    try:
        user_id = private_job_details['projects'][0]['owner_id']
        #get client info
        client_info = get_client_info(user_id)
        client_info = client_info['result']
    except:
        client_info = "none"
    #get bidders
    bidders = get_bidders(id)
    bidders = bidders['result']
    
    private_jobs['overview'] = private_job_overview
    private_jobs['details'] = private_job_details
    private_jobs['client_info'] = client_info
    private_jobs['bidders'] = bidders
    newpath = path_to_json + "/private_jobs" 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    with open(newpath + "//" + str(id) + ".json", "w", encoding='UTF-8') as f:
        json.dump(private_jobs, f, indent=4, ensure_ascii=False)


# convert unix timestamp
#import time
#utc_time = time.gmtime(1683330001)
#print(time.strftime("%Y-%m-%d %H:%M:%S+00:00 (UTC)", utc_time))  



