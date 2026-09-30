from gemini_client import generate_text

from config import (
    USE_LOCAL_EXPLAINER,
    LOCAL_MODEL_NAME
)


_local_pipeline = None


def _local_explain(
    topic: str
) -> str:

    global _local_pipeline

    try:

        from transformers import pipeline

    except ImportError as exc:

        raise RuntimeError(
            "Transformers is not installed."
        ) from exc


    if _local_pipeline is None:

        _local_pipeline = pipeline(

            "text2text-generation",

            model=LOCAL_MODEL_NAME
        )


    prompt = f"""
Explain the following topic to a beginner
using very simple English.

Topic:

{topic}

Give:

1. Definition
2. Main idea
3. Important points
4. Simple example
"""


    result = _local_pipeline(

        prompt,

        max_new_tokens=200,

        do_sample=False
    )


    return result[0][
        "generated_text"
    ].strip()


def explain_topic(
    topic: str
) -> str:

    # Try the local LaMini model
    # when enabled.

    if USE_LOCAL_EXPLAINER:

        try:

            return _local_explain(
                topic
            )

        except Exception:

            # Fall back to Gemini
            # if local model fails.

            pass


    prompt = f"""
Explain this educational topic
for a beginner.

Topic:

{topic}

Use the following structure:

1. Simple Definition
2. Main Idea
3. Important Points
4. Simple Example

Use easy English.
Avoid unnecessary technical words.
"""


    return generate_text(
        prompt
    )