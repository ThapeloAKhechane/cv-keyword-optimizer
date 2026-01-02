import streamlit as st
import os
import pandas as pd
from datetime import datetime

# ----------------------------
# LOAD ADMIN PASSWORD (LOCAL + CLOUD SAFE)
# ----------------------------
ADMIN_PASSWORD = None

if "ADMIN_PASSWORD" in st.secrets:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
else:
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# 🔍 TEMPORARY DEBUG LINE (REMOVE AFTER CONFIRMATION)
st.write("Password loaded:", bool(ADMIN_PASSWORD))

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Admin Dashboard")

# ----------------------------
# SECURITY CHECK
# ----------------------------
if not ADMIN_PASSWORD:
    st.error("❌ Admin password is not configured.")
    st.stop()

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    password_input = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):
        if password_input == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.success("Access granted")
            st.rerun()
        else:
            st.error("Incorrect password")

    st.stop()

# ----------------------------
# DASHBOARD CONTENT
# ----------------------------
st.success("Welcome, Admin")

# ----------------------------
# LOAD DATA
# ----------------------------
def load_csv(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()

leads = load_csv("leads.csv")
payments = load_csv("payment_clicks.csv")
feedback = load_csv("usage_log.csv")

# ----------------------------
# KEY METRICS
# ----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Email Leads", len(leads))
col2.metric("Checkout Clicks", len(payments))

conversion_rate = (
    round((len(payments) / len(leads)) * 100, 2)
    if len(leads) > 0 else 0
)
col3.metric("Lead → Checkout %", f"{conversion_rate}%")
col4.metric("Feedback Entries", len(feedback))

# ----------------------------
# EMAIL LEADS
# ----------------------------
st.subheader("📧 Email Leads")
st.dataframe(leads, use_container_width=True)

# ----------------------------
# PAYMENT INTENT TIMELINE
# ----------------------------
st.subheader("💳 Payment Intent Timeline")

if not payments.empty and "timestamp" in payments.columns:
    payments["timestamp"] = pd.to_datetime(
        payments["timestamp"],
        errors="coerce"
    )

    payments = payments.dropna(subset=["timestamp"])
    payments = payments.sort_values("timestamp", ascending=False)

    st.dataframe(payments, use_container_width=True)
else:
    st.info("No valid payment timestamp data available.")

# Debug helper (admin-only visibility)
with st.expander("🔍 Payments CSV Structure"):
    st.write(payments.columns.tolist())

# ----------------------------
# USER FEEDBACK
# ----------------------------
st.subheader("⭐ User Feedback")
st.dataframe(feedback, use_container_width=True)

# ----------------------------
# INSIGHTS
# ----------------------------
st.subheader("🧠 Insights")

if conversion_rate < 10:
    st.warning("Low conversion rate. Improve value messaging or CTA.")
elif conversion_rate < 25:
    st.info("Average conversion. Try urgency or testimonials.")
else:
    st.success("Strong conversion rate.")

st.markdown("---")
st.caption("Admin access is protected. Unauthorized users are blocked.")
