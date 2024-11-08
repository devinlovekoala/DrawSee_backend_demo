import os
import uuid
from datetime import datetime
from fastapi import UploadFile, File, HTTPException, Depends, APIRouter

from config.config import PDF_DIR, WORD_DIR
from database import db
from schemas import ResponseModel, RequestModel
from service.LLM import process_user_question
from service.auth import get_current_user

router = APIRouter()

@router.post("/start_chat")
async def start_chat(openid: str, current_user: dict = Depends(get_current_user)):
    # 生成聊天 ID 和集合名称
    chat_id = str(uuid.uuid4())
    collection_name = f"chat_records_{chat_id}"

    # 插入聊天记录元信息
    chat_meta = {
        "_id": chat_id,
        "user_id": current_user["_id"],
        "openid": openid,
        "created_at": datetime.utcnow()
    }
    await db["chat_records_meta"].insert_one(chat_meta)

    # 初始化聊天记录集合为空
    await db[collection_name].insert_one({"chat_id": chat_id, "message": []})
    return {"chat_id": chat_id}

@router.get("/api/chat/{chat_id}", response_model=ResponseModel)
async def get_chat_history(chat_id: str, knowledge_base_id: str, current_user: dict = Depends(get_current_user)):
    # 获取聊天集合和知识库集合名称
    chat_collection_name = f"chat_records_{chat_id}"
    knowledge_collection_name = f"knowledge_points_{knowledge_base_id}"

    # 验证用户权限
    chat_meta = await db["chat_records_meta"].find_one({"_id": chat_id})
    if not chat_meta or chat_meta["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # 获取聊天记录和知识库资源
    chat_record = await db[chat_collection_name].find_one({"chat_id": chat_id})
    knowledge_point = await db[knowledge_collection_name].find_one({"_id": knowledge_base_id})

    if not chat_record:
        raise HTTPException(status_code=404, detail="Chat not found")

    # 处理消息和资源
    message = chat_record.get("message", [])
    for msg in message:
        attachments = []
        if knowledge_point:
            for resource in knowledge_point.get('resource', []):
                if resource['type'] in ['pdf', 'word']:
                    attachments.append({
                        "id": resource['value'],
                        "type": resource['type']
                    })
            msg["iframe"] = next((res['value'] for res in knowledge_point.get('resource', []) if res['type'] == 'animation_iframe'), None)
            msg["bilibili_iframe"] = next((res['value'] for child in knowledge_point.get('children', []) for res in child.get('resource', []) if res['type'] == 'bilibili'), None)

    return ResponseModel(openid=chat_record['openid'], chat_id=chat_record['chat_id'], message=message)

@router.post("/api/chat", response_model=ResponseModel)
async def create_chat(request: RequestModel):
    chat_id = str(uuid.uuid4())
    collection_name = f"chat_records_{chat_id}"

    # 获取问题的解释
    explanations = await process_user_question(request.message[-1]['content'])

    # 记录聊天内容
    chat_record = {
        "chat_id": chat_id,
        "openid": request.openid,
        "message": explanations
    }
    await db[collection_name].insert_one(chat_record)

    return ResponseModel(openid=request.openid, chat_id=chat_id, message=explanations)

@router.post("/api/document")
async def upload_document(knowledge_base_id: str, file: UploadFile = File(...)):
    # 创建文档 ID 并确定文件类型
    document_uuid = str(uuid.uuid4())
    file_type = None

    # 检查并保存文件类型
    if file.content_type == 'application/pdf':
        file_path = os.path.join(PDF_DIR, f"{document_uuid}.pdf")
        file_type = 'pdf'
    elif file.content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        file_path = os.path.join(WORD_DIR, f"{document_uuid}.docx")
        file_type = 'word'
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 保存文件
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 将文档信息存入对应知识库
    collection_name = f"knowledge_points_{knowledge_base_id}"
    resource = {
        "id": document_uuid,
        "type": file_type,
        "value": file_path
    }
    await db[collection_name].update_one({"_id": knowledge_base_id}, {"$push": {"resource": resource}})

    return {
        "id": document_uuid,
        "type": file_type,
        "message": f"{file.filename} uploaded successfully."
    }