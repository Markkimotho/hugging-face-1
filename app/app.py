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
    
    # Helper function to check summary quality
    def poor_quality(summary: str) -> bool:
        if len(summary.split()) < 10:
            return True
        if "the text" in summary.lower():
            return True
        return False

    # Add a guiding prefix to the text input to help model summarize better
    prompt_text = (
        "Summarize the following text into a concise, clear, and meaningful summary:\n\n" 
        + text
    )
    
    try:
        # First summarization attempt
        summary = summarizer(
            prompt_text,
            max_length=130,
            min_length=40,
            truncation=True,
            do_sample=False
        )[0]["summary_text"]

        # If summary is poor quality, retry once with a stronger prompt
        if poor_quality(summary):
            stronger_prompt = (
                "You are an expert summarization engine. "
                "Please produce a high-quality, insightful summary focusing on key points only:\n\n"
                + text
            )
            summary = summarizer(
                stronger_prompt,
                max_length=150,
                min_length=50,
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
