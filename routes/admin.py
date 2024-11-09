from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from database import users_collection
from schemas import AdminLoginRequest, CreateAdminResponse, CreateAdminRequest, Token, SuperAdminLoginRequest
from service.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_superadmin_user, get_password_hash

router = APIRouter()

# 管理员注册接口（仅限superadmin）
@router.post("/admin/register", response_model=CreateAdminResponse)
async def admin_register(request: CreateAdminRequest):
    # 检查是否已经存在相同用户名的用户
    existing_user = await users_collection.find_one({"username": request.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 创建新的管理员用户
    admin_user = {
        "username": request.username,
        "password_hash": get_password_hash(request.password),
        "role": "admin",
        "knowledge_base_ids": []
    }
    result = await users_collection.insert_one(admin_user)
    new_user = await users_collection.find_one({"_id": result.inserted_id})

    return {
        "message": "Admin user registered successfully",
        "user_id": str(new_user["_id"]),
        "username": new_user["username"]
    }

# 管理员登录接口
@router.post("/admin/login")
async def admin_login(request: AdminLoginRequest):
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["username"], "user_id": str(user["_id"])},
                                     expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # 添加 role 字段到返回数据中
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user["_id"]),
        "role": user["role"]
    }

# 验证 superadmin 身份的接口
@router.post("/superadmin-login", response_model=Token)
async def superadmin_login(request: SuperAdminLoginRequest):
    super_user = await authenticate_user(request.username, request.password)
    if not super_user or super_user["role"] != "superadmin":
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": super_user["username"], "user_id": str(super_user["_id"])},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer", "user_id": str(super_user["_id"])}

