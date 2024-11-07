import os
import uuid
from datetime import datetime
from fastapi import UploadFile, File, HTTPException, Depends, APIRouter
from database import db
from main import PDF_DIR, WORD_DIR
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

    # 创建对应的聊天记录集合（初始化为空）
    await db[collection_name].insert_one({})  # 可根据需要插入初始数据或留空

    return {"chat_id": chat_id}
# 获取聊天记录
@router.get("/api/chat/{chat_id}", response_model=ResponseModel)
async def get_chat_history(chat_id: str, knowledge_base_id: str):
    # 动态定位知识库集合和聊天记录集合
    collection_name = f"chat_records_{chat_id}"
    chat_collection = db[collection_name]
    knowledge_collection = db[f"knowledge_points_{knowledge_base_id}"]

    chat_record = chat_collection.find_one({"chat_id": chat_id})
    if chat_record is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    # 处理资源
    message = chat_record['message']
    for msg in message:
        attachments = []
        knowledge_point = knowledge_collection.find_one({"_id": chat_id})
        if knowledge_point:
            for resource in knowledge_point['resource']:
                if resource['type'] in ['pdf', 'word']:
                    attachments.append({
                        "id": resource['value'],
                        "type": resource['type']
                    })
            msg["iframe"] = next((res['value'] for res in knowledge_point['resource'] if res['type'] == 'animation_iframe'), None)
            msg["bilibili_iframe"] = next((res['value'] for child in knowledge_point['children'] for res in child['resource'] if res['type'] == 'bilibili'), None)

    response = ResponseModel(
        openid=chat_record['openid'],
        chat_id=chat_record['chat_id'],
        message=message
    )
    return response


# 创建聊天记录
@router.post("/api/chat", response_model=ResponseModel)
async def create_chat(request: RequestModel):
    chat_id = str(uuid.uuid4())
    collection_name = f"chat_records_{chat_id}"
    chat_collection = db[collection_name]

    explanations = await process_user_question(request.message[-1]['content'])

    chat_record = {
        "chat_id": chat_id,
        "openid": request.openid,
        "message": explanations
    }
    chat_collection.insert_one(chat_record)

    return ResponseModel(openid=request.openid, chat_id=chat_id, message=explanations)


# 上传文档资源
@router.post("/api/document")
async def upload_document(knowledge_base_id: str, file: UploadFile = File(...)):
    document_uuid = str(uuid.uuid4())
    file_type = None

    if file.content_type == 'application/pdf':
        file_path = os.path.join(PDF_DIR, f"{document_uuid}.pdf")
        file_type = 'pdf'
    elif file.content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        file_path = os.path.join(WORD_DIR, f"{document_uuid}.docx")
        file_type = 'word'
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 将文档信息存入指定知识库
    collection_name = f"knowledge_points_{knowledge_base_id}"
    knowledge_collection = db[collection_name]
    resource = {
        "id": document_uuid,
        "type": file_type,
        "value": file_path
    }
    knowledge_collection.update_one({"_id": knowledge_base_id}, {"$push": {"resource": resource}})

    return {
        "id": document_uuid,
        "type": file_type,
        "message": f"{file.filename} uploaded successfully."
    }