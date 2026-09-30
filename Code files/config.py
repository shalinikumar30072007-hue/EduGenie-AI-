import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# --------------------------------
# Gemini Configuration
# --------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


# Use a current stable model for new projects.
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
).strip()

GEMINI_FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-2.5-flash-lite"
).strip()


# --------------------------------
# Optional Local Explanation Model
# --------------------------------

USE_LOCAL_EXPLAINER = os.getenv(
    "USE_LOCAL_EXPLAINER",
    "false"
).lower() == "true"


LOCAL_MODEL_NAME = os.getenv(
    "LOCAL_MODEL_NAME",
    "MBZUAI/LaMini-Flan-T5-783M"
).strip()


# --------------------------------
# Input Limit
# --------------------------------

MAX_INPUT_CHARS = int(
    os.getenv(
        "MAX_INPUT_CHARS",
        "30000"
    )
)