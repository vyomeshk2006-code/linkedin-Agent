import os
from dotenv import load_dotenv
from utils.memory_manager import (
    get_user_session,
    update_user_session,
    add_to_conversation,
    get_conversation_history
)
from utils.helpers import (
    print_section,
    print_agent_response,
    print_user_message,
    validate_linkedin_url
)
from agent.profile_analyzer import analyze_profile
from agent.roadmap_generator import generate_roadmap
from agent.competitor_analyzer import analyze_competitors
from agent.content_assistant import draft_linkedin_post
from agent.career_advisor import start_career_discovery, process_career_answer
from agent.internship_advisor import find_internships
from agent.job_fit_scorer import score_job_fit

load_dotenv()

def get_user_info():
    print_section("Welcome to LinkedIn Career Agent")
    print("Your AI-powered career coach\n")
    
    name = input("Enter your name: ").strip()
    user_id = name.lower().replace(" ", "_")
    
    session = get_user_session(user_id)
    
    if session.get("goals"):
        print(f"\nWelcome back {name}!")
        print(f"Your goal: {session['goals']}")
        print(f"Your location: {session.get('location', 'Not set')}")
        use_existing = input("\nUse existing profile? (yes/no): ").strip().lower()
        if use_existing == "yes":
            return user_id, session
    
    linkedin_url = input("Enter your LinkedIn profile URL: ").strip()
    while not validate_linkedin_url(linkedin_url):
        print("Invalid LinkedIn URL. Must contain 'linkedin.com/in/'")
        linkedin_url = input("Enter your LinkedIn profile URL: ").strip()
    
    goals = input("What is your target role/goal? (e.g. AI engineering internship by 2027): ").strip()
    location = input("What is your target job market? (e.g. United States, Tampa FL): ").strip()
    
    update_user_session(user_id, {
        "linkedin_url": linkedin_url,
        "goals": goals,
        "location": location,
        "name": name
    })
    
    return user_id, get_user_session(user_id)


def show_menu():
    print_section("What would you like to do?")
    print("1. Analyze my LinkedIn profile")
    print("2. Generate my career roadmap")
    print("3. Analyze competitors")
    print("4. Find internship opportunities")
    print("5. Score job fit")
    print("6. Draft a LinkedIn post")
    print("7. Career discovery (I don't know what I want)")
    print("8. Exit")
    return input("\nChoose an option (1-8): ").strip()


def run_agent():
    user_id, session = get_user_info()
    
    goals = session.get("goals")
    location = session.get("location", "United States")
    linkedin_url = session.get("linkedin_url")
    profile_data = session.get("profile_data")
    
    while True:
        choice = show_menu()
        conversation_history = get_conversation_history(user_id)
        
        if choice == "1":
            profile_data, response = analyze_profile(linkedin_url, goals, location)
            if profile_data:
                update_user_session(user_id, {"profile_data": profile_data})
                add_to_conversation(user_id, "user", "Analyze my LinkedIn profile")
                add_to_conversation(user_id, "assistant", response)
            print_agent_response(response)
        
        elif choice == "2":
            if not profile_data:
                print("\nPlease analyze your profile first (option 1)")
                continue
            response = generate_roadmap(profile_data, goals, location, conversation_history)
            add_to_conversation(user_id, "user", "Generate my career roadmap")
            add_to_conversation(user_id, "assistant", response)
            print_agent_response(response)
        
        elif choice == "3":
            print("\nEnter competitor LinkedIn URLs (one per line, empty line to finish):")
            competitor_urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                if validate_linkedin_url(url):
                    competitor_urls.append(url)
                else:
                    print("Invalid URL skipped")
            
            if competitor_urls:
                if not profile_data:
                    print("\nPlease analyze your profile first (option 1)")
                    continue
                response = analyze_competitors(profile_data, goals, competitor_urls, location)
                add_to_conversation(user_id, "user", "Analyze my competitors")
                add_to_conversation(user_id, "assistant", response)
                print_agent_response(response)
        
        elif choice == "4":
            if not profile_data:
                print("\nPlease analyze your profile first (option 1)")
                continue
            response = find_internships(profile_data, goals, location, conversation_history)
            add_to_conversation(user_id, "user", "Find internship opportunities")
            add_to_conversation(user_id, "assistant", response)
            print_agent_response(response)
        
        elif choice == "5":
            print("\nPaste the job description (empty line to finish):")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            job_description = "\n".join(lines)
            
            if not profile_data:
                print("\nPlease analyze your profile first (option 1)")
                continue
            response = score_job_fit(profile_data, job_description, goals, location, conversation_history)
            add_to_conversation(user_id, "user", f"Score job fit for: {job_description[:100]}")
            add_to_conversation(user_id, "assistant", response)
            print_agent_response(response)
        
        elif choice == "6":
            achievement = input("\nWhat did you achieve? (e.g. completed Google AI certification): ").strip()
            print("Post type: certification / project / milestone / learning")
            post_type = input("Enter post type: ").strip()
            if not profile_data:
                profile_data = {"fullName": session.get("name", "Unknown")}
            response = draft_linkedin_post(profile_data, achievement, post_type, conversation_history)
            add_to_conversation(user_id, "user", f"Draft LinkedIn post about: {achievement}")
            add_to_conversation(user_id, "assistant", response)
            print_agent_response(response)
        
        elif choice == "7":
            print_section("Career Discovery Mode")
            response = start_career_discovery(conversation_history)
            print_agent_response(response)
            add_to_conversation(user_id, "assistant", response)
            
            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in ["exit", "quit", "back"]:
                    break
                print_user_message(user_input)
                add_to_conversation(user_id, "user", user_input)
                conversation_history = get_conversation_history(user_id)
                response = process_career_answer(user_input, conversation_history)
                print_agent_response(response)
                add_to_conversation(user_id, "assistant", response)
        
        elif choice == "8":
            print("\nGoodbye! Keep building your profile.")
            break
        
        else:
            print("\nInvalid option. Please choose 1-8.")


if __name__ == "__main__":
    run_agent()
