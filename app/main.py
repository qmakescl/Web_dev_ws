from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import init_db
from .routers import auth, posts, likes, comments

app = FastAPI(title="Insta-Lite API")

# 데이터베이스 초기화
init_db()

# 정적 파일 서버 설정 (이미지 업로드 등)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(likes.router, prefix="/api/posts", tags=["likes"])
app.include_router(comments.router, prefix="/api/posts", tags=["comments"])

# HTML 페이지 라우트
@app.get("/")
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/posts/{post_id}")
async def post_detail_page(request: Request, post_id: int):
    return templates.TemplateResponse("post_detail.html", {"request": request, "post_id": post_id})
