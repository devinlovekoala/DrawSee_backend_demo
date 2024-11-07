from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://root:Dev.3205@localhost:27017/")
db = client["knowledge_db"]
knowledge_points_collection = db["knowledge_points"]
chat_records_collection = db["chat_records"]
users_collection = db["users"]
