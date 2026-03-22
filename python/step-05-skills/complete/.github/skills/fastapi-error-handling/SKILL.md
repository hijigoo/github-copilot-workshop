---
name: fastapi-error-handling
description: 'FastAPI 애플리케이션의 에러 처리 및 예외 관리 모범 사례'
---

# FastAPI 에러 처리 모범 사례

목표는 FastAPI 애플리케이션에서 일관되고 사용자 친화적인 에러 응답을 제공하는 것입니다.

## 커스텀 예외 클래스

- 도메인별 커스텀 예외를 정의합니다. (예: `TodoNotFoundError`, `DuplicateTodoError`)
- 기본 예외 클래스를 만들어 공통 속성을 관리합니다.
- 예외에는 항상 사용자 친화적인 한국어 메시지를 포함합니다.

```python
class AppException(Exception):
    """애플리케이션 기본 예외 클래스"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class TodoNotFoundError(AppException):
    """TODO 항목을 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, todo_id: int):
        super().__init__(
            message=f"TODO(id={todo_id})를 찾을 수 없습니다",
            status_code=404
        )
```

## 에러 응답 스키마

- 모든 에러 응답은 통일된 JSON 구조를 따릅니다:
  ```json
  {
    "detail": "에러 메시지",
    "error_code": "NOT_FOUND",
    "timestamp": "2024-01-01T00:00:00Z"
  }
  ```
- Pydantic `BaseModel`로 에러 응답 스키마를 정의합니다.
- `response_model`과 `responses`를 엔드포인트에 명시합니다.

## 예외 핸들러 등록

- `@app.exception_handler()`로 커스텀 예외를 처리합니다.
- 전역 예외 핸들러로 예상치 못한 에러를 잡습니다.
- 에러 로깅을 포함합니다.

```python
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "error_code": exc.error_code}
    )
```

## HTTP 상태 코드 규칙

- `400 Bad Request`: 잘못된 입력 데이터
- `404 Not Found`: 리소스를 찾을 수 없음
- `409 Conflict`: 중복 리소스 생성 시도
- `422 Unprocessable Entity`: 유효성 검증 실패 (FastAPI 기본)
- `500 Internal Server Error`: 예상치 못한 서버 에러

## 유효성 검증 에러

- Pydantic `ValidationError`는 FastAPI가 자동으로 422로 변환합니다.
- 추가 비즈니스 규칙 검증은 커스텀 예외로 처리합니다.
- 검증 에러 메시지는 한국어로 작성합니다.

## 에러 처리 안티패턴

- ❌ 빈 `except:` 블록 사용 금지
- ❌ 에러를 삼키지 않기 (조용히 무시하지 않기)
- ❌ 500 에러에 내부 구현 세부사항 노출 금지
- ❌ `HTTPException`을 직접 raise하는 대신 커스텀 예외 사용
- ✅ 항상 적절한 로깅과 함께 에러를 처리
