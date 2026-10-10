from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.pdf import router as pdf_router
from app.api.pdf_summary import router as summary_router

app = FastAPI(
    title="ChatPDF RAG API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(pdf_router)
app.include_router(summary_router)


@app.get("/")
def home():

    return {
        "message": "ChatPDF RAG API Running"
    }