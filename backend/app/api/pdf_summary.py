from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.db.chroma import collection
from app.services.summary_service import generate_summary

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Summary"]
)


@router.get("/{pdf_id}/summary")
def get_summary(
    pdf_id: str,
    user_id: str = Depends(get_current_user)
):

    data = collection.get(
        where={"pdf_id": pdf_id},
        include=["documents"]
    )

    documents = data["documents"]

    if not documents:
        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    text = "\n".join(documents[:20])

    summary = generate_summary(text)

    return {
        "summary": summary
    }