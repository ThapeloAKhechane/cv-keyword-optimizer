import streamlit as st
from nlp import compare_cv_to_job

st.set_page_config(
    page_title="Free CV Keyword Optimizer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Free CV Keyword Optimizer")
st.write(
    "Paste your CV and the job description below. "
    "See how well your CV matches the job keywords."
)

cv_text = st.text_area("Your CV", height=200)
job_text = st.text_area("Job Description", height=200)

if st.button("Analyze CV"):
    if cv_text and job_text:
        result = compare_cv_to_job(cv_text, job_text)

        st.subheader(f"✅ Match Score: {result['match_score']}%")

        if result["missing_keywords"]:
            st.subheader("❌ Missing Keywords")
            st.write(result["missing_keywords"])
        else:
            st.success("Your CV already matches very well 🎉")
    else:
        st.warning("Please paste both your CV and the job description.")
