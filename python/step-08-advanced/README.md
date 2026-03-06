# Step 8. 고급 워크플로우 — Plan 기능 + Custom Agent 조합

> ⏱️ 25분 | 난이도 ⭐⭐⭐
>
> 🎯 **핵심 학습: Copilot Plan 기능, Custom Agent 조합, Context Rot 관리**
>
> **체감: "큰 기능도 체계적으로!"**

---

## 이전 단계 코드

`starter/` = Step 7 완성 코드 (Custom Agent 3종 포함: `@reviewer`, `@sdd`, `@refactor`)

---

## Copilot Plan 기능이란?

Agent 모드에서 Copilot에게 큰 작업을 요청하면, 바로 코드를 생성하는 대신
**구현 계획(Plan)을 먼저 제시**하도록 할 수 있습니다.

- Chat 입력창 하단 **도구 선택 버튼**(🔧)에서 `Plan` 도구를 활성화
- 또는 프롬프트에 "계획만 세워줘, 구현은 하지 마" 라고 명시

Plan이 생성되면 각 단계를 **리뷰하고 수정한 뒤** 구현을 진행할 수 있습니다.

> 📸 **스크린샷**: Agent가 Plan을 생성하여 단계별 체크리스트를 보여주는 모습
> ![Plan 기능](./assets/plan-phase-output.png)

---

## 태스크: Plan → 구현 → 리뷰 (25분)

### Step 1 — Plan으로 계획 수립

Plan 모드 Chat에 입력:

```
TODO 앱에 다음 3가지 기능을 추가하려고 해:

1. 카테고리 시스템 — TODO에 카테고리를 지정할 수 있게
2. 통계 API — 카테고리별 완료율, 우선순위 분포
3. 검색 기능 — 제목/설명 키워드 검색

각 기능에 대해 필요한 파일 변경, 스키마, 테스트 케이스를 정리해줘.
```

**관찰 포인트:**
- Agent가 기존 코드 구조(`models.py`, `schemas.py`, `main.py`)를 파악하는 과정
- 3개 기능 간 의존성을 어떻게 정리하는지 (카테고리 → 통계 순서 등)
- 제시한 테스트 케이스가 충분한지

### Step 2 — 구현

계획을 확인했으면 구현을 시작합니다. 두 가지 방법 중 선택하세요:

#### 방법 A: `Start Implementation` 버튼 (한 번에 실행)

Plan 결과 하단의 **`Start Implementation`** 버튼을 클릭하면, 계획 전체를 순서대로 자동 실행합니다.

Agent가 3개 기능을 모두 구현하고 테스트까지 통과시키는 과정을 지켜보세요.

#### 방법 B: Chat에서 기능별로 요청 (단계적 실행)

기능을 하나씩 나눠서 진행하고 싶다면 Chat에서 직접 요청합니다:

```
위 계획에 따라 1번 카테고리 시스템부터 구현해줘.
테스트도 작성하고 pytest -v로 통과까지 확인해줘.
```

통과를 확인한 뒤 다음 기능으로 넘어갑니다:

```
다음으로 2번 통계 API를 구현해줘. 구현 후 테스트까지 통과시켜줘.
```

같은 방식으로 3번 검색 기능까지 반복합니다.

> 💡 **핵심**: 한 번에 모든 것을 요청하지 않고, **기능별로 구현 → Agent가 테스트 검증 → 다음**을 반복합니다.

### Step 3 — reviewer 에이전트로 코드 리뷰

3개 기능을 모두 구현하고 전체 테스트가 통과하면, Step 7에서 만든 `reviewer` 에이전트로 품질을 점검합니다.

Chat 하단의 Agent 선택 버튼에서 `reviewer`를 선택한 후:

```
#file:app/main.py 이 코드를 리뷰해줘. 카테고리/통계/검색 기능이 새로 추가됐어.
```

**관찰 포인트:**
- Critical / Warning / Suggestion 분류가 적절한지
- 보안·성능·유지보수 관점의 피드백 품질
- 수정 제안이 구체적이고 실행 가능한지

리뷰에서 지적된 사항은 Agent 모드로 돌아가서 수정을 요청합니다:

```
리뷰 피드백을 반영해줘. 수정 후 pytest 실행해서 회귀 테스트도 확인해줘.
```

### Step 4 — Production-Ready 보강

다시 Agent 모드로 전환하여 production 기능을 추가합니다.

```
TODO 앱에 production-ready 기능을 추가해줘:
- CORS 설정 (localhost:5173, localhost:3000)
- Health check 엔드포인트 (GET /health)
- 요청/응답 로깅 미들웨어
- structured logging 설정

테스트도 업데이트하고 전체 통과까지.
```

구현이 완료되면 서버를 실행합니다:

```
서버 띄워줘.
```

Agent가 서버를 실행하면 http://localhost:8000/docs 에 접속하여 카테고리, 통계, 검색, health check 엔드포인트를 확인합니다.

### 💡 Context Rot과 `/clear`

Step 1 → 4를 이어서 진행하다 보면 대화가 매우 길어집니다.
Agent의 응답 품질이 떨어지는 것을 느끼면 — 이것이 **Context Rot**입니다.

**징후**: 이전에 만든 코드를 무시함, 같은 실수를 반복함, 엉뚱한 파일을 수정함

**해결법:**

```
/clear
```

초기화 후 핵심 파일만 참조하여 재시작:

```
#file:app/main.py #file:app/models.py #file:app/schemas.py

위 파일들을 기반으로, CORS 미들웨어와 health check 엔드포인트를 추가해주세요.
```

---

## ✅ 검증 체크리스트

- [ ] Plan 기능으로 3개 기능의 구현 계획을 세움
- [ ] 카테고리 시스템 구현 + 테스트 통과
- [ ] 통계 API 구현 + 테스트 통과
- [ ] 검색 기능 구현 + 테스트 통과
- [ ] `reviewer` 에이전트로 코드 리뷰 수행 및 피드백 반영
- [ ] Production-ready 기능 추가 (CORS, health check, logging)
- [ ] Context Rot 발생 시 `/clear`로 해결하는 경험

---

## 🔧 에러가 나면? — 고급 디버깅 전략

복잡한 작업일수록 에러도 복잡합니다. 상황에 맞는 방법을 선택하세요.

### Context Rot이 의심될 때

대화가 길어져서 Copilot이 엉뚱한 코드를 생성하면:
1. `/clear`로 컨텍스트 초기화
2. 에러 메시지와 관련 파일만 새로 지정해서 질문:
   ```
   새 대화야. #file:app/main.py #file:tests/test_todos.py
   pytest가 실패하고 있어. 분석해서 수정해줘
   ```

### 여러 파일에 걸친 에러일 때

Agent 모드에서:
```
터미널에 에러가 났어. 관련 파일 모두 확인해서 수정해줘
```
> Agent가 다중 파일을 동시에 분석하고 수정합니다.

### 테스트가 부분적으로 실패할 때

```
pytest에서 3개 중 1개만 실패해. 실패하는 테스트만 분석해서 구현을 수정해줘
```

> 💡 이 단계까지 오셨다면 지금까지 배운 모든 기능(Chat, `/fix`, Agent, Custom Agent)을 조합해서 문제를 해결할 수 있습니다.

---

## 핵심 인사이트

> **"Plan으로 방향을 잡고, Agent로 실행하고, Custom Agent로 검증하라"**
>
> - **Plan 기능**: 큰 작업은 바로 코딩하지 않고 계획부터 세운다
> - **기능별 반복**: 한 번에 다 만들지 않고 구현 → 검증을 반복한다
> - **역할 분담**: `reviewer` 에이전트로 리뷰, Agent 모드로 수정
> - **Context Rot**: 대화가 길어지면 `/clear`로 초기화, 파일 참조만 새로 지정

---

## 다음 단계

축하합니다! 🎉 메인 트랙의 모든 단계를 완료했습니다!

**보너스 트랙**으로 넘어가세요:
→ [Step 9. Multi-Agent 워크플로우](../step-09-multi-agent/README.md)

또는 **보너스 트랙**으로 넘어가세요:
- **[Step 10 — Docker](../step-10-bonus-a-docker/README.md)**: Copilot으로 Docker 컨테이너화
- **[Step 11 — React.js 프론트엔드](../step-11-bonus-b-react/README.md)**: TODO API를 소비하는 React UI
- **[Step 12 — Spring Boot 백엔드](../step-12-bonus-c-spring/README.md)**: Java로 같은 API 구현
- **[Step 13 — Chat Debug View](../step-13-bonus-d-debug/README.md)**: Copilot 내부 동작 분석
- **[Step 14 — Spec Kit](../step-14-bonus-e-speckit/README.md)**: Spec-Driven Development 자동화
