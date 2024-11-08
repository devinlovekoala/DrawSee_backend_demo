from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserResponse, Token, LoginRequest
from database import users_collection
from datetime import timedelta
from service.auth import get_password_hash, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user_data = {
        "username": user.username,
        "email": user.email,
        "password_hash": get_password_hash(user.password),
        "role": "user"
    }
    result = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": result.inserted_id})

    return {
        "user_id": str(new_user["_id"]),
        "username": new_user["username"],
        "email": new_user["email"],
        "role": new_user["role"]
    }

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    user = await authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["username"], "user_id": str(user["_id"])},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": access_token, "token_type": "bearer", "user_id": str(user["_id"])}
