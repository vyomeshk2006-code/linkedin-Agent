from tools.claude_client import ask_claude
from tools.apify_scraper import scrape_linkedin_profile, scrape_linkedin_posts
from utils.helpers import format_profile_for_claude, print_section

def analyze_profile(linkedin_url, user_goals, location):

    print_section("Scraping LinkedIn Profile")
    print("Fetching profile data, please wait...")

    try:
        profile_data = scrape_linkedin_profile(linkedin_url)
    except Exception as e:
        return None, f"⚠️ Failed to scrape LinkedIn profile.\n\n**Reason:** {str(e)}"

    if not profile_data:
        return None, "Failed to scrape LinkedIn profile. Apify did not return any data — please check your Apify account or try again later."

    print("Fetching your posts, please wait...")
    posts_data = scrape_linkedin_posts(linkedin_url)
    profile_data["posts"] = posts_data if posts_data else []

    formatted_profile = format_profile_for_claude(profile_data)
    formatted_posts = format_profile_for_claude(posts_data) if posts_data else "No posts found"

    system_prompt = """You are an expert LinkedIn career coach and recruiter with 10+ years of experience. 
    You analyze LinkedIn profiles and provide specific, actionable feedback to help people land their target roles.
    Always be direct, honest, and specific. Never give generic advice."""

    prompt = f"""Analyze this LinkedIn profile for someone targeting: {user_goals}
    Location/Market: {location}
    
    Profile Data:
    {formatted_profile}
    Recent LinkedIn Posts:
    {formatted_posts}
    
    Provide a comprehensive analysis with the following sections:
    
    1. OVERALL RATING (X/10) with brief justification
    
    2. PROFILE LEANING - What role/field does this profile currently lean toward based on the content?
    
    3. SECTION BY SECTION ANALYSIS:
       - Headline: Current assessment + specific rewrite suggestion. Include exact keywords 
         recruiters search for in target role so profile appears in searches.
       - About/Bio: Current assessment + specific rewrite suggestion
       - Experience: Analyze each experience listed. Does it align with target role?
         Should any experience be removed or de-emphasized? How should each be reframed?
         What kind of experience should they be pursuing next?
       - Skills: What's missing for target role? What to add, remove, or reorder?
       - Education: What to highlight? Relevant coursework to mention?
       - Certifications: What certifications are missing for this target role?
       - Featured Section: What should be pinned and why?
       - Projects: Do they have projects listed? Do they align with target role?
         If no projects, what specific projects should they build?
         If yes, how should existing projects be better presented?
       - Posts/Activity: How active are they on LinkedIn? What is the quality of their posts?
         What topics should they be posting about to build credibility in their target field?
         How often should they post and in what format?
       - Profile Photo + Banner: Do they have a profile photo and banner?
         What kind of photo and banner works best for their target role and industry?
       - External Links: Do they have GitHub, portfolio, or personal website linked?
         For CS/tech roles this is critical — what links should they add?
       - Recommendations: Do they have recommendations? Who should they request them from?
         What should those recommendations highlight?
       - Connection Strategy: How many connections do they have? Are they connecting with
         the right people? Who specifically should they be connecting with —
         recruiters, professionals, alumni — to accelerate their job search?
       - Job Preferences: Are their job preferences and open to work settings optimized?
         Should they have the open to work badge on or off given their situation?
    
    4. TOP 3 CRITICAL GAPS - The most important things holding this profile back from target role
    
    5. QUICK WINS - 3 things they can fix today in under 10 minutes
    
    6. BEYOND THE PROFILE - Specific actions to take outside of LinkedIn:
       - If student: relevant clubs to join, hackathons to participate in, competitions to enter
       - Open source projects to contribute to
       - Communities to join in their target field
       - Events, conferences, or meetups to attend
       - Any other activities that would strengthen their candidacy
    
    Be specific. Reference actual content from their profile.
    No generic advice. Every recommendation must be tailored to their specific profile and target role."""

    print_section("Analyzing Your Profile")
    response = ask_claude(prompt, system_prompt=system_prompt)

    return profile_data, response