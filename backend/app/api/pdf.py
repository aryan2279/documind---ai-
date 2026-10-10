from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth import (
    get_current_user
)

from app.db.mongo import (
    pdf_collection
)

from app.db.chroma import (
    collection
)

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Management"]
)


@router.get("/list")
def get_pdfs(
    user_id: str = Depends(
        get_current_user
    )
):

    pdfs = list(
        pdf_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        )
    )

    return pdfs


@router.delete("/{pdf_id}")
def delete_pdf(
    pdf_id: str,
    user_id: str = Depends(
        get_current_user
    )
):

    pdf_collection.delete_one(
        {
            "pdf_id": pdf_id,
            "user_id": user_id
        }
    )

    chroma_data = collection.get(
        where={"pdf_id": pdf_id}
    )

    ids = chroma_data["ids"]

    if ids:
        collection.delete(ids=ids)

    return {
        "message": "PDF Deleted"
    }