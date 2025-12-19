from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from datetime import datetime

from nlp import compare_cv_to_job

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "message": None
        }
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze(
    request: Request,
    cv_text: str = Form(...),
    job_text: str = Form(...),
    email: str = Form(None)
):
    # Run NLP comparison (CV and Job text are NOT stored)
    result = compare_cv_to_job(cv_text, job_text)

    # Optional: save email safely (ONLY email, no CV data)
    if email:
        with open("leads.csv", "a", encoding="utf-8") as f:
            f.write(f"{email},{datetime.now()}\n")

        message = "✅ Thanks! Your email was recorded. We may send helpful CV tips."
    else:
        message = None

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "message": message
        }
    )


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return HTMLResponse(
        """
        <h2>About This Tool</h2>
        <p>
        This free AI-powered CV Keyword Optimizer was built using Python and NLP
        to help job seekers improve CV relevance and ATS compatibility.
        </p>

        <p>
        🔒 We do NOT store CV or job description content.<br>
        📧 Emails (if provided) are used only to send helpful resources.<br>
        💻 Source code is openly available on GitHub.
        </p>

        <p>
        <a href="https://github.com/ThapeloAKhechane/cv-keyword-optimizer" target="_blank">
        View GitHub Repository
        </a>
        </p>

        <p><b>Disclaimer:</b> This tool assists with keyword optimization only.
        It does not guarantee job placement.</p>
        """
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
