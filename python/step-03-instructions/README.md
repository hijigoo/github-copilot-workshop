# Step 3. Instructions

> ⏱️ 20분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: `copilot-instructions.md` + 경로 지정 지침(Path-specific Instructions)**
>
> **체감: "매번 같은 말 반복 안 해도 된다!"****

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | Step 2 완성 코드 (docstring + 테스트 포함 TODO API) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

---

## 왜 세 번째인가?

Step 2에서 Chat을 쓸 때 매번 "한글로 대답해줘", "pytest 쓰고 있어" 등을 반복했을 겁니다.
**Instructions**는 이런 반복을 **한 번에 제거**합니다.

---

## 사용자 지정 지침(Custom Instructions)이란?

리포지토리에 사용자 지정 지침을 추가하면, 프로젝트를 이해하고 변경 내용을 작성 및 테스트하는 방법에 대해 Copilot을 안내할 수 있습니다.

Copilot은 다음 유형의 사용자 지정 지침 파일을 지원합니다:

- `.github/copilot-instructions.md` — **리포지토리 전체 지침** (항상 적용)
- `.github/instructions/**/*.instructions.md` — **경로 지정 지침** (특정 파일에만 적용)

```
.github/
├── copilot-instructions.md          ← 리포지토리 전체 지침 (항상 적용)
└── instructions/
    ├── testing.instructions.md      ← tests/** 에서만 적용 (내용에 폴더 지정)
    └── api.instructions.md          ← app/** 에서만 적용 (내용에 폴더 지정)
```

> 📖 자세한 내용: [GitHub Copilot에 대한 리포지토리 사용자 지정 지침 추가하기](https://docs.github.com/ko/copilot/how-tos/configure-custom-instructions/add-repository-instructions?tool=vscode)

> 📖 지원 범위: [Custom Instructions 지원 현황](https://docs.github.com/en/copilot/reference/custom-instructions-support)

---

## 태스크 1: 리포지토리 전체 지침 작성 (5분)

`.github/copilot-instructions.md` 생성:

```markdown
# 프로젝트 규칙

## 언어
- 모든 응답은 한국어로 작성
- 코드 주석도 한국어

## 기술 스택
- Python 3.12+ / FastAPI / Pydantic v2
- DB: SQLite + SQLModel
- 테스트: pytest + httpx (FastAPI TestClient)

## 코드 스타일 & 네이밍 컨벤션
- 함수명 / 변수명 / 파일명: snake_case (예: get_todos, todo_list, schemas.py)
- 클래스명: PascalCase
- 상수: UPPER_SNAKE_CASE (예: MAX_PAGE_SIZE)
- 타입 힌트 필수
- docstring: Google 스타일
- Pydantic 스키마: 용도별 접미사 사용
  - 생성 요청: XxxCreate (예: TodoCreate)
  - 수정 요청: XxxUpdate (예: TodoUpdate)
  - 응답: XxxResponse (예: TodoResponse)
- 테스트 함수: test_동작_조건_결과() (예: test_create_todo_returns_201)

## API 규칙
- RESTful 엔드포인트
- 응답은 항상 Pydantic 모델로 직렬화
- 에러는 HTTPException으로 처리
- 에러 응답 형식: {"detail": "메시지"}
```

---

## 태스크 2: 경로 지정 지침 작성 (10분)

`.github/instructions/` 디렉토리에 `NAME.instructions.md` 파일을 만들면,
**특정 경로의 파일에서만 적용되는 지침**을 정의할 수 있습니다.

파일 상단에 YAML frontmatter로 `applyTo`를 지정합니다. glob 패턴을 사용하며, 쉼표로 여러 패턴을 지정할 수 있습니다.

```yaml
---
applyTo: "**/*.py"           # 모든 Python 파일에 적용
---
```

### glob 패턴 참고

| 패턴 | 매칭 대상 |
|------|----------|
| `*` | 현재 디렉토리의 모든 파일 |
| `**` 또는 `**/*` | 모든 디렉토리의 모든 파일 |
| `*.py` | 현재 디렉토리의 `.py` 파일 |
| `**/*.py` | 모든 디렉토리의 `.py` 파일 (재귀) |
| `src/*.py` | `src/` 바로 아래의 `.py` 파일만 |
| `src/**/*.py` | `src/` 하위 모든 `.py` 파일 (재귀) |

> 📖 자세한 내용: [경로 지정 사용자 지정 지침 만들기](https://docs.github.com/ko/copilot/how-tos/configure-custom-instructions/add-repository-instructions?tool=vscode#creating-path-specific-custom-instructions-1)

### 테스트 전용 규칙

`.github/instructions/testing.instructions.md`:

```markdown
---
applyTo: "tests/**"
---
# 테스트 규칙

## 프레임워크
- pytest + FastAPI TestClient 사용
- httpx 기반 비동기 테스트 지원

## 네이밍
- 함수명: test_동작_조건_결과()
  - 예: test_create_todo_with_valid_data_returns_201()
  - 예: test_get_todo_with_invalid_id_returns_404()

## 구조
- Given-When-Then 주석 패턴 사용
  - 각 단계의 코드 위에 `# Given:`, `# When:`, `# Then:` 주석을 작성
  - 예시:
    ```python
    def test_create_todo_with_valid_data_returns_201():
        # Given: 유효한 TODO 데이터
        payload = {"title": "테스트", "description": "설명", "priority": 1}

        # When: POST /todos 요청
        response = client.post("/todos", json=payload)

        # Then: 201 상태 코드와 생성된 TODO 반환
        assert response.status_code == 201
        assert response.json()["title"] == "테스트"
    ```
- 각 테스트는 독립적 (다른 테스트에 의존 X)

## 커버리지
- 정상 케이스 + 에러 케이스 + 경계값 각각 최소 1개
- 모든 HTTP 상태 코드 테스트
```

### API 코드 전용 규칙

`.github/instructions/api.instructions.md`:

```markdown
---
applyTo: "app/**"
---
# API 코드 규칙

## 엔드포인트
- 모든 엔드포인트에 response_model 지정
- status_code 명시적 설정 (200, 201, 204)
- 경로 매개변수에 타입 지정

## 에러 처리
- 404: 리소스를 찾을 수 없음
- 422: 유효성 검사 실패 (Pydantic 자동)
- 에러 메시지는 한국어

## 구조
- 라우터별 파일 분리 고려
- 비즈니스 로직은 서비스 레이어로 분리
```

### 검증: 경로 지정 지침 동작 확인

**① 테스트 지침 확인** — `tests/test_main.py`를 열고 Chat에 입력:

> "방금 생성한 testing.instructions.md 지침을 확인하고, 그 규칙에 맞게 get_todos 함수에 대한 테스트를 작성해줘"

→ 확인 포인트:
- [ ] 함수명이 `test_동작_조건_결과()` 패턴인가?
- [ ] `# Given:` / `# When:` / `# Then:` 주석이 있는가?
- [ ] 정상 + 에러 케이스를 모두 작성했는가?

**② API 코드 지침 확인** — `app/main.py`를 열고 Chat에 입력:
적용될 지침: **.github/copilot-instructions.md, .github/instructions/api.instructions.md**

> "PATCH /todos/{id} 부분 수정 엔드포인트를 추가해줘"

지침이 적용되면 다음이 변경됩니다:

- [ ] **에러 처리**: `HTTPException(status_code=404, detail="한국어 메시지")`로 404를 처리하는가?
- [ ] **에러 메시지**: 에러 메시지가 한국어로 작성되었는가?
- [ ] **response_model**: `response_model=TodoResponse` 지정되어 있는가?

어떤 인스트럭션을 참고했는지 알고 싶으면 아래 명령을 입력하세요:

```
참고한 모든 인스트럭션의 경로를 포함한 이름 알려줘
```

> 💡 경로 지정 지침은 `applyTo` 패턴과 일치하는 파일을 **열거나, 참조하거나, 수정할 때** 자동 적용됩니다.

---

## ✅ 검증 체크리스트

### 태스크 1: 리포지토리 전체 지침
- [ ] `.github/copilot-instructions.md` 파일 생성 완료

### 태스크 2: 경로 지정 지침
- [ ] `.github/instructions/testing.instructions.md` 생성 완료
- [ ] `.github/instructions/api.instructions.md` 생성 완료

### 태스크 3: 지침 동작 실습 및 검증
- [ ] 테스트 경로 지정 지침 확인: `test_동작_조건_결과()` 네이밍 패턴, Given-When-Then 주석 적용됨
- [ ] API 경로 지정 지침 확인: response_model 지정, 에러 메시지 한국어 적용됨
- [ ] 경로 지정 지침이 해당 폴더에서만 적용됨을 확인

---

## 핵심 인사이트

> **"사용자 지정 지침 = AI에 대한 투자"**
>
> 한 번 잘 써두면 Copilot의 **모든 응답**이 달라집니다.
> 팀에서는 이 파일을 Git에 커밋하여 **팀 AI 컨벤션**으로 사용할 수 있습니다.

---

## 다음 단계

→ [Step 4. Prompt Files](../step-04-prompt-files/README.md)
