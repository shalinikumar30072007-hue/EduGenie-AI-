import json

from typing import List

from pydantic import (
    BaseModel,
    Field
)

from gemini_client import generate_json


# --------------------------------
# Quiz Question Model
# --------------------------------

class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str


# --------------------------------
# Quiz Response Model
# --------------------------------

class QuizResponse(BaseModel):

    questions: List[
        QuizQuestion
    ] = Field(
        min_length=3,
        max_length=3
    )


# --------------------------------
# Remove Markdown JSON
# --------------------------------

def clean_json_block(
    text: str
) -> str:

    text = text.strip()


    if text.startswith("```"):

        lines = text.splitlines()


        if lines:

            if lines[0].startswith("```"):

                lines = lines[1:]


        if lines:

            if lines[-1].strip() == "```":

                lines = lines[:-1]


        text = "\n".join(
            lines
        ).strip()


        if text.lower().startswith(
            "json"
        ):

            text = text[4:].lstrip()


    return text


# --------------------------------
# Generate Quiz
# --------------------------------

def generate_quiz(
    source_text: str
) -> dict:

    prompt = f"""
Create exactly 3 multiple-choice
questions from the educational text below.

Rules:

1. Create exactly 3 questions.
2. Each question must have exactly 4 options.
3. Only one option must be correct.
4. correct_answer must exactly match
   one of the four options.
5. Give a short explanation.
6. Questions must be based only on
   the supplied text.
7. Return valid JSON matching
   the requested schema.

Educational Text:

{source_text}
"""


    raw = generate_json(
        prompt,
        QuizResponse
    )


    cleaned = clean_json_block(
        raw
    )


    try:

        quiz = QuizResponse.model_validate_json(
            cleaned
        )

    except Exception:

        quiz = QuizResponse.model_validate(
            json.loads(cleaned)
        )


    return quiz.model_dump()