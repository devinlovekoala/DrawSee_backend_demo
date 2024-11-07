import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import knowledge_points_collection, db
from schemas import KnowledgePoint
from service.auth import get_current_user, get_admin_user

router = APIRouter()

@router.post("/knowledge_points/")
async def create_knowledge_point(point: KnowledgePoint):
    point_data = point.dict(exclude={"_id"})
    result = await knowledge_points_collection.insert_one(point_data)
    return {"_id": str(result.inserted_id)}

@router.get("/knowledge_points/{point_id}")
async def get_knowledge_point(point_id: str):
    point = await knowledge_points_collection.find_one({"_id": ObjectId(point_id)})
    if not point:
        raise HTTPException(status_code=404, detail="Knowledge Point not found")
    return point

@router.put("/knowledge_points/{point_id}")
async def update_knowledge_point(point_id: str, point: KnowledgePoint):
    result = await knowledge_points_collection.update_one(
        {"_id": ObjectId(point_id)}, {"$set": point.dict(exclude={"_id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Knowledge Point not found")
    return {"status": "Knowledge Point updated"}

@router.delete("/knowledge_points/{point_id}")
async def delete_knowledge_point(point_id: str):
    result = await knowledge_points_collection.delete_one({"_id": ObjectId(point_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Knowledge Point not found")
    return {"status": "Knowledge Point deleted"}


@router.post("/create_knowledge_base")
async def create_knowledge_base(name: str, current_user: dict = Depends(get_admin_user)):
    # 生成知识库 ID 和集合名称
    knowledge_base_id = str(uuid.uuid4())
    collection_name = f"knowledge_points_{knowledge_base_id}"

    # 插入知识库元信息到 knowledge_bases 集合
    knowledge_base = {
        "_id": knowledge_base_id,
        "name": name,
        "creator_id": current_user["_id"],
        "created_at": datetime.utcnow()
    }
    await db["knowledge_bases"].insert_one(knowledge_base)

    # 更新用户的 knowledge_bases 列表
    await db["users"].update_one({"_id": current_user["_id"]}, {"$push": {"knowledge_bases": knowledge_base_id}})

    # 创建对应的知识库集合（可以选择插入初始数据）
    await db[collection_name].insert_one({
        "name": "root",  # 示例根节点
        "resource": [],
        "children": []
    })

    return {"knowledge_base_id": knowledge_base_id}

@router.get("/knowledge_bases/{knowledge_base_id}")
async def get_knowledge_base(knowledge_base_id: str, current_user: dict = Depends(get_current_user)):
    knowledge_base = await db["knowledge_bases.json"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    collection_name = f"knowledge_points_{knowledge_base_id}"
    points = await db[collection_name].find().to_list(100)
    return points

@router.post("/knowledge_bases/{knowledge_base_id}/add_point")
async def add_knowledge_point(knowledge_base_id: str, name: str, resources: list, current_user: dict = Depends(get_current_user)):
    knowledge_base = await db["knowledge_bases.json"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    collection_name = f"knowledge_points_{knowledge_base_id}"
    knowledge_point = {
        "name": name,
        "resource": resources,
        "children": []
    }
    result = await db[collection_name].insert_one(knowledge_point)
    return {"knowledge_point_id": str(result.inserted_id)}