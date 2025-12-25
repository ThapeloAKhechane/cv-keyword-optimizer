import streamlit as st
from datetime import datetime
from nlp import compare_cv_to_job

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="High-Level CV Generator & ATS Optimizer",
    page_icon="📄",
    layout="centered"
)

# ----------------------------
# SESSION STATE
# ----------------------------
if "unlocked" not in st.session_state:
    st.session_state["unlocked"] = False

# ----------------------------
# PAYPAL LINK
# ----------------------------
PAYPAL_PAYMENT_LINK = "https://www.paypal.com/ncp/payment/Z53DVGAC8WN7C"

# ----------------------------
# TITLE & INTRO
# ----------------------------
st.title("High-Level CV Generator & ATS Optimizer")

st.write(
    "Create a professional CV and optimize it for Applicant Tracking Systems (ATS)."
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
        <strong>✅ Secure & Private</strong><br>
        🔒 We do NOT store your CV or job description<br>
        📧 Email required to send helpful CV tips<br>
        💳 One-time PayPal payment (no subscriptions)
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ----------------------------
# USER INPUTS
# ----------------------------
st.subheader("Personal Information")
name = st.text_input("Full Name")
email = st.text_input("Email (Required)")
phone = st.text_input("Phone (Optional)")
city = st.text_input("City")
country = st.text_input("Country")

st.subheader("Professional Summary")
summary = st.text_area("2–4 sentence professional summary", height=100)

st.subheader("Education")
education = st.text_area("Degrees, Institutions, Years", height=100)

st.subheader("Work Experience")
work_experience = st.text_area(
    "Roles, Companies, Achievements", height=150
)

st.subheader("Skills")
skills = st.text_area("Skills (comma-separated)", height=100)

st.subheader("Certifications & Languages (Optional)")
certifications = st.text_area("Certifications / Languages", height=80)

st.subheader("Hobbies / Interests (Optional)")
hobbies = st.text_area("Hobbies / Interests", height=80)

st.subheader("Job Description (for ATS Analysis)")
job_description = st.text_area("Paste job description here", height=150)

# ----------------------------
# GENERATE BUTTON
# ----------------------------
generate_clicked = st.button("Generate CV")

# ----------------------------
# CV BUILDER
# ----------------------------
def build_complete_cv():
    sections = [
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
    return "\n".join([s for s in sections if s.strip()])

# ----------------------------
# BULLET GENERATOR
# ----------------------------
def generate_cv_bullets(missing_keywords):
    bullets = []
    for kw in missing_keywords:
        bullets.append(f"- Demonstrated hands-on experience with {kw}.")
        bullets.append(f"- Applied {kw} in real-world professional scenarios.")
    return bullets

# ----------------------------
# PROCESS
# ----------------------------
if generate_clicked:
    if not email:
        st.warning("Email is required.")
    elif not name or not summary or not work_experience or not skills:
        st.warning("Please complete all required fields.")
    else:
        # Save email lead
        with open("leads.csv", "a", encoding="utf-8") as f:
            f.write(f"{email},{datetime.now()}\n")

        st.success("CV generated successfully.")

        complete_cv = build_complete_cv()

        st.subheader("Generated CV")
        st.text_area("Your CV", complete_cv, height=400)

        st.markdown("---")

        # ----------------------------
        # PAYWALL SECTION
        # ----------------------------
        if not st.session_state["unlocked"]:
            st.subheader("🔒 ATS Optimization Locked")

            st.write(
                "Unlock ATS analysis, keyword matching, and improvement suggestions."
            )

            st.markdown(
                f"""
                <a href="{PAYPAL_PAYMENT_LINK}" target="_blank">
                    <button style="
                        background-color:#0070ba;
                        color:white;
                        padding:14px 22px;
                        border:none;
                        border-radius:6px;
                        font-size:16px;
                        cursor:pointer;
                    ">
                        💳 Pay with PayPal to Unlock
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                "Secure PayPal checkout • One-time payment • No refunds after analysis"
            )

            if st.button("✅ I have completed payment"):
                st.session_state["unlocked"] = True
                st.success("Payment confirmed. ATS features unlocked.")

        # ----------------------------
        # ATS ANALYSIS (UNLOCKED)
        # ----------------------------
        if st.session_state["unlocked"] and job_description.strip():
            st.markdown("---")
            st.subheader("ATS Analysis Results")

            result = compare_cv_to_job(complete_cv, job_description)

            st.metric("Match Score", f"{result['match_score']}%")

            if result["missing_keywords"]:
                st.write("### Missing Keywords")
                st.write(result["missing_keywords"])

                st.write("### Suggested Bullet Points")
                for bullet in generate_cv_bullets(result["missing_keywords"]):
                    st.write(bullet)
            else:
                st.success("Your CV is already well-optimized 🎉")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption("⚠️ Disclaimer: This tool improves ATS keyword alignment only.")
st.caption("© 2025 High-Level CV Optimizer")
