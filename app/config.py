import os

SECRET_KEY = "insta-lite-secret-key-for-workshop"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DATABASE_URL = "data/insta.db"
UPLOAD_DIR = "static/uploads"

# 업로드 디렉토리가 없으면 생성
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
