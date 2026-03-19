---
name: python-pytest
description: 'pytest를 활용한 Python 단위 테스트 및 픽스처 모범 사례'
---

# pytest 모범 사례

목표는 pytest를 사용하여 효과적인 단위 테스트를 작성하는 것이며, 픽스처, 파라미터화 테스트, FastAPI 테스트를 포함합니다.

## 프로젝트 설정

- 테스트 파일은 `tests/` 디렉토리에 위치시킵니다.
- 다음 패키지를 설치합니다:
  - `pytest`
  - `httpx` (FastAPI 비동기 테스트용)
- 테스트 실행:
  - `pytest -v`
  - `pytest -v tests/test_specific.py`

## 테스트 구조

- 테스트 파일 이름은 `test_`로 시작해야 합니다. (예: `test_todo.py`)
- 테스트 함수 이름은 `test_`로 시작해야 합니다.
- 관련 테스트를 클래스로 그룹화합니다. (예: `TestCreateTodo`, `TestListTodos`)
- 클래스 이름은 `Test`로 시작해야 합니다.
- Arrange-Act-Assert (AAA) 패턴을 따릅니다.

## Fixtures (픽스처)

- `conftest.py`에 공유 픽스처를 정의합니다.
- `@pytest.fixture`로 테스트 데이터와 의존성을 관리합니다.
- 픽스처 스코프:
  - `function` (기본값): 각 테스트마다 실행
  - `class`: 클래스당 한 번 실행
  - `module`: 모듈당 한 번 실행
  - `session`: 전체 테스트 세션당 한 번 실행
- `yield`를 사용해 setup/teardown을 처리합니다.

## 일반 테스트

- 하나의 테스트는 하나의 동작만 검증해야 합니다.
- 테스트는 서로 독립적이고 반복 실행 가능해야 합니다.
- 테스트 간 의존성을 피해야 합니다.
- 헬퍼 함수 (예: `create_test_todo()`)로 테스트 데이터 생성을 간소화합니다.

## 파라미터화 테스트

- `@pytest.mark.parametrize`를 사용합니다.
- 단일 파라미터:
  - `@pytest.mark.parametrize("input_val", [1, 2, 3])`
- 복수 파라미터:
  - `@pytest.mark.parametrize("input_val, expected", [(1, 2), (2, 4)])`
- ID 지정:
  - `ids=["case1", "case2"]`로 테스트 케이스에 이름 부여

## Assertions (검증)

- `assert` 문을 직접 사용합니다.
- 예외 테스트:
  - `with pytest.raises(ValueError):`
  - `with pytest.raises(ValueError, match="메시지 패턴"):`
- 근사값 비교:
  - `pytest.approx()`

## FastAPI 테스트

- `TestClient`를 사용하여 API 엔드포인트를 테스트합니다.
- `conftest.py`에서 의존성 오버라이드를 설정합니다.
- 인메모리 SQLite로 DB 격리를 수행합니다.
- HTTP 메서드별 테스트: `client.get()`, `client.post()`, `client.patch()`, `client.delete()`
- 응답 검증: `response.status_code`, `response.json()`

## 테스트 구성

- 기능 또는 엔드포인트별로 테스트 파일을 분리합니다.
- `@pytest.mark.skip(reason="사유")`으로 테스트 비활성화
- `@pytest.mark.xfail`로 예상 실패 표시
- `-k` 옵션으로 특정 테스트만 실행:
  - `pytest -k "test_create"`
- `--tb=short`로 간결한 트레이스백 출력
