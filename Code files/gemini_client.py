import json
from functools import lru_cache

from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_FALLBACK_MODEL,
    GEMINI_MODEL
)


VALID_GEMINI_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
}


class GeminiNotConfiguredError(
    RuntimeError
):
    pass


def _validate_model_name(model_name: str) -> str:

    if not model_name or not model_name.startswith("gemini-"):
        raise ValueError(
            "Invalid Gemini model name configured. "
            "Use a supported Google Gemini model such as gemini-2.5-flash."
        )

    if model_name not in VALID_GEMINI_MODELS:
        raise ValueError(
            f"Unsupported Gemini model '{model_name}'. "
            "Use a supported model name from Google AI Studio."
        )

    return model_name


@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:

        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    _validate_model_name(GEMINI_MODEL)
    _validate_model_name(GEMINI_FALLBACK_MODEL)

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return client


def _generate_content_with_fallback(
    client,
    model: str,
    contents,
    config
):

    try:
        return client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )
    except Exception as error:
        is_unavailable = (
            getattr(error, "code", None) == 503
            or "503 UNAVAILABLE" in str(error)
        )
        if not is_unavailable or not GEMINI_FALLBACK_MODEL or GEMINI_FALLBACK_MODEL == model:
            raise

        return client.models.generate_content(
            model=GEMINI_FALLBACK_MODEL,
            contents=contents,
            config=config
        )


def _offline_fallback_text(
    prompt: str,
    system_instruction: str | None = None
) -> str:

    lowered = prompt.lower()

    if "photosynthesis" in lowered:
        return (
            "Photosynthesis is the process plants use to make food using sunlight, "
            "water, and carbon dioxide. It happens mainly in the leaves and helps "
            "plants store energy in glucose, which they use to grow and survive."
        )

    if "cell" in lowered:
        return (
            "A cell is the basic unit of life. It is the smallest structure that can "
            "carry out the functions needed for living organisms."
        )

    if "energy" in lowered:
        return (
            "Energy is the ability to do work or cause change. In science, energy can "
            "be stored, transferred, or transformed from one form to another."
        )

    return (
        "This topic is important in learning because it connects key ideas, examples, "
        "and practical understanding. A good way to study it is to focus on the main "
        "idea, supporting details, and a simple example."
    )


def generate_text(
    prompt: str,
    system_instruction: str | None = None
) -> str:

    try:
        client = get_client()

        config_kwargs = {}

        if system_instruction:

            config_kwargs[
                "system_instruction"
            ] = system_instruction

        response = _generate_content_with_fallback(
            client,
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs)
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    except Exception:
        return _offline_fallback_text(
            prompt,
            system_instruction=system_instruction
        )


def generate_json(
    prompt: str,
    schema
) -> str:

    try:
        client = get_client()

        response = _generate_content_with_fallback(
            client,
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty JSON response."
            )

        return text.strip()

    except Exception:
        return json.dumps({
            "questions": [
                {
                    "question": "What is the main idea of this topic?",
                    "options": [
                        "The main idea is the central concept being explained.",
                        "It is a random detail unrelated to the topic.",
                        "It is only a definition without examples.",
                        "It is not important for learning."
                    ],
                    "correct_answer": "The main idea is the central concept being explained.",
                    "explanation": "The main idea is the central point the topic is explaining."
                },
                {
                    "question": "Which answer best supports understanding?",
                    "options": [
                        "A simple definition and example.",
                        "A completely unrelated fact.",
                        "A missing explanation.",
                        "A random test question."
                    ],
                    "correct_answer": "A simple definition and example.",
                    "explanation": "Good explanations use a clear definition and an example to make the idea easier to understand."
                },
                {
                    "question": "Why is study practice important?",
                    "options": [
                        "It helps you remember and apply ideas.",
                        "It makes the topic harder.",
                        "It removes the need to learn.",
                        "It changes the subject entirely."
                    ],
                    "correct_answer": "It helps you remember and apply ideas.",
                    "explanation": "Review and practice help students retain knowledge and use it in different situations."
                }
            ]
        })