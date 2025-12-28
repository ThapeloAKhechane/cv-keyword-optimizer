import streamlit as st
from datetime import datetime
from io import BytesIO

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
# SAFE FILE LOGGING (CLOUD SAFE)
# ----------------------------
def write_log(filename, line):
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

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
    "Create a professional CV and see how well it matches a job description using ATS-style analysis."
)

# ----------------------------
# TRUST BOX
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
        📧 Email required for CV insights<br>
        ⚠️ Premium unlocks ATS-optimized formatting & PDF download
    </div>
    """,
    unsafe_allow_html=True
)

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
summary = st.text_area("2–4 sentences", height=100)

st.subheader("Education")
education = st.text_area("Degrees, institutions, years", height=100)

st.subheader("Work Experience")
work_experience = st.text_area("Roles, companies, achievements", height=150)

st.subheader("Skills")
skills = st.text_area("Comma-separated", height=100)

st.subheader("Certifications / Languages (Optional)")
certifications = st.text_area("Optional", height=80)

st.subheader("Job Description (For ATS Check)")
job_description = st.text_area("Paste job description", height=150)

# ----------------------------
# CV BUILDER
# ----------------------------
def build_complete_cv():
    return f"""
{name}
{city}, {country}
Email: {email} | Phone: {phone}

----------------------------------------

PROFESSIONAL SUMMARY
{summary}

----------------------------------------

EDUCATION
{education}

----------------------------------------

WORK EXPERIENCE
{work_experience}

----------------------------------------

SKILLS
{skills}

----------------------------------------

CERTIFICATIONS & LANGUAGES
{certifications}
""".strip()

# ----------------------------
# PDF GENERATION (CLEAN & PROFESSIONAL)
# ----------------------------
def generate_pdf(text):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x_margin = 40
    y = height - 40

    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = height - 40
        c.setFont("Helvetica", 10)
        c.drawString(x_margin, y, line)
        y -= 14

    c.save()
    buffer.seek(0)
    return buffer

# ----------------------------
# FREE TRIAL ACTION
# ----------------------------
if st.button("Generate CV & Analyze"):
    if not email:
        st.warning("Email is required.")
    elif st.session_state.used_free_trial:
        st.warning("Free trial already used. Unlock premium to continue.")
    else:
        st.session_state.used_free_trial = True
        write_log("leads.csv", f"{email},{datetime.now()}")

        cv_text = build_complete_cv()

        st.success("CV generated successfully.")
        st.subheader("Generated CV")
        st.text_area("Preview", cv_text, height=350)

        if job_description.strip():
            result = compare_cv_to_job(cv_text, job_description)

            st.subheader("ATS Match Result")
            st.metric("Match Score", f"{result['match_score']}%")

            if result["missing_keywords"]:
                st.write("Missing Keywords:")
                st.write(result["missing_keywords"])
            else:
                st.success("Strong ATS compatibility.")

        st.warning(
            "⚠️ Recruiters scan CVs in seconds. "
            "Premium unlocks optimized formatting & downloadable PDF."
        )

# ----------------------------
# PREMIUM SECTION
# ----------------------------
st.markdown("---")
st.subheader("🔓 Unlock Premium")

st.write(
    """
    **Premium Includes**
    - Clean ATS-friendly formatting
    - Structured professional PDF
    - Downloadable CV
    """
)

if st.button("Unlock Premium with PayPal"):
    if email:
        st.session_state.premium_unlocked = True
        write_log("payment_clicks.csv", f"{datetime.now()},{email}")
        st.success("Premium unlocked. PDF download is now available below.")
    else:
        st.warning("Please enter your email first.")

# ----------------------------
# PDF DOWNLOAD (PREMIUM)
# ----------------------------
if st.session_state.premium_unlocked:
    pdf = generate_pdf(build_complete_cv())
    st.download_button(
        "📄 Download Your Professional CV (PDF)",
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

if st.button("Submit Feedback") and email:
    write_log("usage_log.csv", f"{datetime.now()},{email},{rating},{comment}")
    st.success("Thank you for your feedback!")

# ----------------------------
# TRANSPARENCY
# ----------------------------
st.markdown(
    """
    <div style="
        margin-top:25px;
        padding:18px;
        border-radius:8px;
        background-color:#020617;
        color:#facc15;
        font-size:16px;
        line-height:1.7;
    ">
        <strong>Transparency Notice</strong><br>
        • No data resale<br>
        • No CVs permanently stored<br>
        • Emails used only for CV insights<br>
        • Educational & professional use only
    </div>
    """,
    unsafe_allow_html=True
)
