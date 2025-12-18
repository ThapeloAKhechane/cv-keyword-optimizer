from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from nlp import compare_cv_to_job

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None}
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze(
    request: Request,
    cv_text: str = Form(...),
    job_text: str = Form(...)
):
    result = compare_cv_to_job(cv_text, job_text)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
