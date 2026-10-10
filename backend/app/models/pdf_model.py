from pydantic import BaseModel


class PDFResponse(BaseModel):
    pdf_id: str
    file_name: str
    total_chunks: int