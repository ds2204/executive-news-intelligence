import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Executive News Intelligence Engine")

st.title("Executive News Intelligence Engine")
st.write("AI-powered rule-based news intelligence for executives.")

st.markdown("### About")
st.write("""
This tool analyzes structured technology news scenarios and generates executive-level insights.
The intelligence logic replicates the rule-based engine built in Assignment 4 using n8n.
Designed for business leaders who need fast strategic awareness.

Created by Deepa Shenoy.
""")

# -----------------------------
# Input Section
# -----------------------------
st.markdown("### Select News Scenario")

scenario = st.selectbox(
    "Choose a scenario to analyze:",
    [
        "AI & Startup Activity",
        "Regulation & Policy News",
        "General Tech Updates"
    ]
)

generate = st.button("Generate Executive Report")

# -----------------------------
# Intelligence Engine
# -----------------------------
if generate:

    # Structured input dataset (replicates A4 input layer)
    if scenario == "AI & Startup Activity":
        articles = [
            {
                "title": "AI startup announces major acquisition",
                "content": "The company reported record growth and innovation in artificial intelligence."
            },
            {
                "title": "Tech firm launches new AI platform",
                "content": "The launch signals expansion and increased market share."
            }
        ]

    elif scenario == "Regulation & Policy News":
        articles = [
            {
                "title": "Government proposes new AI regulation",
                "content": "New privacy laws may impact technology companies."
            },
            {
                "title": "Major tech company faces investigation",
                "content": "Regulatory scrutiny increases after data privacy lawsuit."
            }
        ]

    else:
        articles = [
            {
                "title": "Tech conference highlights innovation trends",
                "content": "Startups showcase product launches and new features."
            },
            {
                "title": "Industry report shows steady growth",
                "content": "Market expansion continues across sectors."
            }
        ]

    results = []

    for article in articles:
        title = article["title"]
        text = (article["title"] + " " + article["content"]).lower()

        # Rule-based scoring logic (from A4)
        impact_keywords = ["layoff", "regulation", "lawsuit", "acquisition", "merger", "ai", "ban"]
        positive_words = ["growth", "launch", "record", "innovation", "increase"]
        negative_words = ["loss", "decline", "cut", "ban", "layoff", "investigation"]

        impact_score = sum(2 for word in impact_keywords if word in text)
        sentiment_score = (
            sum(1 for word in positive_words if word in text)
            - sum(1 for word in negative_words if word in text)
        )

        # Impact classification
        if impact_score >= 4:
            impact_level = "High"
        elif impact_score >= 2:
            impact_level = "Medium"
        else:
            impact_level = "Low"

        # Sentiment classification
        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Topic detection
        topic = "General Technology"
        if "ai" in text:
            topic = "Artificial Intelligence"
        elif "privacy" in text or "regulation" in text:
            topic = "Policy & Regulation"
        elif "startup" in text:
            topic = "Startups"

        # Executive Insight
        if impact_level == "High":
            executive_insight = (
                "This development may require immediate executive attention due to potential "
                "strategic or regulatory implications."
            )
        elif impact_level == "Medium":
            executive_insight = (
                "This trend should be monitored as it may influence market or operational decisions."
            )
        else:
            executive_insight = (
                "This update is informational and does not require immediate executive action."
            )

        results.append({
            "Title": title,
            "Topic": topic,
            "Impact Level": impact_level,
            "Sentiment": sentiment,
            "Executive Insight": executive_insight
        })

    df = pd.DataFrame(results)

    st.markdown("### Executive Intelligence Report")
    st.dataframe(df, use_container_width=True)

    # Download option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Report as CSV",
        data=csv,
        file_name="executive_news_intelligence_report.csv",
        mime="text/csv"
    )