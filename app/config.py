import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = "insta-lite-secret-key-for-workshop"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 데이터베이스 경로 설정 (절대 경로 사용)
DATABASE_PATH = os.path.join(ROOT_DIR, "data", "insta.db")
DATABASE_URL = str(DATABASE_PATH)

UPLOAD_DIR = os.path.join(ROOT_DIR, "static", "uploads")

# 디렉토리가 없으면 생성
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
