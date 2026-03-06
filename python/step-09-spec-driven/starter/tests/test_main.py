"""TODO API 엔드포인트 테스트 모듈.

FastAPI TestClient를 사용하여 모든 CRUD 엔드포인트를 검증합니다.
테스트 함수명은 test_동작_조건_결과 네이밍 컨벤션을 따릅니다.
Given-When-Then 주석으로 테스트 구조를 명확히 합니다.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app, todos, next_id
import app.main as main_module


@pytest.fixture(autouse=True)
def reset_store():
    """각 테스트 실행 전에 인메모리 저장소를 초기화합니다."""
    todos.clear()
    main_module.next_id = 1
    yield


client = TestClient(app)


# ── 생성(Create) 테스트 ──────────────────────────────────────


def test_생성_제목만전달_201반환():
    """제목만 전달하여 TODO를 생성하면 201과 생성된 항목을 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 제목만 포함한 TODO 생성 요청
    response = client.post("/todos", json={"title": "테스트 할 일"})

    # Then: 201 상태코드와 생성된 TODO 반환
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "테스트 할 일"
    assert data["completed"] is False
    assert data["id"] == 1


def test_생성_설명포함_설명저장됨():
    """제목과 설명을 함께 전달하면 설명이 포함된 TODO가 생성됩니다."""
    # Given: 빈 저장소 상태
    # When: 제목과 설명을 포함한 TODO 생성 요청
    response = client.post(
        "/todos",
        json={"title": "할 일", "description": "상세 설명"},
    )

    # Then: 설명이 포함된 TODO 반환
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "상세 설명"


# ── 조회(Read) 테스트 ────────────────────────────────────────


def test_조회_초기상태_빈목록반환():
    """초기 상태에서 TODO 목록을 조회하면 빈 리스트를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 목록 조회 요청
    response = client.get("/todos")

    # Then: 빈 리스트 반환
    assert response.status_code == 200
    assert response.json() == []


def test_조회_생성후_목록포함():
    """TODO를 생성한 뒤 목록을 조회하면 생성된 항목이 포함됩니다."""
    # Given: 2개의 TODO가 생성된 상태
    client.post("/todos", json={"title": "첫 번째"})
    client.post("/todos", json={"title": "두 번째"})

    # When: 목록 조회 요청
    response = client.get("/todos")

    # Then: 2개의 항목이 포함된 리스트 반환
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


# ── 수정(PUT Update) 테스트 ──────────────────────────────────


def test_수정_존재하는항목_200반환():
    """존재하는 TODO를 PUT으로 수정하면 200과 수정된 항목을 반환합니다."""
    # Given: TODO가 1개 생성된 상태
    client.post("/todos", json={"title": "원래 제목"})

    # When: PUT으로 제목과 완료 상태 수정 요청
    response = client.put(
        "/todos/1",
        json={"title": "수정된 제목", "completed": True},
    )

    # Then: 수정된 TODO 반환
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "수정된 제목"
    assert data["completed"] is True


def test_수정_없는항목_404반환():
    """존재하지 않는 TODO를 PUT으로 수정하려 하면 404를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 존재하지 않는 ID로 수정 요청
    response = client.put("/todos/999", json={"title": "없는 항목"})

    # Then: 404 상태코드 반환
    assert response.status_code == 404


# ── 부분 수정(PATCH) 테스트 ──────────────────────────────────


def test_부분수정_완료상태변경_200반환():
    """PATCH로 완료 상태만 변경하면 200과 수정된 항목을 반환합니다."""
    # Given: TODO가 1개 생성된 상태
    client.post("/todos", json={"title": "할 일"})

    # When: PATCH로 완료 상태만 변경 요청
    response = client.patch("/todos/1", json={"completed": True})

    # Then: 완료 상태만 변경되고 나머지는 유지
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "할 일"


def test_부분수정_제목변경_제목만수정됨():
    """PATCH로 제목만 변경하면 제목만 수정되고 나머지 필드는 유지됩니다."""
    # Given: TODO가 1개 생성된 상태
    client.post("/todos", json={"title": "원래 제목", "description": "원래 설명"})

    # When: PATCH로 제목만 변경 요청
    response = client.patch("/todos/1", json={"title": "새 제목"})

    # Then: 제목만 변경되고 설명은 유지
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "새 제목"
    assert data["description"] == "원래 설명"


def test_부분수정_없는항목_404반환():
    """존재하지 않는 TODO를 PATCH로 수정하려 하면 404를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 존재하지 않는 ID로 PATCH 요청
    response = client.patch("/todos/999", json={"completed": True})

    # Then: 404 상태코드 반환
    assert response.status_code == 404


# ── 삭제(Delete) 테스트 ──────────────────────────────────────


def test_삭제_존재하는항목_204반환():
    """존재하는 TODO를 삭제하면 204를 반환하고 목록에서 제거됩니다."""
    # Given: TODO가 1개 생성된 상태
    client.post("/todos", json={"title": "삭제할 항목"})

    # When: 삭제 요청
    response = client.delete("/todos/1")

    # Then: 204 상태코드 반환 및 목록에서 제거
    assert response.status_code == 204
    response = client.get("/todos")
    assert response.json() == []


def test_삭제_없는항목_404반환():
    """존재하지 않는 TODO를 삭제하려 하면 404를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 존재하지 않는 ID로 삭제 요청
    response = client.delete("/todos/999")

    # Then: 404 상태코드 반환
    assert response.status_code == 404
