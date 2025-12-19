import streamlit as st
from datetime import datetime

from nlp import compare_cv_to_job

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
    "This tool helps job seekers optimize keywords for ATS (Applicant Tracking Systems)."
)

# ----------------------------
# TRUST BOX
# ----------------------------
st.markdown(
    """
    <div style="background-color:#f0f8ff; padding:15px; border-radius:6px; font-size:14px;">
    ✅ <b>100% Free tool</b><br>
    🔒 <b>We do NOT store your CV or job description</b><br>
    📧 <b>Email is optional</b> and used only to send helpful CV tips<br>
    💻 Built with <b>Python & NLP</b> (open-source foundation)
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
# PROCESSING
# ----------------------------
if analyze_clicked:
    if not cv_text or not job_text:
        st.warning("Please paste both your CV and the job description.")
    else:
        # Run NLP comparison (NO STORAGE of CV/job text)
        result = compare_cv_to_job(cv_text, job_text)

        # ----------------------------
        # RESULTS
        # ----------------------------
        st.markdown("---")
        st.subheader("Results")

        st.metric(
            label="ATS Match Score",
            value=f"{result['match_score']}%"
        )

        # Explanation
        st.info(
            "Most companies use Applicant Tracking Systems (ATS) to scan CVs before a recruiter sees them. "
            "Low keyword match scores may result in automatic rejection, even if you are qualified."
        )

        # Missing keywords
        st.write("### Missing Keywords")
        if result["missing_keywords"]:
            st.write(
                "These important keywords appear in the job description but not strongly in your CV:"
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
            "If you would like help rewriting your CV or generating ATS-optimized bullet points, "
            "optional paid assistance may be available."
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
    "⚠️ Disclaimer: This tool assists with keyword optimization only and does not guarantee job placement."
)
