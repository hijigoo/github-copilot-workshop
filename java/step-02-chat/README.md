# Step 2. Copilot Chat

> ⏱️ 20분 | 난이도 ⭐
>
> 🎯 **핵심 학습: Chat 패널 + `@`, `#`, `/` 명령어**
>
> **체감: "대화로 코드를 다룰 수 있다!"**

---

## 이전 단계 코드

`starter/` = Step 1 완성 코드 (인메모리 CRUD TODO API)

---

## 왜 두 번째인가?

Step 1에서 수동으로 코드를 작성했으니, 이제 **대화**로 코드를 다루는 경험을 합니다.
"검색 + 코딩 + 질문"이 한 곳에서 해결됩니다.

---

## Chat 열기

| IDE | 방법 |
|-----|------|
| IntelliJ | 우측 사이드바 > GitHub Copilot Chat |

---

## `@`, `#`, `/` — Chat 명령어 기본 개념

Chat에서는 세 가지 특수 기호를 조합하여 Copilot과 대화합니다.

| 기호 | 역할 | 설명 | 예시 |
|------|------|------|------|
| `@` | **누구에게** (컨텍스트 제공자) | Copilot이 참고할 컨텍스트 범위를 지정합니다 | `@workspace`, `@terminal` |
| `#` | **무엇을 참고** (파일/선택 영역) | 특정 파일이나 선택 영역을 명시적으로 전달합니다 | `#file:TodoController.java`, `#selection` |
| `/` | **무엇을** (액션) | Copilot에게 수행할 작업을 지시합니다 | `/explain`, `/fix`, `/tests` |

### 조합 예시

```
@workspace /explain #file:TodoController.java
```
→ "**워크스페이스**를 참고하여, **TodoController.java**를 **설명해줘**"

> 💡 세 기호를 모두 쓸 필요는 없습니다. 필요한 것만 조합하면 됩니다.

---

## 태스크 A: `@` — 프로젝트 맥락 질문 (3분)

Chat에 입력:

```
@workspace 이 프로젝트에 Spring Data JPA를 적용하려면 어떻게 해야 하나요?
```

**관찰**: `@workspace`가 프로젝트의 파일 구조와 의존성을 분석하여 맞춤 답변을 합니다.

---

## 태스크 B: `#` — 코드 설명 받기 (3분)

Chat에 입력:

```
/explain #file:TodoController.java 한국어로 설명해줘
```

**관찰**: `#file:`로 파일을 지정하면 Copilot이 해당 파일의 구조와 각 엔드포인트의 역할을 한국어로 설명합니다.

---

## 태스크 C: `/fix` — 버그 수정 (5분)

1. `TodoController.java`의 `createTodo` 메서드에서 **의도적 버그** 삽입:

```java
// 이 부분을 일부러 잘못 고치세요:
Todo newTodo = new Todo();
newTodo.setId(nextId++);
newTodo.setTitle(request.getDescription());  // ← 버그! title이 아니라 description
newTodo.setCompleted(true);                   // ← 버그! 기본값이 true
```

2. 버그가 있는 코드를 선택하고:

```
/fix
```

**관찰**: Copilot이 잘못된 필드 매핑과 기본값을 정확히 찾아냅니다.

---

## 태스크 D: `/tests` — 테스트 코드 생성 (5분)

```
/tests #file:TodoController.java
```

**관찰**: Copilot이 JUnit 5 + MockMvc 기반 테스트를 작성합니다.

생성된 테스트 실행:

```bash
./gradlew test
```

---

## ✅ 검증 체크리스트

- [ ] `@workspace` 질문에 프로젝트 맥락이 반영된 답변 확인
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
