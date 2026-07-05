from tools.claude_client import ask_claude
from utils.helpers import print_section

def find_internships(profile_data, user_goals, location, conversation_history=None):
    
    system_prompt = """You are an expert tech recruiter and internship advisor with deep knowledge
    of the tech industry hiring landscape, internship programs, and eligibility requirements.
    You give realistic, honest assessments of a candidate's eligibility for specific programs.
    Never sugarcoat. If someone isn't ready for a role, tell them exactly what's missing.
    
    IMPORTANT: Carefully calculate any timelines using today's actual date. Carefully read the Experience,
    Projects, and Posts sections in full before claiming something is 'missing' — project experience is
    often described within Experience entries or LinkedIn posts, not only in a dedicated Projects section."""
    
    prompt = f"""Based on this person's profile, assess their internship eligibility and recommend opportunities.
    
    Target Role/Goals: {user_goals}
    Location/Market: {location}
    
    Current Profile:
    - Name: {profile_data.get('full_name', profile_data.get('fullName', 'Unknown'))}
    - Headline: {profile_data.get('headline', 'Not provided')}
    - Summary/About: {profile_data.get('summary', 'Not provided')}
    - Skills: {profile_data.get('skills', [])}
    - Experience: {profile_data.get('experiences', [])}
    - Education: {profile_data.get('education', [])}
    - Certifications: {profile_data.get('certifications', [])}
    - Projects: {profile_data.get('projects', 'Not listed as a dedicated section, check Experience and Posts')}
    - Recent LinkedIn Posts: {profile_data.get('posts', 'Not available')}
    
    Provide a detailed internship eligibility report:
    
    1. OVERALL ELIGIBILITY SCORE (X/10)
       - Honest assessment of how competitive they are right now
       - Main factors helping their eligibility
       - Main factors hurting their eligibility
    
    2. INTERNSHIPS THEY ARE ELIGIBLE FOR RIGHT NOW
       - List specific companies and programs they can apply to today
       - For each: company name, program name, requirements they meet, how to apply
       - Focus on realistic matches not dream companies
    
    3. INTERNSHIPS THEY ARE CLOSE TO BEING ELIGIBLE FOR
       - Programs they could reach in 3-6 months with specific improvements
       - For each: what exactly is missing and how to get it
    
    4. DREAM INTERNSHIPS TO TARGET LONG TERM
       - Top companies in their target field (Google, Meta, Microsoft etc)
       - Honest gap analysis — what they need to be competitive there
       - Timeline to become eligible
    
    5. APPLICATION STRATEGY
       - Which internships to apply to first
       - How to position their profile for each type of company
       - Specific tips for international students if applicable
       - Best platforms to find and apply for internships in their target field
    
    6. WHAT TO DO THIS WEEK
       - Immediate actions to improve internship eligibility
       - Which job boards to set up alerts on
       - Who to reach out to on LinkedIn for referrals
    
    Be specific with company names, program names, and requirements.
    Consider their location and visa status if mentioned.
    Double check any date-based timeline calculations against today's actual date."""
    
    print_section("Finding Internship Opportunities")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response