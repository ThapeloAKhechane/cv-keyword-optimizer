import streamlit as st
import pandas as pd

# ----------------------------
# ADMIN PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🔐",
    layout="wide"
)

# ----------------------------
# ADMIN AUTH
# ----------------------------
ADMIN_PASSWORD = "admin123"  # CHANGE THIS LATER

st.title("🔐 Admin Dashboard")

password = st.text_input("Enter admin password", type="password")

if password != ADMIN_PASSWORD:
    st.warning("Unauthorized access")
    st.stop()

st.success("Access granted")

# ----------------------------
# LOAD DATA
# ----------------------------
def load_csv(path, columns=None):
    try:
        return pd.read_csv(path)
    except:
        if columns:
            return pd.DataFrame(columns=columns)
        return pd.DataFrame()

leads = load_csv("../leads.csv", ["email", "timestamp"])
usage = load_csv("../usage_log.csv", ["timestamp", "email", "rating", "comment"])

# ----------------------------
# METRICS
# ----------------------------
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Leads", len(leads))

with col2:
    st.metric("Total Feedback Entries", len(usage))

with col3:
    avg_rating = usage["rating"].mean() if not usage.empty else 0
    st.metric("Average Rating", round(avg_rating, 2))

# ----------------------------
# LEADS TABLE
# ----------------------------
st.markdown("## 📧 Email Leads")
st.dataframe(leads, use_container_width=True)

# ----------------------------
# FEEDBACK TABLE
# ----------------------------
st.markdown("## ⭐ User Feedback")
st.dataframe(usage, use_container_width=True)

# ----------------------------
# INSIGHTS
# ----------------------------
st.markdown("## 🧠 Insights")

if not usage.empty:
    high_ratings = usage[usage["rating"] >= 4]
    st.write(f"Users rating 4⭐ or higher: {len(high_ratings)}")

    if not high_ratings.empty:
        st.write("Top feedback comments:")
        for c in high_ratings["comment"].dropna().head(5):
            st.write(f"- {c}")
else:
    st.info("No feedback data yet.")

st.markdown("---")
st.caption("Admin-only internal dashboard")
