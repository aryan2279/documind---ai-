from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    pdf_id: str | None = None