# Step 5. Prompt Files

> ⏱️ 20분 | 난이도 ⭐⭐
>
> 🎯 **핵심 학습: `.github/prompts/*.prompt.md`**
>
> **체감: "/ 하나로 반복 작업이 끝난다!"**

---

## 이전 단계 코드

`starter/` = Step 4 완성 코드 (SDD 완료: DTO + priority + pagination)

---

## 왜 다섯 번째인가?

Step 3의 **Instructions**가 "항상 적용되는 규칙"이라면,
**Prompt Files**는 "필요할 때 꺼내 쓰는 매크로"입니다.

| 구분 | Instructions | Prompt Files |
|------|-------------|--------------|
| 적용 시점 | 항상 자동 | `/명령어`로 수동 호출 |
| 용도 | 프로젝트 규칙 | 반복 작업 자동화 |
| 비유 | 교칙 | 도구 상자 |

---

## Prompt Files란?

`.github/prompts/` 폴더에 `.prompt.md` 파일을 생성하면,
Chat에서 `/파일명`으로 호출할 수 있습니다.

```
.github/prompts/
├── test.prompt.md           → /test 로 호출
├── spec-implement.prompt.md → /spec-implement 로 호출
└── refactor.prompt.md       → /refactor 로 호출
```

---

## 태스크 1: 테스트 생성 프롬프트 (5분)

`.github/prompts/test.prompt.md` 생성:

```markdown
---
agent: "agent"
description: "선택한 모듈에 대한 테스트를 자동 생성합니다"
---

#file:dto/ 의 DTO 스펙을 참조하여,
다음 대상에 대한 테스트를 작성해주세요:

대상: ${input:testTarget}

## 규칙
- JUnit 5 + MockMvc 사용
- @Nested 클래스로 그룹핑
- Given-When-Then 주석 패턴
- 메서드명: test_동작_조건_결과()
- 정상 케이스 / 에러 케이스 / 경계값 각각 최소 1개
- 한국어 주석과 설명
```

### 사용법

1. Chat에서 `/test` 입력
2. `testTarget`에 `PATCH /todos/{id}` 입력
3. Copilot이 해당 엔드포인트의 테스트를 자동 생성

---

## 태스크 2: SDD 워크플로우 프롬프트 (5분)

`.github/prompts/spec-implement.prompt.md` 생성:

```markdown
---
agent: "agent"
description: "스펙 기반으로 DTO → 테스트 → 구현을 순서대로 수행합니다"
---

다음 기능을 Spec-Driven Development로 구현해주세요:

기능: ${input:featureDescription}

## 순서 (반드시 이 순서대로!)
1. **SPEC**: dto/ 패키지에 DTO record 추가
2. **TEST**: test/에 테스트 작성 (실패하는 상태)
3. **IMPL**: controller/, service/ 에 구현 코드 작성
4. **VERIFY**: ./gradlew test로 전체 테스트 통과 확인

## 참고 파일
#file:dto/
```

### 사용법

1. Chat에서 `/spec-implement` 입력
2. `featureDescription`에 `TODO에 마감일(dueDate) 기능 추가` 입력
3. Copilot이 SDD 순서대로 자동 구현

---

## 태스크 3: 리팩토링 프롬프트 (5분)

`.github/prompts/refactor.prompt.md` 생성:

```markdown
---
agent: "agent"
description: "선택한 코드를 리팩토링합니다"
---

다음 대상을 리팩토링해주세요:

대상: ${input:refactorTarget}

## 규칙
- 동작 변경 없이 구조만 개선
- 리팩토링 전후 테스트 통과 필수 (./gradlew test)
- 변경 사항을 한국어로 요약해주세요

## 리팩토링 관점
- 코드 중복 제거
- 메서드/클래스 분리
- 네이밍 개선
- 타입 안전성 향상
```

---

## 태스크 4: 프롬프트 파일 활용 실습 (5분)

1. `/test` → `GET /todos 페이지네이션` 에 대한 테스트 생성
2. `/spec-implement` → `TODO에 태그(tags) 기능 추가`
3. 생성된 코드를 검토하고 `./gradlew test`로 검증

---

## ✅ 검증 체크리스트

- [ ] `.github/prompts/test.prompt.md` 생성
- [ ] `.github/prompts/spec-implement.prompt.md` 생성
- [ ] `.github/prompts/refactor.prompt.md` 생성
- [ ] `/test` 입력 시 프롬프트 파일이 로드됨
- [ ] `/spec-implement`로 새 기능 SDD 자동 실행

---

## 핵심 인사이트

> **"자주 하는 요청은 Prompt File로 만들어라"**
>
> Chat 히스토리에 묻히는 반복 프롬프트를 파일로 저장하면:
> - 팀원 누구나 동일한 품질로 사용 가능
> - Git에 커밋하여 버전 관리
> - `${input:변수}`로 유연하게 재사용

---

## 다음 단계

→ [Step 5. Agent 모드](../step-05-agent/README.md)
