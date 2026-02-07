from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db_connection
from ..auth import get_current_user
from ..models import TokenData

router = APIRouter()

@router.post("/{post_id}/like")
async def toggle_like(post_id: int, current_user: TokenData = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 게시물 존재 여부 확인
    cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    # 이미 좋아요를 눌렀는지 확인
    cursor.execute(
        "SELECT id FROM likes WHERE post_id = ? AND user_id = ?",
        (post_id, current_user.user_id)
    )
    like = cursor.fetchone()
    
    try:
        if like:
            # 좋아요 취소
            cursor.execute("DELETE FROM likes WHERE id = ?", (like["id"],))
            message = "좋아요가 취소되었습니다"
        else:
            # 좋아요 추가
            cursor.execute(
                "INSERT INTO likes (post_id, user_id) VALUES (?, ?)",
                (post_id, current_user.user_id)
            )
            message = "좋아요를 눌렀습니다"
        
        conn.commit()
        conn.close()
        return {"message": message}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
