# Step 8. Multi-Agent 워크플로우

> ⏱️ 25분 | 난이도 ⭐⭐⭐
>
> 🎯 **핵심 학습: Custom Agent 간 역할 분담 + 자동 연쇄 호출**
>
> **체감: "Agent들이 서로 협업하며 프로젝트를 만들어간다!"**

---

## 코드 폴더

Step 7 완성 코드 (Plan + Custom Agent 조합 워크플로우) 위에서 이어서 진행합니다. 이 스텝은 README 가이드만 제공합니다.

---

## 왜 Multi-Agent인가?

Step 6에서 `@reviewer`, `@sdd`, `@refactor` 같은 Custom Agent를 **개별로** 호출했습니다.
Step 7에서는 Plan + Agent를 **순차적으로** 조합했습니다.

이번 스텝에서는 **하나의 Agent가 다른 Agent를 호출하는 연쇄 워크플로우**를 만듭니다.

| 단계 | 방식 | 비유 |
|------|------|------|
| Step 6 | 개별 Agent 호출 | 팀원 한 명에게 개별 지시 |
| Step 7 | 순차적 Agent 조합 | 팀장이 팀원에게 순서대로 지시 |
| **Step 8** | **Agent 간 연쇄 호출** | **팀이 자율적으로 협업** |

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

---

## 태스크 1: 전문 Agent 3종 만들기 (7분)

기존 Agent를 확장하거나 새로 만듭니다.

### @architect — 설계 전문

`.github/agents/architect.agent.md`:

```markdown
---
name: architect
description: "시스템 아키텍처 설계 및 스펙 정의 전문 Agent"
tools: ["read", "edit", "search"]
---

당신은 시니어 Python 아키텍트입니다.
기능 요청을 받으면 **설계 산출물만** 작성합니다.

## 역할
- app/schemas.py에 Pydantic 스펙(타입) 정의
- 아키텍처 결정 문서화 (ADR 형식)
- 파일 구조 설계

## 출력 형식
1. **설계 요약** — 변경 범위와 영향도
2. **스펙 파일** — schemas.py 수정/추가
3. **파일 구조** — 생성/수정할 파일 목록

## 제약
- 구현 코드를 직접 작성하지 마세요
- 스펙과 설계만 담당합니다
- 기존 스펙과의 호환성을 반드시 확인하세요

## 참고 파일
#file:app/schemas.py
#file:app/models.py
```

### @developer — 구현 전문

`.github/agents/developer.agent.md`:

```markdown
---
name: developer
description: "설계된 스펙을 기반으로 코드를 구현하는 전문 Agent"
tools: ["read", "edit", "search", "execute"]
---

당신은 시니어 Python 백엔드 개발자입니다.
설계된 스펙과 테스트를 기반으로 **구현만** 담당합니다.

## 역할
- app/ 아래 구현 코드 작성
- 기존 코드와의 호환성 유지
- 구현 후 pytest 실행으로 검증

## 워크플로우
1. 스펙(schemas.py) 확인
2. 테스트 파일 확인 (어떤 동작이 기대되는지)
3. 구현 코드 작성
4. `pytest -v` 실행으로 검증
5. 실패 시 수정 반복

## 제약
- 스펙(schemas.py)을 수정하지 마세요 — 그건 architect의 역할입니다
- 테스트를 수정하지 마세요 — 그건 tester의 역할입니다
- 코드가 테스트를 통과하도록 구현에만 집중하세요

## 참고 파일
#file:app/schemas.py
#file:app/models.py
#file:app/main.py
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
- pytest 실행 및 결과 보고

## 테스트 규칙
- pytest + FastAPI TestClient 사용
- 함수명: test_동작_조건_결과()
- Given-When-Then 주석 패턴
- 각 테스트는 독립적

## 출력 형식
1. **테스트 파일** — 작성된 테스트
2. **실행 결과** — pytest 출력
3. **커버리지 요약** — 테스트한 케이스 목록

## 제약
- 구현 코드를 수정하지 마세요 — 테스트가 실패하면 보고만 하세요
- 스펙을 수정하지 마세요
- 테스트 작성과 실행에만 집중하세요

## 참고 파일
#file:app/schemas.py
```

---

## 태스크 2: Orchestrator Agent 만들기 (8분)

### @orchestrator — 전체 워크플로우 지휘

`.github/agents/orchestrator.agent.md`:

```markdown
---
name: orchestrator
description: "Multi-Agent 워크플로우를 지휘하여 기능을 설계 → 테스트 → 구현 → 검증하는 총괄 Agent"
---

당신은 소프트웨어 프로젝트 매니저입니다.
기능 요청을 받으면 다음 **4단계 파이프라인**을 순서대로 실행합니다.

## 🔄 Multi-Agent 파이프라인

### Phase 1: 🏗️ 설계 (Architect 역할)
시니어 아키텍트로서:
- 기능 요구사항을 분석합니다
- app/schemas.py에 Pydantic 스펙을 추가합니다
- 영향받는 파일 목록을 정리합니다
- ✅ 완료 시 "Phase 1 완료: [설계 요약]"을 출력합니다

### Phase 2: 🧪 테스트 (Tester 역할)
시니어 QA 엔지니어로서:
- Phase 1의 스펙을 기반으로 테스트를 작성합니다
- 정상/에러/경계값 케이스를 포함합니다
- pytest + FastAPI TestClient 사용
- test_동작_조건_결과() 네이밍, Given-When-Then 주석
- ✅ 완료 시 "Phase 2 완료: [테스트 N개 작성]"을 출력합니다

### Phase 3: 💻 구현 (Developer 역할)
시니어 백엔드 개발자로서:
- Phase 1의 스펙과 Phase 2의 테스트를 모두 통과하도록 구현합니다
- 기존 코드와의 호환성을 유지합니다
- 구현 후 `pytest -v` 실행
- 실패 시 수정 반복
- ✅ 완료 시 "Phase 3 완료: [구현 요약]"을 출력합니다

### Phase 4: 🔍 리뷰 (Reviewer 역할)
시니어 코드 리뷰어로서:
- Phase 3의 구현 코드를 점검합니다
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

## 참고 파일
#file:app/schemas.py
#file:app/models.py
#file:app/main.py
```

---

## 태스크 3: Multi-Agent 실행 (10분)

### 3-1. Orchestrator로 새 기능 구현

Chat 하단의 Agent 선택 버튼에서 `orchestrator`를 선택한 후:

```
TODO 앱에 "즐겨찾기(favorite)" 기능을 추가해줘.

요구사항:
- TODO에 즐겨찾기 여부(is_favorite) 필드 추가
- PATCH /api/v1/todos/{id}/favorite 로 즐겨찾기 토글
- GET /api/v1/todos?favorite=true 로 즐겨찾기만 필터링
- 즐겨찾기된 TODO가 목록 상단에 표시
```

### 3-2. 파이프라인 관찰

Agent가 4단계를 순서대로 실행하는 과정을 관찰합니다:

| Phase | Agent 역할 | 기대 산출물 |
|-------|-----------|-----------|
| 1 | Architect | schemas.py에 `is_favorite` 필드 + 필터/정렬 스펙 |
| 2 | Tester | 즐겨찾기 토글, 필터링, 정렬 테스트 |
| 3 | Developer | main.py, models.py 구현 + pytest 통과 |
| 4 | Reviewer | 코드 품질 리뷰 + 개선 사항 |

### 3-3. 개별 Agent와 비교

같은 기능을 **개별 Agent**로 구현할 때와 비교해 보세요:

```
# 이전 방식 (Step 6): 수동으로 하나씩 호출
@architect  → 설계해줘
@tester     → 테스트 작성해줘
@developer  → 구현해줘
@reviewer   → 리뷰해줘

# Multi-Agent 방식 (Step 8): 한 번에 전체 파이프라인
@orchestrator → 즐겨찾기 기능 추가해줘
```

### 관찰 포인트
- [ ] Phase 간 전환이 자연스러운가?
- [ ] 각 Phase의 제약이 지켜지는가? (예: Architect가 구현을 하지 않는지)
- [ ] Phase 3에서 테스트 실패 시 수정을 반복하는가?
- [ ] Phase 4에서 Critical 이슈 발견 시 회귀하는가?
- [ ] 최종 결과물의 품질이 개별 호출보다 나은가?

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

---

## ✅ 검증 체크리스트

- [ ] `@architect`, `@developer`, `@tester` Agent 생성
- [ ] `@orchestrator` Agent 생성
- [ ] `@orchestrator`에게 새 기능 요청 시 4단계 파이프라인이 순서대로 실행
- [ ] Phase 간 역할 분리가 지켜짐
- [ ] 테스트 실패 시 Developer가 수정을 반복
- [ ] 리뷰에서 Critical 이슈 발견 시 회귀 처리
- [ ] `pytest -v` 전체 통과
- [ ] 최종 리뷰 보고서 출력

---

## 핵심 인사이트

> **"Agent에게 역할을 나누면 품질이 올라간다"**
>
> - **단일 Agent**: 설계 + 구현 + 테스트 + 리뷰를 한꺼번에 → 역할 충돌, 품질 불안정
> - **Multi-Agent**: 각 역할에 전문성과 제약을 부여 → 체계적 결과물
> - **Orchestrator 패턴**: 한 번의 요청으로 전체 파이프라인 자동 실행
> - **회귀 루프**: 리뷰 → 수정 → 재리뷰로 품질을 반복 개선
>
> 실제 팀에서 역할을 분담하듯, Agent에게도 역할을 나누면 더 나은 결과를 얻습니다.

---

## 다음 단계

→ [Step 9. Spec-Driven Development](../step-09-spec-driven/README.md)

또는 **보너스 트랙**으로 넘어가세요:
- **[Step 10 — Docker](../step-10-bonus-a-docker/README.md)**: Copilot으로 Docker 컨테이너화
- **[Step 11 — React 프론트엔드](../step-11-bonus-b-react/README.md)**: TODO 앱 UI 만들기
- **[Step 12 — Spring Boot](../step-12-bonus-c-spring/README.md)**: Java로 같은 API 구현
- **[Step 13 — Chat Debug View](../step-13-bonus-d-debug/README.md)**: Copilot 내부 동작 분석
- **[Step 14 — Spec Kit](../step-14-bonus-e-speckit/README.md)**: Spec-Driven Development 자동화
