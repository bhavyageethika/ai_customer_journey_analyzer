import streamlit as st
from analyze_journeys import analyze_journeys_from_json, ask_question

st.set_page_config(page_title="AI Customer Journey Insights", layout="wide")
st.title(" AI-Powered E-commerce Customer Journey Analyzer")

uploaded = st.file_uploader("Upload your customer data json file", type="json")

if uploaded:
    raw_json = uploaded.read().decode("utf-8")
    with st.spinner("AI-Powered E-commerce Customer Journey Analyzer"):
        insights = analyze_journeys_from_json(raw_json)

    #st.subheader(" GPT Insights Summary")
    #st.json(insights)

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
    st.subheader("💬 Ask a question about these insights")
    question = st.text_input("Ask here", placeholder="e.g. What causes most drop-offs?")
    if question:
        with st.spinner("Thinking..."):
            reply = ask_question(question, insights)
        st.markdown("**Answer:**")
        st.write(reply)
else:
    st.info("📂 Please upload a JSON file to begin.")