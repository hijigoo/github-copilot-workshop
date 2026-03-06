"""TODO API 엔드포인트 종합 테스트 모듈.

schemas.py에 정의된 스펙(Priority, 페이지네이션, Field 유효성 검사, due_date)을
기반으로 작성된 테스트입니다.

테스트 함수명은 test_동작_조건_결과 네이밍 컨벤션을 따릅니다.
Given-When-Then 주석으로 테스트 구조를 명확히 합니다.
"""

import pytest
from datetime import datetime
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


def test_생성_유효한데이터_201반환():
    """유효한 제목과 우선순위로 TODO를 생성하면 201과 생성된 항목을 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 유효한 데이터로 TODO 생성 요청
    response = client.post(
        "/todos",
        json={"title": "테스트 할 일", "priority": "high"},
    )

    # Then: 201 상태코드와 생성된 TODO 반환
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "테스트 할 일"
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert data["id"] == 1
    assert data["created_at"] is not None
    assert data["updated_at"] is None
    assert data["due_date"] is None


def test_생성_기본우선순위_medium설정():
    """우선순위를 지정하지 않으면 기본값 medium으로 생성됩니다."""
    # Given: 빈 저장소 상태
    # When: 우선순위 없이 TODO 생성 요청
    response = client.post("/todos", json={"title": "기본 우선순위"})

    # Then: priority가 medium으로 설정됨
    assert response.status_code == 201
    data = response.json()
    assert data["priority"] == "medium"


def test_생성_빈제목_422반환():
    """빈 문자열로 제목을 전달하면 422 유효성 검사 에러를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 빈 제목으로 TODO 생성 요청
    response = client.post("/todos", json={"title": ""})

    # Then: 422 유효성 검사 에러 반환
    assert response.status_code == 422


def test_생성_제목초과_422반환():
    """200자를 초과하는 제목을 전달하면 422 유효성 검사 에러를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 201자 제목으로 TODO 생성 요청
    long_title = "가" * 201
    response = client.post("/todos", json={"title": long_title})

    # Then: 422 유효성 검사 에러 반환
    assert response.status_code == 422


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


def test_생성_마감일포함_마감일저장됨():
    """마감일을 포함하여 TODO를 생성하면 due_date가 저장됩니다."""
    # Given: 빈 저장소 상태
    due = "2026-12-31T23:59:59"

    # When: 마감일을 포함한 TODO 생성 요청
    response = client.post(
        "/todos",
        json={"title": "연말 할 일", "due_date": due},
    )

    # Then: 마감일이 포함된 TODO 반환
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"] is not None
    assert "2026-12-31" in data["due_date"]


def test_생성_마감일없음_None반환():
    """마감일 없이 TODO를 생성하면 due_date가 None입니다."""
    # Given: 빈 저장소 상태
    # When: 마감일 없이 TODO 생성 요청
    response = client.post("/todos", json={"title": "마감일 없는 할 일"})

    # Then: due_date가 None
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"] is None


# ── 조회(Read) + 페이지네이션 테스트 ─────────────────────────


def test_조회_초기상태_빈목록반환():
    """초기 상태에서 TODO 목록을 조회하면 빈 리스트를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 목록 조회 요청
    response = client.get("/todos")

    # Then: 빈 리스트와 total=0 반환
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["size"] == 10


def test_조회_생성후_목록포함():
    """TODO를 생성한 뒤 목록을 조회하면 생성된 항목이 포함됩니다."""
    # Given: 2개의 TODO가 생성된 상태
    client.post("/todos", json={"title": "첫 번째"})
    client.post("/todos", json={"title": "두 번째"})

    # When: 목록 조회 요청
    response = client.get("/todos")

    # Then: 2개의 항목이 포함된 응답 반환
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_조회_페이지네이션_첫페이지():
    """페이지네이션으로 첫 페이지만 조회할 수 있습니다."""
    # Given: 5개의 TODO가 생성된 상태
    for i in range(1, 6):
        client.post("/todos", json={"title": f"할 일 {i}"})

    # When: page=1, size=2로 조회 요청
    response = client.get("/todos", params={"page": 1, "size": 2})

    # Then: 2개 항목과 total=5 반환
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["size"] == 2


def test_조회_페이지네이션_마지막페이지():
    """페이지네이션으로 마지막 페이지를 조회하면 남은 항목만 반환됩니다."""
    # Given: 5개의 TODO가 생성된 상태
    for i in range(1, 6):
        client.post("/todos", json={"title": f"할 일 {i}"})

    # When: page=3, size=2로 조회 요청 (마지막 페이지)
    response = client.get("/todos", params={"page": 3, "size": 2})

    # Then: 1개 항목과 total=5 반환
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 5
    assert data["page"] == 3


# ── 우선순위 필터링 테스트 ───────────────────────────────────


def test_필터_우선순위_해당항목만반환():
    """우선순위 필터를 적용하면 해당 우선순위의 항목만 반환됩니다."""
    # Given: 다양한 우선순위의 TODO가 생성된 상태
    client.post("/todos", json={"title": "긴급", "priority": "high"})
    client.post("/todos", json={"title": "보통", "priority": "medium"})
    client.post("/todos", json={"title": "여유", "priority": "low"})
    client.post("/todos", json={"title": "또 긴급", "priority": "high"})

    # When: priority=high로 필터링 조회 요청
    response = client.get("/todos", params={"priority": "high"})

    # Then: high 우선순위 항목만 반환
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert all(item["priority"] == "high" for item in data["items"])


def test_필터_우선순위와페이지네이션_조합():
    """우선순위 필터와 페이지네이션을 함께 사용할 수 있습니다."""
    # Given: medium 우선순위 TODO가 3개 생성된 상태
    for i in range(1, 4):
        client.post("/todos", json={"title": f"보통 {i}", "priority": "medium"})
    client.post("/todos", json={"title": "긴급", "priority": "high"})

    # When: priority=medium, page=1, size=2로 조회 요청
    response = client.get(
        "/todos", params={"priority": "medium", "page": 1, "size": 2}
    )

    # Then: medium 항목 중 첫 2개와 total=3 반환
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["page"] == 1


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

    # Then: 수정된 TODO 반환 및 updated_at 설정
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "수정된 제목"
    assert data["completed"] is True
    assert data["updated_at"] is not None


def test_수정_우선순위변경_반영됨():
    """PUT으로 우선순위를 변경하면 변경된 값이 반영됩니다."""
    # Given: medium 우선순위의 TODO가 1개 생성된 상태
    client.post("/todos", json={"title": "할 일", "priority": "medium"})

    # When: PUT으로 우선순위를 high로 변경 요청
    response = client.put("/todos/1", json={"priority": "high"})

    # Then: 우선순위가 high로 변경됨
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "high"


def test_수정_마감일변경_반영됨():
    """PUT으로 마감일을 변경하면 변경된 값이 반영됩니다."""
    # Given: 마감일이 없는 TODO가 1개 생성된 상태
    client.post("/todos", json={"title": "할 일"})

    # When: PUT으로 마감일 변경 요청
    due = "2026-06-30T18:00:00"
    response = client.put("/todos/1", json={"due_date": due})

    # Then: 마감일이 설정됨
    assert response.status_code == 200
    data = response.json()
    assert data["due_date"] is not None
    assert "2026-06-30" in data["due_date"]


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

    # Then: 완료 상태만 변경되고 나머지는 유지, updated_at 설정
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "할 일"
    assert data["updated_at"] is not None


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


def test_부분수정_마감일변경_마감일만수정됨():
    """PATCH로 마감일만 변경하면 마감일만 수정되고 나머지 필드는 유지됩니다."""
    # Given: TODO가 1개 생성된 상태
    client.post("/todos", json={"title": "할 일", "priority": "high"})

    # When: PATCH로 마감일만 변경 요청
    due = "2026-09-15T10:00:00"
    response = client.patch("/todos/1", json={"due_date": due})

    # Then: 마감일만 변경되고 나머지는 유지
    assert response.status_code == 200
    data = response.json()
    assert data["due_date"] is not None
    assert "2026-09-15" in data["due_date"]
    assert data["title"] == "할 일"
    assert data["priority"] == "high"


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
    assert response.json()["total"] == 0


def test_삭제_없는항목_404반환():
    """존재하지 않는 TODO를 삭제하려 하면 404를 반환합니다."""
    # Given: 빈 저장소 상태
    # When: 존재하지 않는 ID로 삭제 요청
    response = client.delete("/todos/999")

    # Then: 404 상태코드 반환
    assert response.status_code == 404
