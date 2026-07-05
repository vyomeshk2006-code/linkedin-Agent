import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from tools.claude_client import ask_claude
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

    anthropic_key = st.sidebar.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    apify_key = st.sidebar.text_input("Apify API Key", type="password", placeholder="apify_api_...")

    st.sidebar.markdown("---")
    st.sidebar.markdown("Built by Vyomesh Kumar")
    st.sidebar.markdown("[GitHub](https://github.com/vyomeshk2006-code)")

    return anthropic_key, apify_key


def setup_user_info():
    st.subheader("👤 Your Profile")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", placeholder="Vyomesh Kumar")
        linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/yourprofile")
    with col2:
        goals = st.text_input("Target Role/Goal", placeholder="AI Engineering Internship by 2027")
        location = st.text_input("Target Job Market", placeholder="United States / Tampa, FL")
    return name, linkedin_url, goals, location


def render_followup(tab_key, user_id):
    """Reusable follow-up question box for any tab — isolated conversation per tab."""
    state_key = f"{tab_key}_messages"
    if state_key not in st.session_state:
        st.session_state[state_key] = []

    st.markdown("---")
    st.markdown("**💬 Have a follow-up question about this?**")

    input_key = f"followup_input_{tab_key}_{len(st.session_state[state_key])}"
    followup = st.text_input("Ask a follow-up question", key=input_key)

    if st.button("Ask", key=f"followup_btn_{tab_key}_{len(st.session_state[state_key])}"):
        if followup:
            st.session_state[state_key].append({"role": "user", "content": followup})
            with st.spinner("Thinking..."):
                response = ask_claude(followup, conversation_history=st.session_state[state_key])
            st.session_state[state_key].append({"role": "assistant", "content": response})
            st.rerun()

    for msg in st.session_state[state_key]:
        if msg["role"] == "assistant":
            st.markdown(f"**Agent:** {msg['content']}")


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

    if "profile_data" not in st.session_state:
        st.session_state.profile_data = session.get("profile_data")

    st.markdown("---")
    st.subheader("🚀 What would you like to do?")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Profile Analysis", "🗺️ Career Roadmap", "🔍 Competitor Analysis",
        "💼 Internships", "✅ Job Fit Score", "✍️ Draft Post", "🧭 Career Discovery"
    ])

    with tab1:
        st.subheader("📊 LinkedIn Profile Analysis")
        st.markdown("Get a comprehensive audit of your LinkedIn profile with specific recommendations for every section.")

        if st.button("🔍 Analyze My Profile", type="primary", key="analyze"):
            with st.spinner("Scraping your LinkedIn profile... (this can take a few minutes)"):
                profile_data, response = analyze_profile(linkedin_url, goals, location)

            if profile_data:
                st.session_state.profile_data = profile_data
                st.session_state.profile_analysis_response = response
                update_user_session(user_id, {"profile_data": profile_data})
                add_to_conversation(user_id, "user", "Analyze my LinkedIn profile")
                add_to_conversation(user_id, "assistant", response)
            else:
                st.error(response)

        if "profile_analysis_response" in st.session_state:
            st.markdown(st.session_state.profile_analysis_response)
            render_followup("profile", user_id)

    with tab2:
        st.subheader("🗺️ Career Roadmap")
        st.markdown("Get a personalized action plan with specific certifications, projects, and timeline.")

        if st.button("🗺️ Generate My Roadmap", type="primary", key="roadmap"):
            if not st.session_state.profile_data:
                st.warning("⚠️ Please analyze your profile first (Profile Analysis tab)")
            else:
                with st.spinner("Building your personalized roadmap..."):
                    response = generate_roadmap(st.session_state.profile_data, goals, location, None)
                st.session_state.roadmap_response = response
                add_to_conversation(user_id, "user", "Generate my career roadmap")
                add_to_conversation(user_id, "assistant", response)

        if "roadmap_response" in st.session_state:
            st.markdown(st.session_state.roadmap_response)
            render_followup("roadmap", user_id)

    with tab3:
        st.subheader("🔍 Competitor Analysis")
        st.markdown("Compare your profile against competitors and find out how to outpace them.")

        competitor_input = st.text_area(
            "Enter competitor LinkedIn URLs (one per line)",
            placeholder="https://www.linkedin.com/in/competitor1\nhttps://www.linkedin.com/in/competitor2"
        )

        if st.button("🔍 Analyze Competitors", type="primary", key="competitors"):
            if not st.session_state.profile_data:
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
                        response = analyze_competitors(st.session_state.profile_data, goals, valid_urls, location)
                    st.session_state.competitor_response = response
                    add_to_conversation(user_id, "user", "Analyze my competitors")
                    add_to_conversation(user_id, "assistant", response)

        if "competitor_response" in st.session_state:
            st.markdown(st.session_state.competitor_response)
            render_followup("competitor", user_id)

    with tab4:
        st.subheader("💼 Internship Opportunities")
        st.markdown("Find internships you're eligible for right now and what you need for your dream companies.")

        if st.button("💼 Find Internships", type="primary", key="internships"):
            if not st.session_state.profile_data:
                st.warning("⚠️ Please analyze your profile first (Profile Analysis tab)")
            else:
                with st.spinner("Finding internship opportunities..."):
                    response = find_internships(st.session_state.profile_data, goals, location, None)
                st.session_state.internship_response = response
                add_to_conversation(user_id, "user", "Find internship opportunities")
                add_to_conversation(user_id, "assistant", response)

        if "internship_response" in st.session_state:
            st.markdown(st.session_state.internship_response)
            render_followup("internship", user_id)

    with tab5:
        st.subheader("✅ Job Fit Scorer")
        st.markdown("Paste a job description and find out exactly how well you match it.")

        job_description = st.text_area("Paste Job Description Here", placeholder="Copy and paste the full job description...", height=200)

        if st.button("✅ Score My Fit", type="primary", key="jobfit"):
            if not st.session_state.profile_data:
                st.warning("⚠️ Please analyze your profile first (Profile Analysis tab)")
            elif not job_description:
                st.warning("⚠️ Please paste a job description")
            else:
                with st.spinner("Scoring your job fit..."):
                    response = score_job_fit(st.session_state.profile_data, job_description, goals, location, None)
                st.session_state.jobfit_response = response
                add_to_conversation(user_id, "user", "Score job fit")
                add_to_conversation(user_id, "assistant", response)

        if "jobfit_response" in st.session_state:
            st.markdown(st.session_state.jobfit_response)
            render_followup("jobfit", user_id)

    with tab6:
        st.subheader("✍️ Draft LinkedIn Post")
        st.markdown("Tell us what you achieved and we'll write a LinkedIn post that gets engagement.")

        achievement = st.text_input("What did you achieve?", placeholder="Completed Google AI Essentials certification")
        post_type = st.selectbox("Post Type", ["certification", "project", "milestone", "learning"])

        if st.button("✍️ Draft My Post", type="primary", key="post"):
            if not achievement:
                st.warning("⚠️ Please describe your achievement")
            else:
                profile_for_post = st.session_state.profile_data or {"fullName": name}
                with st.spinner("Drafting your LinkedIn post..."):
                    response = draft_linkedin_post(profile_for_post, achievement, post_type, None)
                st.session_state.post_response = response
                add_to_conversation(user_id, "user", f"Draft LinkedIn post about: {achievement}")
                add_to_conversation(user_id, "assistant", response)

        if "post_response" in st.session_state:
            st.markdown(st.session_state.post_response)
            render_followup("post", user_id)

    with tab7:
        st.subheader("🧭 Career Discovery")
        st.markdown("Not sure what career path to pursue? Let our AI career counselor guide you through a conversation.")

        if "career_discovery_active" not in st.session_state:
            st.session_state.career_discovery_active = False
        if "career_discovery_messages" not in st.session_state:
            st.session_state.career_discovery_messages = []

        if not st.session_state.career_discovery_active:
            if st.button("🧭 Start Career Discovery", type="primary", key="career"):
                st.session_state.career_discovery_active = True
                with st.spinner("Starting career discovery..."):
                    response = start_career_discovery()
                st.session_state.career_discovery_messages.append({"role": "assistant", "content": response})
                st.rerun()
        else:
            for msg in st.session_state.career_discovery_messages:
                if msg["role"] == "assistant":
                    st.markdown(f"**Agent:** {msg['content']}")

            input_key = f"career_input_{len(st.session_state.career_discovery_messages)}"
            user_input = st.text_input("Your answer:", key=input_key)
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Send", key=f"send_career_{len(st.session_state.career_discovery_messages)}"):
                    if user_input:
                        st.session_state.career_discovery_messages.append({"role": "user", "content": user_input})
                        with st.spinner("Thinking..."):
                            response = process_career_answer(user_input, st.session_state.career_discovery_messages)
                        st.session_state.career_discovery_messages.append({"role": "assistant", "content": response})
                        st.rerun()
            with col2:
                if st.button("End Discovery", key="end_career"):
                    st.session_state.career_discovery_active = False
                    st.session_state.career_discovery_messages = []
                    st.rerun()


if __name__ == "__main__":
    main()