import json
from datetime import datetime

def format_profile_for_claude(profile_data):
    return json.dumps(profile_data, indent=2)

def print_section(title):
    print("\n"+ "="*50)
    print(f" {title}")
    print("="*50)

def print_agent_response(response):
    print(f"\n🤖 Agent: {response}\n")

def print_user_message(message):
    print(f"\n👤 You: {message}\n")

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def truncate_text(text, max_length=500):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def validate_linkedin_url(url):
    return "linkedin.com/in/" in url

