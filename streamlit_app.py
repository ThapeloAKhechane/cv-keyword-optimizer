import streamlit as st
from fpdf import FPDF
import re

# =============================
# CONFIGURATION
# =============================
APP_NAME = "AI CV & ATS Optimizer"
ADMIN_EMAIL = "khechanethapelo5@gmail.com"
PAYPAL_LINK = "https://www.paypal.com/ncp/payment/Z53DVGAC8WN7C"

# =============================
# SESSION STATE
# =============================
if "free_used" not in st.session_state:
    st.session_state.free_used = False

if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

# =============================
# UTILITY FUNCTIONS
# =============================
def sanitize_text(text: str) -> str:
    replacements = {
        "–": "-",
        "—": "-",
        "•": "-",
        "’": "'",
        "“": '"',
        "”": '"',
        "…": "...",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    return text.encode("latin-1", errors="ignore").decode("latin-1")

def extract_keywords(text):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    return list(set(words))

def ats_score(cv, jd):
    cv_words = extract_keywords(cv)
    jd_words = extract_keywords(jd)
    matched = set(cv_words).intersection(set(jd_words))
    score = int((len(matched) / max(len(jd_words), 1)) * 100)
    return score, matched

def basic_pdf(cv_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    safe_text = sanitize_text(cv_text)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf

def premium_pdf(cv_text):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "Professional CV", ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", size=11)

    safe_text = sanitize_text(cv_text)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 8, "- " + line)

    return pdf

def ai_rewrite(cv, keywords):
    return (
        "PROFESSIONAL SUMMARY\n"
        "Results-driven professional with strong experience in "
        + ", ".join(list(keywords)[:6]) +
        ". Proven ability to deliver measurable results and adapt quickly.\n\n"
        + cv
    )

# =============================
# UI SETUP
# =============================
st.set_page_config(page_title=APP_NAME, layout="wide")
st.title(APP_NAME)
st.caption("Beat ATS systems • Get noticed • One free trial")

# =============================
# USER EMAIL
# =============================
email = st.text_input("Your email (required for premium access)")

if email.strip().lower() == ADMIN_EMAIL.lower():
    st.session_state.premium_unlocked = True

# =============================
# FREE CORE TOOL
# =============================
st.header("🟢 Free ATS CV Check (1 Free Trial)")

cv_text = st.text_area("Paste your CV here", height=200)
jd_text = st.text_area("Paste Job Description here", height=150)

if st.button("Analyze CV"):
    if st.session_state.free_used:
        st.warning("You have already used your free trial.")
    elif not cv_text or not jd_text:
        st.error("Please provide both CV and job description.")
    else:
        st.session_state.free_used = True

        score, matched = ats_score(cv_text, jd_text)

        st.success(f"ATS Match Score: {score}%")
        st.write("### Matched Keywords")
        st.write(", ".join(sorted(matched)))

        st.info("This is a basic preview. Premium unlocks AI rewriting & professional formatting.")

        try:
            pdf = basic_pdf(cv_text)
            st.download_button(
                "Download Basic PDF",
                data=pdf.output(dest="S").encode("latin-1"),
                file_name="basic_cv.pdf",
                mime="application/pdf"
            )
        except Exception:
            st.error("PDF generation failed due to unsupported characters.")

# =============================
# PRIVACY NOTICE
# =============================
st.markdown("---")
st.caption(
    "🔒 Privacy Notice: CVs and job descriptions are processed only in-session. "
    "We do NOT store, sell, or reuse your data."
)

# =============================
# PREMIUM PREVIEW
# =============================
st.markdown("---")
st.header("🔒 Premium Features (Preview)")

col1, col2, col3 = st.columns(3)
col1.metric("AI CV Rewrite", "Locked 🔒")
col2.metric("Modern CV Design", "Locked 🔒")
col3.metric("Professional PDF", "Locked 🔒")

st.caption("Unlock professional-level CV rewriting and formatting.")

# =============================
# PAYPAL UNLOCK SECTION
# =============================
if not st.session_state.premium_unlocked:
    st.markdown("### Unlock Premium")
    st.write("✔ One-time upgrade\n✔ Professional CV\n✔ AI rewriting")

    st.link_button("Unlock with PayPal", PAYPAL_LINK)

    st.info(
        "After payment, return here and enter the same email used on PayPal. "
        "Premium access is enabled manually during early access."
    )

# =============================
# PREMIUM SECTION
# =============================
if st.session_state.premium_unlocked and cv_text and jd_text:
    st.markdown("---")
    st.header("👑 Premium CV Builder")

    score, matched = ats_score(cv_text, jd_text)
    rewritten_cv = ai_rewrite(cv_text, matched)

    st.subheader("AI-Rewritten CV")
    st.text_area("Optimized CV", rewritten_cv, height=300)

    try:
        pdf = premium_pdf(rewritten_cv)
        st.download_button(
            "Download Professional PDF",
            data=pdf.output(dest="S").encode("latin-1"),
            file_name="professional_cv.pdf",
            mime="application/pdf"
        )
    except Exception:
        st.error("Professional PDF generation failed due to unsupported characters.")

    st.success("Premium unlocked. Full access granted.")

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("Built to help candidates pass ATS filters and secure interviews.")
