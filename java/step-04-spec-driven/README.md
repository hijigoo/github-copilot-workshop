# Step 4. Spec-Driven Development (SDD)

> ⏱️ 25분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: DTO 정의 → 테스트 → 구현 패턴**
>
> **체감: "스펙을 먼저 쓰니 AI가 놀랍도록 정확하다!"**

---

## 이전 단계 코드

`starter/` = Step 3 완성 코드 (copilot-instructions.md + 경로 지정 지침 설정)

---

## 왜 네 번째인가?

Instructions로 **스타일**을 잡았다면, SDD로 **정확도**를 극대화합니다.

기존 접근: "TODO 앱에 우선순위 기능 추가해줘" → Copilot이 추측하며 구현
SDD 접근: **DTO 스펙 정의 → 테스트 작성 → 구현 위임** → Copilot이 정확히 구현

---

## SDD (Spec-Driven Development)란?

```
1. SPEC  — DTO/인터페이스 정의 (무엇이 필요한가?)
2. TEST  — 스펙 기반 테스트 작성 (어떻게 검증하나?)
3. IMPL  — Copilot에게 구현 위임 (테스트를 통과시켜줘!)
4. VERIFY — 테스트 실행 (정말 통과하나?)
```

---

## 태스크 1: 스펙(DTO) 먼저 정의 (7분)

`src/main/java/com/example/todo/dto/` 패키지에 DTO를 생성합니다.

> ⚠️ **구현은 하지 마세요!** 타입만 정의합니다.

### Priority enum

```java
package com.example.todo.dto;

public enum Priority {
    LOW, MEDIUM, HIGH
}
```

### TodoCreateRequest

```java
package com.example.todo.dto;

import jakarta.validation.constraints.*;

public record TodoCreateRequest(
    @NotBlank @Size(min = 1, max = 200)
    String title,

    @Size(max = 1000)
    String description,

    Priority priority  // 기본값: MEDIUM
) {
    public TodoCreateRequest {
        if (priority == null) priority = Priority.MEDIUM;
    }
}
```

### TodoResponse

```java
package com.example.todo.dto;

import java.time.LocalDateTime;

public record TodoResponse(
    Long id,
    String title,
    String description,
    Priority priority,
    boolean completed,
    LocalDateTime createdAt,
    LocalDateTime updatedAt
) {}
```

### TodoUpdateRequest

```java
package com.example.todo.dto;

import jakarta.validation.constraints.*;

public record TodoUpdateRequest(
    @Size(min = 1, max = 200)
    String title,

    @Size(max = 1000)
    String description,

    Priority priority,
    Boolean completed
) {}
```

### TodoListResponse

```java
package com.example.todo.dto;

import java.util.List;

public record TodoListResponse(
    List<TodoResponse> items,
    long total,
    int page,
    int size
) {}
```

### 관찰 포인트

- `@NotBlank`, `@Size` → 빈 제목 방지, 길이 제한
- `Priority` enum → 우선순위 제한
- `TodoListResponse` → 페이지네이션 구조
- record 클래스가 "계약서" 역할을 합니다

---

## 태스크 2: 스펙 기반 테스트 작성 (8분)

Copilot Chat에서:

```
#file:dto/TodoCreateRequest.java
#file:dto/TodoResponse.java
#file:dto/TodoListResponse.java

이 DTO 스펙을 기반으로 TodoControllerTest.java에 테스트를 작성해줘.

아직 구현은 없으니 테스트만 작성해줘. 다음 케이스를 반드시 포함:
- 정상 생성 (201 + 응답 검증)
- 빈 제목으로 생성 시 400 에러
- 우선순위별 필터링 (GET /todos?priority=HIGH)
- 페이지네이션 동작 (GET /todos?page=1&size=5)
- 존재하지 않는 TODO 조회 시 404
```

### 기대하는 테스트 구조

```java
@Nested
class CreateTodo {
    @Test
    void test_createTodo_withValidData_returns201() throws Exception {
        // Given: 유효한 TODO 데이터
        // When: POST /todos 호출
        // Then: 201 응답 + 생성된 TODO 반환
    }

    @Test
    void test_createTodo_withEmptyTitle_returns400() throws Exception {
        // Given: 제목이 빈 문자열
        // When: POST /todos 호출
        // Then: 400 유효성 검사 에러
    }
}
```

---

## 태스크 3: Copilot에게 구현 위임 (7분)

> ⚠️ **주의: Controller와 관련 클래스를 새로 작성합니다!**

Chat에서:

```
#file:dto/TodoCreateRequest.java
#file:dto/TodoResponse.java
#file:dto/TodoUpdateRequest.java
#file:dto/TodoListResponse.java
#file:TodoControllerTest.java

위 DTO 스펙과 테스트를 참고하여,
모든 테스트가 통과하도록 TodoController.java를 구현해줘.

기존 인메모리 저장소를 유지하되:
- Priority 지원
- 페이지네이션 지원
- 필터링 지원
을 추가해야 합니다.
```

---

## 태스크 4: 테스트로 검증 (3분)

```bash
./gradlew test
```

**모든 테스트가 통과해야 합니다!**

만약 실패하면:
- Chat에서 `/fix #file:TodoControllerTest.java` 실행
- 또는 실패한 테스트를 선택하고 원인 분석 요청

---

## ✅ 검증 체크리스트

- [ ] `dto/` 패키지에 DTO record 정의 완료
- [ ] 테스트가 먼저 작성됨 (Red 단계)
- [ ] Copilot이 구현을 완성 (Green 단계)
- [ ] `./gradlew test` 전체 통과
- [ ] 우선순위 필터링 동작 확인
- [ ] 페이지네이션 동작 확인

---

## 핵심 인사이트

> **"AI에게 '무엇을 만들지'가 아니라 '어떤 조건을 만족할지'를 알려줘라"**
>
> 스펙(DTO) + 테스트 = AI에게 가장 명확한 지시.
> "우선순위 기능 추가해줘" vs "이 스펙과 테스트를 통과하는 코드를 작성해줘"
> → 후자가 항상 더 정확합니다.

---

## 다음 단계

→ [Step 5. Prompt Files](../step-05-prompt-files/README.md)
