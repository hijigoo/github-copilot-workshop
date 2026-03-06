# Step 3. Instructions

> ⏱️ 20분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: `copilot-instructions.md` + 경로 지정 지침(Path-specific Instructions)**
>
> **체감: "매번 같은 말 반복 안 해도 된다!"**

---

## 이전 단계 코드

`starter/` = Step 2 완성 코드 (Javadoc + 테스트 포함 TODO API)

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

> 📖 자세한 내용: [GitHub Copilot에 대한 리포지토리 사용자 지정 지침 추가하기](https://docs.github.com/ko/copilot/how-tos/configure-custom-instructions/add-repository-instructions?tool=vscode)

---

## 태스크 1: 리포지토리 전체 지침 작성 (5분)

`.github/copilot-instructions.md` 생성:

```markdown
# 프로젝트 규칙

## 언어
- 모든 응답은 한국어로 작성
- 코드 주석, Javadoc도 한국어

## 기술 스택
- Java 17+ / Spring Boot 3.x / Spring Data JPA
- DB: H2 (개발), PostgreSQL (프로덕션)
- 테스트: JUnit 5 + MockMvc + @SpringBootTest
- 빌드: Gradle (Kotlin DSL)

## 코드 스타일 & 네이밍 컨벤션
- 패키지명: 소문자 (예: com.example.todo.controller)
- 클래스명: PascalCase (예: TodoController, TodoService)
- 메서드명: camelCase (예: createTodo, findById)
- 상수: UPPER_SNAKE_CASE (예: MAX_PAGE_SIZE)
- DTO: record 클래스 사용, 용도별 접미사
  - 생성 요청: XxxCreateRequest (예: TodoCreateRequest)
  - 수정 요청: XxxUpdateRequest (예: TodoUpdateRequest)
  - 응답: XxxResponse (예: TodoResponse)
- 테스트 메서드: test_동작_조건_결과() (예: test_createTodo_returns201)

## 아키텍처
- Controller → Service → Repository 레이어 구조
- Entity와 DTO를 분리 (entity/ vs dto/)
- @Valid로 요청 검증

## API 규칙
- RESTful 엔드포인트
- 에러는 ResponseStatusException으로 처리
- 에러 메시지는 한국어
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

### 검증: 경로 지정 지침 동작 확인

**① 테스트 지침 확인** — 테스트 파일을 열고 Chat에 입력:

> "TodoController에 대한 테스트를 작성해줘"

→ 확인 포인트:
- [ ] 메서드명이 `test_동작_조건_결과()` 패턴인가?
- [ ] `// Given:` / `// When:` / `// Then:` 주석이 있는가?
- [ ] `@Nested` 클래스로 그룹핑 되었는가?

**② API 코드 지침 확인** — Controller 파일을 열고 Chat에 입력:

> "GET /todos/{id} 단건 조회 엔드포인트를 추가해줘"

→ 확인 포인트:
- [ ] `@ResponseStatus` 지정되어 있는가?
- [ ] 에러 메시지가 한국어인가? (예: `"TODO를 찾을 수 없습니다"`)
- [ ] Javadoc이 한국어로 작성되었는가?

---

## ✅ 검증 체크리스트

- [ ] `.github/copilot-instructions.md` (리포지토리 전체 지침) 생성 완료
- [ ] `.github/instructions/testing.instructions.md` (경로 지정 지침) 생성
- [ ] `.github/instructions/api.instructions.md` (경로 지정 지침) 생성
- [ ] 경로 지정 지침이 해당 폴더에서만 적용됨을 확인

---

## 핵심 인사이트

> **"사용자 지정 지침 = AI에 대한 투자"**
>
> 한 번 잘 써두면 Copilot의 **모든 응답**이 달라집니다.
> 팀에서는 이 파일을 Git에 커밋하여 **팀 AI 컨벤션**으로 사용할 수 있습니다.

---

## 다음 단계

→ [Step 4. Spec-Driven Development](../step-04-spec-driven/README.md)
