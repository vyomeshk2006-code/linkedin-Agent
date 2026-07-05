import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_url, apify_key=None):
    key = apify_key or os.getenv("APIFY_API_KEY")
    url = f"https://api.apify.com/v2/acts/anchor~linkedin-profile-enrichment/runs?token={key}"
    
    payload = {
        "startUrls": [
            {
                "url": linkedin_url,
                "id": "1"
            }
        ]
    }
    
    response = requests.post(url, json=payload)
    run_data = response.json()
    
    run_id = run_data["data"]["id"]
    
    dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={key}"
    
    for _ in range(20):
        time.sleep(15)
        result = requests.get(dataset_url)
        items = result.json()
        if items:
            return items[0]
    
    return None


def scrape_linkedin_posts(linkedin_url, apify_key=None):
    key = apify_key or os.getenv("APIFY_API_KEY")
    url = f"https://api.apify.com/v2/acts/harvestapi~linkedin-profile-posts/runs?token={key}"
    
    payload = {
        "targetUrls": [linkedin_url],
        "maxPosts": 5,
        "includeQuotePosts": True,
        "includeReposts": False,
        "scrapeReactions": False,
        "scrapeComments": False
    }
    
    response = requests.post(url, json=payload)
    run_data = response.json()
    
    run_id = run_data["data"]["id"]
    
    dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={key}"
    
    for _ in range(20):
        time.sleep(10)
        result = requests.get(dataset_url)
        items = result.json()
        if items:
            return items
    
    return []
