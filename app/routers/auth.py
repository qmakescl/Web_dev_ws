from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db_connection
from ..models import UserCreate, UserResponse, Token
from ..auth import get_password_hash, verify_password, create_access_token
import sqlite3

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 이메일 중복 확인
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 이메일입니다"
        )
    
    # 비밀번호 해싱 및 사용자 저장
    hashed_password = get_password_hash(user.password)
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user.email, hashed_password)
        )
        user_id = cursor.lastrowid
        conn.commit()
        
        # 저장된 사용자 정보 가져오기
        cursor.execute("SELECT id, email, created_at FROM users WHERE id = ?", (user_id,))
        new_user = cursor.fetchone()
        conn.close()
        return dict(new_user)
    except Exception as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, email, password FROM users WHERE email = ?", (form_data.username,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 틀립니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWT 토큰 생성
    access_token = create_access_token(
        data={"sub": user["email"], "id": user["id"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}
