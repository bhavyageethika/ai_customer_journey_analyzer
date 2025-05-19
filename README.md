# AI‑Powered E‑commerce Customer Journey Analyzer (Streamlit)

This prototype ingests anonymized customer‑journey data, uses GPT‑4 to
extract behavioral insights, and presents them in a simple Streamlit UI.


## Quick Start (≈2 min)
Upload any customer journey log JSON and receive GPT-based insights + chat support.

## Run Locally

Important set the api key via virtual environment else the app falls back to default : 
$env:OPENAI_API_KEY = "sk..."
or export OPENAI_API_KEY="sk-..."

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py



# 🧠 AI-Powered E-commerce Customer Journey Analyzer

This Streamlit app leverages OpenAI’s GPT-4 to analyze customer journey logs and uncover user behavior patterns, conversion bottlenecks, and product optimization opportunities — without writing a single line of SQL.

📂 Upload anonymized customer sessions in JSON format, and get:
- AI-generated insights across 6 behavioral dimensions
- Suggested visualizations for funnel drop-offs and user behavior
- A chat interface to ask follow-up questions

---

## ✨ Features

- **File Upload:** Upload your own JSON journey logs (sessions and events)
- **GPT-4 Analysis:** Summarizes conversion behavior, drop-offs, cart abandonment, search issues
- **Suggested Visualizations:** Recommends how to visualize each problem area
- **Live Q&A Chat:** Ask questions and get context-aware GPT answers based on the insights
- **Secure Key Handling:** API key is loaded via environment variable, not hardcoded

---

AI Insights Generated
Each uploaded file triggers:

Calculation of session stats: conversion rate, search success, cart abandonment

A structured prompt sent to GPT-4

JSON-formatted insight response across these categories:

"patterns": common user flows

"differences": behavior differences between buyers and abandoners

"drop_offs": key friction points

"search_analysis": search performance and behavior

"cart_abandonment": reasons and mitigation ideas

"recommendations": actionable suggestions + visualizations

Q&A Chat
Ask questions like:

“Why do users abandon carts?”

“How can we improve product page conversions?”

The AI uses your generated insights as context to answer.


Assumptions
Session data is anonymized and non-PII

Each event has a type and appears in chronological order

OpenAI API key is available via OPENAI_API_KEY

GPT-4 or GPT-4o-mini is available to the developer

No persistent storage or database is needed

Uploaded files fit within memory (~few thousand sessions)


Trade-offs Made
•	No database or persistent storage
The app processes uploaded data in-memory for simplicity. This means sessions and insights are not stored or cached.
•	No authentication or user management
The app is intended for internal demo purposes. For production, you'd want login control and per-user history.
•	Model latency and API dependency
GPT-4 is powerful but adds 2–6 seconds of latency per request. If OpenAI API quota is exceeded, the app falls back to hardcoded logic.
•	Visualization is text-only
Insight sections suggest visualizations, but the app doesn't render charts yet. This keeps the prototype lightweight but limits visual exploration.
Ideas for Future Improvements
•	Add visual dashboards
Use Altair or Plotly to render funnel charts, search effectiveness heatmaps, and cart abandonment over time.
•	Fine-tuned model or local LLM
Replace GPT with a fine-tuned smaller model or an open-source LLM (like Mistral) to reduce cost and latency.
•	Session uploads + versioning
Let users upload multiple datasets, store them securely, and compare insights over time.
•	Query history and export
Store all questions and answers asked in the chat, and allow export to PDF or Markdown.
•	Granular segmentation
Let users slice the data by country, device, or referrer — and regenerate insights per segment.
•	Experiment integration
If you're running A/B tests, you could add experiment tags and generate variant-specific insights.

Security
The OpenAI API key is loaded via os.getenv("OPENAI_API_KEY")

.env file support is enabled if using python-dotenv

API keys should never be committed to the repo



Appendix

Summary of Trade-offs Made (extended)
Area	Trade-off
1. Storage	No database or caching — all analysis is in-memory per session.
2. Authentication	No user login or multi-user session tracking.
3. Upload scope	Supports only one uploaded file at a time; no batch or multi-session comparisons.
4. File format	Only supports JSON format with pre-defined schema.
5. Frontend	No frontend framework or styling — relies on Streamlit’s default UI.
6. Visuals	Text-only output — no embedded charts or visual dashboards.
7. Prompting	GPT prompt is fixed; no real-time prompt tuning or model control exposed to user.
8. Model selection	Hardcoded to GPT-4 (gpt-4o-mini); doesn’t dynamically fallback to gpt-3.5 or open models.
9. Upload validation	Assumes uploaded JSON is well-formed; no advanced schema validation or error feedback.
10. Real-time interaction	No websocket/live interaction — all responses are synchronous.
11. Speed vs Depth	Used GPT-4 for quality, accepting slower response time.
12. Cost	Uses OpenAI API which may incur cost with every file upload or chat question.
13. Localization	Only supports English output; no multilingual support.
14. Mobile UX	Streamlit UI is not optimized for mobile responsiveness.
15. Exporting	No download options for results (PDF, CSV, etc.).
16. Dataset size	Not optimized for large-scale datasets (e.g., >10k sessions).
17. Analytics depth	Computes only top-level stats; no funnel depth or session paths per cohort.
18. Access control	Everyone using the app sees the same model and API key.
19. Rate limiting	No protection against rapid successive OpenAI calls.
20. Logging	No audit trail or server-side logs for session uploads or API calls.


Ideas for Future Improvements (extended)
Area	Feature
1. Charting	Render funnel charts, pie charts, histograms, and time-series directly using Altair/Plotly.
2. Segment Filtering	Let users filter insights by country, referrer, or device type before sending to GPT.
3. Multi-file support	Allow multiple JSON uploads and comparison across them.
4. Live Chat History	Store and persist chat conversations per session for later review.
5. PDF Export	One-click PDF or Markdown export of the insights and chat log.
6. Dashboard Mode	Show funnel progression with metrics + GPT insights side-by-side.
7. Auto-analysis on Upload	Auto-run analysis when file is uploaded instead of waiting for user to click.
8. Custom Prompt Builder	Expose prompt tuning UI for advanced users to refine GPT behavior.
9. Model Selector	Toggle between GPT-4, GPT-3.5, Claude, Mistral, or local models via dropdown.
10. Prompt Templates	Provide prompt presets like “marketing insights,” “UX feedback,” or “churn root causes.”
11. Collaboration	Let teams collaborate and leave comments on insights.
12. Versioning	Save and compare insights generated from different file uploads.
13. Data Validation	Add schema and format validator with detailed error messages before analyzing.
14. Chat Co-Pilot	Use a dedicated agent that can remember context and explain GPT insights.
15. Shareable Links	Create public URLs or embeds to share analysis with others.
16. Streamlit Cloud Deployment	Host it online with auto-refresh, auth, and session management.
17. LLM Fine-tuning	Fine-tune a model with custom e-commerce data for deeper insights.
18. Role-specific Views	Show different summaries depending on viewer (e.g., product, marketing, ops).
19. Integration with GA4 / Mixpanel	Ingest behavioral logs directly from live analytics platforms.
20. AI Summarized Dashboard Video	Auto-generate a Loom-style video summary of insights for stakeholders.



   