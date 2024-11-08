from config.config import SUPERPASS
from database import users_collection
from passlib.context import CryptContext

# 使用 passlib 进行密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_superadmin():
    # 检查是否已经存在 superadmin 用户
    existing_superadmin = await users_collection.find_one({"role": "superadmin"})
    if existing_superadmin:
        print("Superadmin already exists.")
        return

    superadmin_user = {
        "username": "superadmin",
        "password_hash": pwd_context.hash(SUPERPASS),
        "role": "superadmin",
        "knowledge_base_ids": []
    }
    await users_collection.insert_one(superadmin_user)
    print("Superadmin user created successfully.")