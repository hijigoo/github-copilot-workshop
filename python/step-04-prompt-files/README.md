# Step 4. Prompt Files

> ⏱️ 20분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: `.github/prompts/*.prompt.md`**
>
> **체감: "/ 하나로 반복 작업이 끝난다!"**

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | Step 3 완성 코드 + SDD 적용 완료 (schemas + priority + pagination) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

---

## 왜 Prompt Files인가?

Step 3의 **Instructions**가 "항상 적용되는 규칙"이라면,
**Prompt Files**는 "필요할 때 꺼내 쓰는 매크로"입니다.

| 구분 | Instructions | Prompt Files |
|------|-------------|--------------|
| 적용 시점 | 항상 자동 | `/명령어`로 수동 호출 |
| 용도 | 프로젝트 규칙 | 반복 작업 자동화 |
| 비유 | 교칙 | 도구 상자 |

---

## Prompt Files란?

`.github/prompts/` 폴더에 `.prompt.md` 파일을 생성하면,
Chat에서 `/파일명`으로 호출할 수 있습니다.

```
.github/prompts/
├── test-code.prompt.md      → /test-code 로 호출
├── spec-implement.prompt.md → /spec-implement 로 호출
└── refactor.prompt.md       → /refactor 로 호출
```

![Prompt Files 폴더 구조](../screenshot/step04-prompts-folder.png)

### 프롬프트 파일 구조

```markdown
---
agent: "agent"           ← 프론트매터 (YAML 헤더)
description: "설명"
---

프롬프트 본문              ← Copilot에게 전달되는 실제 지시
```

| 부분 | 역할 |
|------|------|
| `agent` | 프롬프트를 실행할 에이전트 지정. (미지정 시 현재 에이전트 사용, `tools` 지정 시 기본값은 `agent`) |
| `description` | Chat에서 `/명령어` 입력 시 목록에 표시되는 설명 텍스트 |
| `name` | 프롬프트 이름. Chat에서 `/` 뒤에 표시됨 (미지정 시 파일명 사용) |
| `model` | 프롬프트 실행 시 사용할 언어 모델 (미지정 시 현재 선택된 모델 사용) |
| `tools` | 프롬프트에서 사용할 도구 목록. MCP 서버 전체 도구는 `<서버명>/*` 형식 |
| `argument-hint` | Chat 입력란에 표시되는 힌트 텍스트 |
| 프롬프트 본문 | `---` 아래의 마크다운 내용. `#file:`, `${input:}` 등을 사용해 컨텍스트와 사용자 입력을 포함 |

**`agent` 속성 값:**

| 값 | 설명 |
|----|------|
| `"agent"` | **Agent 모드** — 파일 생성·수정, 터미널 명령 실행, 도구 호출 등 자율적으로 작업 수행 |
| `"ask"` | **Ask 모드** — 코드 설명, 질문 답변 등 읽기 전용 응답만 제공 (파일 수정 불가) |
| `"plan"` | **Plan 모드** — 구현 계획을 생성하고 제안 (직접 실행하지 않음) |
| 커스텀 에이전트 이름 | `.github/agents/` 에 정의된 커스텀 에이전트를 지정하여 실행 |

---

## 태스크 1: 테스트 생성 프롬프트 (5분)

`.github/prompts/test-code.prompt.md` 생성:

```markdown
---
agent: "agent"
description: "선택한 모듈에 대한 테스트를 자동 생성합니다"
---

다음 대상에 대한 테스트를 작성해주세요:
아래 파라미터는 vscode/askQuestions 도구를 통해 입력받습니다.

대상: ${input:testTarget}

## 규칙
- pytest + FastAPI TestClient 사용
- Given-When-Then 주석 패턴
- 함수명: test_동작_조건_결과()
- 정상 케이스 / 에러 케이스 / 경계값 각각 최소 1개
- 한국어 주석과 설명
```

### 사용법

1. Chat에서 `/test-code` 입력
2. `testTarget`에 `PATCH /todos/{id}` 입력
3. Copilot이 해당 엔드포인트의 테스트를 자동 생성

![Prompt File 자동완성](../screenshot/step04-prompt-file-autocomplete.png)

---

## 태스크 2: SDD 워크플로우 프롬프트 (5분)

`.github/prompts/spec-implement.prompt.md` 생성:

```markdown
---
agent: "agent"
description: "스펙 기반으로 타입 → 테스트 → 구현을 순서대로 수행합니다"
---

다음 기능을 Spec-Driven Development로 구현해주세요:
아래 파라미터는 vscode/askQuestions 도구를 통해 입력받습니다.

기능: ${input:featureDescription}

## 순서 (반드시 이 순서대로!)
1. **SPEC**: app/schemas.py에 타입 스펙 추가
2. **TEST**: tests/에 테스트 작성 (실패하는 상태)
3. **IMPL**: app/에 구현 코드 작성
4. **VERIFY**: pytest로 전체 테스트 통과 확인
```

### 사용법

1. Chat에서 `/spec-implement` 입력
2. Chat에서 입력 팝업이 뜨면 `TODO에 마감일(due_date) 기능 추가` 입력
3. Copilot이 SDD 순서대로 자동 구현

---

## 태스크 3: 리팩토링 프롬프트 (5분)

`.github/prompts/refactor.prompt.md` 생성:

```markdown
---
agent: "agent"
description: "선택한 코드를 리팩토링합니다"
tools: ['vscode/askQuestions', 'edit/editFiles', 'edit/createFile', 'read/readFile', 'execute/runInTerminal', 'execute/runTests']
---

다음 대상을 리팩토링해주세요:

대상: ${input:refactorTarget}

## 규칙
- 동작 변경 없이 구조만 개선
- 리팩토링 전후 테스트 통과 필수 (pytest -v)
- 변경 사항을 한국어로 요약해주세요

## 리팩토링 관점
- 코드 중복 제거
- 함수/클래스 분리
- 네이밍 개선
- 타입 안전성 향상
```

### 사용법

1. Chat에서 `/refactor` 입력
2. Chat에서 입력 팝업이 뜨면 `app/main.py의 TODO CRUD 핸들러` 입력
3. Copilot이 동작 변경 없이 구조를 개선하고 테스트로 검증

---

## 태스크 4: 프롬프트 파일 활용 실습 (5분)

1. `/test-code` → `GET /todos 페이지네이션` 에 대한 테스트 생성
2. `/spec-implement` → `TODO에 태그(tags) 기능 추가`
3. 생성된 코드를 검토하고 `pytest -v`로 검증

---

## ✅ 검증 체크리스트

- [ ] `.github/prompts/test-code.prompt.md` 생성
- [ ] `.github/prompts/spec-implement.prompt.md` 생성
- [ ] `.github/prompts/refactor.prompt.md` 생성
- [ ] `/test-code` 입력 시 프롬프트 파일이 로드됨
- [ ] `/spec-implement`로 새 기능 SDD 자동 실행

---


## 핵심 인사이트

> **"자주 하는 요청은 Prompt File로 만들어라"**
>
> Chat 히스토리에 묻히는 반복 프롬프트를 파일로 저장하면:
> - 팀원 누구나 동일한 품질로 사용 가능
> - Git에 커밋하여 버전 관리
> - `${input:변수}`로 유연하게 재사용

---

## 다음 단계

→ [Step 5. Skills](../step-05-skills/README.md)

> 💡 SDD를 아직 해보지 않았다면 → [Step 10. SDD (보너스)](../step-10-spec-driven/README.md)
