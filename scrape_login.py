import os
import json
import requests
import pandas as pd
from time import sleep

# get job overview by pages
def get_job_overview(page):
    print("downloaded overview page for page " + str(page))
    cookies = {}

    headers = { }

    data = {}

    response = requests.post(url,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    json_response = response.json()
    return json_response

# get project details
def get_job_details(seo_url):
    import requests

    headers = { }

    params = {}

    response = requests.get(url, params=params, headers=headers)
    json_response = response.json()
    return json_response

# get client info
def get_client_info(client_id):
    headers = {}

    params = {}

    response = requests.get(url, params=params, headers=headers)
    json_response = response.json()
    return json_response

# get bidders
def get_bidders(id):
    headers = {}

    params = {}
    url = '' + str(id) + '/bids'
    response = requests.get(url, params=params, headers=headers)
    json_response = response.json()
    return json_response


# get details for all private jobs
folder = "" #define location where you want data to be stored


# get the url of each project 
page_limit = get_job_overview(1)['iTotalRecords'] // 100 + 2 # in order to get the maximum page

# scrape
# change newpath
for page in range(1, page_limit):
    
    job_overview = get_job_overview(page)
    jsonString = json.dumps(job_overview, indent=2)
    print("total open jobs "  + str(job_overview['iTotalRecords']))
    
    newpath = folder + "/date/batch" + str(page) 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    path_to_overview = newpath + "/overview"
    if not os.path.exists(path_to_overview):
        os.makedirs(path_to_overview)
    with open(path_to_overview + "//overview_batch"+str(page) +".json", "w") as outfile:
        outfile.write(jsonString)
    
    a = 0
    for job in job_overview['aaData']:
        individual_job = {}
        id = job[0]
        seo_url = job[21].split('/')[2:]
        seo_url = '/'.join(seo_url) # get unique seo_url for each job
        a += 1
        print("NO." + str(a), ":" , str(id)) #check which one is wrong
        # get details
        try:      
            job_details = get_job_details(seo_url)
            job_details = job_details['result']
            
        except (KeyError, IndexError):
            job_details = "none"
        try:
            user_id = job_details['projects'][0]['owner_id']
            #get client info
            client_info = get_client_info(user_id)
            client_info = client_info['result']
        except (KeyError, IndexError):
            client_info = "none"
    #get bidders
        try:
            bidders = get_bidders(id)
            bidders = bidders['result']
        except (KeyError, IndexError):
            bidders = 'none'
        individual_job['job_details'] = job_details
        individual_job['client_info'] = client_info
        individual_job['bidders'] = bidders
        with open(newpath + "//" + str(id) + ".json", "w", encoding='UTF-8') as f:
            json.dump(individual_job, f, indent=4, ensure_ascii=False)
        
        sleep(0.5)

# convert unix timestamp
#import time
#utc_time = time.gmtime(1684954848)
#print(time.strftime("%Y-%m-%d %H:%M:%S+00:00 (UTC)", utc_time))  

