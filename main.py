import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from init_superadmin import create_superadmin
from routes import knowledge_points, chat_records, users, admin
from schemas import MatrixTransformation
from service.manim.elementary_trans import render_matrix_transformation
from service.manim.matrix_trans import matrix_trans

app = FastAPI()

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(knowledge_points.router, prefix="/api", tags=["Knowledge Points"])
app.include_router(chat_records.router, prefix="/api", tags=["Chat Records"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 动画iframe模板
templates = Jinja2Templates(directory=os.path.join(os.getcwd(), 'templates'))

# 注册启动事件
@app.on_event("startup")
async def on_startup():
    await create_superadmin()

# @app.get('/api/{knowledge}', response_class=HTMLResponse)
# async def index(request: Request, knowledge: str):
#     template_path = f"animation/{knowledge}.html"
#     return templates.TemplateResponse(template_path, {"request": request, "video_path": None})


@app.post("/elementary_trans")
async def process_matrix(data: MatrixTransformation):
    try:
        parsed_data = eval(data.matrix)
        matrix = parsed_data[0]
        swap_rows = parsed_data[1]
        multiply_row = parsed_data[2]
        row_addition = parsed_data[3]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"输入格式不正确: {str(e)}")

    try:
        video_path = render_matrix_transformation(matrix, swap_rows, multiply_row, row_addition)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"视频渲染失败: {str(e)}")

    return video_path

@app.post("/matrix_trans")
async def process_matrix(request: Request):
    try:
        # 获取JSON请求体中的 matrix 参数
        data = await request.json()
        matrix_str = data.get("matrix")  # 获取 matrix 参数
        print(matrix_str)

        if matrix_str:
            video_path_matrix = matrix_trans(matrix_str)
            relative_video_path_matrix = os.path.relpath(video_path_matrix, os.path.abspath('static'))
            relative_video_path_matrix = relative_video_path_matrix.replace('\\', '/')
            return {"video_path": relative_video_path_matrix}
        else:
            raise HTTPException(status_code=400, detail="参数 matrix 缺失")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"视频渲染失败: {str(e)}")




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
