from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from ..database import get_db_connection
from ..models import PostResponse, TokenData
from ..auth import get_current_user
from ..config import UPLOAD_DIR
import os
import uuid
import shutil
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(
    content: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user)
):
    # 파일 확장자 확인
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    # 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    img_path = f"/static/uploads/{file_name}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO posts (user_id, img_path, content) VALUES (?, ?, ?)",
            (current_user.user_id, img_path, content)
        )
        post_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        new_post = cursor.fetchone()
        conn.close()
        return dict(new_post)
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PostResponse])
async def read_posts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return [dict(post) for post in posts]

@router.get("/{post_id}", response_model=PostResponse)
async def read_post(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    if not post:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    return dict(post)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    content: Optional[str] = Form(None),
    current_user: TokenData = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 존재 여부 및 권한 확인
    cursor.execute("SELECT user_id FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    if not post:
        conn.close()
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    if post["user_id"] != current_user.user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    
    try:
        cursor.execute(
            "UPDATE posts SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (content, post_id)
        )
        conn.commit()
        
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        updated_post = cursor.fetchone()
        conn.close()
        return dict(updated_post)
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{post_id}")
async def delete_post(post_id: int, current_user: TokenData = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 존재 여부 및 권한 확인
    cursor.execute("SELECT user_id, img_path FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    if not post:
        conn.close()
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    if post["user_id"] != current_user.user_id:
        conn.close()
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    
    try:
        # DB에서 삭제
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()
        
        # 이미지 파일 삭제 (선택 사항이나 깔끔함을 위해)
        # img_file_path = post["img_path"].replace("/static/", "static/")
        # if os.path.exists(img_file_path):
        #     os.remove(img_file_path)
            
        return {"message": "게시물이 삭제되었습니다"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
