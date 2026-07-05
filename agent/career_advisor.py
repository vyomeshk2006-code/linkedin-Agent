from tools.claude_client import ask_claude
from utils.helpers import print_section

def start_career_discovery(conversation_history=None):
    
    system_prompt = """You are a career counselor and mentor specializing in tech careers.
    You help people discover which tech career path suits them best through thoughtful questions.
    You ask one question at a time, listen carefully to answers, and build a complete picture
    of the person before making recommendations.
    Be conversational, warm, and encouraging. Never overwhelm with multiple questions at once."""
    
    prompt = """Start a career discovery conversation with this person.
    
    Ask them the first question to understand what kind of tech career suits them.
    Focus on understanding:
    - What they enjoy doing
    - How they like to work
    - What kind of problems excite them
    - What their day to day life should look like
    
    Ask only ONE question to start. Keep it conversational and friendly.
    After they answer you will ask follow up questions one at a time.
    After 5-6 questions recommend 2-3 specific career paths with explanation of why each fits them."""
    
    print_section("Career Discovery Mode")
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response


def process_career_answer(user_answer, conversation_history):
    
    system_prompt = """You are a career counselor specializing in tech careers.
    You are in the middle of a career discovery conversation.
    Based on the conversation so far and this new answer, either:
    1. Ask the next most relevant follow up question to learn more, OR
    2. If you have enough information (5-6 exchanges), provide career path recommendations
    
    If recommending careers:
    - Recommend 2-3 specific tech career paths
    - Explain exactly why each fits based on their answers
    - For each path explain: day to day work, skills needed, salary range, growth potential
    - Ask which one resonates most so you can build their roadmap"""
    
    prompt = f"""The person just answered: {user_answer}
    
    Based on the full conversation history and this answer, continue the career discovery.
    Remember — one question at a time if still gathering info, or full recommendations if ready."""
    
    response = ask_claude(prompt, system_prompt=system_prompt, conversation_history=conversation_history)
    
    return response