import streamlit as st
from datetime import datetime
from io import BytesIO
import os

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
if "used_free_trial" not in st.session_state:
    st.session_state.used_free_trial = False

if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

# ----------------------------
# TITLE & INTRO
# ----------------------------
st.title("High-Level CV Generator & ATS Optimizer")

st.write(
    "Create a professional CV and check how well it matches a job description using ATS-style analysis."
)

# ----------------------------
# TRUST & FREE TRIAL BOX
# ----------------------------
st.markdown(
    """
    <div style="
        background-color:#111827;
        padding:16px;
        border-radius:8px;
        color:#e5e7eb;
        font-size:15px;
        line-height:1.6;
    ">
        ✅ <strong>1 Free Trial (No Payment Required)</strong><br>
        🔒 We do <strong>NOT</strong> permanently store CVs or job descriptions<br>
        📧 Email required to receive CV insights<br>
        💻 Built with <strong>Python, NLP & AI</strong><br>
        ⚠️ Premium unlocks advanced AI features & PDF download
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
summary = st.text_area("Brief professional summary (2–4 sentences)", height=100)

st.subheader("Education")
education = st.text_area("Degrees, institutions, years, achievements", height=100)

st.subheader("Work Experience")
work_experience = st.text_area(
    "Job titles, companies, responsibilities, achievements", height=150
)

st.subheader("Skills")
skills = st.text_area("Skills (comma-separated)", height=100)

st.subheader("Certifications / Languages (Optional)")
certifications = st.text_area("Optional", height=80)

st.subheader("Job Description (For ATS Check)")
job_description = st.text_area("Paste job description here", height=150)

# ----------------------------
# BUILD CV
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
        "\nCertifications & Languages:\n" + certifications if certifications else ""
    ]
    return "\n".join([s for s in sections if s.strip()])

# ----------------------------
# PDF GENERATION
# ----------------------------
def generate_pdf(text):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    for line in text.split("\n"):
        c.drawString(40, y, line[:110])
        y -= 14
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    buffer.seek(0)
    return buffer

# ----------------------------
# FREE TRIAL ACTION
# ----------------------------
if st.button("Generate CV & Analyze"):
    if not email:
        st.warning("Email is required to continue.")
    elif st.session_state.used_free_trial:
        st.warning("Your free trial has been used. Unlock premium to continue.")
    else:
        st.session_state.used_free_trial = True

        with open("leads.csv", "a", encoding="utf-8") as f:
            f.write(f"{email},{datetime.now()}\n")

        complete_cv = build_complete_cv()

        st.success("Your CV has been generated.")
        st.subheader("Generated CV")
        st.text_area("Your CV", complete_cv, height=350)

        if job_description.strip():
            result = compare_cv_to_job(complete_cv, job_description)

            st.subheader("ATS Match Result")
            st.metric("Match Score", f"{result['match_score']}%")

            if result["missing_keywords"]:
                st.write("Missing Keywords:")
                st.write(result["missing_keywords"])
            else:
                st.success("Your CV matches the job very well.")

        st.info(
            "This free trial shows a basic analysis. "
            "Premium unlocks AI rewriting and PDF download."
        )

# ----------------------------
# PREMIUM SECTION
# ----------------------------
st.markdown("---")
st.subheader("🔓 Unlock Premium")

st.write(
    """
    **Premium Features**
    - Advanced AI CV rewriting
    - Stronger ATS optimization
    - Professional formatting
    - Downloadable PDF
    """
)

if st.button("Unlock Premium with PayPal"):
    if email:
        with open("payment_clicks.csv", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()},{email}\n")

        st.success("Redirecting to secure PayPal checkout…")
        st.markdown(
            '<meta http-equiv="refresh" content="2;url=https://www.paypal.com/ncp/payment/Z53DVGAC8WN7C">',
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter your email before proceeding.")

# ----------------------------
# PDF DOWNLOAD (PREMIUM ONLY)
# ----------------------------
if st.session_state.used_free_trial and st.session_state.premium_unlocked:
    pdf = generate_pdf(build_complete_cv())
    st.download_button(
        "Download CV as PDF",
        pdf,
        file_name="High_Level_CV.pdf",
        mime="application/pdf"
    )

# ----------------------------
# FEEDBACK
# ----------------------------
st.markdown("---")
st.subheader("Rate This Tool")

rating = st.slider("How useful was this tool?", 1, 5, 5)
comment = st.text_area("Optional comment", height=80)

if st.button("Submit Feedback"):
    with open("usage_log.csv", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()},{email},{rating},{comment}\n")
    st.success("Thank you for your feedback!")

# ----------------------------
# TRANSPARENCY NOTICE (VISIBLE & READABLE)
# ----------------------------
st.markdown(
    """
    <div style="
        margin-top:25px;
        padding:18px;
        border-radius:8px;
        background-color:#020617;
        color:#facc15;
        font-size:17px;
        line-height:1.8;
    ">
        <strong>Transparency Notice</strong><br>
        • No data resale<br>
        • CVs and job descriptions are not permanently stored<br>
        • Emails are used only for CV-related insights<br>
        • No job guarantees<br>
        • Educational & professional use only
    </div>
    """,
    unsafe_allow_html=True
)
