import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def ask_claude(prompt, system_prompt=None, conversation_history=None, api_key=None):
    
    key = api_key or os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=key)
    
    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    kwargs = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 8096,
        "messages": messages
    }
    
    if system_prompt:
        kwargs["system"] = system_prompt

    response = client.messages.create(**kwargs)
    return response.content[0].text