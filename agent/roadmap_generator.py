from tools.claude_client import ask_claude
from utils.helpers import print_section

def generate_roadmap(profile_data, user_goals, location, conversation_history=None):
    
    system_prompt = """You are an expert career strategist and technical mentor with deep knowledge 
    of the tech industry, hiring requirements, and skill development paths.
    You create specific, actionable roadmaps tailored to each person's current situation and target role.
    Always recommend specific resources, not generic ones.
    
    IMPORTANT: Carefully calculate any timelines using today's actual date. Carefully read the Experience,
    Projects, and Posts sections in full before claiming something is 'missing' — project experience is
    often described within Experience entries or LinkedIn posts, not only in a dedicated Projects section."""
    
    prompt = f"""Based on this person's profile and goals, create a detailed career roadmap.
    
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
    
    Create a comprehensive roadmap with the following:
    
    1. CURRENT LEVEL ASSESSMENT
       - Where they stand right now for target role (Beginner/Intermediate/Advanced)
       - What they already have that's valuable
       - The main gap between current state and target role
    
    2. CERTIFICATIONS ROADMAP
       - List specific certifications needed in priority order
       - For each certification: name, provider, estimated time, cost, why it matters for target role
       - Which to do first, second, third
    
    3. PROJECTS ROADMAP
       - List 5 specific projects to build in order of complexity
       - For each project: what to build, tech stack to use, what it demonstrates to recruiters
       - How to present each project on LinkedIn and GitHub
    
    4. SKILLS TO LEARN
       - Specific technical skills missing for target role in priority order
       - For each skill: best free resource to learn it, estimated time to learn
    
    5. TIMELINE
       - Month by month breakdown of what to focus on
       - Realistic milestones for the next 6 months
       - When they will be ready to start applying
    
    6. WEEKLY ACTION PLAN
       - Specific tasks for this week to get started immediately
       - How many hours per week to dedicate to each area
    
    Be extremely specific. Name actual certifications, actual projects, actual resources.
    No generic advice like 'learn Python' — say exactly what to learn and where.
    Double check any date-based timeline calculations against today's actual date."""
    
    print_section("Generating Your Roadmap")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response