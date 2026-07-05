from tools.claude_client import ask_claude
from utils.helpers import print_section

def score_job_fit(profile_data, job_description, user_goals, location, conversation_history=None):
    
    system_prompt = """You are an expert tech recruiter with deep knowledge of hiring requirements
    and candidate evaluation. You give honest, specific assessments of how well a candidate
    matches a job description. Never sugarcoat. If someone isn't ready, tell them exactly what's missing
    and what to do about it.
    
    IMPORTANT: Carefully calculate any timelines mentioned (e.g. months until a target date) using today's
    actual date. Carefully read the Experience, Projects, and Posts sections in full before claiming
    something is 'missing' — project experience or technical work is often described within Experience
    entries or LinkedIn posts, not only in a dedicated Projects section. Do not claim someone lacks a
    GitHub link or project evidence without first checking all provided fields, including posts and
    experience descriptions, for that information."""
    
    prompt = f"""Evaluate how well this person fits the following job description.
    
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
    
    Provide a detailed job fit analysis:
    
    1. FIT SCORE (X/10)
       - Overall match score with brief justification
       - Should they apply? Yes/No/Maybe with clear reasoning
    
    2. REQUIREMENTS THEY MEET
       - List every requirement from the job description they currently satisfy
       - How strongly they meet each one
    
    3. REQUIREMENTS THEY ARE MISSING
       - List every requirement they don't meet
       - For each missing requirement: how long would it take to acquire it
    
    4. HOW TO POSITION THEMSELVES
       - What to highlight in their application for this specific role
       - How to rewrite their headline for this job
       - What to emphasize in their cover letter
       - Which projects or experiences to lead with
    
    5. APPLICATION DECISION
       - Clear recommendation: apply now, apply after improvements, or skip
       - If apply after improvements: exactly what to fix first and how long it takes
       - If skip: what similar roles are a better fit right now
    
    6. TAILORING TIPS
       - Specific keywords from the job description to add to their LinkedIn
       - How to reframe existing experience to match this role
       - What to mention in the first paragraph of their cover letter
    
    Be specific. Reference actual requirements from the job description and actual content from their profile,
    including their posts and experience descriptions. Double check any date-based timeline calculations."""
    
    print_section("Scoring Job Fit")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response