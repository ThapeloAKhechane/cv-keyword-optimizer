import streamlit as st
from datetime import datetime
from nlp import compare_cv_to_job

# UI TRUST FIX – FORCED UPDATE

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="High-Level CV Generator & ATS Optimizer",
    page_icon="📄",
    layout="centered"
)

# ----------------------------
# TITLE & INTRO
# ----------------------------
st.title("High-Level CV Generator & ATS Optimizer")

st.write(
    "Create a complete high-quality CV, then check it against any job description to optimize for ATS."
)

# ----------------------------
# TRUST BOX
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
        📧 <strong>Email is required</strong> to receive helpful CV tips<br>
        💻 Built with <strong>Python & NLP</strong> (open-source foundation)
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")  # spacing

# ----------------------------
# USER INPUTS FOR CV GENERATION
# ----------------------------
st.subheader("Personal Information")
name = st.text_input("Full Name")
email = st.text_input("Email (Required)")
phone = st.text_input("Phone (Optional)")
city = st.text_input("City")
country = st.text_input("Country")

st.subheader("Professional Summary")
summary = st.text_area("Brief professional summary (2–4 sentences)", height=100)

st.subheader("Education")
education = st.text_area("Degrees, Institutions, Graduation Years, Achievements", height=100)

st.subheader("Work Experience")
work_experience = st.text_area(
    "Job Titles, Companies, Dates, Key Responsibilities / Achievements", height=150
)

st.subheader("Skills")
skills = st.text_area("Technical / soft skills (comma-separated)", height=100)

st.subheader("Certifications & Languages (Optional)")
certifications = st.text_area("List certifications and languages", height=80)

st.subheader("Hobbies / Interests (Optional)")
hobbies = st.text_area("List hobbies or interests", height=80)

# ----------------------------
# JOB DESCRIPTION FOR ATS CHECK
# ----------------------------
st.subheader("Job Description for ATS Check")
job_description = st.text_area("Paste job description here", height=150)

# ----------------------------
# ANALYZE / GENERATE BUTTON
# ----------------------------
analyze_clicked = st.button("Generate CV & Analyze")

# ----------------------------
# HELPER FUNCTION TO CREATE CV
# ----------------------------
def build_complete_cv():
    cv_sections = [
        f"Name: {name}",
        f"Email: {email}",
        f"Phone: {phone}" if phone else "",
        f"Location: {city}, {country}",
        "\nProfessional Summary:\n" + summary,
        "\nEducation:\n" + education,
        "\nWork Experience:\n" + work_experience,
        "\nSkills:\n" + skills,
        ("\nCertifications & Languages:\n" + certifications) if certifications else "",
        ("\nHobbies / Interests:\n" + hobbies) if hobbies else ""
    ]
    return "\n".join([s for s in cv_sections if s.strip() != ""])

# ----------------------------
# HELPER FUNCTION TO GENERATE CV BULLETS
# ----------------------------
def generate_cv_bullets(missing_keywords):
    bullets = []
    for kw in missing_keywords:
        bullets.append(f"- Demonstrated experience with {kw}.")
        bullets.append(f"- Successfully applied {kw} in practical projects.")
    return bullets

# ----------------------------
# PROCESSING
# ----------------------------
if analyze_clicked:
    # --- VALIDATE EMAIL ---
    if not email:
        st.warning("Please enter your email before generating your CV.")
    elif not name or not summary or not work_experience or not skills:
        st.warning("Please fill in at least your Name, Summary, Work Experience, and Skills.")
    else:
        # --- SAVE EMAIL LEAD ---
        with open("leads.csv", "a", encoding="utf-8") as f:
            f.write(f"{email},{datetime.now()}\n")

        st.success("Thanks! Your email was recorded. We may send helpful CV tips.")

        # --- GENERATE COMPLETE CV ---
        complete_cv = build_complete_cv()
        st.subheader("Generated Complete CV")
        st.text_area("Your CV", complete_cv, height=400)

        # --- RUN ATS ANALYSIS ---
        if job_description.strip():
            result = compare_cv_to_job(complete_cv, job_description)

            st.markdown("---")
            st.subheader("ATS Analysis Results")

            st.metric(label="Match Score", value=f"{result['match_score']}%")

            st.write("### Missing Keywords")
            if result["missing_keywords"]:
                st.write(result["missing_keywords"])
                st.write("### Suggested CV Bullet Points")
                bullets = generate_cv_bullets(result["missing_keywords"])
                for b in bullets:
                    st.write(b)
            else:
                st.success("Your CV already matches very well 🎉")

            st.info(
                "Most companies use ATS (Applicant Tracking Systems) to scan CVs. "
                "Ensure your CV contains the relevant keywords to improve your chances."
            )

        else:
            st.info("No job description provided. You can copy the generated CV and paste a job description to analyze later.")

        # ----------------------------
        # USER FEEDBACK (STARS)
        # ----------------------------
        st.markdown("---")
        st.subheader("Rate the Usefulness of This Tool")

        # Star rating (1 to 5)
        rating = st.slider("How useful was this system?", 1, 5, 5)

        # Optional comment
        comment = st.text_area("Any additional comments? (Optional)", height=80)

        # Submit feedback button
        if st.button("Submit Feedback"):
            with open("usage_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()},{email},{result.get('match_score','')},{rating},{comment}\n")
            st.success("Thank you! Your feedback has been recorded.")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption("🔍 Transparency: Source code available on GitHub")
st.caption("⚠️ Disclaimer: Tool assists with keyword optimization; no job guarantees.")
