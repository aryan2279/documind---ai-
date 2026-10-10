from google import genai

from app.core.config import (
    GEMINI_API_KEY
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(
    question,
    context,
    history
):

    prompt = f"""
You are a helpful AI assistant.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Rules:
1. Answer using the provided context.
2. If answer is not present,
   say information not found.
3. Use conversation history
   for follow-up questions.
"""

    response = (
        client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    )

    return response.text