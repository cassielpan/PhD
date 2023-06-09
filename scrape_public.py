import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
from time import sleep

# get the overview of the jobs
def get_job_overview(page):
    print("downloaded overview page for page " + str(page))
    headers = {}
    job_start = (page-1)* 100
    response = requests.get(
         headers=headers
    )
    json_response = response.json()
    return json_response


# get the details of the projects
projects = []
def get_job_detail(url):
    job = {}
    client = {}
    verification = []
    freelancer = {}
    bidder_name = []
    bidder_link = []
    bidder_info = []
    bidder_price = []
    bidder_rating = []
    bidder_review = []
    bidder_earning_label =[]
    bidder_earning_progress = []
    winner = {}
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    # skills, location(may not exist), and project ud
    try:
        section_details = []
        for section in data.find_all('p', class_ ='PageProjectViewLogout-detail-tags'):
            section_individual = section.text
            section_details.append(section_individual)
        project_id = section_individual.rsplit(':', 1)[1].rsplit('#', 1)[1].strip()      
    except:
        section_details = "none"
        project_id = "none"
    # get the title
    try:
        title = data.find('h1',class_="PageProjectViewLogout-header-title").text
    except:
        title = "none"
    # get budget range
    try:    
        budget_range = data.find('p',class_="PageProjectViewLogout-header-byLine").text
        budget_range = budget_range.split(' ', 1)[1]
    except:
        budget_range = "none"
    # get job description
    try:
        job_description = data.find('p',class_="PageProjectViewLogout-detail-paragraph").text
        job_description = job_description.rsplit(':', 1)[1].strip() # only keep contents and delete first white space
    except:
        job_description = "none"
    # get skills
    try:
        skills = data.find('p',class_="PageProjectViewLogout-detail-tags").text
        skills = skills.rsplit(':', 1)[1].strip()
    except:
        skills = "none"    
    # get rating
    try:
        rating = data.find('span',class_="Rating Rating--labeled profile-user-rating PageProjectViewLogout-detail-reputation-item")["data-star_rating"]
    except:
        rating = "none"    
    # get the number of reviews
    try:
        review = data.find('span',class_="Rating-review").text
        review = review.split('(', 1)[1].split(')')[0].strip("\n").strip() # clear the output, remove blank spaces
    except:
        review = "none"    
    # get the place of the requests
    try:
        place = data.find('span',{"itemprop" : "addressLocality"}).text.strip()
    except:
        place = "none"    
    # get the info about verification
    try:
        for li_tag in data.find_all('li', class_ = "is-verified verified-item Tooltip--top"):
            all_info = li_tag['data-qtsb-label']
            verification.append(all_info)
    except:
        verification = "none" 
    # remaining open days
    try:    
        open_days = data.find('div', class_ = "Grid-col Grid-col--tablet-3").text.strip()
    except:
        open_days = "none" 
    # overview of bidding info
    try:
        bidding = data.find('h2', class_ = "Card-heading").text
    except:
        bidding = "none" 
    # details about all freelancers
    try:
        all_free = data.find_all('div', class_ = "PageProjectViewLogout-freelancerInfo")
        for bidder in all_free:
            name = bidder.find('a', class_ = "FreelancerInfo-username").text
            link = bidder.find('a', class_ = "FreelancerInfo-username")["href"]
            link_complete = "https://www.freelancer.com" + str(link) 
            info = bidder.find('p', class_ = "FreelancerInfo-about")["data-descr-full"]
            price = bidder.find('div', class_ = "FreelancerInfo-price").text
            rating = bidder.find('div', class_ = "Rating Rating--labeled")["data-star_rating"]
            review = bidder.find('div',class_="Rating-review").text
            review = review.split('(', 1)[1].split(')')[0].strip("\n").strip()
            earning_label = bidder.find('span',class_="Earnings-label").text
            earning_progress = bidder.find('span',class_="Earnings-progress")["style"]
            earning_progress = earning_progress.rsplit(':', 1)[1].strip().rstrip(';')
            #改成user分别储存
            bidder_name.append(name)
            bidder_link.append(link_complete)
            bidder_info.append(info)
            bidder_price.append(price)
            bidder_rating.append(rating)
            bidder_review.append(review)
            bidder_earning_label.append(earning_label)
            bidder_earning_progress.append(earning_progress)
    except:
        bidder_name = "none"
        bidder_link = "none"
        bidder_info = "none"
        bidder_price = "none"
        bidder_rating = "none"
        bidder_review = "none"
        bidder_earning_label = "none"
        bidder_earning_progress = "none"
        
    # other jobs from this client and similar jobs
    try:
        other_jobs_details = {}
        other_title = []
        other_link = []
        other_jobs = {}
        all_other_jobs = []
        aside = data.find('div', "Grid-col Grid-col--desktopSmall-4")
        for section in aside.find_all('section', 'PageProjectViewLogout-section'):
            category = section.find("h2", 'Card-heading').text
            for jobs in section.find_all('li', class_ = "StyledList-item"):
                job_title = jobs.find('a', class_ = "PageProjectViewLogout-section-link").text
                job_link = jobs.find('a', class_ = "PageProjectViewLogout-section-link")["href"]
                job_link_c = "https://www.freelancer.com" + str(job_link)
                other_title.append(job_title)
                other_link.append(job_link_c)
                other_jobs_details = dict(zip(other_title, other_link))
                other_jobs['job_category'] = category
                other_jobs['job_details'] = other_jobs_details
            all_other_jobs.append(other_jobs)
            other_title = []
            other_link = []
            other_jobs_details = {}
            other_jobs = {}
    except:
        all_other_jobs = "none"
    #winner
    try:
        award_info = data.find('div', class_ = 'PageProjectViewLogout-awardedTo')
        winner_name = award_info.find('a', class_ = "FreelancerInfo-username").text
        winner_link = award_info.find('a', class_ = "FreelancerInfo-username")["href"]
        winner_link_complete = "https://www.freelancer.com" + str(winner_link) 
        winner_info = award_info.find('p', class_ = "FreelancerInfo-about")["data-descr-full"]
        winner_price = award_info.find('div', class_ = "FreelancerInfo-price").text
        winner_rating = award_info.find('div', class_ = "Rating Rating--labeled")["data-star_rating"]
        winner_review = award_info.find('div',class_="Rating-review").text
        winner_review = winner_review.split('(', 1)[1].split(')')[0].strip("\n").strip()
        winner_earning_label = award_info.find('span',class_="Earnings-label").text
        winner_earning_progress = award_info.find('span',class_="Earnings-progress")["style"]
        winner_earning_progress = winner_earning_progress.rsplit(':', 1)[1].strip().rstrip(';')
    except:
        winner_name = "none"
        winner_link_complete = "none"
        winner_info = "none"
        winner_price = "none"
        winner_rating = "none"
        winner_review = "none"
        winner_earning_label = "none"
        winner_earning_progress = "none"         
    job["number"] = a
    job["project_id"] = project_id
    job["url"] = url
    job["title"] = title
    job["budget_range"] = budget_range
    job["job_description"] = job_description
    job["skills"] = skills
    job["open_days"] = open_days
    job["section_tag"] = section_details
    client["rating"] = rating
    client["review"] = review
    client["place"] = place
    client["verification"] = verification
    job["bidding"] = bidding
    freelancer["name"] = bidder_name
    freelancer["link"] = bidder_link
    freelancer["info"] = bidder_info
    freelancer["price"] = bidder_price
    freelancer["rating"] = bidder_rating
    freelancer["review"] = bidder_review
    freelancer["earning_label"] = bidder_earning_label
    freelancer["earning_progress"] = bidder_earning_progress
    # ask if the code can be clear, inorder to have users one by one
    df=pd.DataFrame.from_dict(freelancer,orient='index').transpose()
    freelancer = df.apply(pd.Series.explode).to_dict(orient='records')
    winner["name"] = winner_name
    winner["link"] = winner_link_complete
    winner["info"] = winner_info
    winner["price"] = winner_price
    winner["rating"] = winner_rating
    winner["review"] = winner_review
    winner["earning_label"] = winner_earning_label
    winner["earning_progress"] = winner_earning_progress
    #include all to job list
    job["client"] = client
    job["winner"] = winner
    job["freelancers"] = freelancer
    job["other_jobs"] = all_other_jobs
    projects.append(job)
    return projects
    

folder = "" #define location where you want data to be stored

# scrape
## redefine: date in newpath
for page in range(1,101):
    private_list_id = []
    private_list_link = []
    private_projects = []
    link_list_all = []
    projects = []
    project_overview = get_job_overview(page)
    jsonString = json.dumps(project_overview, indent=2)
    print("total open jobs "  + str(project_overview['iTotalRecords']))
            
    newpath = folder + "/08.05.2023/batch" + str(page) 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    with open(newpath + "//overview_batch"+str(page) +".json", "w") as outfile:
        outfile.write(jsonString)  

    # get public job urls
    for job in project_overview['aaData']:
        try:
            link_list = "" + str(job["seo_url"])  
            link_list_all.append(link_list)
        except: # get projects of private jobs
            private_projects.append(job)
        jsonStringPrivate = json.dumps(private_projects, indent=2)
        with open(newpath + "//" + str(page) + "_private.json", "w") as outfile:
            outfile.write(jsonStringPrivate)
    # get job details     
    a = 0
    print("existing public projects for page " + str(page) + ": " + str(len(link_list_all)))
    for i in link_list_all:
        a += 1
        print("NO." + str(a), ":", i) #check which one is wrong
        project_detail = get_job_detail(i)
        jsonStringDetails = json.dumps(project_detail, indent=2)
        with open(newpath + "//" + str(page) + "_details.json", "w") as outfile:
            outfile.write(jsonStringDetails)
        sleep(0.5)

    
    





