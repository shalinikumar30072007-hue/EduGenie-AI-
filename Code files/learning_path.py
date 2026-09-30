from gemini_client import generate_text


def get_learning_recommendations(
    topic: str
) -> str:

    prompt = f"""
Create a structured learning path
for the following topic.

Topic:

{topic}

Create the learning path using:

1. Beginner Level
2. Intermediate Level
3. Advanced Level
4. Practice Activities
5. Suggested Resources

For each level:

- Explain what to learn.
- Give important subtopics.
- Give a simple suggested timeline.
- Explain what the learner should
  be able to do after completing
  that level.

Use simple English.

Do not invent specific URLs.
"""


    return generate_text(
        prompt
    )