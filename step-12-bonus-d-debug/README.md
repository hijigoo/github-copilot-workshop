# Bonus D. Chat Debug View — AI 대화 디버깅

> ⏱️ 15분 | 난이도 ⭐~⭐⭐ | **체감: "Copilot이 왜 이렇게 답했는지 직접 들여다본다!"**
>
> 🎯 **목표**: Chat Debug View로 Copilot의 내부 동작(System Prompt, Context, Tool 호출 등)을 직접 확인하는 방법 체험

---

## 📚 사전 준비

- **메인 트랙 Step 02 이상 완료** (Copilot Chat 사용법 숙지)
- VS Code + GitHub Copilot 확장 설치 완료
- Step 06 `complete/` 코드 사용 (또는 본인이 작업 중인 코드)

---

## 📖 배경 지식: Chat Debug View란?

Chat Debug View는 Copilot에게 보낸 프롬프트가 내부적으로 어떻게 처리되는지 **원시 데이터를 직접 확인**할 수 있는 디버깅 도구입니다.

| 확인 가능한 항목 | 설명 |
|----------------|------|
| **System Prompt** | AI의 행동·능력·제약을 정의하는 지침 (Instructions 포함 여부 확인) |
| **User Prompt** | 모델에 실제로 전달된 프롬프트 텍스트 |
| **Context** | 요청에 첨부된 파일, 심볼 등 컨텍스트 항목 |
| **Response** | 모델의 전체 응답 (추론 과정 포함) |
| **Tool responses** | 요청 중 호출된 도구의 입출력 |

> 💡 "Copilot이 왜 이런 답변을 했지?", "내 Instructions가 제대로 적용된 건가?", "파일 컨텍스트가 누락된 건 아닌가?" — 이런 궁금증을 Chat Debug View로 해결할 수 있습니다.

---

## 🔍 실습 1: Chat Debug View 열기

### 1-1. 여는 방법

**방법 1 — Command Palette:**
1. `⇧⌘P` (macOS) 또는 `Ctrl+Shift+P` (Windows/Linux) 를 눌러 Command Palette를 엽니다
2. `Developer: Show Chat Debug View` 를 입력하고 선택합니다

**방법 2 — Chat 메뉴:**
1. Chat 패널 상단의 **`···` (더보기)** 메뉴를 클릭합니다
2. **"Show Chat Debug View"** 를 선택합니다

→ 에디터 하단에 Chat Debug View 패널이 열립니다.

### 관찰 포인트
- [ ] Chat Debug View 패널이 정상적으로 열리는가?

---

## 🔬 실습 2: 디버그 출력 읽기 — 각 섹션 이해하기 (5분)

> Chat Debug View가 열린 상태에서 Copilot Chat에 질문을 보내고, 각 섹션의 내용을 확인합니다.

### 2-1. 기본 질문 보내기

**💬 Copilot Chat:**
```
#file:step-06-agent/complete/app/main.py 이 파일의 첫 번째 라우터 함수를 설명해줘
```

### 2-2. Chat Debug View에서 각 섹션 펼쳐보기

| 섹션 | 내용 | 확인할 것 |
|------|------|----------|
| **System prompt** | AI의 행동, 능력, 제약을 정의하는 지침 | 커스텀 Instructions나 Agent 설명이 올바르게 들어갔는지 |
| **User prompt** | 모델에 전달된 실제 프롬프트 텍스트 | `#file:` 멘션이 실제 파일 내용으로 해석되었는지 |
| **Context** | 요청에 첨부된 파일, 심볼 등 컨텍스트 항목 | 기대한 파일과 컨텍스트가 포함되어 있는지 |
| **Response** | 모델의 전체 응답 (추론 과정 포함) | 모델이 요청을 어떻게 해석했는지 |
| **Tool responses** | 요청 중 호출된 도구의 입출력 | 도구가 올바른 입력을 받고 기대한 출력을 반환했는지 |

> 💡 Agent 모드에서는 하나의 요청에 여러 Tool이 호출될 수 있어, **Tool responses** 섹션이 특히 유용합니다.

### 관찰 포인트
- [ ] 각 섹션을 펼쳐서 내용을 확인했는가?
- [ ] User prompt에서 `#file:` 멘션이 실제 파일 내용으로 해석된 것을 확인했는가?

---

## 🛠️ 실습 3: Instructions 적용 여부 확인 (5분)

> 프로젝트의 `.github/copilot-instructions.md`가 실제로 System Prompt에 포함되는지 확인합니다.

### 3-1. 간단한 질문 보내기

**💬 Copilot Chat:**
```
간단한 Python 함수를 하나 만들어줘
```

### 3-2. System Prompt 확인

**Chat Debug View에서:**
1. **System prompt** 섹션을 펼칩니다
2. `.github/copilot-instructions.md`의 내용(예: "모든 주석은 한국어로")이 포함되어 있는지 확인합니다

> 💡 Instructions 내용이 보이지 않는다면? 파일 위치(`.github/copilot-instructions.md`)와 파일명이 정확한지, VS Code 설정에서 Copilot Instructions가 활성화되어 있는지 확인하세요.

### 관찰 포인트
- [ ] System Prompt 안에 프로젝트의 Instructions 내용이 포함되어 있는가?
- [ ] Instructions 내용이 Copilot의 응답에 실제로 반영되었는가? (예: 한국어 주석)

---

## 📂 실습 4: 컨텍스트 누락 확인 (5분)

> `#file:` 멘션으로 전달한 파일이 실제로 컨텍스트에 포함되는지 확인합니다.

### 4-1. 여러 파일 참조하여 질문

**💬 Copilot Chat:**
```
#file:step-06-agent/complete/app/main.py
#file:step-06-agent/complete/app/schemas.py
이 두 파일의 관계를 설명해줘
```

### 4-2. Context 섹션 확인

**Chat Debug View에서:**
1. **Context** 섹션을 펼칩니다
2. 두 파일(`main.py`, `schemas.py`)이 모두 컨텍스트에 포함되어 있는지 확인합니다
3. 파일이 누락되었다면 워크스페이스 인덱싱 상태를 확인합니다

### 4-3. 트러블슈팅 — AI가 워크스페이스 파일을 무시할 때

Copilot이 프로젝트 코드 대신 일반적인 답변만 할 때:

1. **Chat Debug View** → **Context** 섹션에서 워크스페이스 파일이 컨텍스트에 포함되었는지 확인
2. 파일이 없다면 `#file:` 이나 `#codebase` 멘션을 명시적으로 추가
3. 워크스페이스 인덱싱이 활성화되어 있는지 확인

### 관찰 포인트
- [ ] Context 섹션에서 기대한 파일이 모두 나타나는가?
- [ ] 파일이 누락된 경우 원인을 파악할 수 있는가?

---

## ✅ 전체 체크리스트

- [ ] Command Palette(`⇧⌘P`) 또는 Chat `···` 메뉴로 Chat Debug View를 열었다
- [ ] System Prompt, User Prompt, Context, Response, Tool responses 섹션을 확인했다
- [ ] `#file:` 멘션이 Context에 올바르게 포함되는 것을 확인했다
- [ ] Instructions 파일이 System Prompt에 포함되는 것을 확인했다
- [ ] 컨텍스트 누락 시 진단 방법을 이해했다

---

## 💡 핵심 인사이트

- **Chat Debug View**: Copilot에게 "무엇을 보냈는지(System/User Prompt, Context)"와 "무엇을 받았는지(Response, Tool 응답)"의 원시 데이터를 직접 확인할 수 있습니다. "왜 이런 답변이 나왔지?"라는 궁금증을 해소하는 가장 확실한 방법입니다.
- **핵심 원칙**: Copilot의 답변이 이상하면, Copilot을 탓하기 전에 Chat Debug View로 실제로 무엇이 전달되었는지 먼저 확인하세요.

---

## 🔗 참고 링크

- [VS Code 공식 문서 — Debug chat interactions](https://code.visualstudio.com/docs/copilot/chat/chat-debug-view)
