import streamlit as st
import os
from datetime import datetime
import csv
from dotenv import load_dotenv
import openai

from nlp import compare_cv_to_job

# ----------------------------
# LOAD ENVIRONMENT VARIABLES
# ----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please check your .env file.")
    st.stop()

openai.api_key = OPENAI_API_KEY

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="High-Level CV Generator & ATS Optimizer",
    page_icon="📄",
    layout="centered"
)

# ----------------------------
# SESSION STATE (FREE TRIAL)
# ----------------------------
if "free_used" not in st.session_state:
    st.session_state.free_used = False

# ----------------------------
# TITLE
# ----------------------------
st.title("High-Level CV Generator & ATS Optimizer")

st.write(
    "Build a **professional, ATS-optimized CV**, then analyze it against any job description."
)

# ----------------------------
# TRUST BOX
# ----------------------------
st.markdown("""
<div style="background:#f0f8ff;padding:15px;border-radius:6px;font-size:14px;">
✅ <b>1 Free Trial</b> (no payment)<br>
🔒 <b>We do NOT store CV or job descriptions</b><br>
📧 <b>Email required</b> for CV insights<br>
💻 Built with <b>Python, NLP & AI</b><br>
⚠️ Premium unlocks advanced AI rewriting
</div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------
# USER INPUTS
# ----------------------------
st.subheader("Personal Information")
name = st.text_input("Full Name")
email = st.text_input("Email (Required)")
city = st.text_input("City")
country = st.text_input("Country")

st.subheader("Professional Summary")
summary = st.text_area("2–4 sentence summary")

st.subheader("Work Experience")
experience = st.text_area("Roles, achievements, responsibilities")

st.subheader("Education")
education = st.text_area("Degrees, institutions")

st.subheader("Skills")
skills = st.text_area("Comma-separated skills")

st.subheader("Job Description")
job_description = st.text_area("Paste job description")

# ----------------------------
# BUTTON
# ----------------------------
analyze = st.button("Generate CV & Analyze")

# ----------------------------
# CV BUILDER
# ----------------------------
def build_cv():
    return f"""
{name}
{city}, {country}
Email: {email}

PROFESSIONAL SUMMARY
{summary}

WORK EXPERIENCE
{experience}

EDUCATION
{education}

SKILLS
{skills}
"""

# ----------------------------
# AI REWRITE (PREMIUM)
# ----------------------------
def ai_rewrite(cv_text):
    prompt = f"""
Rewrite the following CV to be highly professional,
ATS-optimized, achievement-focused and modern.

CV:
{cv_text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content

# ----------------------------
# MAIN LOGIC
# ----------------------------
if analyze:
    if not email:
        st.warning("Email is required.")
        st.stop()

    if not all([name, summary, experience, skills]):
        st.warning("Please fill in all required sections.")
        st.stop()

    # Save email
    with open("leads.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([email, datetime.now()])

    cv_text = build_cv()

    # ATS ANALYSIS
    result = compare_cv_to_job(cv_text, job_description)

    st.subheader("ATS Match Result")
    st.metric("Match Score", f"{result['match_score']}%")

    st.write("Missing Keywords:", result["missing_keywords"])

    # ----------------------------
    # FREE TRIAL LIMIT
    # ----------------------------
    if not st.session_state.free_used:
        st.session_state.free_used = True

        st.info("""
You are viewing **FREE TRIAL results**.

🔓 Premium unlocks:
• AI-rewritten CV  
• Strong bullet points  
• ATS keyword injection  
• Professional formatting
""")

    else:
        st.warning("Free trial used.")

        st.markdown("### 🔓 Unlock Premium")
        st.markdown("""
**Get the full AI-optimized CV instantly**

✔ Deep AI rewrite  
✔ ATS keyword alignment  
✔ Strong achievement bullets  
✔ Ready-to-submit CV
""")

        st.markdown(
            """
            <a href="https://www.paypal.com/ncp/payment/Z53DVGAC8WN7C" target="_blank">
            <button style="background:#0070ba;color:white;padding:12px 20px;border:none;border-radius:5px;font-size:16px;">
            Pay with PayPal – Unlock Premium
            </button>
            </a>
            """,
            unsafe_allow_html=True
        )

        st.stop()

    # ----------------------------
    # PREMIUM AI REWRITE (AFTER PAYMENT)
    # ----------------------------
    if st.checkbox("I have paid – Generate Premium CV"):
        with st.spinner("AI is rewriting your CV..."):
            premium_cv = ai_rewrite(cv_text)

        st.subheader("Premium AI-Optimized CV")
        st.text_area("Your Premium CV", premium_cv, height=450)

    # ----------------------------
    # FEEDBACK
    # ----------------------------
    st.subheader("Rate this tool")
    rating = st.slider("How useful was this?", 1, 5, 5)
    comment = st.text_area("Optional feedback")

    if st.button("Submit Feedback"):
        with open("usage_log.csv", "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(
                [datetime.now(), email, rating, comment]
            )
        st.success("Thank you for your feedback!")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption("Transparency • No data resale • Educational use")
