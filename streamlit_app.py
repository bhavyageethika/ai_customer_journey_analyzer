import streamlit as st
from analyze_journeys import analyze_journeys_from_json, ask_question

st.set_page_config(page_title="AI Customer Journey Insights", layout="wide")
st.title(" AI-Powered E-commerce Customer Journey Analyzer")

# Initialize session state to cache uploaded file and insights
if "json_data" not in st.session_state:
    st.session_state["json_data"] = None
if "insights" not in st.session_state:
    st.session_state["insights"] = None

uploaded = st.file_uploader("Upload your customer data json file", type="json")

# Save uploaded JSON to session state
if uploaded:
    st.session_state["json_data"] = uploaded.read().decode("utf-8")

if st.session_state["json_data"]:
    # Refresh Button
    if st.button("🔄 Refresh Analysis") or st.session_state["insights"] is None:
        with st.spinner("Reanalyzing data with GPT..."):
            st.session_state["insights"] = analyze_journeys_from_json(st.session_state["json_data"])

    insights = st.session_state["insights"]
    if any("Exception occurred" in v for v in insights.values()):
        st.warning("⚠️ GPT failed to generate insights. See example placeholders or check terminal for details.")

    SECTIONS = [
        ("patterns", "Common Behavior Patterns"),
        ("differences", "Successful vs Abandoned Journeys"),
        ("drop_offs", "Key Drop-off Points"),
        ("search_analysis", "Search & Discovery Analysis"),
        ("cart_abandonment", "Cart Abandonment Trends"),
        ("recommendations", "Recommendations to Improve Conversion"),
    ]

    for key, label in SECTIONS:
        val = insights.get(key)
        if isinstance(val, str) and val.strip():
            st.subheader(label)
            st.write(val)
        else:
            st.info(f"⚠️ No content found for: {label}")

    st.markdown("---")
    st.subheader("Ask a question about these insights")
    question = st.text_input("Ask here", placeholder="e.g. What causes most drop-offs?")
    if question:
        with st.spinner("Thinking..."):
            reply = ask_question(question, insights)
        st.markdown("**Answer:**")
        st.write(reply)
else:
    st.info("📂 Please upload a JSON file to begin.")