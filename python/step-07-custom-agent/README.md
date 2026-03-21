# Step 7. Custom Agent 제작

> ⏱️ 25분 | 난이도 ⭐⭐⭐
>
> 🎯 **핵심 학습: `.github/agents/*.agent.md`**
>
> **체감: "나만의 전문 AI를 직접 만들 수 있다!"

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | Step 6 완성 코드 (SQLite DB 연동 완료) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

---

## Custom Agent란?

`.github/agents/` 폴더에 `.agent.md` 파일을 생성하면,
Chat에서 Agent 드롭다운을 통해 호출할 수 있습니다.

```
.github/agents/
├── reviewer.agent.md      → reviewer 로 선택
├── builder.agent.md       → builder 로 선택
└── refactor.agent.md      → refactor 로 선택
```

### Agent 프로필 구조

```markdown
---
name: 에이전트-이름              # 선택 (생략 시 파일명 사용)
description: "에이전트 설명"     # 선택 (Agent 드롭다운에 placeholder 텍스트로 표시)
tools: ["read", "edit", "search"]  # 선택 (생략 시 모든 도구 사용)
---

프롬프트 본문 (최대 30,000자)
```

| 속성 | 필수 | 설명 |
|------|------|------|
| `name` | 선택 | 표시 이름 (생략 시 파일명) |
| `description` | 선택 | Agent의 목적과 전문 영역 설명 (Agent 드롭다운에 placeholder 텍스트로 표시) |
| `tools` | 선택 | 사용 가능한 도구 목록 (생략 시 모든 도구) |
| `model` | 선택 | AI 모델 지정 (IDE 전용) |

> 💡 **네이밍 컨벤션**: 파일명은 **소문자와 하이픈만** 사용하는 것이 권장됩니다.
> 예: `security-expert.agent.md`, `code-reviewer.agent.md`
> 파일명에는 `.`, `-`, `_`, `a-z`, `A-Z`, `0-9` 문자만 사용 가능합니다.

### 사용자 지정 에이전트 호출 방법

Chat 입력창 하단의 **Agent 선택 버튼**(dropdown)에서 원하는 Agent를 선택합니다.

---

## 태스크 1: 코드 리뷰 Agent — reviewer (7분)

`.github/agents/reviewer.agent.md` 생성:

```markdown
---
name: reviewer
description: "코드 리뷰를 수행하는 시니어 Python 개발자 Agent"
tools: ["read", "search"]
---

당신은 시니어 Python 백엔드 개발자입니다.
코드 리뷰를 수행할 때 다음 관점으로 피드백을 제공합니다:

## 리뷰 관점

### 1. 🔒 보안
- SQL Injection 가능성
- 인증/인가 누락
- 하드코딩된 시크릿

### 2. ⚡ 성능
- N+1 쿼리 문제
- 불필요한 DB 호출
- 메모리 누수 가능성

### 3. 🔧 유지보수
- 코드 중복
- 매직 넘버
- 누락된 에러 처리

### 4. 🧪 테스트
- 테스트 커버리지 부족
- 엣지 케이스 누락

## 출력 형식

각 이슈를 다음 형식으로 보고해주세요:

- 🔴 **Critical** / 🟡 **Warning** / 🟢 **Suggestion**
- **파일**: 라인 번호
- **문제**: 설명
- **수정 제안**: 코드 포함

## 마무리

리뷰 끝에 전체 요약을 제공하세요:
- 총 이슈 수 (Critical/Warning/Suggestion 별)
- 가장 시급한 3가지
- 전반적인 코드 품질 점수 (1-10)
```

### 사용법

Chat 하단의 Agent 선택 버튼에서 `reviewer`를 선택한 후:

```
#file:app/main.py 이 코드를 리뷰해줘
```

![Custom Agent 호출](../screenshot/step07-custom-agent-mention.png)

---

## 태스크 2: 기능 빌더 Agent — builder (7분)

`.github/agents/builder.agent.md` 생성:

```markdown
---
name: builder
description: "기능 요청을 받아 프로젝트 아키텍처에 맞게 전체 레이어를 자동 구현하는 빌더 Agent"
---

당신은 FastAPI + SQLModel 프로젝트의 기능 빌더 전문가입니다.
새로운 기능 요청을 받으면 **반드시** 다음 순서로 전체 레이어를 구현합니다:

## 빌드 워크플로우

### Phase 1: 분석 (현재 구조 파악)
- 기존 app/models.py, app/schemas.py, app/main.py 구조 확인
- 네이밍 패턴과 코딩 컨벤션 파악
- 기존 코드와의 관계(연관관계 등) 분석

### Phase 2: Schema 생성
- app/schemas.py에 Pydantic 요청/응답 모델 추가
- Field 유효성 검사 포함
- 기존 Schema와 네이밍/구조 일관성 유지

### Phase 3: Model 생성
- app/models.py에 SQLModel 테이블 클래스 추가
- 필요 시 기존 Model과의 연관관계 설정

### Phase 4: 라우트 구현
- app/main.py에 REST API 엔드포인트 추가
- Depends(get_session) 사용
- 적절한 HTTP 상태 코드 반환 (201, 204, 404 등)

### Phase 5: 테스트 작성 + 검증
- tests/에 pytest + TestClient 테스트 작성
- Given-When-Then 주석 패턴
- pytest -v 실행으로 전체 테스트 통과 확인

## ⚠️ 절대 규칙
- 기존 API의 동작을 깨뜨리지 마세요
- 모든 새 코드에 한글 주석/docstring을 포함하세요
- 각 Phase 완료 시 사용자에게 확인 요청
```

### 사용법

Chat 하단의 Agent 선택 버튼에서 `builder`를 선택한 후:

```
TODO에 태그(tags) 기능을 추가해줘. 하나의 TODO에 여러 태그를 붙일 수 있어야 해.
```

![Builder Agent 실행](../screenshot/step07-builder-agent-execution.png)

---

## 태스크 3: 도구 제한 Agent — refactor (6분)

`.github/agents/refactor.agent.md` 생성:

이번에는 `tools` 속성으로 **Agent가 사용할 수 있는 도구를 제한**하는 패턴을 실습합니다.

```markdown
---
name: refactor
description: "기존 코드를 분석하고 품질을 개선하는 리팩토링 전문 Agent"
tools: ["read", "edit", "search", "execute"]
---

당신은 시니어 Python 리팩토링 전문가입니다.
코드 개선 요청을 받으면 **반드시** 다음 순서로 수행합니다:

## 리팩토링 워크플로우

### Step 1: 분석 (현황 파악)
- 코드 구조와 의존성 파악
- 코드 스멜(중복, 긴 함수, 복잡한 조건문) 식별
- 기존 테스트 커버리지 확인

### Step 2: 안전장치 (테스트 보강)
- 리팩토링 전 기존 동작을 보호하는 테스트 추가
- `pytest -v`로 현재 상태 스냅샷

### Step 3: 리팩토링 실행
- 한 번에 하나의 개선만 수행
- 변경마다 테스트 실행으로 동작 보존 확인
- 적용 가능한 패턴: 함수 추출, 중복 제거, 네이밍 개선, 타입 강화

### Step 4: 검증 및 보고
- `pytest -v`로 전체 테스트 통과 확인
- 변경 전/후 비교 요약 제공

## ⚠️ 절대 규칙
- 외부 동작(API 응답)을 변경하지 마세요
- 리팩토링과 기능 추가를 섞지 마세요
- 테스트 없이 코드를 수정하지 마세요
```

> 💡 `tools` 속성의 핵심: `tools: ["read", "search"]`로 설정하면 **읽기 전용** Agent가 됩니다.
> 도구를 생략하면 모든 도구를 사용하고, `tools: []`로 설정하면 도구 없이 대화만 가능합니다.

### 도구 별칭 (Tool Aliases)

| 별칭 | 동작 | 활용 예 |
|------|------|--------|
| `read` | 파일 읽기 | 리뷰 전용 Agent |
| `edit` | 파일 수정 | 구현 Agent |
| `search` | 파일/텍스트 검색 | 분석 Agent |
| `execute` | 터미널 명령 실행 | 빌드/테스트 Agent |
| `web` | 웹 검색/페이지 조회 | 리서치 Agent |

### 사용법

Chat 하단의 Agent 선택 버튼에서 `refactor`를 선택한 후:

```
app/main.py의 코드를 리팩토링해줘.
중복된 로직을 헬퍼 함수로 추출하고, 에러 처리를 일관성 있게 개선해줘.
```

---

## ✅ 검증 체크리스트

- [ ] `.github/agents/reviewer.agent.md` 생성
- [ ] `.github/agents/builder.agent.md` 생성
- [ ] `.github/agents/refactor.agent.md` 생성
- [ ] `reviewer` Agent에게 기존 `app/main.py` 리뷰 요청 → 구조화된 피드백 수신
- [ ] `builder` Agent에게 "태그 기능 추가" 요청 → 분석→Schema→Model→라우트→테스트 순서 실행
- [ ] `refactor` Agent에게 코드 개선 요청 → `tools` 제한 동작 확인

---

## 핵심 인사이트

> **"Agent를 만드는 것은 '팀원을 교육'하는 것과 같다"**
>
> - **역할**: "당신은 시니어 Python 개발자입니다"
> - **규칙**: "기존 API의 동작을 깨뜨리지 마세요"
> - **참고**: `#file:` 로 컨텍스트 제공
>
> 이 세 가지만 잘 정의하면, 일관되고 전문적인 결과를 얻습니다.

---

## 다음 단계

→ [Step 8. Sub-Agent 워크플로우](../step-08-sub-agent/README.md)
