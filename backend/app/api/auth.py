from fastapi import APIRouter
from fastapi import HTTPException

from app.models.auth_model import (
    SignupRequest,
    LoginRequest
)

from app.db.mongo import (
    users_collection
)

from app.utils.security import (
    hash_password,
    verify_password
)

from app.services.auth_service import (
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(data: SignupRequest):

    existing_user = users_collection.find_one(
        {
            "email": data.email
        }
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(
            data.password
        )
    }

    result = users_collection.insert_one(
        user
    )

    token = create_access_token(
        str(result.inserted_id)
    )

    return {
        "message": "Signup Successful",
        "token": token
    }


@router.post("/login")
def login(data: LoginRequest):

    user = users_collection.find_one(
        {
            "email": data.email
        }
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    valid_password = verify_password(
        data.password,
        user["password"]
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    token = create_access_token(
        str(user["_id"])
    )

    return {
        "message": "Login Successful",
        "token": token
    }