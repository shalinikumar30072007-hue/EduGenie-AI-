from gemini_client import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
Summarize the following educational
passage.

Requirements:

1. Keep the important information.
2. Remove unnecessary repetition.
3. Use simple English.
4. Make it useful for revision.
5. Use headings and bullet points
   where appropriate.
6. Do not add information that is
   not present in the passage.

Educational Passage:

{text}
"""


    return generate_text(
        prompt
    )