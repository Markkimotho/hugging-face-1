from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from transformers import pipeline

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

summarizer = pipeline(
    "summarization",
    MODEL_NAME,
    truncation=True
)

app = FastAPI()

# Mount static directory cleanly
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Tell FastAPI where to find templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/summarize", response_class=HTMLResponse)
async def summarize(request: Request, text: str = Form(...)):

    if len(text.strip()) < 10:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Text is too short to summarize.",
                "input_text": text
            }
        )

    try:
        summary = summarizer(
            text,
            max_length=120,
            min_length=30,
            truncation=True,
            do_sample=False
        )[0]["summary_text"]

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": summary,
                "input_text": text
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error: {str(e)}",
                "input_text": text
            }
        )
