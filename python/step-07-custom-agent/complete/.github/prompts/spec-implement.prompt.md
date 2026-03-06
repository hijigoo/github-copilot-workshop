---
mode: agent
description: "Spec-Driven Development 워크플로우로 새 기능을 구현합니다. 스펙 → 테스트 → 구현 → 검증 순서를 따릅니다."
---

# Spec-Driven Development 프롬프트

## 참조 파일

#file:app/schemas.py
#file:app/models.py
#file:app/database.py
#file:.github/copilot-instructions.md

## 기능 설명

${input:featureDescription:구현할 기능을 설명하세요 (예: TODO에 태그(tags) 필드를 추가하여 생성, 수정, 조회 시 태그를 관리할 수 있도록 합니다)}

## 워크플로우

다음 4단계를 **순서대로** 수행합니다:

### 1단계: SPEC (스펙 정의)

- `app/schemas.py`에 새로운 필드 또는 모델을 추가합니다.
- `app/models.py`에 대응하는 데이터베이스 컬럼을 추가합니다.
- Pydantic v2 `Field` 유효성 검사를 활용합니다.
- 기존 스키마와의 일관성을 유지합니다.
- 한국어 docstring과 description을 작성합니다.

### 2단계: TEST (테스트 작성)

- 스펙에 기반하여 테스트를 **먼저** 작성합니다.
- `test_동작_조건_결과` 네이밍과 Given-When-Then 구조를 따릅니다.
- 정상 케이스와 에러 케이스를 모두 포함합니다.
- `client` 픽스처를 사용합니다 (conftest.py에서 DB 초기화 자동 처리).

### 3단계: IMPL (구현)

- `app/main.py`에서 새 기능을 구현합니다.
- 테스트가 통과하도록 최소한의 코드를 작성합니다.
- SQLModel 세션을 통해 데이터베이스에 접근합니다.
- 한국어 docstring을 업데이트합니다.

### 4단계: VERIFY (검증)

- `python -m pytest tests/ -v` 명령으로 전체 테스트를 실행합니다.
- 기존 테스트가 깨지지 않았는지 확인합니다.
- 새로 추가한 테스트가 모두 통과하는지 확인합니다.

## 주의사항

- 기존 기능을 절대 깨뜨리지 않습니다.
