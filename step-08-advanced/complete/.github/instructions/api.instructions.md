---
applyTo: "app/**"
---

# API 코드 작성 지침

## 엔드포인트 규칙

- 모든 엔드포인트에 `response_model`을 명시합니다.
- 생성 엔드포인트는 `status_code=201`을 설정합니다.
- 삭제 엔드포인트는 `status_code=204`를 설정합니다.
- 부분 수정은 `PATCH` 메서드를 사용하고, `model_dump(exclude_unset=True)`로 전달된 필드만 업데이트합니다.
- 전체 수정은 `PUT` 메서드를 사용합니다.

## 데이터베이스 규칙

- 모든 엔드포인트에서 `session: Session = Depends(get_session)`을 사용합니다.
- ORM 모델(`models.py`)과 API 스키마(`schemas.py`)를 분리합니다.
- `session.add()`, `session.commit()`, `session.refresh()` 패턴을 따릅니다.
- 조회 시 `select()` 문과 `session.exec()`를 사용합니다.

## 에러 처리

- 리소스를 찾을 수 없을 때 `HTTPException(status_code=404)`를 발생시킵니다.
- `detail` 메시지는 **한국어**로 작성합니다.
- 예시: `"TODO를 찾을 수 없습니다"`

## 모델 규칙

- Pydantic v2의 `BaseModel`을 API 스키마에 사용합니다.
- SQLModel의 `SQLModel`을 데이터베이스 모델에 사용합니다.
- 선택적 필드는 `Optional[타입] = None`으로 선언합니다.
- 응답 모델에는 `id`, `created_at` 등 서버 생성 필드를 포함합니다.

## Docstring

- 모든 함수에 **Google 스타일** docstring을 한국어로 작성합니다.
- `Args`, `Returns`, `Raises` 섹션을 적절히 포함합니다.
- 예시:
  ```python
  def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
      """새로운 TODO 항목을 생성합니다.

      Args:
          todo: 생성할 TODO의 제목과 설명을 담은 요청 데이터.
          session: SQLModel 데이터베이스 세션 (의존성 주입).

      Returns:
          TodoResponse: 생성된 TODO 항목의 전체 정보.
      """
  ```
