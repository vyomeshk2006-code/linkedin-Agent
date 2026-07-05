from datetime import date
from tools.claude_client import ask_claude
from utils.helpers import print_section

def score_job_fit(profile_data, job_description, user_goals, location, conversation_history=None):
    
    today = date.today().strftime("%B %d, %Y")
    
    system_prompt = """You are an expert tech recruiter with deep knowledge of hiring requirements
    and candidate evaluation. You give honest, specific assessments of how well a candidate
    matches a job description. Never sugarcoat. If someone isn't ready, tell them exactly what's missing
    and what to do about it.
    
    IMPORTANT: You will be given today's actual date. Use it to calculate any timelines mentioned
    (e.g. months until a target date) — never guess or estimate this.
    
    If the candidate's stated academic year or status (e.g. 'sophomore') conflicts with dates you might
    infer from education start/end years, always trust their explicitly stated status over your own inference."""
    
    prompt = f"""Today's date is {today}. Evaluate how well this person fits the following job description.
    
    Target Role/Goals: {user_goals}
    Location/Market: {location}
    
    CANDIDATE PROFILE:
    - Name: {profile_data.get('full_name', profile_data.get('fullName', 'Unknown'))}
    - Headline: {profile_data.get('headline', 'Not provided')}
    - Summary/About: {profile_data.get('summary', 'Not provided')}
    - Skills: {profile_data.get('skills', [])}
    - Experience: {profile_data.get('experiences', [])}
    - Education: {profile_data.get('education', [])}
    - Certifications: {profile_data.get('certifications', [])}
    - Projects: {profile_data.get('projects', 'Not listed as a dedicated section, check Experience and Posts')}
    - Recent LinkedIn Posts: {profile_data.get('posts', 'Not available')}
    
    JOB DESCRIPTION:
    {job_description}
    
    BEFORE evaluating fit, complete this mandatory first step:
    
    0. WHAT THEY'VE ALREADY BUILT — Read through Experience, Projects, and every LinkedIn Post in full,
       word for word. List every real project, tool, or technical work you find evidence of, quoting or
       referencing the specific post or experience entry it came from. This step is required even if
       Posts or Experience appear brief — do not proceed to gap analysis until this extraction is complete.
       If after careful reading there is genuinely nothing there, state that explicitly, but only after
       having actually checked every field.
    
    Then provide the full job fit analysis:
    
    1. FIT SCORE (X/10)
       - Overall match score with brief justification
       - Should they apply? Yes/No/Maybe with clear reasoning
    
    2. REQUIREMENTS THEY MEET
       - List every requirement from the job description they currently satisfy
       - How strongly they meet each one, referencing what you found in step 0
    
    3. REQUIREMENTS THEY ARE MISSING
       - List every requirement they don't meet
       - For each missing requirement: how long would it take to acquire it (using today's date for any calculations)
    
    4. HOW TO POSITION THEMSELVES
       - What to highlight in their application for this specific role, based on what you found in step 0
       - How to rewrite their headline for this job
       - What to emphasize in their cover letter
       - Which projects or experiences to lead with
    
    5. APPLICATION DECISION
       - Clear recommendation: apply now, apply after improvements, or skip
       - If apply after improvements: exactly what to fix first and how long it takes (calculated from today's date)
       - If skip: what similar roles are a better fit right now
    
    6. TAILORING TIPS
       - Specific keywords from the job description to add to their LinkedIn
       - How to reframe existing experience to match this role
       - What to mention in the first paragraph of their cover letter
    
    Be specific. Reference actual requirements from the job description and the actual projects/posts
    you identified in step 0. All timeline calculations must be based on today's actual date given above."""
    
    print_section("Scoring Job Fit")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response