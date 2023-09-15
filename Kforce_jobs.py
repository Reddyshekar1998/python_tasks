from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import csv

# url = "https://www.kforce.com/find-work/search-jobs/#/?t=&l=%5B%5D"


# Pagination for 1000 jobs
for p in range(0,2000,1000):
    data = {"count":True,
            "select":"Industry, Title, Id, PostDate, Responsibilities, Skills, City, State, Zip, SalaryMin, SalaryMax, SalaryText, ReferenceCode, TypeCode, VisaSponsorshipJob, ApplyUrl",
            "facets":["Industry","TypeCode","Remote","ClientIndustry","TKSkills","PostDate, values:2023-09-11T21:48:35+05:30|2023-09-13T21:48:35+05:30"],
            "filter":"",
            "queryType":"simple",
            "search":"",
            "searchFields":"Industry, Title, Responsibilities, Skills, City, State, Zip",
            "highlight":"Responsibilities",
            "searchMode":"any",
            "skip":p,
            "top":1000
            }
    
# creating empty lists
    job_details = []
 

# url of kforce jobs API
    url = "https://kforcewebeast.search.windows.net/indexes/kforcewebjobentity/docs/search?api-version=2016-09-01"

    headers = {
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
    "Api-Key":"1603E4DC4C87A8E41D6BBDE4EEA4EFB7",
    "Content-Length":"520",
    "Content-Type":"application/json; charset=UTF-8",
    "Origin":"https://www.kforce.com",
    "Referer":"https://www.kforce.com/"}

# Passing headers and body to the requests
    response = requests.post(url, headers=headers, json=data)
    s = BeautifulSoup(response.content, 'html5lib').text

# Converting object format into json format
    dict = json.loads(s)
    print(len(dict['value']))
    for i in range(0,len(dict['value'])):
        job_title = dict["value"][i]["Title"]
        job_type = dict["value"][i]["TypeCode"]
        if job_type == "Direct Hire":
            job_type = "Permanent"
        else:
            job_type = job_type
        state = dict["value"][i]["State"]
        city = dict["value"][i]["City"]
        job_id = dict["value"][i]["ReferenceCode"]
        salary_min = dict["value"][i]["SalaryMin"]
        salary_max = dict["value"][i]["SalaryMax"]
        salary_text = dict["value"][i]["SalaryText"]
        if salary_text == "Years":
            salary_text = "Annually"
        elif salary_text == "Hours":
            salary_text = "Hourly"
        else:
            salary_text = salary_text
        salary = '$'+ salary_min + ' - ' + '$'+salary_max + ' per ' + salary_text
        description = dict["value"][i]["Responsibilities"]
        requirement = dict["value"][i]["Skills"]
        location = city + ', ' + state

# Appending the values into lists
        job_details.append([job_title,job_type,job_id,location,city,state,salary,description,requirement])
# Dumping list into csv
    with open('kforce_jobs.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Job role','Job type','Job ID','location','City','State','salary','Job description','Requirements'])
        writer.writerows(job_details)

