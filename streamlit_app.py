import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from utils.memory_manager import (
    get_user_session,
    update_user_session,
    add_to_conversation,
    get_conversation_history
)
from utils.helpers import validate_linkedin_url
from agent.profile_analyzer import analyze_profile
from agent.roadmap_generator import generate_roadmap
from agent.competitor_analyzer import analyze_competitors
from agent.content_assistant import draft_linkedin_post
from agent.career_advisor import start_career_discovery, process_career_answer
from agent.internship_advisor import find_internships
from agent.job_fit_scorer import score_job_fit

st.set_page_config(
    page_title="LinkedIn Career Agent",
    page_icon="💼",
    layout="wide"
)

def setup_sidebar():
    st.sidebar.title("⚙️ Configuration")
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("🔑 API Keys")
    st.sidebar.markdown("Get your free API keys:")
    st.sidebar.markdown("- [Anthropic API Key](https://console.anthropic.com)")
    st.sidebar.markdown("- [Apify API Key](https://console.apify.com)")
    
    anthropic_key = st.sidebar.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-..."
    )
    
    apify_key = st.sidebar.text_input(
        "Apify API Key",
        type="password",
        placeholder="apify_api_..."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("Built by Vyomesh Kumar")
    st.sidebar.markdown("[GitHub](https://github.com/vyomeshk2006-code)")
    
    return anthropic_key, apify_key


def setup_user_info():
    st.subheader("👤 Your Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", placeholder="Vyomesh Kumar")
        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            placeholder="https://www.linkedin.com/in/yourprofile"
        )
    
    with col2:
        goals = st.text_input(
            "Target Role/Goal",
            placeholder="AI Engineering Internship by 2027"
        )
        location = st.text_input(
            "Target Job Market",
            placeholder="United States / Tampa, FL"
        )
    
    return name, linkedin_url, goals, location


def main():
    anthropic_key, apify_key = setup_sidebar()
    
    st.title("💼 LinkedIn Career Agent")
    st.markdown("*Your AI-powered career coach — analyze your profile, build your roadmap, and land your target role*")
    st.markdown("---")
    
    if not anthropic_key or not apify_key:
        st.warning("⚠️ Please enter your API keys in the sidebar to get started.")
        st.info("💡 Your API keys are never stored — they only exist for your current session.")
        st.stop()
    
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
    os.environ["APIFY_API_KEY"] = apify_key
    
    name, linkedin_url, goals, location = setup_user_info()
    
    if not name or not linkedin_url or not goals or not location:
        st.info("👆 Please fill in all your details above to continue.")
        st.stop()
    
    if not validate_linkedin_url(linkedin_url):
        st.error("❌ Invalid LinkedIn URL. Must contain 'linkedin.com/in/'")
        st.stop()
    
    user_id = name.lower().replace(" ", "_")
    session = get_user_session(user_id)
    update_user_session(user_id, {
        "linkedin_url": linkedin_url,
        "goals": goals,
        "location": location,
        "name": name
    })
    
    st.markdown("---")
    st.subheader("🚀 What would you like to do?")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Profile Analysis",
        "🗺️ Career Roadmap",
        "🔍 Competitor Analysis",
        "💼 Internships",
        "✅ Job Fit Score",
        "✍️ Draft Post",
        "🧭 Career Discovery"
    ])
    
    conversation_history = get_conversation_history(user_id)
    profile_data = session.get("profile_data")
    
    with tab1:
        st.subheader("📊 LinkedIn Profile Analysis")
        st.markdown("Get a comprehensive audit of your LinkedIn profile with specific recommendations for every section.")
        
        if st.button("🔍 Analyze My Profile", type="primary", key="analyze"):
            with st.spinner("Scraping your LinkedIn profile... (this takes 30-60 seconds)"):
                profile_data, response = analyze_profile(linkedin_url, goals, location)
            
            if profile_data:
                update_user_session(user_id, {"profile_data": profile_data})
                add_to_conversation(user_id, "user", "Analyze my LinkedIn profile")
                add_to_conversation(user_id, "assistant", response)
                st.markdown(response)
            else:
                st.error(response)
    
    with tab2:
        st.subheader("🗺️ Career Roadmap")
        st.markdown("Get a personalized action plan with specific certifications, projects, and timeline.")
        
        if st.button("🗺️ Generate My Roadmap", type="primary", key="roadmap"):
            if not profile_data:
                st.warning("⚠️ Please analyze your profile first (Profile Analysis tab)")
            else:
                with st.spinner("Building your personalized roadmap..."):
                    response = generate_roadmap(profile_data, goals, location, conversation_history)
                add_to_conversation(user_id, "user", "Generate my career roadmap")
                add_to_conversation(user_id, "assistant", response)
                st.markdown(response)
    
    with tab3:
        st.subheader("🔍 Competitor Analysis")
        st.markdown("Compare your profile against competitors and find out how to outpace them.")
        
        competitor_input = st.text_area(
            "Enter competitor LinkedIn URLs (one per line)",
            placeholder="https://www.linkedin.com/in/competitor1\nhttps://www.linkedin.com/in/competitor2"
        )
        
        if st.button("🔍 Analyze Competitors", type="primary", key="competitors"):
            if not profile_data:
                st.warning("⚠️ Please analyze your profile first (Profile Analysis tab)")
            elif not competitor_input:
                st.warning("⚠️ Please enter at least one competitor URL")
            else:
                competitor_urls = [url.strip() for url in competitor_input.split("\n") if url.strip()]
                valid_urls = [url for url in competitor_urls if validate_linkedin_url(url)]
                
                if not valid_urls:
                    st.error("❌ No valid LinkedIn URLs found")
                else:
                    with st.spinner(f"Scraping {len(valid_urls)} competitor profiles..."):
                        response = analyze_competitors(profile_data, goals, valid_urls, location)
                    add_to_conversation(user_id, "user", "Analyze my competitors")
                    add_to_conversation(user_id, "assistant", response)
                    st.markdown(response)
    
    with tab4:
        st.subheader("💼 Internship Opportunities")
        st.markdown("Find internships you're eligible for right now and what you need for your dream companies.")
        
        if st.button("💼 Find Internships", type="primary", key="internships"):
            if not profile_data:
                st.warning("⚠️ Please analyze your profile first (Profile Analysis tab)")
            else:
                with st.spinner("Finding internship opportunities..."):
                    response = find_internships(profile_data, goals, location, conversation_history)
                add_to_conversation(user_id, "user", "Find internship opportunities")
                add_to_conversation(user_id, "assistant", response)
                st.markdown(response)
    
    with tab5:
        st.subheader("✅ Job Fit Scorer")
        st.markdown("Paste a job description and find out exactly how well you match it.")
        
        job_description = st.text_area(
            "Paste Job Description Here",
            placeholder="Copy and paste the full job description...",
            height=200
        )
        
        if st.button("✅ Score My Fit", type="primary", key="jobfit"):
            if not profile_data:
                st.warning("⚠️ Please analyze your profile first (Profile Analysis tab)")
            elif not job_description:
                st.warning("⚠️ Please paste a job description")
            else:
                with st.spinner("Scoring your job fit..."):
                    response = score_job_fit(profile_data, job_description, goals, location, conversation_history)
                add_to_conversation(user_id, "user", f"Score job fit")
                add_to_conversation(user_id, "assistant", response)
                st.markdown(response)
    
    with tab6:
        st.subheader("✍️ Draft LinkedIn Post")
        st.markdown("Tell us what you achieved and we'll write a LinkedIn post that gets engagement.")
        
        achievement = st.text_input(
            "What did you achieve?",
            placeholder="Completed Google AI Essentials certification"
        )
        
        post_type = st.selectbox(
            "Post Type",
            ["certification", "project", "milestone", "learning"]
        )
        
        if st.button("✍️ Draft My Post", type="primary", key="post"):
            if not achievement:
                st.warning("⚠️ Please describe your achievement")
            else:
                if not profile_data:
                    profile_data = {"fullName": name}
                with st.spinner("Drafting your LinkedIn post..."):
                    response = draft_linkedin_post(profile_data, achievement, post_type, conversation_history)
                add_to_conversation(user_id, "user", f"Draft LinkedIn post about: {achievement}")
                add_to_conversation(user_id, "assistant", response)
                st.markdown(response)
    
    with tab7:
        st.subheader("🧭 Career Discovery")
        st.markdown("Not sure what career path to pursue? Let our AI career counselor guide you through a conversation.")
        
        if "career_discovery_active" not in st.session_state:
            st.session_state.career_discovery_active = False
        
        if not st.session_state.career_discovery_active:
            if st.button("🧭 Start Career Discovery", type="primary", key="career"):
                st.session_state.career_discovery_active = True
                with st.spinner("Starting career discovery..."):
                    response = start_career_discovery(conversation_history)
                add_to_conversation(user_id, "assistant", response)
                st.markdown(response)
        else:
            conversation_history = get_conversation_history(user_id)
            for msg in conversation_history[-10:]:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**Agent:** {msg['content']}")
            
            user_input = st.text_input("Your answer:", key="career_input")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Send", key="send_career"):
                    if user_input:
                        add_to_conversation(user_id, "user", user_input)
                        conversation_history = get_conversation_history(user_id)
                        with st.spinner("Thinking..."):
                            response = process_career_answer(user_input, conversation_history)
                        add_to_conversation(user_id, "assistant", response)
                        st.rerun()
            with col2:
                if st.button("End Discovery", key="end_career"):
                    st.session_state.career_discovery_active = False
                    st.rerun()


if __name__ == "__main__":
    main()