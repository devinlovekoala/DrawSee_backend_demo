import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import db
from schemas import KnowledgePoint
from service.auth import get_current_user, get_admin_user

router = APIRouter()

@router.post("/knowledge_bases/{knowledge_base_id}/points")
async def create_knowledge_point(knowledge_base_id: str, point: KnowledgePoint, current_user: dict = Depends(get_current_user)):
    # 检查用户是否有权限访问该知识库
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # 确定该知识库的知识点集合名
    collection_name = f"knowledge_points_{knowledge_base_id}"
    point_data = point.dict(exclude={"_id"})

    # 插入新的知识点
    result = await db[collection_name].insert_one(point_data)
    return {"_id": str(result.inserted_id)}

@router.get("/knowledge_bases/{knowledge_base_id}/points/{point_id}")
async def get_knowledge_point(knowledge_base_id: str, point_id: str, current_user: dict = Depends(get_current_user)):
    # 检查用户是否有权限访问该知识库
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # 获取知识点集合名并查找指定知识点
    collection_name = f"knowledge_points_{knowledge_base_id}"
    point = await db[collection_name].find_one({"_id": ObjectId(point_id)})
    if not point:
        raise HTTPException(status_code=404, detail="Knowledge Point not found")
    return point

@router.put("/knowledge_bases/{knowledge_base_id}/points/{point_id}")
async def update_knowledge_point(knowledge_base_id: str, point_id: str, point: KnowledgePoint, current_user: dict = Depends(get_current_user)):
    # 检查用户是否有权限访问该知识库
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # 更新知识点信息
    collection_name = f"knowledge_points_{knowledge_base_id}"
    result = await db[collection_name].update_one(
        {"_id": ObjectId(point_id)}, {"$set": point.dict(exclude={"_id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Knowledge Point not found")
    return {"status": "Knowledge Point updated"}

@router.delete("/knowledge_bases/{knowledge_base_id}/points/{point_id}")
async def delete_knowledge_point(knowledge_base_id: str, point_id: str, current_user: dict = Depends(get_current_user)):
    # 检查用户是否有权限访问该知识库
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # 删除指定知识点
    collection_name = f"knowledge_points_{knowledge_base_id}"
    result = await db[collection_name].delete_one({"_id": ObjectId(point_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Knowledge Point not found")
    return {"status": "Knowledge Point deleted"}


@router.post("/create_knowledge_base")
async def create_knowledge_base(name: str, description: str = "", current_user: dict = Depends(get_admin_user)):
    knowledge_base_id = str(uuid.uuid4())
    collection_name = f"knowledge_points_{knowledge_base_id}"

    knowledge_base = {
        "_id": knowledge_base_id,
        "name": name,
        "description": description,
        "creator_id": current_user["_id"],
        "created_at": datetime.utcnow()
    }
    await db["knowledge_bases"].insert_one(knowledge_base)

    await db["users"].update_one({"_id": current_user["_id"]}, {"$push": {"knowledge_bases": knowledge_base_id}})

    await db[collection_name].insert_one({
        "name": "root",
        "resource": [],
        "children": []
    })
    return {"knowledge_base_id": knowledge_base_id}


@router.get("/knowledge_bases")
async def list_knowledge_bases(current_user: dict = Depends(get_current_user)):
    knowledge_bases = await db["knowledge_bases"].find({"creator_id": current_user["_id"]}).to_list(100)
    return knowledge_bases


@router.get("/knowledge_bases/{knowledge_base_id}")
async def get_knowledge_base(knowledge_base_id: str, current_user: dict = Depends(get_current_user)):
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    collection_name = f"knowledge_points_{knowledge_base_id}"
    points = await db[collection_name].find().to_list(100)
    return {"knowledge_base": knowledge_base, "points": points}


@router.put("/knowledge_bases/{knowledge_base_id}")
async def update_knowledge_base(knowledge_base_id: str, name: str, description: str,
                                current_user: dict = Depends(get_current_user)):
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    await db["knowledge_bases"].update_one(
        {"_id": knowledge_base_id},
        {"$set": {"name": name, "description": description}}
    )
    return {"message": "Knowledge base updated successfully"}


@router.delete("/knowledge_bases/{knowledge_base_id}")
async def delete_knowledge_base(knowledge_base_id: str, current_user: dict = Depends(get_current_user)):
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    collection_name = f"knowledge_points_{knowledge_base_id}"
    await db["knowledge_bases"].delete_one({"_id": knowledge_base_id})
    await db[collection_name].drop()

    await db["users"].update_one({"_id": current_user["_id"]}, {"$pull": {"knowledge_bases": knowledge_base_id}})
    return {"message": "Knowledge base deleted successfully"}


@router.post("/knowledge_bases/{knowledge_base_id}/add_point")
async def add_knowledge_point(knowledge_base_id: str, name: str, resources: list, current_user: dict = Depends(get_current_user)):
    # 检查用户是否有权限访问该知识库
    knowledge_base = await db["knowledge_bases"].find_one({"_id": knowledge_base_id})
    if not knowledge_base or knowledge_base["creator_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    # 确定该知识库的知识点集合名
    collection_name = f"knowledge_points_{knowledge_base_id}"
    knowledge_point = {
        "name": name,
        "resource": resources,
        "children": []
    }
    # 插入新的知识点
    result = await db[collection_name].insert_one(knowledge_point)
    return {"knowledge_point_id": str(result.inserted_id)}