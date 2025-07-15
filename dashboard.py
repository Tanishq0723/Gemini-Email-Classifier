
# dashboard.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

CSV_PATH = "C:\\Users\\tanis\\classified_emails.csv"   # adjust if the file lives elsewhere

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

# ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Email Insights", layout="wide")
st.title("📊  Smart Email Insights")

df = load_data(CSV_PATH)

# ── Sidebar filters ─────────────────────────────────────────────
st.sidebar.header("Filters")
categories = st.sidebar.multiselect(
    "Category", sorted(df["category"].unique()), default=list(df["category"].unique())
)
sentiments = st.sidebar.multiselect(
    "Sentiment", sorted(df["sentiment"].unique()), default=list(df["sentiment"].unique())
)
urgencies = st.sidebar.multiselect(
    "Urgency", sorted(df["urgency"].unique()), default=list(df["urgency"].unique())
)

filtered = df[
    df["category"].isin(categories)
    & df["sentiment"].isin(sentiments)
    & df["urgency"].isin(urgencies)
]

st.markdown(f"**{len(filtered)} emails** match the current filters.")

# ── Metrics row ─────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Complaints", int((df["category"] == "complaint").sum()))
col2.metric("Positive Emails", int((df["sentiment"] == "positive").sum()))
col3.metric("High‑Urgency", int((df["urgency"] == "high").sum()))

# ── Category distribution chart ────────────────────────────────
st.subheader("Emails by Category")
cat_counts = filtered["category"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(cat_counts, labels=cat_counts.index, autopct="%1.0f%%", startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

# ── Sentiment bar chart ────────────────────────────────────────
st.subheader("Sentiment Breakdown")
sent_counts = filtered["sentiment"].value_counts()
fig2, ax2 = plt.subplots()
ax2.bar(sent_counts.index, sent_counts.values)
ax2.set_xlabel("Sentiment")
ax2.set_ylabel("Count")
st.pyplot(fig2)

# ── High‑urgency table ─────────────────────────────────────────
st.subheader("🚨 High‑Urgency Emails")
st.dataframe(
    filtered[filtered["urgency"] == "high"][["subject", "category", "sentiment"]],
    use_container_width=True,
    hide_index=True,
)
