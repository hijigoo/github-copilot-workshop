---
applyTo: "tests/**"
---

# 테스트 작성 지침

## 테스트 프레임워크

- **pytest**와 FastAPI **TestClient**를 사용합니다.
- `httpx`는 TestClient 내부에서 사용되므로 별도 임포트하지 않습니다.

## 테스트 함수 네이밍

- `test_동작_조건_결과` 형식을 따릅니다.
- 예시:
  - `test_생성_제목만전달_201반환`
  - `test_수정_없는항목_404반환`
  - `test_삭제_존재하는항목_204반환`
  - `test_부분수정_완료상태변경_200반환`

## 테스트 구조

- **Given-When-Then** 주석으로 테스트 구조를 명확히 합니다:
  ```python
  def test_생성_제목만전달_201반환(client):
      """제목만 전달하여 TODO를 생성하면 201을 반환합니다."""
      # Given: 빈 데이터베이스 상태
      # When: 제목만 포함한 TODO 생성 요청
      response = client.post("/todos", json={"title": "테스트"})
      # Then: 201 상태코드와 생성된 TODO 반환
      assert response.status_code == 201
  ```

## 픽스처

- `conftest.py`에서 `session` 픽스처가 `autouse=True`로 설정되어 매 테스트마다 인메모리 DB를 생성합니다.
- `client` 픽스처를 테스트 함수의 인자로 받아 사용합니다.
- `get_session` 의존성을 오버라이드하여 테스트 격리를 보장합니다.

## 검증 원칙

- 상태 코드를 항상 먼저 검증합니다.
- 응답 본문의 핵심 필드를 검증합니다.
- 404 케이스는 반드시 포함합니다.
- docstring은 한국어로 테스트 목적을 설명합니다.
