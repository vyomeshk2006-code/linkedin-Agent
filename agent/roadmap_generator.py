from datetime import date
from tools.claude_client import ask_claude
from utils.helpers import print_section

def generate_roadmap(profile_data, user_goals, location, conversation_history=None):
    
    today = date.today().strftime("%B %d, %Y")
    
    system_prompt = """You are an expert career strategist and technical mentor with deep knowledge 
    of the tech industry, hiring requirements, and skill development paths.
    You create specific, actionable roadmaps tailored to each person's current situation and target role.
    Always recommend specific resources, not generic ones.
    
    IMPORTANT: You will be given today's actual date. Use it to calculate any timelines mentioned
    (e.g. months until a target date) — never guess or estimate this.
    
    If the candidate's stated academic year or status (e.g. 'sophomore') conflicts with dates you might
    infer from education start/end years, always trust their explicitly stated status over your own inference."""
    
    prompt = f"""Today's date is {today}. Based on this person's profile and goals, create a detailed career roadmap.
    
    Target Role/Goals: {user_goals}
    Location/Market: {location}
    
    Current Profile Summary:
    - Name: {profile_data.get('full_name', profile_data.get('fullName', 'Unknown'))}
    - Current Headline: {profile_data.get('headline', 'Not provided')}
    - Summary/About: {profile_data.get('summary', 'Not provided')}
    - Skills: {profile_data.get('skills', [])}
    - Experience: {profile_data.get('experiences', [])}
    - Education: {profile_data.get('education', [])}
    - Certifications: {profile_data.get('certifications', [])}
    - Projects: {profile_data.get('projects', 'Not listed as a dedicated section, check Experience and Posts')}
    - Recent LinkedIn Posts: {profile_data.get('posts', 'Not available')}
    
    BEFORE building the roadmap, complete this mandatory first step:
    
    0. WHAT THEY'VE ALREADY BUILT — Read through Experience, Projects, and every LinkedIn Post in full,
       word for word. List every real project, tool, or technical work you find evidence of, quoting or
       referencing the specific post or experience entry it came from. This step is required even if
       Posts or Experience appear brief — do not proceed until this extraction is complete. If after
       careful reading there is genuinely nothing there, state that explicitly, but only after having
       actually checked every field.
    
    Then create a comprehensive roadmap with the following:
    
    1. CURRENT LEVEL ASSESSMENT
       - Where they stand right now for target role (Beginner/Intermediate/Advanced), factoring in
         what you found in step 0
       - What they already have that's valuable
       - The main gap between current state and target role
    
    2. CERTIFICATIONS ROADMAP
       - List specific certifications needed in priority order
       - For each certification: name, provider, estimated time, cost, why it matters for target role
       - Which to do first, second, third
    
    3. PROJECTS ROADMAP
       - Acknowledge any existing projects found in step 0 first, then list 5 specific NEW projects to
         build in order of complexity
       - For each project: what to build, tech stack to use, what it demonstrates to recruiters
       - How to present each project on LinkedIn and GitHub
    
    4. SKILLS TO LEARN
       - Specific technical skills missing for target role in priority order
       - For each skill: best free resource to learn it, estimated time to learn
    
    5. TIMELINE
       - Month by month breakdown of what to focus on, calculated from today's actual date
       - Realistic milestones for the next 6 months
       - When they will be ready to start applying (state the actual month/year, calculated correctly)
    
    6. WEEKLY ACTION PLAN
       - Specific tasks for this week to get started immediately
       - How many hours per week to dedicate to each area
    
    Be extremely specific. Name actual certifications, actual projects, actual resources.
    No generic advice like 'learn Python' — say exactly what to learn and where.
    All timeline calculations must be based on today's actual date given above — double check your math."""
    
    print_section("Generating Your Roadmap")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response