
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag import ask_question, compare_interviews


app = FastAPI(
    title="Hasamex AI Case Study API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class GuideRequest(BaseModel):
    question: str
    expert: str


@app.get("/")
def root():
    return {
        "message": "Hasamex AI Case Study API is running"
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        return ask_question(question)

    except Exception as error:
        print(f"Ask AI error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process the question."
        ) from error


@app.post("/guide")
def interview_guide(request: GuideRequest):
    question = request.question.strip()
    expert = request.expert.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if not expert:
        raise HTTPException(
            status_code=400,
            detail="Expert must be selected."
        )

    try:
        return ask_question(
            question=question,
            expert=expert
        )

    except Exception as error:
        print(f"Interview Guide error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process the interview guide question."
        ) from error


@app.post("/compare")
def cross_interview_analysis():
    try:
        return compare_interviews()

    except Exception as error:
        print(f"Cross-Interview Analysis error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Failed to compare the interviews."
        ) from error