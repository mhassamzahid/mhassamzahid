"""Profile content: the single source of truth for every image and the README.

Every fact mirrors the portfolio's src/data/site.ts and the CV PDF it quotes.
Nothing here is invented; team projects list only the parts Hassam built.
"""

NAME_FIRST = "Hassam"
NAME_LAST = "Zahid"
ROLE = "AI Engineer"
HANDLE = "mhassamzahid"
LOCATION = "Karachi, PK"
UTC_OFFSET = "UTC+5"
AVAILABILITY = "Open to AI Engineer roles"
EMAIL = "mhassam.dev@gmail.com"
SITE = "https://mhassamzahid.vercel.app"
SITE_LABEL = "mhassamzahid.vercel.app"
CV_URL = f"{SITE}/Hassam_Zahid_AI_Engineer_CV.pdf"
GITHUB = f"https://github.com/{HANDLE}"

THESIS = ("I turn scattered business tools into ", "one AI-powered workflow", ".")

TAGLINE = ("Production AI systems: RAG assistants, MCP integrations, voice agents and n8n "
           "automation, with the FastAPI backends and Next.js frontends that put them in "
           "front of users.")

CURRENT = {"role": "Python Developer", "company": "Axioware Solutions", "since": "2025-09"}

HERO_TAGS = ["RAG", "MCP", "Voice agents", "n8n", "FastAPI", "Next.js", "AWS"]

# The tools that orbit the agent in the hero: the real integrations from the CV.
ORBIT_INNER = ["pgvector", "MCP", "Claude API", "OpenAI API"]
ORBIT_OUTER = ["GoHighLevel", "Salesforce", "ElevenLabs", "Fathom", "Asana", "n8n", "Twilio", "Maqsam"]

# Headline figures: each one is a direct quote from the CV.
METRICS = [
    {"value": "15+", "label": "business workflows automated with n8n", "glyph": "nodes"},
    {"value": "70%", "label": "less manual operations across client accounts", "glyph": "shrink"},
    {"value": "99.5%", "label": "processing accuracy on enterprise data pipelines", "glyph": "dots"},
    {"value": "1+ yr", "label": "shipping AI systems in production", "glyph": "months"},
]

EXPERIENCE = [
    {
        "role": "Python Developer",
        "company": "Axioware Solutions",
        "location": "Karachi, Pakistan",
        "period": "Sep 2025 – Present",
        "highlights": [
            "Designed and deployed AI-powered automation with **n8n across 15+ business workflows**, "
            "reducing manual operations by **70%** across client accounts.",
            "Built backend services with **FastAPI, PostgreSQL and Redis**, including JWT authentication, "
            "rate limiting and auto-scaling infrastructure on AWS.",
            "Integrated **GoHighLevel, Salesforce and the Meta Graph API with OpenAI and Claude** into unified "
            "data pipelines, maintaining **99.5% processing accuracy** across multiple enterprise accounts.",
            "Shipped production **ElevenLabs voice agents** backed by FastAPI tool endpoints and an "
            "**MCP server**, deployed on AWS EC2 for live, real-time conversations.",
        ],
    },
]

EDUCATION = {
    "degree": "BS Software Engineering",
    "school": "Usman Institute of Technology",
    "period": "2022 – 2026",
    "fyp": "UIT University website: Next.js + Sanity.io CMS so staff publish without a developer",
}

# Career lanes for the timeline. Dates are month precision ("YYYY-MM"); end None = now.
TIMELINE = [
    {"lane": "Degree", "title": "BS Software Engineering", "where": "Usman Institute of Technology",
     "start": "2022-01", "end": "2026-12", "precision": "year"},
    {"lane": "Final year project", "title": "UIT University website", "where": "Next.js + Sanity.io",
     "start": "2025-01", "end": "2025-12", "precision": "year"},
    {"lane": "Industry", "title": "Python Developer", "where": "Axioware Solutions",
     "start": "2025-09", "end": None, "precision": "month", "current": True},
]

SKILL_GROUPS = [
    ("AI & Automation", [
        ("Lm", "LLMs"), ("Rg", "RAG"), ("Ag", "LLM agents"), ("Mc", "MCP"), ("N8", "n8n"),
        ("Oa", "OpenAI API"), ("Cl", "Claude API"), ("El", "ElevenLabs"), ("Pe", "Prompt eng."),
        ("Pv", "pgvector"),
    ]),
    ("Backend", [
        ("Py", "Python"), ("Fa", "FastAPI"), ("Nd", "Node.js"), ("Ex", "Express"),
        ("Re", "REST APIs"), ("Jw", "JWT auth"),
    ]),
    ("Frontend", [
        ("Nx", "Next.js"), ("Rx", "React"), ("Ts", "TypeScript"), ("Tw", "Tailwind CSS"),
        ("Hc", "HTML/CSS"),
    ]),
    ("Cloud & Data", [
        ("Aw", "AWS"), ("Lx", "Linux"), ("Ci", "CI/CD"), ("Pg", "PostgreSQL"), ("Rd", "Redis"),
        ("Sb", "Supabase"),
    ]),
    ("Integrations", [
        ("Gh", "GoHighLevel"), ("Sf", "Salesforce"), ("Mg", "Meta Graph"), ("As", "Asana"),
        ("Ft", "Fathom"), ("Mq", "Maqsam"), ("Gd", "Google Docs"),
    ]),
]

HOW_I_WORK = [
    ("Start from the workflow,", "not the model",
     "I map where the information actually lives and who needs it, then decide what the LLM "
     "should do. Most of the value is in the plumbing around it."),
    ("Ship the", "thin slice first",
     "One working path end to end, in production, early. It surfaces the real problems while "
     "they are still cheap to fix."),
    ("Automate the", "boring parts",
     "If a task is done by hand more than twice a week, it becomes a workflow. That is where "
     "most of the 70% reduction in manual operations came from."),
]

# Featured case studies (portfolio order). `system` is the real architecture.
PROJECTS = [
    {
        "slug": "haxmind", "title": "HaxMind", "subtitle": "Internal AI assistant",
        "category": "AI systems", "context": "Client: HAX Consulting", "credit": "Built the assistant",
        "summary": "One chat interface over internal SOPs and live data from five business tools, "
                   "replacing manual lookups across all of them.",
        "stack": ["RAG", "LLM agents", "MCP", "pgvector", "Supabase", "Asana API"],
        "metric": "Five tools, one chat interface",
        "system": {"inputs": ["Internal SOPs", "Maqsam calls", "Fathom transcripts", "GoHighLevel (MCP)",
                              "Asana", "Employee records"],
                   "core": "RAG agent", "detail": "pgvector + LLM", "outputs": ["Chat answers"]},
    },
    {
        "slug": "ai-sales-call-analysis", "title": "AI Sales Call Analysis", "subtitle": "Discovery call pipeline",
        "category": "Automation", "context": "Automation engineer", "credit": "Built the pipeline",
        "summary": "An n8n pipeline that turns every discovery call into a client-facing summary "
                   "and an internal sales brief.",
        "stack": ["n8n", "LLM summarization", "Sales automation"],
        "metric": "Two outputs from every call",
        "system": {"inputs": ["Discovery call"], "core": "n8n pipeline", "detail": "LLM summaries",
                   "outputs": ["Client summary", "Sales brief"]},
    },
    {
        "slug": "vyva-voice-companion", "title": "VYVA", "subtitle": "MCP tools for a voice agent",
        "category": "Voice agents", "context": "2025 – 2026", "credit": "Team contributor",
        "summary": "Tool endpoints behind a senior-care ElevenLabs voice companion: medication "
                   "management, reminder calls and brain-coach sessions.",
        "stack": ["FastAPI", "MCP", "ElevenLabs", "PostgreSQL", "Alembic"],
        "metric": "Agent acts mid-call, hands-free",
        "system": {"inputs": ["ElevenLabs agent"], "core": "MCP server", "detail": "FastAPI tools",
                   "outputs": ["Medications", "Reminder calls", "Brain coach"]},
    },
    {
        "slug": "call-ai-automation", "title": "Call AI Automation", "subtitle": "Pipeline for AI phone agents",
        "category": "Voice agents", "context": "2026", "credit": "Team contributor",
        "summary": "Places ElevenLabs outbound calls through Twilio, then extracts, scores and routes "
                   "every conversation into Salesforce, Sheets and analytics.",
        "stack": ["FastAPI", "ElevenLabs", "Twilio", "Claude API", "Celery", "Redis"],
        "metric": "Every call scored and routed",
        "system": {"inputs": ["ElevenLabs calls", "GoHighLevel", "Lead sheets"], "core": "FastAPI",
                   "detail": "Claude / OpenAI", "outputs": ["Salesforce", "Google Sheets", "WhatsApp", "Analytics"]},
    },
    {
        "slug": "bidcraft", "title": "BidCraft", "subtitle": "RAG proposal generator",
        "category": "AI systems", "context": "2026", "credit": "Built the backend",
        "summary": "Streams tailored Upwork proposals grounded in a freelancer's own past projects, "
                   "retrieved by vector similarity in Postgres.",
        "stack": ["FastAPI", "Mistral", "pgvector", "Supabase", "AWS Lambda"],
        "metric": "Bids streamed token by token",
        "system": {"inputs": ["Upwork job post", "Past projects", "Saved memory", "Editable prompts"],
                   "core": "RAG pipeline", "detail": "pgvector top-k",
                   "outputs": ["Streamed bid", "Q&A answers", "Bid versions"]},
    },
    {
        "slug": "fpl-farms", "title": "FPL Farms", "subtitle": "E-commerce platform",
        "category": "Web platforms", "context": "Client: FPL Farms", "credit": "Solo build",
        "summary": "A production storefront and admin platform for a Karachi natural foods brand, "
                   "from catalog and checkout to articles and SEO.",
        "stack": ["Next.js", "TypeScript", "Supabase", "Tailwind CSS", "SEO"],
        "metric": "Live at fplfarms.com",
        "system": {"inputs": ["Shoppers", "Admin team"], "core": "Next.js app", "detail": "Supabase + R2",
                   "outputs": ["Orders", "Order emails", "Social cards"]},
    },
]

# More work, listed as a table in the README. Only verifiable links.
ARCHIVE = [
    ("Restaurant voice-ordering backend", "FastMCP server in FastAPI: menu, caller lookup, orders and "
     "Twilio SMS as tools for a voice agent; order API on AWS Lambda", "FastAPI · FastMCP · Supabase · Twilio",
     f"{GITHUB}/brad-backend", "Repo"),
    ("Halcyon travel portal", "Four booking archetypes incl. a 9-step Umrah package builder with a live "
     "quote; Django + Wagtail CMS with silent fallback", "Next.js 16 · React 19 · Tailwind v4 · Wagtail",
     f"{GITHUB}/airline-saas", "Repo"),
    ("Property comps pipeline", "Address in, comparable listings and recent sales out: geocoding, "
     "stealth Playwright session, ±20% sqft/lot filtering, SQLite", "Python · Playwright · FastAPI",
     f"{GITHUB}/property-scraper", "Repo"),
    ("Loxo revenue report", "Attributes revenue, jobs and CVs per company from ATS placements, "
     "with a web UI on top", "Python · Next.js · Loxo API", f"{GITHUB}/loxo-automation", "Repo"),
    ("Speech dataset builder", "Collects YouTube/Instagram audio and labels each clip as human or "
     "AI-generated speech with Mistral", "Python · Mistral API · yt-dlp", f"{GITHUB}/video-downloader", "Repo"),
    ("CV / LinkedIn generator", "Form submission in, tailored CV + LinkedIn copy out, formatted in "
     "Google Docs", "n8n · OpenAI API · Google Docs API", f"{SITE}/work/automated-cv-linkedin-generator",
     "Case study"),
    ("UIT University website", "Final year project: staff create pages and publish posts without a "
     "developer", "Next.js · Sanity.io · Vercel", "https://usamania-university.vercel.app", "Live"),
]
