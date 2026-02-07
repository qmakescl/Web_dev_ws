from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database import get_db_connection
from ..models import CommentCreate, CommentResponse, TokenData
from ..auth import get_current_user

router = APIRouter()

@router.post("/{post_id}/comments", response_model=CommentResponse)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: TokenData = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 게시물 존재 여부 확인
    cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    try:
        cursor.execute(
            "INSERT INTO comments (post_id, user_id, comment) VALUES (?, ?, ?)",
            (post_id, current_user.user_id, comment_data.comment)
        )
        comment_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
        new_comment = cursor.fetchone()
        conn.close()
        return dict(new_comment)
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{post_id}/comments", response_model=List[CommentResponse])
async def read_comments(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC", (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return [dict(c) for c in comments]
