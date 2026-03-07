# Step 7. Multi-Agent 워크플로우

> ⏱️ 25분 | 난이도 ⭐⭐⭐
>
> 🎯 **핵심 학습: Custom Agent 간 역할 분담 + 자동 연쇄 호출**
>
> **체감: "Agent들이 협업하며 프로젝트를 처음부터 만들어간다!"**

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | **빈 FastAPI 프로젝트** (main.py에 app 인스턴스만 존재) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

> 💡 **왜 처음부터?**
> 앞 스텝에서 만든 TODO API 코드를 **모두 지우고** 빈 프로젝트에서 시작합니다.
> Multi-Agent가 설계 → 테스트 → 구현 → 리뷰를 **처음부터 끝까지** 자동으로 수행하는 과정을 체험하기 위해서입니다.

---

## 왜 Multi-Agent인가?

Step 6에서 `@reviewer`, `@builder`, `@refactor` 같은 Custom Agent를 **개별로** 호출했습니다.

이번 스텝에서는 **하나의 Agent가 여러 전문 역할을 순서대로 수행하며 프로젝트 전체를 처음부터 구축**합니다.

| 단계 | 방식 | 비유 |
|------|------|------|
| Step 6 | 개별 Agent 호출 | 팀원 한 명에게 개별 지시 |
| **Step 7** | **Agent 간 연쇄 호출** | **팀이 빈 사무실에서 프로젝트를 자율적으로 구축** |
| Step 8 | Plan + Agent 조합 | 팀장이 계획 후 팀원에게 순서대로 지시 |

---

## 사전 준비: 프로젝트 초기화

`starter/` 폴더에는 다음만 포함되어 있습니다:

```
starter/
├── requirements.txt          ← 의존성만 정의
├── app/
│   ├── __init__.py
│   └── main.py               ← FastAPI() 인스턴스와 health check만 존재
└── tests/
    ├── __init__.py
    └── test_health.py         ← health check 테스트만 존재
```

> ⚠️ **models.py, schemas.py, database.py, 라우트 핸들러는 존재하지 않습니다.**
> 이 모든 것을 Multi-Agent가 생성합니다.

---

## 개념: Multi-Agent 패턴

### Orchestrator Agent 패턴

하나의 **오케스트레이터 Agent**가 전체 워크플로우를 관리하며, 필요에 따라 전문 Agent를 호출합니다.

```
@orchestrator (지휘자)
  ├── @architect  → 아키텍처 설계 및 스펙 정의
  ├── @developer  → 구현
  ├── @tester     → 테스트 작성 및 실행
  └── @reviewer   → 코드 리뷰 및 품질 점검
```

### 핵심 메커니즘

Agent의 프롬프트 본문에서 **다른 Agent의 역할과 규칙을 내장**하여, 하나의 Agent가 여러 전문 페르소나(역할)를 **단계별로 전환**하며 작업합니다.

실제로는 `@orchestrator` 하나의 Agent가 Phase별로 "지금부터 Architect 역할이야" → "지금부터 Tester 역할이야" 식으로 **페르소나를 전환**합니다. 별도 Agent를 직접 호출하는 것이 아니라, 프롬프트 안에 각 역할의 규칙과 제약을 명시해두고 순서대로 실행하는 패턴입니다.

---

## 태스크 1: 전문 Agent 3종 만들기 (7분)

### @architect — 설계 전문

`.github/agents/architect.agent.md`:

```markdown
---
name: architect
description: "시스템 아키텍처 설계 및 Schema/Model 정의 전문 Agent"
tools: ["read", "edit", "search"]
---

당신은 시니어 Python/FastAPI 아키텍트입니다.
기능 요청을 받으면 **설계 산출물만** 작성합니다.

## 역할
- app/schemas.py에 Pydantic BaseModel 정의
- app/models.py에 SQLModel 테이블 클래스 설계
- app/database.py에 DB 연결 설정
- 파일 구조 설계

## 출력 형식
1. **설계 요약** — 변경 범위와 영향도
2. **Schema/Model/Database 파일** — 생성
3. **파일 구조** — 생성할 파일 전체 목록

## 제약
- 구현 코드(라우트 핸들러)를 직접 작성하지 마세요
- 스펙과 설계만 담당합니다
```

### @developer — 구현 전문

`.github/agents/developer.agent.md`:

```markdown
---
name: developer
description: "설계된 스펙을 기반으로 코드를 구현하는 전문 Agent"
tools: ["read", "edit", "search", "execute"]
---

당신은 시니어 Python/FastAPI 백엔드 개발자입니다.
설계된 스펙과 테스트를 기반으로 **구현만** 담당합니다.

## 역할
- app/main.py에 라우트 핸들러 작성
- 기존 코드와의 호환성 유지
- 구현 후 pytest -v 실행으로 검증

## 워크플로우
1. Schema/Model/Database 스펙 확인
2. 테스트 파일 확인 (어떤 동작이 기대되는지)
3. 라우트 핸들러 구현
4. `pytest -v` 실행으로 검증
5. 실패 시 수정 반복

## 제약
- Schema/Model/Database를 수정하지 마세요 — 그건 architect의 역할입니다
- 테스트를 수정하지 마세요 — 그건 tester의 역할입니다
- 코드가 테스트를 통과하도록 구현에만 집중하세요
```

### @tester — 테스트 전문

`.github/agents/tester.agent.md`:

```markdown
---
name: tester
description: "스펙 기반 테스트 작성 및 품질 검증 전문 Agent"
tools: ["read", "edit", "search", "execute"]
---

당신은 시니어 QA 엔지니어입니다.
스펙을 기반으로 **테스트만** 작성하고 실행합니다.

## 역할
- tests/ 아래 테스트 코드 작성
- 정상/에러/경계값 케이스 작성
- pytest -v 실행 및 결과 보고

## 테스트 규칙
- pytest + TestClient(httpx) 사용
- 클래스로 그룹핑 (TestCreateTodo, TestListTodos 등)
- 메서드명: test_동작_조건_결과()
- conftest.py에 인메모리 SQLite 세션 fixture 설정
- 각 테스트는 독립적

## 출력 형식
1. **테스트 파일** — 작성된 테스트
2. **실행 결과** — pytest -v 출력
3. **커버리지 요약** — 테스트한 케이스 목록

## 제약
- 구현 코드를 수정하지 마세요 — 테스트가 실패하면 보고만 하세요
- Schema/Model을 수정하지 마세요
- 테스트 작성과 실행에만 집중하세요
```

---

## 태스크 2: Orchestrator Agent 만들기 (8분)

### @orchestrator — 전체 워크플로우 지휘

`.github/agents/orchestrator.agent.md`:

```markdown
---
name: orchestrator
description: "Multi-Agent 워크플로우를 지휘하여 빈 프로젝트에서 기능을 설계 → 테스트 → 구현 → 검증하는 총괄 Agent"
subAgents: ["architect", "tester", "developer", "reviewer"]
---

당신은 소프트웨어 프로젝트 매니저입니다.
기능 요청을 받으면 **빈 프로젝트에서 전체 구조를 처음부터** 만들어냅니다.
다음 서브 에이전트들을 순서대로 호출하여 **4단계 파이프라인**을 실행합니다.

## 팀 구성 (서브 에이전트)
- `@architect` — Phase 1: 설계 (database.py, models.py, schemas.py)
- `@tester` — Phase 2: 테스트 작성 (pytest + TestClient)
- `@developer` — Phase 3: 구현 (main.py 라우트 핸들러) + 테스트 통과
- `@reviewer` — Phase 4: 코드 리뷰 + 품질 점검

## 🔄 Multi-Agent 파이프라인

### Phase 1: 🏗️ 설계 (Architect 역할)
시니어 FastAPI 아키텍트로서:
- 기능 요구사항을 분석합니다
- 파일 구조를 설계합니다 (models.py, schemas.py, database.py)
- app/database.py에 Engine, get_session(), create_db_and_tables()를 생성합니다
- app/models.py에 SQLModel 테이블 클래스를 생성합니다
- app/schemas.py에 Pydantic BaseModel을 생성합니다
- ✅ 완료 시 "Phase 1 완료: [설계 요약]"을 출력합니다

### Phase 2: 🧪 테스트 (Tester 역할)
시니어 QA 엔지니어로서:
- Phase 1의 스펙을 기반으로 테스트를 작성합니다
- tests/conftest.py에 인메모리 SQLite fixture를 설정합니다
- CRUD 전체에 대한 테스트를 포함합니다
- 정상/에러/경계값 케이스를 포함합니다
- pytest + TestClient 사용
- 클래스로 그룹핑, test_동작_조건_결과() 네이밍
- ✅ 완료 시 "Phase 2 완료: [테스트 N개 작성]"을 출력합니다

### Phase 3: 💻 구현 (Developer 역할)
시니어 백엔드 개발자로서:
- Phase 1의 스펙과 Phase 2의 테스트를 모두 통과하도록 구현합니다
- app/main.py에 lifespan + 라우트 핸들러 작성
- 구현 후 `pytest -v` 실행
- 실패 시 수정 반복
- ✅ 완료 시 "Phase 3 완료: [구현 요약]"을 출력합니다

### Phase 4: 🔍 리뷰 (Reviewer 역할)
시니어 코드 리뷰어로서:
- Phase 1~3에서 생성된 전체 코드를 점검합니다
- 보안, 성능, 유지보수 관점에서 피드백
- 🔴 Critical / 🟡 Warning / 🟢 Suggestion으로 분류
- Critical 이슈가 있으면 Phase 3으로 돌아가 수정
- ✅ 완료 시 "Phase 4 완료: [리뷰 요약, 품질 점수 X/10]"을 출력합니다

## ⚠️ 절대 규칙
- 반드시 Phase 1 → 2 → 3 → 4 순서로 진행
- 각 Phase 완료 시 요약을 출력
- Phase 3에서 테스트 실패 시 코드 수정 (테스트 수정 금지!)
- Phase 4에서 Critical 이슈 발견 시 Phase 3으로 회귀
- 전체 완료 후 최종 요약 보고서 출력

## 참고
- 프레임워크: FastAPI + SQLModel + Pydantic v2
- DB: SQLite (로컬 파일)
- 테스트: pytest + TestClient + httpx
- ORM 모델은 models.py, API 스키마는 schemas.py (분리 필수)
```

---

## 태스크 3: Multi-Agent 실행 (10분)

### 3-1. Orchestrator로 TODO API 전체 구현

Chat 하단의 Agent 선택 버튼에서 `orchestrator`를 선택한 후:

```
빈 FastAPI 프로젝트에서 TODO API를 처음부터 만들어줘.
각 Phase 시작 시 현재 어떤 Agent 역할을 수행 중인지 표시해줘 

요구사항:
- Todo 모델: id, title, description, completed, created_at, updated_at
- CRUD REST API:
  - POST   /api/v1/todos       → 생성 (201)
  - GET    /api/v1/todos        → 전체 조회 (페이지네이션: page, size)
  - GET    /api/v1/todos/{id}   → 단건 조회
  - PATCH  /api/v1/todos/{id}   → 수정
  - DELETE /api/v1/todos/{id}   → 삭제 (204)
- title은 필수, 1~200자 제한
- completed 기본값 False
- 존재하지 않는 id 조회/수정/삭제 시 404
- 모든 코드에 한글 주석/docstring 포함

```

> 📸 **스크린샷**: Chat 하단의 Agent 선택 드롭다운에서 `orchestrator`를 선택하는 화면
>
> ![Orchestrator Agent 선택](./images/step07-orchestrator-select.png)

### 3-2. 파이프라인 관찰

Agent가 4단계를 순서대로 실행하며 **빈 프로젝트를 완성해가는 과정**을 관찰합니다:

| Phase | Agent 역할 | 기대 산출물 |
|-------|-----------|-----------|
| 1 | Architect | database.py + models.py + schemas.py 생성 |
| 2 | Tester | conftest.py + CRUD 전체 테스트 작성 |
| 3 | Developer | main.py에 lifespan + 라우트 핸들러 구현 + 테스트 통과 |
| 4 | Reviewer | 전체 코드 품질 리뷰 + 개선 사항 |

> 📸 **스크린샷**: Orchestrator Agent가 Phase 1→4 파이프라인을 순서대로 실행하며 빈 프로젝트에서 전체 API를 구축하는 Chat 패널 화면
>
> ![Multi-Agent 파이프라인 실행](./images/step07-pipeline-execution.png)

### 3-3. 완성 결과 확인

파이프라인 완료 후 생성된 파일 구조를 확인합니다:

```
app/
├── __init__.py
├── main.py          ← Phase 3에서 라우트 핸들러 추가
├── database.py      ← Phase 1에서 생성
├── models.py        ← Phase 1에서 생성
└── schemas.py       ← Phase 1에서 생성

tests/
├── __init__.py
├── conftest.py      ← Phase 2에서 생성
├── test_health.py   ← 기존
└── test_todos.py    ← Phase 2에서 생성
```

### 3-4. 개별 Agent와 비교

같은 기능을 **개별 Agent**로 구현할 때와 비교해 보세요:

```
# 이전 방식 (Step 6): 수동으로 하나씩 호출
@architect  → 설계해줘
@tester     → 테스트 작성해줘
@developer  → 구현해줘
@reviewer   → 리뷰해줘

# Multi-Agent 방식 (Step 7): 한 번의 요청으로 전체 프로젝트 구축
@orchestrator → TODO API를 처음부터 만들어줘
```

### 관찰 포인트
- [ ] **빈 프로젝트에서 완전한 API가 생성되었는가?**
- [ ] Phase 간 전환이 자연스러운가?
- [ ] 각 Phase의 제약이 지켜지는가? (예: Architect가 구현을 하지 않는지)
- [ ] Phase 3에서 테스트 실패 시 수정을 반복하는가?
- [ ] Phase 4에서 Critical 이슈 발견 시 회귀하는가?
- [ ] `pytest -v` 전체 통과하는가?

---

## 🔧 Multi-Agent 프롬프트 디자인 팁

### 역할 분리 원칙

```
각 Agent에 "하지 마세요" 제약을 명시:
- Architect: "구현 코드를 작성하지 마세요"
- Tester: "구현 코드를 수정하지 마세요"
- Developer: "스펙을 수정하지 마세요"
- Reviewer: "코드를 직접 수정하지 마세요"
```

### 회귀 루프 설계

```
Phase 4(리뷰) → Critical 발견 → Phase 3(수정) → Phase 4(재리뷰)
이 루프가 무한히 반복되지 않도록 최대 2회로 제한하는 것이 좋습니다.
```

### 빈 프로젝트에서 시작하는 장점

```
1. Multi-Agent의 위력을 극적으로 체감
2. "한 번의 요청으로 프로젝트 전체 구축" 경험
3. 각 Phase의 역할이 명확히 드러남 (전부 새로 생성하므로)
4. 기존 코드와의 충돌/호환성 문제가 없어 깔끔한 학습
```

---

## ✅ 검증 체크리스트

- [ ] `@architect`, `@developer`, `@tester` Agent 생성
- [ ] `@orchestrator` Agent 생성
- [ ] **빈 프로젝트에서** `@orchestrator`에게 TODO API 전체 구현 요청
- [ ] Phase 1: database.py + models.py + schemas.py 생성됨
- [ ] Phase 2: conftest.py + CRUD 테스트 작성됨
- [ ] Phase 3: main.py에 라우트 핸들러 구현 + 테스트 통과
- [ ] Phase 4: 코드 리뷰 + 품질 점수 출력
- [ ] `pytest -v` 전체 통과
- [ ] 최종 리뷰 보고서 출력

---

## 핵심 인사이트

> **"빈 프로젝트에서 한 번의 요청으로 완성 — 그것이 Multi-Agent의 힘"**
>
> - **단일 Agent**: 설계 + 구현 + 테스트 + 리뷰를 한꺼번에 → 역할 충돌, 품질 불안정
> - **Multi-Agent**: 각 역할에 전문성과 제약을 부여 → 체계적 결과물
> - **Orchestrator 패턴**: 한 번의 요청으로 전체 파이프라인 자동 실행
> - **빈 프로젝트에서 시작**: Multi-Agent가 처음부터 끝까지 만들어내는 과정을 극적으로 체감
>
> 실제 팀에서 역할을 분담하듯, Agent에게도 역할을 나누면 더 나은 결과를 얻습니다.

---

## 다음 단계

→ [Step 8. 고급 워크플로우](../step-08-advanced/README.md)
