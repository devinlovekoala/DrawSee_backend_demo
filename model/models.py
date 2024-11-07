from pymongo import MongoClient

class KnowledgePoint:
    def __init__(self, _id, name, resource, children):
        self._id = _id
        self.name = name
        self.resource = resource
        self.children = children

class ChatRecord:
    def __init__(self, chat_id, openid, message):
        self.chat_id = chat_id
        self.openid = openid
        self.message = message

client = MongoClient('mongodb://root:Dev.3205@localhost:27017/')
db = client['knowledge_db']  # 数据库名称
knowledge_points_collection = db['knowledge_points']  # 知识点集合
chat_records_collection = db['chat_records']