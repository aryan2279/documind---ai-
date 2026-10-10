from datetime import datetime, timedelta

from jose import jwt

from app.core.config import (
    JWT_SECRET,
    JWT_ALGORITHM
)


def create_access_token(user_id: str):

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token