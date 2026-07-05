import json
import os
from datetime import datetime
MEMORY_FILE = "memory/user_sessions.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE,"r") as f:
            return json.load(f)
    return {}

def save_memory(data):
    with open (MEMORY_FILE,"w") as f:
        json.dump(data, f, indent=2)

def get_user_session(user_id):
    memory = load_memory()
    if user_id not in memory:
        memory[user_id] = {
            "created_at": datetime.now().isoformat(),
            "conversation_history": [],
            "profile_data": None,
            "goals": None,
            "last_recommendations": None
        }
        save_memory(memory)
    return memory[user_id]

def update_user_session(user_id, updates):
    memory = load_memory()
    if user_id in memory:
        memory[user_id].update(updates)
        memory[user_id]["last_updated"] = datetime.now().isoformat()
        save_memory(memory)

def add_to_conversation(user_id, role, content):
    memory = load_memory()
    if user_id in memory:
        memory[user_id]["conversation_history"].append({
            "role": role,
            "content": content
        })
        save_memory(memory)

def get_conversation_history(user_id):
    session = get_user_session(user_id)
    return session.get("conversation_history", [])
