# Step 5. Skills

> ⏱️ 15분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: `.github/skills/<name>/SKILL.md`**
>
> **체감: "Copilot이 우리 팀의 테스트 규칙을 알고 있다!"**

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | Step 4 완성 코드 (기본 CRUD + Prompt Files) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 (+ Skills 추가) — 막힐 때 참고하세요 |

---

## 왜 Skills인가?

Step 3의 **Instructions**가 "항상 적용되는 규칙"이고,
Step 4의 **Prompt Files**가 "필요할 때 꺼내 쓰는 매크로"라면,
**Skills**는 "Copilot이 상황에 맞게 자동으로 꺼내 쓰는 전문 지식"입니다.

| 구분 | Instructions | Prompt Files | Skills |
|------|-------------|--------------|--------|
| 적용 시점 | 항상 자동 | `/명령어`로 수동 호출 | Copilot이 관련성 판단 시 자동 |
| 용도 | 프로젝트 규칙 | 반복 작업 자동화 | 도메인 전문 지식 |
| 비유 | 교칙 | 도구 상자 | 전문가 참고서 |

> 📖 **참고**: [GitHub 공식 문서 — About agent skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

---

## Skills란?

Skills는 `.github/skills/` 디렉토리에 위치하는 Markdown 파일로, Copilot Agent가 특정 도메인에 대한 **모범 사례(best practices)** 를 자동으로 참고할 수 있게 합니다.

### Instructions와의 차이점

- **Instructions** (`.github/copilot-instructions.md`): 모든 대화에 항상 포함
- **Skills** (`.github/skills/<skill-name>/SKILL.md`): Copilot이 대화 맥락을 분석하여 관련성이 높을 때 자동으로 포함

### Skills 파일 구조

`.github/skills/<skill-name>/SKILL.md` 형식으로 작성합니다:

```markdown
---
name: skill-name
description: '이 스킬이 다루는 내용에 대한 설명'
---

# 스킬 제목

여기에 모범 사례, 규칙, 가이드라인 등을 작성합니다.
```

- **YAML Frontmatter** (`---` 사이): `name`과 `description`은 필수입니다. Copilot이 이 정보를 기반으로 스킬의 관련성을 판단합니다.
- **본문**: Markdown 형식으로 상세 가이드를 작성합니다.

---

## 태스크 1: pytest Skills 파일 생성 (5분)

### 1-1. Skills 디렉토리 생성

프로젝트 루트에서 `.github/skills/` 디렉토리를 만드세요:

```
.github/
├── copilot-instructions.md              ← Step 3에서 생성 (항상 적용)
├── instructions/
│   ├── testing.instructions.md          ← Step 3에서 생성 (테스트 파일에 적용)
│   └── api.instructions.md              ← Step 3에서 생성 (라우트 핸들러에 적용)
├── prompts/                             ← Step 4에서 생성
│   ├── test.prompt.md
│   ├── refactor.prompt.md
│   └── spec-implement.prompt.md
└── skills/                              ← 이번 스텝에서 생성!
    └── python-pytest/
        └── SKILL.md                     → Copilot이 테스트 관련 요청 시 자동 참고
```

### 1-2. Skills 파일 작성

`.github/skills/python-pytest/SKILL.md` 파일을 만들고 아래 내용을 붙여넣으세요:

```markdown
---
name: python-pytest
description: 'pytest를 활용한 Python 단위 테스트 및 픽스처 모범 사례'
---

# pytest 모범 사례

목표는 pytest를 사용하여 효과적인 단위 테스트를 작성하는 것이며, 픽스처, 파라미터화 테스트, FastAPI 테스트를 포함합니다.

## 프로젝트 설정

- 테스트 파일은 `tests/` 디렉토리에 위치시킵니다.
- 다음 패키지를 설치합니다:
  - `pytest`
  - `httpx` (FastAPI 비동기 테스트용)
- 테스트 실행:
  - `pytest -v`
  - `pytest -v tests/test_specific.py`

## 테스트 구조

- 테스트 파일 이름은 `test_`로 시작해야 합니다. (예: `test_todo.py`)
- 테스트 함수 이름은 `test_`로 시작해야 합니다.
- 관련 테스트를 클래스로 그룹화합니다. (예: `TestCreateTodo`, `TestListTodos`)
- 클래스 이름은 `Test`로 시작해야 합니다.
- Arrange-Act-Assert (AAA) 패턴을 따릅니다.

## Fixtures (픽스처)

- `conftest.py`에 공유 픽스처를 정의합니다.
- `@pytest.fixture`로 테스트 데이터와 의존성을 관리합니다.
- 픽스처 스코프:
  - `function` (기본값): 각 테스트마다 실행
  - `class`: 클래스당 한 번 실행
  - `module`: 모듈당 한 번 실행
  - `session`: 전체 테스트 세션당 한 번 실행
- `yield`를 사용해 setup/teardown을 처리합니다.

## 일반 테스트

- 하나의 테스트는 하나의 동작만 검증해야 합니다.
- 테스트는 서로 독립적이고 반복 실행 가능해야 합니다.
- 테스트 간 의존성을 피해야 합니다.
- 헬퍼 함수 (예: `create_test_todo()`)로 테스트 데이터 생성을 간소화합니다.

## 파라미터화 테스트

- `@pytest.mark.parametrize`를 사용합니다.
- 단일 파라미터:
  - `@pytest.mark.parametrize("input_val", [1, 2, 3])`
- 복수 파라미터:
  - `@pytest.mark.parametrize("input_val, expected", [(1, 2), (2, 4)])`
- ID 지정:
  - `ids=["case1", "case2"]`로 테스트 케이스에 이름 부여

## Assertions (검증)

- `assert` 문을 직접 사용합니다.
- 예외 테스트:
  - `with pytest.raises(ValueError):`
  - `with pytest.raises(ValueError, match="메시지 패턴"):`
- 근사값 비교:
  - `pytest.approx()`

## FastAPI 테스트

- `TestClient`를 사용하여 API 엔드포인트를 테스트합니다.
- `conftest.py`에서 의존성 오버라이드를 설정합니다.
- 인메모리 SQLite로 DB 격리를 수행합니다.
- HTTP 메서드별 테스트: `client.get()`, `client.post()`, `client.patch()`, `client.delete()`
- 응답 검증: `response.status_code`, `response.json()`

## 테스트 구성

- 기능 또는 엔드포인트별로 테스트 파일을 분리합니다.
- `@pytest.mark.skip(reason="사유")`으로 테스트 비활성화
- `@pytest.mark.xfail`로 예상 실패 표시
- `-k` 옵션으로 특정 테스트만 실행:
  - `pytest -k "test_create"`
- `--tb=short`로 간결한 트레이스백 출력
```

---

## 태스크 2: Skills 동작 확인 (5분)

### 2-1. 테스트 작성 요청

Copilot Chat (Agent 모드)에서 테스트 작성을 요청해 보세요:

```
TODO API의 엔드포인트에 대한 테스트를 작성해줘
```

### 2-2. Skills 적용 확인

Copilot이 생성한 테스트 코드에서 다음 사항을 확인하세요:

- [ ] 테스트 파일 이름이 `test_`로 시작하는가? (예: `test_todo.py`)
- [ ] `conftest.py`에 공유 픽스처가 정의되었는가?
- [ ] 관련 테스트가 클래스로 그룹화되었는가? (예: `TestCreateTodo`)
- [ ] AAA (Arrange-Act-Assert) 패턴을 따르고 있는가?

> 💡 Skills가 없을 때와 비교하면 차이가 확연합니다. Skills 파일을 삭제하고 같은 요청을 해보면 Copilot이 다른 스타일로 테스트를 생성하는 것을 확인할 수 있습니다.

### 2-3. 파라미터화 테스트 요청

```
할 일 제목의 유효성 검사를 파라미터화 테스트로 작성해줘.
빈 문자열, None, 공백만 있는 경우를 테스트해야 해.
```

확인 포인트:
- [ ] `@pytest.mark.parametrize`가 사용되었는가?
- [ ] 여러 케이스가 하나의 테스트 함수로 검증되는가?

---

## 태스크 3: 추가 Skills 파일 만들기 (5분, 선택)

팀에서 활용할 수 있는 Skills 예시:

| 파일명 | 용도 |
|--------|------|
| `python-pytest/SKILL.md` | pytest 테스트 모범 사례 |
| `fastapi-rest/SKILL.md` | FastAPI REST API 설계 규칙 |
| `python-logging/SKILL.md` | 로깅 표준 (logging 모듈) |
| `code-review/SKILL.md` | 코드 리뷰 체크리스트 |
| `error-handling/SKILL.md` | 예외 처리 패턴 |

---

## 완성 확인

- [ ] `.github/skills/python-pytest/SKILL.md` 파일이 생성됨
- [ ] YAML Frontmatter에 `name`과 `description`이 포함됨
- [ ] Copilot이 테스트 작성 시 Skills의 규칙을 참고함
- [ ] `@pytest.mark.parametrize` 등 Skills에 명시된 패턴이 적용됨

---

## 핵심 인사이트

> **"Skills로 팀의 전문 지식을 Copilot에게 가르쳐라"**
>
> Instructions는 "항상 지켜야 할 규칙"이고, Skills는 "특정 상황에서 참고할 전문 지식"입니다:
> - Copilot이 맥락에 따라 자동으로 관련 Skills를 선택
> - 팀의 모범 사례를 코드화하여 일관성 유지
> - Git에 커밋하여 팀 전체가 동일한 품질 기준 공유

---

## 다음 단계

→ [Step 6. Agent 모드](../step-06-agent/README.md)
