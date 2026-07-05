from datetime import date
from tools.claude_client import ask_claude
from utils.helpers import print_section, extract_post_texts

def score_job_fit(profile_data, job_description, user_goals, location, conversation_history=None):
    
    today = date.today().strftime("%B %d, %Y")
    clean_posts = extract_post_texts(profile_data.get('posts', []))
    
    system_prompt = """You are an expert tech recruiter. You give honest, specific assessments of how well
    a candidate matches a job description. Never sugarcoat, but never claim something is missing without
    having actually checked for it first.
    
    You will be given today's actual date — use it for any timeline math, never guess.
    Trust the candidate's explicitly stated academic year/status over any date you might infer."""
    
    prompt = f"""Today's date is {today}.
    
    CANDIDATE'S ACTUAL LINKEDIN POSTS (read every one before doing anything else):
    {clean_posts}
    
    CANDIDATE PROFILE:
    - Name: {profile_data.get('full_name', profile_data.get('fullName', 'Unknown'))}
    - Headline: {profile_data.get('headline', 'Not provided')}
    - Summary/About: {profile_data.get('summary', 'Not provided')}
    - Skills: {profile_data.get('skills', [])}
    - Experience: {profile_data.get('experiences', [])}
    - Education: {profile_data.get('education', [])}
    - Certifications: {profile_data.get('certifications', [])}
    
    Target Role/Goals: {user_goals}
    Location/Market: {location}
    
    JOB DESCRIPTION TO EVALUATE AGAINST:
    {job_description}
    
    Your response MUST start with this exact required section, in this exact order:
    
    ## PROJECTS AND TECHNICAL WORK FOUND IN POSTS/EXPERIENCE
    List every project or technical work mentioned above, quoting the specific sentence it came from.
    If genuinely none exists after reading everything above, write "No technical projects found in posts
    or experience" — but you may only write that after this section actually appears.
    
    Only after completing that section, continue with the full analysis:
    
    ## 1. FIT SCORE (X/10)
    Overall match score with brief justification. Should they apply? Yes/No/Maybe.
    
    ## 2. REQUIREMENTS THEY MEET
    List every requirement they satisfy, referencing the projects found above where relevant.
    
    ## 3. REQUIREMENTS THEY ARE MISSING
    List every gap. For each: realistic time to close it, calculated using today's date.
    
    ## 4. HOW TO POSITION THEMSELVES
    What to highlight, headline rewrite, cover letter angle, which projects to lead with.
    
    ## 5. APPLICATION DECISION
    Apply now / apply after improvements / skip. Be specific about the timeline, using today's date.
    
    ## 6. TAILORING TIPS
    Keywords to add, how to reframe experience, cover letter opening line.
    
    Do not skip the required first section under any circumstances."""
    
    print_section("Scoring Job Fit")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response