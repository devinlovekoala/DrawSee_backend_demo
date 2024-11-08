from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any


class Resource(BaseModel):
    type: str
    value: str

class KnowledgePoint(BaseModel):
    _id: Optional[str]
    name: str
    resource: List[Resource]
    children: List[str]

class MatrixTransformation(BaseModel):
    matrix: str

# 数据模型
class ResponseModel(BaseModel):
    openid: str
    chat_id: str
    message: List[Dict[str, Any]]

class RequestModel(BaseModel):
    openid: str
    message: List[Dict[str, Any]]
    knowledge_base_id: str  # 新增字段，用于指定知识库

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str

class LoginRequest(BaseModel):
    username: str
    password: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class SuperAdminLoginRequest(BaseModel):
    username: str
    password: str

# class AdminLoginResponse(BaseModel):
#     access_token: str
#     token_type: str
#     user_id: str
#     role: str
#     knowledge_base_ids: list

class CreateAdminRequest(BaseModel):
    username: str
    password: str  # 应在实际生产环境中加密处理
    knowledge_base_ids: Optional[List[str]] = None

class CreateAdminResponse(BaseModel):
    message: str
    user_id: str
    username: str

class AgentCreate(BaseModel):
    name: str
    description: str
    knowledge_base_id: str

class AgentResponse(BaseModel):
    _id: str
    name: str
    description: str
    knowledge_base_id: str