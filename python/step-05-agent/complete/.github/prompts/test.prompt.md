---
mode: agent
description: "테스트 코드를 자동 생성합니다. 대상 모듈의 스키마를 참조하여 pytest + TestClient 기반 테스트를 작성합니다."
---

# 테스트 생성 프롬프트

## 참조 파일

#file:app/schemas.py
#file:tests/conftest.py

## 테스트 대상

${input:testTarget:테스트를 생성할 대상을 입력하세요 (예: POST /todos, GET /todos, 전체 CRUD)}

## 규칙

1. **프레임워크**: `pytest` + FastAPI `TestClient`를 사용합니다.
2. **네이밍**: `test_동작_조건_결과` 형식으로 한국어 테스트명을 사용합니다.
3. **구조**: 각 테스트에 **Given-When-Then** 주석을 포함합니다.
4. **픽스처**: `conftest.py`의 `session`(autouse) + `client` 픽스처를 사용합니다.
5. **검증**: 상태 코드를 먼저 검증하고, 응답 본문의 핵심 필드를 검증합니다.
6. **경계값**: 정상 케이스와 에러 케이스(404, 422)를 모두 포함합니다.
7. **docstring**: 한국어로 테스트 목적을 설명합니다.

## 출력 형식

- `tests/` 디렉토리 아래에 테스트 파일을 생성합니다.
- 모든 테스트 함수는 `client` 픽스처를 인자로 받습니다.
- DB는 `conftest.py`에서 자동으로 초기화되므로 별도 초기화 코드가 필요 없습니다.
