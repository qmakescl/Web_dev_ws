# Insta-Lite 프로젝트 할일 목록

## Phase 1: 프로젝트 설정 및 기본 구조 [x]
- [x] 필요 패키지 설치 (fastapi, uvicorn, bcrypt, python-multipart, python-jose)
- [x] 프로젝트 디렉토리 구조 생성
- [x] SQLite 데이터베이스 스키마 및 초기화 설정

## Phase 2: 백엔드 API 개발 (P0 - 필수 기능) [/]
- [ ] **F1. 인증 시스템** [x]
  - [x] Users 테이블 생성
  - [x] POST `/api/auth/register` - 회원가입
  - [x] POST `/api/auth/login` - 로그인 (JWT 토큰 발급)
  - [x] 인증 미들웨어 (JWT 검증)
- [ ] **F2. 게시글 CRUD** [x]
  - [x] Posts 테이블 생성
  - [x] 이미지 업로드 폴더 설정
  - [x] POST `/api/posts` - 게시물 작성 (이미지 업로드)
  - [x] GET `/api/posts` - 전체 게시물 조회
  - [x] GET `/api/posts/{id}` - 게시물 상세 조회
- [ ] **F4. 수정/삭제 권한 체크** [x]
  - [x] PUT `/api/posts/{id}` - 게시물 수정 (작성자 권한 검증)
  - [x] DELETE `/api/posts/{id}` - 게시물 삭제 (작성자 권한 검증)

## Phase 3: 백엔드 API 개발 (P1 - 보조 기능) [/]
- [ ] **F5. 좋아요 시스템** [x]
  - [x] Likes 테이블 생성
  - [x] POST `/api/posts/{id}/like` - 좋아요 토글
- [ ] **F5. 댓글 시스템** [x]
  - [x] Comments 테이블 생성
  - [x] POST `/api/posts/{id}/comments` - 댓글 작성
  - [x] GET 댓글 조회 (게시물 상세에 포함)

## Phase 4: 백엔드 API 개발 (P2 - 디테일 기능)
- [ ] **F6. 태그 검색**
  - [ ] Tags, PostTags 테이블 생성
  - [ ] 게시물 작성 시 태그 추출 및 저장
  - [ ] GET `/api/tags/{tag_name}` - 태그별 게시물 검색

## Phase 5: 프론트엔드 개발 [x]
- [x] 기본 HTML/CSS 구조 (공통 레이아웃)
- [x] 회원가입 페이지
- [x] 로그인 페이지
- [x] 메인 피드 페이지
- [x] 게시글 작성 폼 (모달 or 별도 페이지)
- [x] 게시글 상세 페이지
- [x] 좋아요/댓글 UI 연동

## Phase 6: 통합 및 검증 [x]
- [x] API-프론트엔드 연동 테스트
- [x] 인수 조건(DoD) 7개 항목 검증
- [x] 에러 핸들링 점검
