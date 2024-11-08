# 服务器IP
import os

HOST = '42.193.107.127'

# 运行端口
PORT = 8000

APP_ID = "a9aed426-616b-4dbc-a8ea-0637d8b7db45"

APP_SECRET = "o7W3WejENgAv6FCR2zX5iOmCZbW8niCK"

BOT_ID = "a9aed426-616b-4dbc-a8ea-0637d8b7db45"


MONGO_PORT = "27017"
MONGO_CONFIG = {
    "url": "mongodb://root:Dev.3205@localhost:27017/",
    "knowledge_database": "test",
    "knowledge_collection": "knowledge_nodes",
}

# API链接
IFRAME_API = f'http://{HOST}:{PORT}/iframe'
STATIC_API = F'http://{HOST}:{PORT}/static'

MATHJAX_PATH = f'{STATIC_API}/js/mathjax/es5/tex-chtml.js'

SUPERPASS = "gjlw.3205"

UPLOAD_DIR = "./docs"
PDF_DIR = os.path.join(UPLOAD_DIR, "pdf")
WORD_DIR = os.path.join(UPLOAD_DIR, "word")

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(WORD_DIR, exist_ok=True)