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

    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Could not reach Apify — network error: {str(e)}")

    try:
        run_data = response.json()
    except ValueError:
        raise Exception("Apify returned an unreadable response. Please check your Apify account status or try again later.")

    if not isinstance(run_data, dict) or "data" not in run_data:
        error_message = "Unknown error"
        if isinstance(run_data, dict):
            error_message = run_data.get("error", {}).get("message", "Unknown error")
        raise Exception(f"Apify scraping failed: {error_message}. Please check your Apify account status (usage limits, billing) or try again later.")

    run_id = run_data["data"].get("id")
    if not run_id:
        raise Exception("Apify did not return a valid run ID. Please check your Apify account status or try again later.")

    dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={key}"

    for _ in range(20):
        time.sleep(15)
        try:
            result = requests.get(dataset_url, timeout=30)
            items = result.json()
        except (requests.exceptions.RequestException, ValueError):
            continue
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

    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.exceptions.RequestException:
        return []

    try:
        run_data = response.json()
    except ValueError:
        return []

    if not isinstance(run_data, dict) or "data" not in run_data:
        return []

    run_id = run_data["data"].get("id")
    if not run_id:
        return []

    dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={key}"

    for _ in range(20):
        time.sleep(10)
        try:
            result = requests.get(dataset_url, timeout=30)
            items = result.json()
        except (requests.exceptions.RequestException, ValueError):
            continue
        if items:
            return items

    return []
