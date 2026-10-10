from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.core.config import (
    JWT_SECRET,
    JWT_ALGORITHM
)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    try:

        token = credentials.credentials

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        return payload["user_id"]

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )