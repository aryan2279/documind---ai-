from datetime import datetime

from fastapi import (
    APIRouter,
    Depends
)

from app.models.chat_model import (
    ChatRequest
)

from app.dependencies.auth import (
    get_current_user
)

from app.services.hybrid_search import (
    hybrid_search
)

from app.services.memory_service import (
    get_recent_history
)

from app.services.rag_service import (
    generate_answer
)

from app.db.mongo import (
    chat_collection
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    data: ChatRequest,
    user_id: str = Depends(
        get_current_user
    )
):

    results = hybrid_search(
        question=data.question,
        user_id=user_id,
        pdf_id=data.pdf_id
    )

    if not results:

        return {
            "answer":
            "No relevant content found."
        }

    context = "\n\n".join(
        [
            item["doc"]
            for item in results
        ]
    )

    history = get_recent_history(
        user_id
    )

    answer = generate_answer(
        data.question,
        context,
        history
    )

    citations = []

    for item in results:

        meta = item["meta"]

        citations.append(
            {
                "file_name":
                meta["file_name"],

                "page":
                meta["page"]
            }
        )

    chat_collection.insert_one(
        {
            "user_id": user_id,
            "question": data.question,
            "answer": answer,
            "created_at":
            datetime.utcnow()
        }
    )

    return {
        "answer": answer,
        "citations": citations
    }

@router.get("/history")
def get_history(
    user_id: str = Depends(
        get_current_user
    )
):

    chats = list(
        chat_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        )
        .sort("created_at", -1)
    )

    return chats