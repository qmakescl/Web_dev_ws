# 데이터베이스 스키마 검토 보고서

## 1. 개요
본 문서는 제품 요구사항 문서(`instructions/prd.md`)에 정의된 데이터베이스 스키마와 실제 구현된 코드(`app/database.py`)를 비교 분석한 결과입니다.

## 2. 비교 요약
전반적으로 PRD의 설계가 충실하게 구현되었습니다. 테이블 목록과 컬럼 구성이 일치합니다.
단, **`post_tags` 테이블 구현에서 수정이 필요한 버그 1건**이 발견되었습니다.

| 테이블 | PRD 정의 | 구현 상태 | 일치 여부 |
|---|---|---|---|
| **Users** | id, email, password, created_at | `users` 테이블로 구현됨 | ✅ 일치 |
| **Posts** | id, user_id, img_path, content, created_at, updated_at | `posts` 테이블로 구현됨 | ✅ 일치 |
| **Comments** | id, post_id, user_id, comment, created_at | `comments` 테이블로 구현됨 | ✅ 일치 |
| **Likes** | id, post_id, user_id | `likes` 테이블로 구현됨 | ✅ 일치 |
| **Tags** | id, name | `tags` 테이블로 구현됨 | ✅ 일치 |
| **PostTags** | post_id, tag_id | `post_tags` 테이블로 구현됨 | ⚠️ **버그 발견** |

## 3. 상세 분석

### 3.1. 일치하는 부분 (Good)
*   **테이블 명명 규칙**: PRD의 CamelCase(`PostTags`)와 달리, 실제 구현은 Python/SQL 표준인 스네이크 케이스(`post_tags`)를 따르고 있어 적절합니다.
*   **데이터 타입**: SQLite 특성에 맞게 `TIMESTAMP`, `TEXT`, `INTEGER` 등이 적절히 사용되었습니다.
*   **제약 조건**: `NOT NULL`, `UNIQUE`, `DEFAULT CURRENT_TIMESTAMP` 등이 빠짐없이 적용되었습니다.

### 3.2. 발견된 문제점 (Critical)

`app/database.py` 파일의 `post_tags` 테이블 정의에서 **Foreign Key(외래키) 설정 오류**가 있습니다.

**현재 코드 (`app/database.py`:76):**
```sql
FOREIGN KEY (post_id) REFERENCES tags (id)
```
*   문제: `post_id` 컬럼이 `tags` 테이블의 `id`를 참조하도록 잘못 정의되었습니다. `tags` 테이블을 참조해야 하는 것은 `tag_id`입니다.

**수정 제안:**
```sql
FOREIGN KEY (tag_id) REFERENCES tags (id)
```

## 4. 조치 권고
`post_tags` 테이블은 아직 기능적으로 사용되고 있지 않지만(P2 기능), 추후 태그 검색 기능 구현 시 심각한 오류를 초래할 수 있으므로 **즉시 수정**하는 것이 좋습니다.

---
**작성일**: 2026-02-09
**검토자**: Google Antigravity
