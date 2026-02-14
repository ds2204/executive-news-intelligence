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
This tool processes the real dataset (data.csv) collected and analyzed in Assignment 4.
It applies rule-based impact scoring, sentiment detection, and topic classification.

Created by Deepa Shenoy

GitHub: https://github.com/ds2204/executive-news-intelligence
""")

# -----------------------------
# Load A4 Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# -----------------------------
# Input Section
# -----------------------------
st.markdown("### Filter by Category")

categories = ["All"] + list(df["label"].unique())
selected_category = st.selectbox("Choose a category:", categories)

generate = st.button("Generate Executive Report")

# -----------------------------
# Intelligence Functions (A4 Logic)
# -----------------------------

def calculate_impact(text):
    impact_keywords = ["policy", "regulation", "lawsuit", "market", "ban", "crisis", "investigation"]
    score = sum(2 for word in impact_keywords if word in text)
    if score >= 4:
        return "High"
    elif score >= 2:
        return "Medium"
    else:
        return "Low"


def detect_sentiment(text):
    positive_words = ["growth", "positive", "breakthrough", "record", "innovation", "increase"]
    negative_words = ["decline", "loss", "ban", "crisis", "controversial", "investigation"]

    sentiment_score = (
        sum(1 for word in positive_words if word in text)
        - sum(1 for word in negative_words if word in text)
    )

    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"


def classify_topic(label):
    return label  # using A4 dataset label directly


def generate_insight(impact_level):
    if impact_level == "High":
        return "This development may require immediate executive attention due to potential strategic implications."
    elif impact_level == "Medium":
        return "This trend should be monitored as it may influence business or operational decisions."
    else:
        return "This update is informational and does not require immediate executive action."

# -----------------------------
# Generate Report
# -----------------------------
if generate:

    working_df = df.copy()

    if selected_category != "All":
        working_df = working_df[working_df["label"] == selected_category]

    results = []

    for _, row in working_df.iterrows():

        text = str(row["text"]).lower()

        topic = classify_topic(row["label"])
        sentiment = detect_sentiment(text)
        impact_level = calculate_impact(text)
        insight = generate_insight(impact_level)

        results.append({
            "Article Text": row["text"][:120] + "...",
            "Category": topic,
            "Impact Level": impact_level,
            "Sentiment": sentiment,
            "Executive Insight": insight
        })

    report_df = pd.DataFrame(results)

    st.markdown("### Executive Intelligence Report")
    st.dataframe(report_df, use_container_width=True)

    # Download CSV
    csv = report_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Report as CSV",
        data=csv,
        file_name="executive_news_intelligence_report.csv",
        mime="text/csv"
    )
