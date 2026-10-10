import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from app.dependencies.auth import (
    get_current_user
)

from app.services.pdf_service import (
    extract_text_with_pages
)

from app.services.chunk_service import (
    create_chunks_with_pages
)

from app.services.embedding_service import (
    get_embedding
)

from app.db.chroma import (
    collection
)

from app.db.mongo import (
    pdf_collection
)

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Depends(
        get_current_user
    )
):

    if file.content_type != "application/pdf":

     raise HTTPException(
        status_code=400,
        detail="Only PDF files allowed"
    )

    pdf_id = str(uuid.uuid4())

    file_path = (
        f"{UPLOAD_DIR}/{pdf_id}.pdf"
    )

    with open(
        file_path,
        "wb"
    ) as f:

        content = await file.read()

        f.write(content)

    pages = extract_text_with_pages(
        file_path
    )

    if not pages:

     raise HTTPException(
        status_code=400,
        detail="No text found in PDF"
       )

    chunks = create_chunks_with_pages(
        pages
    )

    if not chunks:

     raise HTTPException(
        status_code=400,
        detail="No valid content found in PDF"
    )

    ids = []

    documents = []

    embeddings = []

    metadatas = []

    for index, chunk in enumerate(
        chunks
    ):

        ids.append(
            str(uuid.uuid4())
        )

        documents.append(
            chunk["text"]
        )

        embeddings.append(
            get_embedding(
                chunk["text"]
            )
        )

        metadatas.append(
            {
                "pdf_id": pdf_id,
                "user_id": user_id,
                "file_name": file.filename,
                "page": chunk["page"],
                "chunk_number": index
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    pdf_collection.insert_one(
        {
            "pdf_id": pdf_id,
            "user_id": user_id,
            "file_name": file.filename,
            "total_chunks": len(
                chunks
            )
        }
    )

    return {
        "message": "PDF Uploaded",
        "pdf_id": pdf_id,
        "chunks": len(chunks)
    }