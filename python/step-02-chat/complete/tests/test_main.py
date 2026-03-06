"""TODO API 엔드포인트 테스트 모듈.

FastAPI TestClient를 사용하여 모든 CRUD 엔드포인트를 검증합니다.
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


def test_todo_생성_성공():
    """제목만 전달하여 TODO를 생성할 수 있는지 확인합니다."""
    response = client.post("/todos", json={"title": "테스트 할 일"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "테스트 할 일"
    assert data["completed"] is False
    assert data["id"] == 1


def test_todo_생성_설명포함():
    """제목과 설명을 함께 전달하여 TODO를 생성할 수 있는지 확인합니다."""
    response = client.post(
        "/todos",
        json={"title": "할 일", "description": "상세 설명"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "상세 설명"


# ── 조회(Read) 테스트 ────────────────────────────────────────


def test_todo_목록_비어있음():
    """초기 상태에서 빈 목록이 반환되는지 확인합니다."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_todo_목록_조회():
    """TODO를 생성한 뒤 목록에 포함되는지 확인합니다."""
    client.post("/todos", json={"title": "첫 번째"})
    client.post("/todos", json={"title": "두 번째"})
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


# ── 수정(Update) 테스트 ──────────────────────────────────────


def test_todo_수정_성공():
    """TODO의 제목과 완료 상태를 수정할 수 있는지 확인합니다."""
    client.post("/todos", json={"title": "원래 제목"})
    response = client.put(
        "/todos/1",
        json={"title": "수정된 제목", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "수정된 제목"
    assert data["completed"] is True


def test_todo_수정_404():
    """존재하지 않는 TODO를 수정하려 할 때 404 에러가 반환되는지 확인합니다."""
    response = client.put("/todos/999", json={"title": "없는 항목"})
    assert response.status_code == 404


# ── 삭제(Delete) 테스트 ──────────────────────────────────────


def test_todo_삭제_성공():
    """TODO를 삭제한 뒤 목록에서 제거되는지 확인합니다."""
    client.post("/todos", json={"title": "삭제할 항목"})
    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 삭제 후 목록이 비어 있는지 확인
    response = client.get("/todos")
    assert response.json() == []


def test_todo_삭제_404():
    """존재하지 않는 TODO를 삭제하려 할 때 404 에러가 반환되는지 확인합니다."""
    response = client.delete("/todos/999")
    assert response.status_code == 404
