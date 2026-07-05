from tools.claude_client import ask_claude
from utils.helpers import print_section

def draft_linkedin_post(user_profile_data, achievement, post_type, conversation_history=None):
    
    system_prompt = """You are an expert LinkedIn content creator and personal branding specialist.
    You write engaging, authentic LinkedIn posts that get high engagement and build professional credibility.
    You understand what works on LinkedIn — storytelling, specific details, clear takeaways.
    Never write generic posts. Every post must feel personal and specific to the person."""
    
    prompt = f"""Write a LinkedIn post for this person based on their achievement/update.
    
    Person's Name: {user_profile_data.get('fullName', 'Unknown')}
    Current Headline: {user_profile_data.get('headline', 'Not provided')}
    Target Role/Field: {user_profile_data.get('goals', 'Tech professional')}
    
    Achievement/Update to post about:
    {achievement}
    
    Post Type: {post_type}
    
    Write a LinkedIn post that:
    1. Starts with a hook that stops people from scrolling
    2. Tells the story behind the achievement with specific details
    3. Shares what they learned or what this means for their journey
    4. Ends with a clear call to action or question to drive engagement
    5. Uses appropriate emojis sparingly
    6. Is formatted for LinkedIn — short paragraphs, white space, easy to read
    7. Feels authentic and personal, not corporate or generic
    
    Also provide:
    - 5 relevant hashtags to include
    - Best time to post for maximum engagement
    - One alternative hook they could use instead
    
    Post types guide:
    - certification: Focus on the journey, what you learned, why it matters for your goals
    - project: Focus on the problem you solved, tech used, what recruiters should notice
    - milestone: Focus on gratitude, the people who helped, what's next
    - learning: Focus on the insight, how it changed your thinking, practical takeaway"""
    
    print_section("Drafting Your LinkedIn Post")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response