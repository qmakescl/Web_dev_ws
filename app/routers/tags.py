from fastapi import APIRouter, HTTPException, status
from typing import List
from ..database import get_db_connection
from ..models import PostResponse

router = APIRouter()

@router.get("/{tag_name}", response_model=List[PostResponse])
async def search_posts_by_tag(tag_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 태그 ID 찾기
    cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
    tag = cursor.fetchone()
    
    if not tag:
        conn.close()
        return []

    # 태그와 연결된 게시물 찾기
    cursor.execute('''
        SELECT p.* 
        FROM posts p
        JOIN post_tags pt ON p.id = pt.post_id
        WHERE pt.tag_id = ?
        ORDER BY p.created_at DESC
    ''', (tag["id"],))
    
    posts = cursor.fetchall()
    conn.close()
    
    return [dict(post) for post in posts]
