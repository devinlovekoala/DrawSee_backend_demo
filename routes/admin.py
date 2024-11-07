from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta

from database import users_collection
from schemas import AdminLoginResponse, AdminLoginRequest
from service.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest):
    # 验证管理员身份
    user = await users_collection.find_one({"username": request.username})
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied: Not an admin user")

    # 验证密码
    if not await authenticate_user(request.username, request.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 创建访问令牌
    access_token = create_access_token(
        data={"sub": user["username"], "user_id": str(user["_id"])},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # 返回管理员的令牌和信息
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user["_id"]),
        "role": user["role"],
        "knowledge_base_ids": user["knowledge_base_ids"]
    }
