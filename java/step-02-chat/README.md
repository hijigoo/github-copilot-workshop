# Step 2. Copilot Chat

> ⏱️ 20분 | 난이도 ⭐
>
> 🎯 **핵심 학습: Chat 패널 + `@`, `#`, `/` 명령어**
>
> **체감: "대화로 코드를 다룰 수 있다!"**

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | Step 1 완성 코드 (인메모리 CRUD TODO API) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

---

## 왜 두 번째인가?

Step 1에서 수동으로 코드를 작성했으니, 이제 **대화**로 코드를 다루는 경험을 합니다.
"검색 + 코딩 + 질문"이 한 곳에서 해결됩니다.

---

## Chat 열기

| IDE | 방법 |
|-----|------|
| IntelliJ | 우측 사이드바 > GitHub Copilot Chat |

> 📸 **[IntelliJ 스크린샷]** IntelliJ 우측 사이드바에서 GitHub Copilot Chat 탭을 클릭하여 여는 모습
>
> ![Chat 패널 열기](./images/step02-open-chat.png)

---

## Chat 패널 UI 구성

### 입력창 구성

Chat 입력창 주변에는 다음 요소들이 있습니다:

| 요소 | 설명 |
|------|------|
| 📎 (클립 아이콘) | 파일을 드래그하거나 첨부하여 컨텍스트로 전달합니다 |
| 파일 태그 (예: `application.properties`) | 현재 참조 중인 파일. "끄기"를 클릭하면 제외할 수 있습니다 |
| 입력창 | `#`, `@`, `/` 키를 눌러 컨텍스트 추가, 확장 기능, 명령어를 사용할 수 있습니다 |
| 모델 선택기 (예: `Claude Sonnet 4.5`) | 응답에 사용할 AI 모델을 변경할 수 있습니다 |

> 📸 **[IntelliJ 스크린샷]** Chat 입력창의 각 UI 요소 — 클립 아이콘, 파일 태그, 힌트 텍스트, 모드 선택기, 모델 선택기
>
> ![Chat 입력창 구성](./images/step02-chat-input-ui.png)

### 모드 선택 (Ask 드롭다운)

입력창 좌측 하단의 **모드 선택 드롭다운**을 클릭하면 4가지 모드를 선택할 수 있습니다:

| 모드 | 설명 | 이 워크샵에서 배우는 시점 |
|------|------|----------------------|
| **Ask** | 질문/답변 모드. 코드를 직접 수정하지 않고 답변만 합니다 | **이번 Step 2** |
| **Edit** | 지정한 파일들을 직접 편집합니다. 변경할 파일을 선택할 수 있습니다 | Step 5 |
| **Agent** | 자율적으로 파일 생성/수정/삭제 + 터미널 실행까지 수행합니다 | Step 5 |
| **Plan** | 구현 계획을 먼저 세우고, 승인 후 실행합니다 | Step 7 |

> 📸 **[IntelliJ 스크린샷]** Ask 드롭다운을 클릭하면 Ask, Edit, Agent, Plan 4가지 모드가 표시되는 화면
>
> ![모드 선택 드롭다운](./images/step02-mode-dropdown.png)

---

## `#`, `@`, `/` — Chat 명령어 기본 개념

Chat 입력창에는 `Add context (#), extensions (@), commands (/)` 힌트가 표시됩니다.
이 세 가지 특수 기호를 조합하여 Copilot과 대화합니다.

| 기호 | 역할 | 설명 | 예시 |
|------|------|------|------|
| `#` | **컨텍스트 추가** (context) | 특정 파일, 폴더, 또는 Tool을 선택하여 전달합니다 | `#file:TodoController.java` |
| `@` | **확장 기능** (extensions) | Copilot 확장 기능을 호출합니다 | `@project`, `@github` |
| `/` | **명령어** (commands) | Copilot에게 수행할 작업을 지시합니다 | `/explain`, `/fix`, `/tests` |

### `@` 확장 기능 (Extensions)

| 확장 | 설명 |
|------|------|
| `@project` | **프로젝트 컨텍스트** — 현재 프로젝트의 파일 구조, 의존성, 코드를 분석하여 맞춤 답변을 제공합니다 (VS Code의 `@workspace`에 해당) |
| `@github` | **GitHub 스킬** — 웹 검색, 코드 검색 등 GitHub 관련 기능을 활용합니다. `@github #web 최신 Node.js LTS 버전은?` 처럼 웹 검색도 가능합니다 |
| `@github-copilot-coding-agent` | **코딩 에이전트** — GitHub 원격 환경에서 코딩 작업을 수행하는 에이전트를 호출합니다 |

### `/` 명령어 (Commands)

| 명령어 | 설명 |
|--------|------|
| `/explain` | 선택한 코드 또는 현재 파일의 동작을 설명합니다 |
| `/fix` | 선택한 코드의 문제를 분석하고 수정을 제안합니다 |
| `/tests` | 선택한 코드에 대한 단위 테스트를 생성합니다 |
| `/help` | GitHub Copilot 사용법에 대한 간단한 가이드를 보여줍니다 |

> 💡 `/`를 입력하면 사용 가능한 모든 명령어 목록이 표시됩니다.

> 📸 **[IntelliJ 스크린샷]** Chat 입력창에 표시되는 `Add context (#), extensions (@), commands (/)` 힌트
>
> ![Chat 입력 힌트](./images/step02-chat-hint.png)

### 조합 예시

```
@project /explain #file:TodoController.java
```
→ "**프로젝트**를 참고하여, **TodoController.java**를 **설명해줘**"

> 💡 세 기호를 모두 쓸 필요는 없습니다. 필요한 것만 조합하면 됩니다.

---

## 태스크 A: `@` — 프로젝트 맥락 질문 (3분)

> 💡 이 태스크는 **Ask 모드**에서 진행합니다. 좌측 하단 모드 드롭다운이 `Ask`인지 확인하세요.

Chat에 입력:

```
@project 이 프로젝트에 Spring Data JPA를 적용하려면 어떻게 해야 하나요?
```

> 💡 IntelliJ에서는 `@project`를 사용합니다 (VS Code의 `@workspace`에 해당)

> 📸 **[IntelliJ 스크린샷]** Chat 입력창에 `@project` 명령을 입력하고 프로젝트 맥락이 반영된 답변을 받는 화면
>
> ![@project 사용](./images/step02-at-project.png)

**관찰**: `@project`가 프로젝트의 파일 구조와 의존성을 분석하여 맞춤 답변을 합니다.

---

## 태스크 B: `#` — 코드 설명 받기 (3분)

> 💡 이 태스크도 **Ask 모드**에서 진행합니다.

Chat에 입력:

```
/explain #file:TodoController.java 한국어로 설명해줘
```

> 📸 **[IntelliJ 스크린샷]** Chat에서 `#file:TodoController.java`로 파일을 지정하여 코드 설명을 받는 화면
>
> ![#file 코드 설명](./images/step02-file-explain.png)

**관찰**: `#file:`로 파일을 지정하면 Copilot이 해당 파일의 구조와 각 엔드포인트의 역할을 한국어로 설명합니다.

---

## 태스크 C: `/fix` — 버그 수정 (5분)

> ⚠️ 이 태스크는 **Agent 모드**로 전환해야 합니다. 좌측 하단의 모드 드롭다운에서 `Agent`를 선택하세요.

1. `TodoController.java`의 `createTodo` 메서드에서 **의도적 버그** 삽입:

```java
// 이 부분을 일부러 잘못 고치세요:
Todo newTodo = new Todo();
newTodo.setId(nextId++);
newTodo.setTitle(request.getDescription());  // ← 버그! title이 아니라 description
```

2. 버그가 있는 코드를 선택하고 Agent 모드 Chat에 입력:

```
/fix
```

> 📸 **[IntelliJ 스크린샷]** 버그가 있는 코드를 선택한 상태에서 `/fix` 명령을 실행하고 Copilot이 수정 제안을 하는 화면
>
> ![/fix 명령](./images/step02-fix-command.png)

**관찰**: Copilot이 잘못된 필드 매핑과 기본값을 정확히 찾아냅니다.

---

## 태스크 D: `/tests` — 테스트 코드 생성 (5분)

> ⚠️ 이 태스크도 **Agent 모드**에서 진행합니다. (태스크 C에서 이미 전환했다면 그대로 유지)

Agent 모드 Chat에 입력:

```
/tests #file:TodoController.java
```

> 📸 **[IntelliJ 스크린샷]** `/tests` 명령으로 Copilot이 JUnit 5 + MockMvc 기반 테스트 코드를 자동 생성하는 화면
>
> ![/tests 명령](./images/step02-tests-command.png)

**관찰**: Copilot이 JUnit 5 + MockMvc 기반 테스트를 작성합니다.

### 생성된 테스트 실행

**방법 1: IntelliJ에서 실행 (권장)**

생성된 테스트 파일을 열고 클래스명 옆의 ▶️ 실행 버튼을 클릭합니다.

**방법 2: 터미널에서 실행**

```bash
./gradlew test
```

> 💡 JDK 관련 에러가 나면 경로를 직접 지정하세요:
> ```bash
> # macOS
> ./gradlew test -Dorg.gradle.java.home=/opt/homebrew/opt/openjdk@17
>
> # Windows (PowerShell)
> .\gradlew test -Dorg.gradle.java.home="C:\Program Files\Eclipse Adoptium\jdk-17"
> ```

---

## ✅ 검증 체크리스트

- [ ] `@project` 질문에 프로젝트 맥락이 반영된 답변 확인
- [ ] `#file:`로 코드 설명 받음
- [ ] `/fix`로 의도적 버그 수정
- [ ] `/tests`로 테스트 파일 생성 후 `./gradlew test` 통과

---

## 🔧 에러가 나면? — 이 단계에서 배운 기능으로 해결!

### `/fix` 사용하기

에러가 난 파일을 열고 Chat에 입력:
```
/fix #file:TodoController.java
```

### 에러 메시지를 직접 붙여넣기

```
이 에러 수정해줘:
JUnit에서 AssertionError가 나는데, 응답 필드가 expected와 다르대
```

> 💡 `#file:`로 관련 파일을 지정하면 더 정확한 답을 얻습니다.
> 그래도 안 되면 `complete/` 폴더의 코드와 비교해 보세요.

---

## 핵심 인사이트

> **"`#file`로 범위를 좁혀라"**
>
> Copilot에게 프로젝트 전체를 보여주면 답이 흐려집니다.
> `#file:TodoController.java` 처럼 관련 파일만 참조하면 훨씬 정확한 답을 얻습니다.

---

## 다음 단계

→ [Step 3. Instructions](../step-03-instructions/README.md)
