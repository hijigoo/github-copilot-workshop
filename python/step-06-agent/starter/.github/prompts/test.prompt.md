---
mode: agent
description: "테스트 코드를 자동 생성합니다. 대상 모듈의 스키마를 참조하여 pytest + TestClient 기반 테스트를 작성합니다."
---

# 테스트 생성 프롬프트

## 참조 파일

#file:app/schemas.py

## 테스트 대상

${input:testTarget:테스트를 생성할 대상을 입력하세요 (예: POST /todos, GET /todos, 전체 CRUD)}

## 규칙

1. **프레임워크**: `pytest` + FastAPI `TestClient`를 사용합니다.
2. **네이밍**: `test_동작_조건_결과` 형식으로 한국어 테스트명을 사용합니다.
3. **구조**: 각 테스트에 **Given-When-Then** 주석을 포함합니다.
4. **픽스처**: `autouse=True` 픽스처로 매 테스트 전 인메모리 저장소를 초기화합니다.
5. **검증**: 상태 코드를 먼저 검증하고, 응답 본문의 핵심 필드를 검증합니다.
6. **경계값**: 정상 케이스와 에러 케이스(404, 422)를 모두 포함합니다.
7. **docstring**: 한국어로 테스트 목적을 설명합니다.

## 출력 형식

- `tests/` 디렉토리 아래에 테스트 파일을 생성합니다.
- import 문에서 `app.main`의 `app`, `todos`, `next_id`를 가져옵니다.
- `app.main` 모듈을 `main_module`로 임포트하여 `next_id` 리셋에 사용합니다.
