from tools.claude_client import ask_claude
from tools.apify_scraper import scrape_linkedin_profile
from utils.helpers import format_profile_for_claude, print_section

def analyze_competitors(user_profile_data, user_goals, competitor_urls, location):
    
    print_section("Analyzing Competitors")
    print("Scraping competitor profiles, please wait...")
    
    competitor_profiles = []
    for url in competitor_urls:
        print(f"Scraping: {url}")
        profile = scrape_linkedin_profile(url)
        if profile:
            competitor_profiles.append(profile)
    
    if not competitor_profiles:
        return "Could not scrape any competitor profiles. Please check the URLs and try again."
    
    formatted_user = format_profile_for_claude(user_profile_data)
    formatted_competitors = format_profile_for_claude(competitor_profiles)
    
    system_prompt = """You are an expert LinkedIn strategist and competitive analyst.
    You compare professional profiles and identify specific gaps and opportunities.
    Always be direct and specific. Focus on actionable differences, not generic observations."""
    
    prompt = f"""Compare this person's LinkedIn profile against their competitors.
    
    Target Role/Goals: {user_goals}
    Location/Market: {location}
    
    USER'S PROFILE:
    {formatted_user}
    
    COMPETITOR PROFILES:
    {formatted_competitors}
    
    Provide a detailed competitive analysis:
    
    1. COMPETITIVE POSITION
       - Where does the user rank compared to competitors overall?
       - What is their biggest competitive advantage?
       - What is their biggest competitive disadvantage?
    
    2. WHAT COMPETITORS HAVE THAT THE USER DOESN'T
       - Specific skills competitors have that user is missing
       - Certifications competitors have that user doesn't
       - Types of experience competitors have that user lacks
       - Projects competitors showcase that user doesn't have
       - How competitors present themselves differently
    
    3. WHERE THE USER HAS AN EDGE
       - What does the user have that competitors don't?
       - How to leverage these advantages in their profile and applications
    
    4. PROFILE PRESENTATION COMPARISON
       - How do competitors write their headlines vs the user?
       - How do competitors structure their about section vs the user?
       - How do competitors present their experience vs the user?
    
    5. SPECIFIC ACTIONS TO OUTPACE COMPETITORS
       - Exact steps to take to get ahead of each competitor
       - What to prioritize first based on competitive gaps
    
    Be specific. Reference actual content from both the user and competitor profiles."""
    
    print_section("Competitor Analysis Complete")
    response = ask_claude(prompt, system_prompt=system_prompt)
    
    return response