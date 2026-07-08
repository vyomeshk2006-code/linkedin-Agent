# LinkedIn Career Agent

An AI-powered LinkedIn career agent that analyzes your profile, identifies gaps, builds a personalized roadmap, and helps you land your target role.

**[Try the live app →](https://linkedin-agent-07.streamlit.app)**

## What it does

This isn't a static profile scorer — it's a conversational AI agent that scrapes real LinkedIn data (profile fields and posts) and uses Claude to give specific, evidence-based feedback instead of generic advice.

- **Profile Analysis** — Full section-by-section audit of your headline, about, experience, skills, projects, and posts, with a rating and specific rewrite suggestions
- **Career Roadmap** — Personalized plan with specific certifications, projects, and a month-by-month timeline based on your actual background and target role
- **Job Fit Scorer** — Paste any job description and get an honest fit score, gap analysis, and positioning advice based on what you've actually built
- **Internship Finder** — Realistic assessment of which internships you're eligible for now versus which need more work
- **Draft LinkedIn Post** — Turns a project or achievement into a well-written post
- **Career Discovery** — A guided conversation for users who aren't sure what career path to pursue
- **Follow-up questions** — Every feature supports a back-and-forth conversation, not just a one-shot response
- **Persistent memory** — Remembers your profile and conversation history across the session

## Tech stack

- **Python**
- **Claude API (Anthropic)** — powers all analysis, reasoning, and conversation
- **Apify** — scrapes public LinkedIn profile and post data
- **Streamlit** — web interface and deployment

## How it works

1. User enters their own Anthropic and Apify API keys (never stored — only used for that session)
2. The agent scrapes the user's LinkedIn profile and recent posts
3. Claude analyzes the real scraped data — not assumptions — to produce specific, grounded feedback
4. Every feature after the initial profile scan reuses that same data, so scraping only happens once per session

## Running it locally

```bash
git clone https://github.com/vyomeshk2006-code/linkedin-Agent.git
cd linkedin-Agent
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Create a `.env` file in the root with your own keys:

```
ANTHROPIC_API_KEY=your_key_here
APIFY_API_KEY=your_key_here
```

Run the CLI version:

```bash
python main.py
```

Or run the web version locally:

```bash
streamlit run streamlit_app.py
```

## Why bring-your-own-API-keys?

The deployed app doesn't use any developer keys — every visitor enters their own Anthropic and Apify API keys directly in the sidebar. Keys are held only in that browser session and are never stored, logged, or sent anywhere else. This keeps the tool free to run and puts usage entirely in the user's control.

## Project structure

```
linkedin-agent/
├── agent/              # Core agent logic — one file per feature
├── tools/               # Claude API and Apify scraper connections
├── utils/               # Memory manager and shared helper functions
├── memory/              # Local session storage (gitignored)
├── main.py               # CLI version
├── streamlit_app.py      # Web app version
└── requirements.txt
```

## Built by

Vyomesh Kumar — CS sophomore at the University of South Florida

[LinkedIn](https://www.linkedin.com/in/vyomesh-kumar-730103380/) · [GitHub](https://github.com/vyomeshk2006-code)

## License

MIT
