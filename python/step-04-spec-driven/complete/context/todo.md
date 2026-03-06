# 구현 계획

## 생성할 파일
1. `app/schemas.py` — Pydantic 스키마 (Priority enum, TodoCreate, TodoUpdate, TodoResponse, TodoListResponse)
2. `app/main.py` — FastAPI 라우터 (CRUD + 필터링 + 페이지네이션)
3. `tests/test_todos.py` — pytest 테스트

## 구현 순서
1. schemas.py에 타입 정의 (스펙 문서 → 코드 변환)
2. test_todos.py에 테스트 작성 (스펙 기반)
3. main.py에 엔드포인트 구현 (테스트 통과)

## 주의사항
- 인메모리 dict 저장소 사용 (DB 없음)
- Priority는 str Enum으로 정의
- 페이지네이션: page는 1부터 시작
- PATCH: model_dump(exclude_unset=True) 활용
