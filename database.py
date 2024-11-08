from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://root:Dev.3205@localhost:27017/")
db = client["drawsee_test"]

users_collection = db["users"]

def get_knowledge_points_collection(knowledge_base_id: str):
    collection_name = f"knowledge_points_{knowledge_base_id}"
    return db[collection_name]
