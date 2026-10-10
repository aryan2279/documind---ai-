from google import genai

from app.core.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_summary(text):

    prompt = f"""
Create a concise summary of this document.

Document:
{text}

Return:
- Overview
- Key Points
- Important Information
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text