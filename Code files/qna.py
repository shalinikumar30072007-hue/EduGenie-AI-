from gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie, an educational AI assistant.

Your job is to help students understand academic
and general educational topics.

Rules:

1. Give accurate answers.
2. Use simple English.
3. Avoid unnecessarily difficult words.
4. Explain clearly.
5. Use bullet points when useful.
6. Do not invent information.
7. Keep answers concise but useful.
"""


def answer_question(
    question: str
) -> str:

    prompt = f"""
Answer the student's question.

Student Question:

{question}

Give a clear educational answer
that is easy for a student to understand.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION
    )