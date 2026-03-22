# Step 8. Sub-Agent 워크플로우

> ⏱️ 25분 | 난이도 ⭐⭐⭐
>
> 🎯 **핵심 학습: VS Code Sub-Agent 기능으로 Custom Agent 자동 위임**
>
> **체감: "복잡한 작업을 요청하면 Copilot이 알아서 전문 Agent에게 위임한다!"**
>
> 📖 **공식 문서**: [VS Code Sub-Agents](https://code.visualstudio.com/docs/copilot/agents/subagents)

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | **빈 FastAPI 프로젝트** (main.py에 app 인스턴스만 존재) — 여기서 시작하세요 |

> 💡 **왜 처음부터?**
> 앞 스텝에서 만든 TODO API 코드를 **모두 지우고** 빈 프로젝트에서 시작합니다.
> Sub-Agent가 복잡한 작업을 **전문 Agent에게 위임**하여 처리하는 과정을 체험하기 위해서입니다.

---

## 왜 Sub-Agent인가?

Step 7에서 `reviewer`, `builder`, `refactor` 같은 Custom Agent를 **개별로** 선택하여 호출했습니다.

이번 스텝에서는 VS Code의 **Sub-Agent 기능**을 사용하여, Copilot이 복잡한 작업을 수행할 때 **기존 Custom Agent를 자동으로 위임 호출**하는 방식을 실습합니다.

| 단계 | 방식 | 비유 |
|------|------|------|
| Step 7 | 개별 Agent 직접 호출 | 팀원 한 명에게 개별 지시 |
| **Step 8** | **Sub-Agent 자동/직접 위임** | **팀장이 적합한 팀원에게 알아서 업무 배분** |
| Step 9 | Plan + Agent 조합 | 팀장이 계획 후 팀원에게 순서대로 지시 |

---

## 개념: Sub-Agent란?

### Sub-Agent 기능 개요

Sub-Agent는 VS Code에 내장된 기능으로, **복잡한 작업을 격리된 컨텍스트 윈도우에서 독립적으로 수행**하는 메커니즘입니다.

```
메인 Chat 세션
  │
  ├── 🔀 Sub-Agent 위임: builder
  │     └── 격리된 컨텍스트에서 기능 구현 수행
  │     └── 결과를 메인 세션에 반환
  │
  ├── 🔀 Sub-Agent 위임: reviewer
  │     └── 격리된 컨텍스트에서 코드 리뷰 수행
  │     └── 결과를 메인 세션에 반환
  │
  └── 최종 결과 종합
```

### 핵심 특징

| 특징 | 설명 |
|------|------|
| **격리된 컨텍스트** | Sub-Agent는 자체 컨텍스트 윈도우에서 독립적으로 작동 |
| **사용자 개입 없음** | 중간에 사용자 피드백을 요청하지 않고 끝까지 실행 |
| **결과 반환** | 작업 완료 후 결과를 메인 세션에 반환 |
| **기본 상속** | 기본적으로 메인 세션의 도구와 AI 모델을 상속하며, Custom Agent는 자체 모델·도구로 재정의 가능 |

### Sub-Agent의 활용 시나리오

- 복잡한 멀티스텝 작업을 메인 세션 방해 없이 위임
- 대량의 정보 처리 시 메인 컨텍스트 윈도우 오염 방지
- 서로 다른 접근 방식을 독립적으로 탐색

### 위임 방식 2가지

| 방식 | 설명 | 예시 |
|------|------|------|
| **Agent 주도 위임** | 메인 Agent가 작업의 복잡성을 판단하여, 격리된 컨텍스트가 유리한 부분을 적합한 Agent에게 자동 위임 | "이 코드를 리뷰해줘" → `reviewer` 자동 호출 |
| **사용자 힌트 호출** | 프롬프트에서 명시적으로 Sub-Agent 사용을 지시 | "reviewer Agent를 Sub-Agent로 사용해서 리뷰해줘" |

> 💡 **Custom Agent의 `description` 필드가 중요합니다!**
> 자동 위임 시 Copilot은 Agent의 이름과 `description`을 보고 어떤 Agent에게 위임할지 결정합니다.

> ⚠️ **Custom Agent를 Sub-Agent로 사용하는 기능은 실험적(Experimental) 기능입니다.**
>
> Custom Agent의 frontmatter에서 Sub-Agent 호출을 제어할 수 있습니다:
> - `user-invocable: false` — Agent 드롭다운에 표시하지 않고 Sub-Agent로만 사용
> - `disable-model-invocation: true` — 다른 Agent가 이 Agent를 Sub-Agent로 호출하지 못하도록 차단

```markdown
---
name: internal-helper
user-invocable: false (default: True)
disable-model-invocation: true (default: False)
---

This agent can only be invoked as a subagent.

```
---

## 사전 준비: Sub-Agent 활성화

### 1. `runSubagent` 도구 활성화 확인

Sub-Agent를 사용하려면 `runSubagent` 도구가 활성화되어 있어야 합니다.

1. Chat 패널에서 **Agent 모드** 선택
2. 도구 아이콘을 클릭하여 도구 목록에서 `Agent` (또는 `runSubagent`) 도구가 활성화되어 있는지 확인

![도구 활성화 확인](../screenshot/step08-run-subagent-tool.png)

> 💡 Agent 모드에서는 기본적으로 `runSubagent` 도구가 활성화되어 있습니다.
> Custom Agent에서 Sub-Agent를 사용하려면 frontmatter의 `tools`에 `agent`를 포함하세요.
>
> ```markdown
> ---
> tools: ['agent', 'edit', 'search', 'read']
> ---
> ```

### 2. Step 7의 Custom Agent 확인

Sub-Agent는 **새로운 Agent를 만들지 않습니다.** Step 7에서 이미 만든 Custom Agent를 그대로 사용합니다.

`.github/agents/` 폴더에 다음 Agent가 있는지 확인하세요:

```
.github/agents/
├── reviewer.agent.md      → reviewer: 코드 리뷰 전문
├── builder.agent.md       → builder: 기능 구현 전문
└── refactor.agent.md      → refactor: 리팩토링 전문
```

> ⚠️ Agent 파일이 없다면 [Step 7](../step-07-custom-agent/README.md)으로 돌아가 먼저 생성하세요.



## 태스크 1: 자동 위임 체험하기 (10분)

Agent 모드에서 `runSubagent` 도구가 활성화되어 있으면, Copilot 메인 세션에 요청을 보낼 때 **적합한 Custom Agent에게 자동으로 위임**할 수 있습니다.

Chat에서 (Agent를 선택하지 않고) 기본 상태로 다음을 입력합니다:

```
프로젝트 전체 코드를 리뷰하고 개선 사항을 알려줘
```

**관찰 포인트**: Copilot이 `reviewer`의 `description`("코드 리뷰를 수행하는 시니어 Python 개발자 Agent")을 인식하고, 리뷰 작업을 `reviewer` Sub-Agent에게 자동으로 위임하는지 확인합니다.

![Sub-Agent 자동 위임](../screenshot/step08-auto-delegation.png)


---

## 태스크 2: 직접 호출로 Sub-Agent 위임하기 (15분)

태스크 1에서는 Copilot이 자동으로 Agent를 선택했습니다. 이번에는 프롬프트에서 **명시적으로 Sub-Agent를 지정**하여 호출합니다.

Chat에서 (Agent를 선택하지 않고) 기본 상태로 다음을 입력합니다:

```
reviewer Sub-Agent를 사용해서 프로젝트 전체 코드를 리뷰하고 개선 사항을 알려줘
```

**관찰 포인트**: 프롬프트에서 명시적으로 `reviewer`를 지정했을 때, `reviewer` Sub-Agent가 격리된 컨텍스트에서 독립적으로 리뷰를 수행하고, 결과를 메인 세션에 반환하는지 확인합니다.


---

## 태스크 3: 멀티 Sub-Agent 연쇄 워크플로우 (10분)

**하나의 프롬프트에서 여러 Sub-Agent를 순서대로 위임**하는 핵심 패턴을 실습합니다:

```
빈 FastAPI 프로젝트(starter/)에 TODO API를 처음부터 만들어줘.

1단계: builder Sub-Agent를 사용해서 TODO CRUD API를 구현해줘
  - Todo 모델: id, title, description, completed, created_at, updated_at
  - CRUD: POST(201)/GET(페이지네이션)/GET(id)/PATCH/DELETE(204)
  - title 필수(1~200자), completed 기본값 False, 없는 id는 404
  - 한글 주석/docstring 포함

2단계: reviewer Sub-Agent를 사용해서 구현된 코드를 리뷰해줘

3단계: refactor Sub-Agent를 사용해서 리뷰 결과를 반영하여 개선해줘
```

> 💡 **Coordinator 패턴**: Custom Agent `.agent.md` 파일의 frontmatter에 `agents` 속성을 지정하면, 해당 Agent만 Sub-Agent로 사용하도록 제한할 수 있습니다.
>
> ```markdown
> ---
> name: todo-builder
> tools: ['agent', 'edit', 'search', 'read']
> agents: ['builder', 'reviewer', 'refactor']
> ---
> ```

### 관찰 포인트
- [ ] Copilot이 `builder` → `reviewer` → `refactor` 순서로 Sub-Agent에게 위임하는가?
- [ ] 각 Sub-Agent가 자신의 `.agent.md` 규칙을 따르는가?
- [ ] `pytest -v` 전체 통과하는가?

---

## ✅ 검증 체크리스트

- [ ] Agent 모드에서 **`runSubagent` 도구** 활성화 확인
- [ ] Step 7의 `reviewer`, `builder`, `refactor` Agent 존재 확인
- [ ] 자동 위임 또는 직접 호출로 Sub-Agent 위임 동작 확인
- [ ] 하나의 프롬프트에서 여러 Sub-Agent 연쇄 위임 실행
- [ ] `pytest -v` 전체 통과

---

## 핵심 인사이트

> **"새 Agent를 만들지 않는다 — 기존 Agent를 위임한다"**
>
> - **Step 7**: Custom Agent를 만들고 **직접 선택**하여 호출
> - **Step 8**: 같은 Agent를 **Sub-Agent로 자동/직접 위임** — 격리된 컨텍스트에서 독립 실행
> - **자동 위임**: Agent의 `description`이 핵심 — Copilot이 매칭하여 적합한 Agent 선택
> - **직접 호출**: 프롬프트에서 "~~ Sub-Agent를 사용해서"로 명시적 지정
>
> 복잡한 작업을 여러 전문 Agent에게 위임하면, 메인 컨텍스트를 깔끔하게 유지하면서 체계적인 결과를 얻습니다.

---

## 다음 단계

→ [Step 9. 고급 워크플로우](../step-09-advanced/README.md)
