# 태그 검색 구현 계획서

## 목표 (Goal)
누락된 "태그 검색" 기능(Phase 4/P2)을 구현하여 사용자가 게시물에 해시태그를 사용하고 검색할 수 있도록 합니다.

## 사용자 검토 필요
> [!NOTE]
> 이 기능은 `posts` 생성 로직을 수정하여 태그를 자동으로 추출하고 검색을 위한 새로운 API 엔드포인트를 추가하는 작업을 포함합니다.

## 변경 제안 사항

### 백엔드 (Backend)

#### [MODIFY] [app/routers/posts.py](file:///Users/yoonani/Works/workshop/Web_dev_ws/app/routers/posts.py)
- `create_post` 및 `update_post` 함수 업데이트.
- `content`에서 해시태그(예: `#tag`)를 추출하는 로직 추가.
- 태그를 `Tags` 테이블에 저장하고 `PostTags` 테이블에 연결.

#### [NEW] [app/routers/tags.py](file:///Users/yoonani/Works/workshop/Web_dev_ws/app/routers/tags.py)
- `GET /api/tags/{tag_name}` 엔드포인트 구현.
- 주어진 태그와 연관된 게시물 목록 반환.

#### [MODIFY] [app/main.py](file:///Users/yoonani/Works/workshop/Web_dev_ws/app/main.py)
- `tags.router` 등록.

### 프론트엔드 (Frontend)

#### [MODIFY] [static/js/app.js](file:///Users/yoonani/Works/workshop/Web_dev_ws/static/js/app.js)
- `searchPostsByTag(tagName)` 함수 추가.
- 태그 필터링을 처리하도록 `loadPosts` 업데이트.
- 게시물 내용의 해시태그를 클릭 가능하게 변경 (선택 사항이지만 권장됨).

#### [MODIFY] [templates/index.html](file:///Users/yoonani/Works/workshop/Web_dev_ws/templates/index.html)
- 헤더에 검색 입력 필드 추가.

## 검증 계획

### 자동화 테스트 (Automated Tests)
- 새로운 테스트 스크립트 `test_tags.py` 생성하여 다음 수행:
    1. "#test"가 포함된 게시물 생성.
    2. "test" 태그 검색.
    3. 결과에 게시물이 존재하는지 확인.

### 수동 검증 (Manual Verification)
1. 로그인 -> `#cat`으로 게시물 생성.
2. 검색창에 `cat` 입력 -> `#cat` 게시물만 표시되는지 확인.
