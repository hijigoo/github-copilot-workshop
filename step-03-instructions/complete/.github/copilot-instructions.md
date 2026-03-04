# GitHub Copilot 전역 지침

## 언어

- 모든 코드 주석, docstring, 커밋 메시지, 에러 메시지는 **한국어**로 작성합니다.

## 기술 스택

- **언어**: Python 3.11+
- **웹 프레임워크**: FastAPI
- **데이터 검증**: Pydantic v2
- **데이터베이스**: SQLite (SQLModel 사용 예정, 현재는 인메모리)
- **테스트**: pytest + FastAPI TestClient
- **패키지 관리**: pip + requirements.txt

## 코딩 스타일

- 변수명, 함수명: `snake_case`
- 클래스명: `PascalCase`
- 모든 함수에 **타입 힌트**를 사용합니다.
- docstring은 **Google 스타일**로 작성합니다.
- 한 함수는 하나의 역할만 수행합니다 (단일 책임 원칙).

## API 설계 원칙

- **RESTful** 컨벤션을 따릅니다.
- 모든 엔드포인트에 `response_model`을 명시합니다.
- 적절한 HTTP 상태 코드를 사용합니다 (201 생성, 204 삭제, 404 미존재).
- 에러 처리는 `HTTPException`을 사용하며, `detail`은 한국어로 작성합니다.
- 부분 수정은 `PATCH` 메서드를 사용합니다.
- 전체 수정은 `PUT` 메서드를 사용합니다.
