# Step 4. Spec-Driven Development (SDD)

> ⏱️ 25분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: 타입 정의 → 테스트 → 구현 패턴**
>
> **체감: "스펙을 먼저 쓰니 AI가 놀랍도록 정확하다!"**

---

## 이전 단계 코드

`starter/` = Step 3 완성 코드 (copilot-instructions.md + 경로 지정 지침 설정)

### 의존성 설치

```bash
pip install -r requirements.txt
```

> 💡 이전 단계에서 이미 설치했다면 건너뛰어도 됩니다.

---

## 왜 네 번째인가?

Instructions로 **스타일**을 잡았다면, SDD로 **정확도**를 극대화합니다.

기존 접근: "TODO 앱에 우선순위 기능 추가해줘" → Copilot이 추측하며 구현
SDD 접근: **타입 스펙 정의 → 테스트 작성 → 구현 위임** → Copilot이 정확히 구현

---

## SDD (Spec-Driven Development)란?

```
1. SPEC  — 타입/인터페이스 정의 (무엇이 필요한가?)
2. TEST  — 스펙 기반 테스트 작성 (어떻게 검증하나?)
3. IMPL  — Copilot에게 구현 위임 (테스트를 통과시켜줘!)
4. VERIFY — 테스트 실행 (정말 통과하나?)
```

### SDD와 TDD의 관계

| | TDD | SDD |
|---|---|---|
| 순서 | **테스트** → 구현 | **타입/스펙** → 테스트 → 구현 |
| 첫 산출물 | 실패하는 테스트 | 타입 정의 (schemas.py) |
| AI 활용 | 테스트를 보고 구현 생성 | 스펙 + 테스트를 보고 구현 생성 |

SDD는 TDD를 **포함**합니다. 차이는 **시작점**입니다:
- TDD: 테스트 먼저 → 구현
- SDD: **스펙 먼저** → 스펙 기반 테스트 → 구현 → 테스트 검증

스펙(타입)이 있으면 AI가 "무엇을 만들어야 하는지" 더 정확히 파악하므로,
Copilot과 함께 쓸 때 SDD가 특히 효과적입니다.

---

## 태스크 1: 스펙(타입) 먼저 정의 (7분)

`app/schemas.py` 파일을 생성합니다.

> ⚠️ **구현은 하지 마세요!** 타입만 정의합니다.

```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    """TODO 우선순위"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoCreate(BaseModel):
    """TODO 생성 요청 스펙"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: Priority = Priority.MEDIUM


class TodoResponse(BaseModel):
    """TODO 응답 스펙"""
    id: int
    title: str
    description: str | None
    priority: Priority
    completed: bool
    created_at: datetime
    updated_at: datetime | None


class TodoUpdate(BaseModel):
    """TODO 수정 요청 스펙 (부분 업데이트)"""
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: Priority | None = None
    completed: bool | None = None


class TodoListResponse(BaseModel):
    """TODO 목록 응답 스펙 (페이지네이션 포함)"""
    items: list[TodoResponse]
    total: int
    page: int
    size: int
```

### 관찰 포인트

- `Field(..., min_length=1)` → 빈 제목 방지
- `Priority` enum → 우선순위 제한
- `TodoListResponse` → 페이지네이션 구조
- 이 타입들이 "계약서" 역할을 합니다

---

## 태스크 2: 스펙 기반 테스트 작성 (8분)

Copilot Chat에서:

```
#file:app/schemas.py 이 스펙을 기반으로 tests/test_todos.py에 테스트를 작성해줘.

아직 구현은 없으니 테스트만 작성해줘. 다음 케이스를 반드시 포함:
- 정상 생성 (201 + 응답 검증)
- 빈 제목으로 생성 시 422 에러
- 우선순위별 필터링 (GET /todos?priority=high)
- 페이지네이션 동작 (GET /todos?page=1&size=5)
- 존재하지 않는 TODO 조회 시 404
```

### 기대하는 테스트 구조

```python
def test_할일_생성_유효한_데이터_201_반환():
    # Given: 유효한 TODO 데이터
    # When: POST /todos 호출
    # Then: 201 응답 + 생성된 TODO 반환

def test_할일_생성_빈_제목_422_에러():
    # Given: 제목이 빈 문자열
    # When: POST /todos 호출
    # Then: 422 유효성 검사 에러

def test_할일_목록_우선순위_필터링():
    # Given: 다양한 우선순위의 TODO들
    # When: GET /todos?priority=high
    # Then: high 우선순위만 반환
```

---

## 태스크 3: Copilot에게 구현 위임 (7분)

> ⚠️ **주의: `app/main.py`를 통째로 다시 작성합니다!**
>
> 이 단계에서는 기존 `app/main.py`의 내용을 **새로운 스펙(`schemas.py`)에 맞춰 전면 재작성**합니다.
> 기존 코드에 부분적으로 추가하는 것이 아니라, Copilot이 생성한 코드로 **파일 전체를 교체**합니다.
>
> - 기존: `app.models`에서 import → 새로운: `app.schemas`에서 import
> - 기존: 단순 CRUD → 새로운: Priority + 필터링 + 페이지네이션 지원
>
> Copilot Chat의 응답을 `app/main.py`에 **덮어쓰기** 하세요.

Chat에서:

```
#file:app/schemas.py 와 #file:tests/test_todos.py 를 참고하여,
모든 테스트가 통과하도록 app/main.py를 구현해줘.

기존 인메모리 저장소를 유지하되:
- Priority 지원
- 페이지네이션 지원
- 필터링 지원
을 추가해야 합니다.
```

---

## 태스크 4: 테스트로 검증 (3분)

```bash
pytest tests/test_todos.py -v
```

**모든 테스트가 통과해야 합니다!**

만약 실패하면:
- Chat에서 `/fix #file:tests/test_todos.py` 실행
- 또는 실패한 테스트를 선택하고 원인 분석 요청

---

## ✅ 검증 체크리스트

- [ ] `app/schemas.py`에 스펙 타입 정의 완료
- [ ] 테스트가 먼저 작성됨 (Red 단계)
- [ ] Copilot이 구현을 완성 (Green 단계)
- [ ] `pytest -v` 전체 통과
- [ ] 우선순위 필터링 동작 확인 (Swagger UI)
- [ ] 페이지네이션 동작 확인

---

## 🔧 테스트가 실패하면? — Copilot으로 Red → Green

SDD(Spec-Driven Development)에서 테스트 실패는 **정상**입니다. Red → Green이 목표니까요!
하지만 예상과 다른 에러가 나면 Copilot에게 맡기세요.

### 방법 1: Chat에서 테스트 실패 분석

Copilot Chat을 열고 (`Ctrl+Shift+I` / Mac: `Cmd+Shift+I`):
```
터미널에 pytest 에러가 났어. 분석해서 수정해줘
```

### 방법 2: `/fix`로 실패한 테스트 수정

```
/fix #file:tests/test_todos.py
```

### 방법 3: 테스트와 구현 함께 보여주기

```
#file:tests/test_todos.py 의 테스트가 실패해.
#file:app/main.py 에서 뭘 고쳐야 하는지 알려줘
```

> 💡 이 단계에서는 **테스트가 스펙 역할**을 합니다. 테스트 자체를 고치지 말고 구현을 고치세요!
> 그래도 안 되면 `complete/` 폴더의 코드와 비교해 보세요.

---

## 핵심 인사이트

> **"AI에게 '무엇을 만들지'가 아니라 '어떤 조건을 만족할지'를 알려줘라"**
>
> 스펙(타입) + 테스트 = AI에게 가장 명확한 지시.
> "우선순위 기능 추가해줘" vs "이 스펙과 테스트를 통과하는 코드를 작성해줘"
> → 후자가 항상 더 정확합니다.

---

## 다음 단계

→ [Step 5. Prompt Files](../step-05-prompt-files/README.md)
