import streamlit as st
from datetime import datetime

from nlp import compare_cv_to_job
# UI TRUST FIX – FORCED UPDATE

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Free CV Keyword Optimizer",
    page_icon="📄",
    layout="centered"
)

# ----------------------------
# TITLE & INTRO
# ----------------------------
st.title("Free CV Keyword Optimizer")

st.write(
    "Improve your CV by matching it against a job description. "
    "This tool helps job seekers optimize keywords for "
    "ATS (Applicant Tracking Systems)."
)

# ----------------------------
# TRUST BOX (FIXED TEXT VISIBILITY)
# ----------------------------
st.markdown(
    """
    <div style="
        background-color:#f0f8ff;
        padding:15px;
        border-radius:6px;
        font-size:14px;
        color:#000000;
        line-height:1.6;
    ">
        <strong>✅ 100% Free tool</strong><br>
        🔒 <strong>We do NOT store your CV or job description</strong><br>
        📧 <strong>Email is optional</strong> and used only to send helpful CV tips<br>
        💻 Built with <strong>Python & NLP</strong> (open-source foundation)
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")  # spacing

# ----------------------------
# INPUTS
# ----------------------------
st.subheader("Your CV")
cv_text = st.text_area(
    "Paste your CV here",
    height=200
)

st.subheader("Job Description")
job_text = st.text_area(
    "Paste the job description here",
    height=200
)

st.subheader("Email (Optional)")
email = st.text_input(
    "Optional: Enter your email to receive helpful CV tips and insights"
)

# ----------------------------
# ANALYZE BUTTON
# ----------------------------
analyze_clicked = st.button("Analyze CV")

# ----------------------------
# PROCESSING & RESULTS
# ----------------------------
if analyze_clicked:
    if not cv_text or not job_text:
        st.warning("Please paste both your CV and the job description.")
    else:
        # Run NLP comparison (NO storage of CV or job text)
        result = compare_cv_to_job(cv_text, job_text)

        st.markdown("---")
        st.subheader("Results")

        # Match score
        st.metric(
            label="ATS Match Score",
            value=f"{result['match_score']}%"
        )

        # ATS explanation
        st.info(
            "Most companies use Applicant Tracking Systems (ATS) to scan CVs "
            "before a recruiter sees them. If your CV does not contain enough "
            "relevant keywords from the job description, it may be rejected "
            "automatically — even if you are qualified."
        )

        # Missing keywords
        st.write("### Missing Keywords")
        if result["missing_keywords"]:
            st.write(
                "These important keywords appear in the job description but "
                "are missing or weakly represented in your CV:"
            )
            st.write(result["missing_keywords"])
        else:
            st.success("Your CV already matches very well 🎉")

        # ----------------------------
        # EMAIL HANDLING (ETHICAL)
        # ----------------------------
        if email:
            with open("leads.csv", "a", encoding="utf-8") as f:
                f.write(f"{email},{datetime.now()}\n")

            st.success(
                "Thanks! Your email was recorded. "
                "We may send helpful CV tips and insights."
            )

        # ----------------------------
        # SOFT MONETIZATION (NO PRESSURE)
        # ----------------------------
        st.markdown("---")
        st.write(
            "💡 **Tip:** Candidates who improve their ATS score above **50%** "
            "often increase their chances of getting interview callbacks."
        )

        st.write(
            "If you would like help rewriting your CV or generating "
            "ATS-optimized bullet points, optional paid assistance may be available."
        )

# ----------------------------
# FOOTER (LEGITIMACY)
# ----------------------------
st.markdown("---")
st.caption(
    "🔍 Transparency: Source code available on GitHub — "
    "https://github.com/ThapeloAKhechane/cv-keyword-optimizer"
)
st.caption(
    "⚠️ Disclaimer: This tool assists with keyword optimization only "
    "and does not guarantee job placement."
)
