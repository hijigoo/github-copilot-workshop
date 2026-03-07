# Step 3. Instructions

> ⏱️ 20분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: `copilot-instructions.md` + 경로 지정 지침(Path-specific Instructions)**
>
> **체감: "매번 같은 말 반복 안 해도 된다!"**

---

## 코드 폴더

| 폴더 | 설명 |
|------|------|
| `starter/` | Step 2 완성 코드 (Javadoc + 테스트 포함 TODO API) — 여기서 시작하세요 |
| `complete/` | 이번 스텝 완성 코드 — 막힐 때 참고하세요 |

---

## 왜 세 번째인가?

Step 2에서 Chat을 쓸 때 매번 "한글로 대답해줘", "JUnit 5 쓰고 있어" 등을 반복했을 겁니다.
**Instructions**는 이런 반복을 **한 번에 제거**합니다.

---

## 사용자 지정 지침(Custom Instructions)이란?

리포지토리에 사용자 지정 지침을 추가하면, 프로젝트를 이해하고 변경 내용을 작성 및 테스트하는 방법에 대해 Copilot을 안내할 수 있습니다.

Copilot은 다음 유형의 사용자 지정 지침 파일을 지원합니다:

- `.github/copilot-instructions.md` — **리포지토리 전체 지침** (항상 적용)
- `.github/instructions/**/*.instructions.md` — **경로 지정 지침** (특정 파일에만 적용)

```
.github/
├── copilot-instructions.md          ← 리포지토리 전체 지침 (항상 적용)
└── instructions/
    ├── testing.instructions.md      ← tests/** 에서만 적용
    └── api.instructions.md          ← controller/** 에서만 적용
```

> 📸 **[IntelliJ 스크린샷]** IntelliJ Project 탐색기에서 `.github/` 폴더 구조와 `copilot-instructions.md`, `instructions/` 폴더가 보이는 모습
>
> ![Instructions 폴더 구조](./images/step03-instructions-folder.png)

> � **설정에서 지침 확인하기**
>
> IntelliJ 설정에서 등록된 지침 파일을 확인할 수 있습니다:
> **Settings** (`Windows/Linux: Ctrl+Alt+S`, `macOS: Cmd+,`) → **Tools** → **GitHub Copilot** → **Customizations**
>
> ![IntelliJ Copilot Customizations 설정](./images/step03-intellij-customizations.png)

> �📖 자세한 내용: [GitHub Copilot에 대한 리포지토리 사용자 지정 지침 추가하기](https://docs.github.com/ko/copilot/how-tos/configure-custom-instructions/add-repository-instructions?tool=vscode)

---

## 태스크 1: 리포지토리 전체 지침 작성 (5분)

`.github/copilot-instructions.md` 생성:

```markdown
# 프로젝트 규칙

## 언어
- 모든 응답은 한국어로 작성
- 코드 주석, Javadoc도 한국어

## 기술 스택
- Java 17+ / Spring Boot 3.x / Spring Web
- 데이터 저장: 인메모리 List (ArrayList)
- 테스트: JUnit 5 + MockMvc + @SpringBootTest
- 빌드: Gradle (Kotlin DSL)

## 코드 스타일
- 클래스명: PascalCase (예: TodoController)
- 메서드명: camelCase (예: createTodo, findById)
- 상수: UPPER_SNAKE_CASE (예: MAX_TITLE_LENGTH)
- 테스트 메서드: test_동작_조건_결과() (예: test_createTodo_withValidData_returns201)

## API 규칙
- RESTful 엔드포인트
- @ResponseStatus로 상태 코드 명시 (CREATED, NO_CONTENT 등)
- 에러는 ResponseStatusException으로 처리
- 에러 메시지는 한국어

## 테스트 규칙
- @Nested 클래스로 엔드포인트별 그룹핑
- Given-When-Then 주석 패턴 사용
```

---

## 태스크 2: 경로 지정 지침 작성 (10분)

### 테스트 전용 규칙

`.github/instructions/testing.instructions.md`:

```markdown
---
applyTo: "**/test/**"
---
# 테스트 규칙

## 프레임워크
- JUnit 5 + @SpringBootTest + MockMvc

## 네이밍
- 메서드명: test_동작_조건_결과()
  - 예: test_createTodo_withValidData_returns201()
  - 예: test_getTodo_withInvalidId_returns404()

## 구조
- @Nested 클래스로 엔드포인트별 그룹핑
- Given-When-Then 주석 패턴 사용
  - 예시:
    ```java
    @Test
    void test_createTodo_withValidData_returns201() throws Exception {
        // Given: 유효한 TODO 데이터
        String json = """
            {"title": "테스트", "description": "설명"}
            """;

        // When: POST /todos 요청
        var result = mockMvc.perform(post("/todos")
            .contentType(MediaType.APPLICATION_JSON)
            .content(json));

        // Then: 201 상태 코드와 생성된 TODO 반환
        result.andExpect(status().isCreated())
              .andExpect(jsonPath("$.title").value("테스트"));
    }
    ```
- 각 테스트는 독립적 (@Transactional 사용)

## 커버리지
- 정상 케이스 + 에러 케이스 + 경계값 각각 최소 1개
- 모든 HTTP 상태 코드 테스트
```

### API 코드 전용 규칙

`.github/instructions/api.instructions.md`:

```markdown
---
applyTo: "**/controller/**"
---
# API 코드 규칙

## 엔드포인트
- @ResponseStatus로 상태 코드 명시 (CREATED, NO_CONTENT 등)
- @Valid로 요청 검증
- 메서드 파라미터 타입 명확히 지정

## 에러 처리
- 404: ResponseStatusException(HttpStatus.NOT_FOUND, "메시지")
- 400: @Valid + MethodArgumentNotValidException 자동 처리
- 에러 메시지는 한국어

## 구조
- Controller는 비즈니스 로직 없이 Service 위임만
- 반환 타입은 DTO (Entity 직접 반환 금지)
```

---

## 태스크 3: 지침 동작 실습 및 검증 (10분)

태스크 1, 2에서 생성한 지침 파일들이 실제로 Copilot에 올바르게 적용되는지 확인합니다.

### ① 리포지토리 전체 지침 동작 확인

`TodoControllerTest.java` 파일을 열고 Chat에 입력:

> "Instructions에 설정된 규칙을 설명해주고, 그 규칙에 맞게 프로젝트를 리팩토링해줘"

→ 현재 테스트 코드에는 `@Nested` 그룹핑이나 Given-When-Then 주석이 없습니다. 지침이 적용되면 다음이 변경됩니다:

- [ ] 테스트 메서드명이 `test_동작_조건_결과()` 패턴으로 변경되었는가? (예: `test_createTodo_withValidData_returns201`)
- [ ] `@Nested` 클래스로 엔드포인트별 그룹핑이 추가되었는가?
- [ ] `// Given:` / `// When:` / `// Then:` 주석 패턴이 추가되었는가?

> 📸 **[IntelliJ 스크린샷]** Chat에 리팩토링을 요청했을 때, `copilot-instructions.md`의 프로젝트 규칙이 반영된 결과 — `@Nested` 그룹핑, Given-When-Then 주석, 영문 테스트 네이밍이 적용된 모습
>
> ![전체 지침 적용 결과](./images/step03-global-instructions-result.png)

### ② 테스트 경로 지정 지침 확인

기존 테스트 코드를 삭제한 후 새로 생성하여 지침 적용을 확인합니다.

먼저 `TodoControllerTest.java`가 있다면 코드를 모두 삭제하고 진행합니다.

그 다음 테스트 파일을 열고 Chat에 입력:

> "TodoController에 대한 테스트를 작성해줘"

→ 확인 포인트:
- [ ] 메서드명이 `test_동작_조건_결과()` 패턴인가?
- [ ] `// Given:` / `// When:` / `// Then:` 주석이 있는가?
- [ ] `@Nested` 클래스로 그룹핑 되었는가?

> 📸 **[IntelliJ 스크린샷]** 테스트 파일에서 Chat으로 테스트 생성을 요청했을 때, `testing.instructions.md` 지침이 반영된 결과 — `test_동작_조건_결과()` 네이밍과 Given-When-Then 패턴이 적용된 모습
>
> ![테스트 지침 적용 결과](./images/step03-testing-instructions-result.png)

### ③ API 코드 경로 지정 지침 확인

`TodoController.java` 파일을 열고 Chat에 입력:

> "PATCH /todos/{id} 부분 수정 엔드포인트를 추가해줘"

→ `api.instructions.md`의 고유 규칙이 추가 적용되는지 확인합니다:
- [ ] Controller가 Service에 위임하는 구조인가? (기존 코드는 Controller에서 직접 처리)
- [ ] 반환 타입이 DTO인가? (기존 코드는 `Todo` 객체를 직접 반환)

> 📸 **[IntelliJ 스크린샷]** `api.instructions.md` 지침이 반영된 엔드포인트 생성 결과
>
> ![API 지침 적용 결과](./images/step03-api-instructions-result.png)

---

## ✅ 검증 체크리스트

### 태스크 1: 리포지토리 전체 지침
- [ ] `.github/copilot-instructions.md` 파일 생성 완료

### 태스크 2: 경로 지정 지침
- [ ] `.github/instructions/testing.instructions.md` 생성 완료
- [ ] `.github/instructions/api.instructions.md` 생성 완료

### 태스크 3: 지침 동작 실습 및 검증
- [ ] 리포지토리 전체 지침 적용 확인: `@Nested` 그룹핑, Given-When-Then 주석, 테스트 네이밍 변경 등이 반영됨
- [ ] 테스트 경로 지정 지침 확인: `test_동작_조건_결과()` 네이밍 패턴, Given-When-Then 주석 적용됨
- [ ] API 경로 지정 지침 확인: Service 위임 구조, DTO 반환 타입 적용됨
- [ ] 경로 지정 지침이 해당 폴더에서만 적용됨을 확인

---

## 핵심 인사이트

> **"사용자 지정 지침 = AI에 대한 투자"**
>
> 한 번 잘 써두면 Copilot의 **모든 응답**이 달라집니다.
> 팀에서는 이 파일을 Git에 커밋하여 **팀 AI 컨벤션**으로 사용할 수 있습니다.

---

## 다음 단계

→ [Step 4. Prompt Files](../step-04-prompt-files/README.md)
