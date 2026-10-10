from app.db.mongo import (
    chat_collection
)


def get_recent_history(
    user_id: str,
    limit: int = 5
):

    chats = list(
        chat_collection.find(
            {"user_id": user_id}
        )
        .sort("created_at", -1)
        .limit(limit)
    )

    chats.reverse()

    history = ""

    for chat in chats:

        history += (
            f"User: {chat['question']}\n"
        )

        history += (
            f"Assistant: {chat['answer']}\n\n"
        )

    return history