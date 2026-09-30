import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

logger = logging.getLogger(__name__)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# -----------------------------
# Request Models
# -----------------------------

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


# -----------------------------
# Frontend
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# -----------------------------
# Q&A
# -----------------------------

@app.post("/qa")
async def qa(payload: QuestionRequest):

    try:
        answer = answer_question(
            payload.question
        )
    except Exception as error:
        logger.exception("Question answering failed")
        is_unavailable = (
            getattr(error, "code", None) == 503
            or "503 UNAVAILABLE" in str(error)
        )
        raise HTTPException(
            status_code=503 if is_unavailable else 502,
            detail=(
                "Gemini is temporarily unavailable. Please retry shortly."
                if is_unavailable
                else "Gemini could not generate an answer. Check API key, model access, and quota."
            )
        ) from error

    return {
        "answer": answer
    }


# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    explanation = explain_topic(
        payload.text
    )

    return {
        "explanation": explanation
    }


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(payload: TextRequest):

    quiz_data = generate_quiz(
        payload.text
    )

    return {
        "quiz": quiz_data
    }


# -----------------------------
# Summary
# -----------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    summary = summarize_text(
        payload.text
    )

    return {
        "summary": summary
    }


# -----------------------------
# Learning Recommendations
# -----------------------------

@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):

    recommendations = get_learning_recommendations(
        payload.text
    )

    return {
        "recommendations": recommendations
    }