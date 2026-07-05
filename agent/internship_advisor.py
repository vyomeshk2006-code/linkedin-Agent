from datetime import date
from tools.claude_client import ask_claude
from utils.helpers import print_section

def find_internships(profile_data, user_goals, location, conversation_history=None):
    
    today = date.today().strftime("%B %d, %Y")
    
    system_prompt = """You are an expert tech recruiter and internship advisor with deep knowledge
    of the tech industry hiring landscape, internship programs, and eligibility requirements.
    You give realistic, honest assessments of a candidate's eligibility for specific programs.
    Never sugarcoat. If someone isn't ready for a role, tell them exactly what's missing.
    
    IMPORTANT: You will be given today's actual date. Use it to calculate any timelines mentioned
    (e.g. months until a target date) — never guess or estimate this.
    
    If the candidate's stated academic year or status (e.g. 'sophomore') conflicts with dates you might
    infer from education start/end years, always trust their explicitly stated status over your own inference."""
    
    prompt = f"""Today's date is {today}. Based on this person's profile, assess their internship eligibility and recommend opportunities.
    
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
    
    BEFORE assessing eligibility, complete this mandatory first step:
    
    0. WHAT THEY'VE ALREADY BUILT — Read through Experience, Projects, and every LinkedIn Post in full,
       word for word. List every real project, tool, or technical work you find evidence of, quoting or
       referencing the specific post or experience entry it came from. This step is required even if
       Posts or Experience appear brief — do not proceed until this extraction is complete. If after
       careful reading there is genuinely nothing there, state that explicitly, but only after having
       actually checked every field.
    
    Then provide a detailed internship eligibility report:
    
    1. OVERALL ELIGIBILITY SCORE (X/10)
       - Honest assessment of how competitive they are right now, factoring in what you found in step 0
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
       - Timeline to become eligible, calculated from today's actual date
    
    5. APPLICATION STRATEGY
       - Which internships to apply to first
       - How to position their profile for each type of company
       - Specific tips for international students if applicable (note: this candidate is an
         international student from Pakistan, so CPT/OPT visa considerations are directly relevant)
       - Best platforms to find and apply for internships in their target field
    
    6. WHAT TO DO THIS WEEK
       - Immediate actions to improve internship eligibility
       - Which job boards to set up alerts on
       - Who to reach out to on LinkedIn for referrals
    
    Be specific with company names, program names, and requirements.
    Consider their location and visa status if mentioned.
    All timeline calculations must be based on today's actual date given above — double check your math."""
    
    print_section("Finding Internship Opportunities")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response