# Step 9. 고급 워크플로우 — Plan 기능 + Custom Agent 조합

> ⏱️ 25분 | 난이도 ⭐⭐⭐
>
> 🎯 **핵심 학습: Copilot Plan 기능으로 체계적 개발**
>
> **체감: "큰 기능도 체계적으로!"****

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | **빈 FastAPI 프로젝트** (requirements.txt, main.py에 app 인스턴스만 존재) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

> 💡 **왜 처음부터?**
> 앞 스텝에서 만든 TODO API 코드를 **모두 지우고** 빈 프로젝트에서 시작합니다.
> Plan 기능 + Agent 조합으로 설계 → 테스트 → 구현 → 리뷰를 **처음부터 끝까지** 자동으로 수행하는 과정을 체험하기 위해서입니다.

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

## 태스크: Plan → 구현 (25분)

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
- Agent가 빈 프로젝트를 분석하고 필요한 파일 구조(`models.py`, `schemas.py`, `main.py`)를 설계하는 과정
- 3개 기능을 처음부터 만들 때 구현 순서와 의존성을 어떻게 정리하는지 (기본 CRUD → 카테고리 → 통계 → 검색 순서 등)
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

### Step 3 — Production-Ready 보강

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

Step 1 → 3을 이어서 진행하다 보면 대화가 매우 길어집니다.
Agent의 응답 품질이 떨어지는 것을 느끼면 — 이것이 **Context Rot**입니다.

**징후**: 이전에 만든 코드를 무시함, 같은 실수를 반복함, 엉뚱한 파일을 수정함

**해결법:**

```
/clear
```

초기화 후 핵심 파일만 참조하여 재시작:

```
#file:app/main.py #file:app/schemas.py #file:app/models.py

위 파일들을 기반으로, CORS 미들웨어와 health check 엔드포인트를 추가해주세요.
```

---

## ✅ 검증 체크리스트

- [ ] Plan 기능으로 3개 기능의 구현 계획을 세움
- [ ] 카테고리 시스템 구현 + 테스트 통과
- [ ] 통계 API 구현 + 테스트 통과
- [ ] 검색 기능 구현 + 테스트 통과
- [ ] Production-ready 기능 추가 (CORS, health check, logging)

---

## 핵심 인사이트

> **"Plan으로 방향을 잡고, Agent로 실행하라"**
>
> - **Plan 기능**: 큰 작업은 바로 코딩하지 않고 계획부터 세운다
> - **기능별 반복**: 한 번에 다 만들지 않고 구현 → 검증을 반복한다

---

## 다음 단계

축하합니다! 🎉 메인 트랙의 모든 단계를 완료했습니다!

**보너스 트랙**으로 넘어가세요:
→ [Step 10. Spec-Driven Development](../step-10-spec-driven/README.md)

또는 원하는 보너스 트랙을 선택하세요:
- **[Step 11 — README 문서화](../step-11-bonus-readme/README.md)**: Copilot으로 프로젝트 README + Mermaid 다이어그램 생성
- **[Step 12 — Docker](../step-12-bonus-a-docker/README.md)**: Copilot으로 Docker 컨테이너화
- **[Step 13 — React.js 프론트엔드](../step-13-bonus-b-react/README.md)**: TODO API를 소비하는 React UI
