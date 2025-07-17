import requests
from urllib.parse import quote
from dotenv import load_dotenv
import os
load_dotenv()





class RapidJobs:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.google.com/',
            'x-rapidapi-key': os.environ["RAPID_API_KEY"], 
	        'x-rapidapi-host': "jsearch.p.rapidapi.com"
        }
        self.jobsearch_url = "https://jsearch.p.rapidapi.com/search"
        self.jobdetails_url = "https://jsearch.p.rapidapi.com/job-details"

    def refine_json(self, job_data, data):

        for job in data['data']:
            details = {}
            details['id'] = job['job_id']
            details['title'] = job['job_title']
            details['company'] = job['employer_name']
            details['description'] = job['job_description']
            details['image'] = job['employer_logo']
            details['location'] = job['job_location']
            details['employmentType'] = job['job_employment_type']
            details['datePosted'] = job['job_posted_at']
            details['jobProvider'] = job['job_publisher']
            details['url'] = job['job_apply_link']
            job_data['jobs'].append(details)



    def get_jobs(self, roles, country):

        job_data = {"jobs": []}

        for role in roles:
            querystring = {"query":f"{role}","page":"1","num_pages":"1","country":f"{country}","date_posted":"month"}
            response = requests.get(self.jobsearch_url, headers=self.headers, params=querystring)
            data = response.json()
            self.refine_json(job_data, data)
        
        return job_data
        

        

if __name__ == "__main__":

    rapid = RapidJobs()
    rapid.get_jobs(["Cyber Security", "Software Developer"], "us")


