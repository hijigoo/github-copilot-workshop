"""TODO API 테스트 모듈.

카테고리 CRUD, TODO CRUD, 검색, 통계, 헬스 체크 테스트를 포함합니다.
"""

import pytest
from fastapi.testclient import TestClient


# ─── Helper Functions ───────────────────────────────────


def create_test_category(client: TestClient, **overrides) -> dict:
    """테스트용 카테고리를 생성하는 헬퍼 함수."""
    data = {"name": "테스트 카테고리", "description": "테스트용 카테고리입니다"}
    data.update(overrides)
    response = client.post("/api/v1/categories", json=data)
    assert response.status_code == 201
    return response.json()


def create_test_todo(client: TestClient, **overrides) -> dict:
    """테스트용 TODO를 생성하는 헬퍼 함수."""
    data = {
        "title": "테스트 할 일",
        "description": "테스트 설명입니다",
        "priority": "medium",
    }
    data.update(overrides)
    response = client.post("/api/v1/todos", json=data)
    assert response.status_code == 201
    return response.json()


# ─── Health Check ───────────────────────────────────────


class TestHealthCheck:
    """GET /health 테스트"""

    def test_health_check(self, client):
        """헬스 체크가 정상 응답을 반환합니다."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


# ─── Category CRUD Tests ───────────────────────────────


class TestCreateCategory:
    """POST /api/v1/categories 테스트"""

    def test_create_category(self, client):
        """유효한 데이터로 카테고리를 생성합니다."""
        response = client.post(
            "/api/v1/categories",
            json={"name": "업무", "description": "업무 관련 할 일"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "업무"
        assert data["description"] == "업무 관련 할 일"
        assert "id" in data
        assert "created_at" in data

    def test_create_category_without_description(self, client):
        """설명 없이 카테고리를 생성합니다."""
        response = client.post(
            "/api/v1/categories",
            json={"name": "개인"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "개인"
        assert data["description"] is None

    def test_create_category_empty_name(self, client):
        """빈 이름으로 카테고리 생성 시 422를 반환합니다."""
        response = client.post(
            "/api/v1/categories",
            json={"name": ""},
        )
        assert response.status_code == 422

    def test_create_category_long_name(self, client):
        """50자를 초과하는 이름으로 카테고리 생성 시 422를 반환합니다."""
        response = client.post(
            "/api/v1/categories",
            json={"name": "가" * 51},
        )
        assert response.status_code == 422


class TestListCategories:
    """GET /api/v1/categories 테스트"""

    def test_list_categories_empty(self, client):
        """카테고리가 없을 때 빈 목록을 반환합니다."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_categories(self, client):
        """여러 카테고리를 목록으로 조회합니다."""
        create_test_category(client, name="업무")
        create_test_category(client, name="개인")
        create_test_category(client, name="학습")

        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3


class TestGetCategory:
    """GET /api/v1/categories/{id} 테스트"""

    def test_get_category(self, client):
        """카테고리를 ID로 조회합니다."""
        created = create_test_category(client, name="업무")
        response = client.get(f"/api/v1/categories/{created['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "업무"

    def test_get_category_not_found(self, client):
        """존재하지 않는 카테고리 조회 시 404를 반환합니다."""
        response = client.get("/api/v1/categories/9999")
        assert response.status_code == 404


class TestUpdateCategory:
    """PATCH /api/v1/categories/{id} 테스트"""

    def test_update_category_name(self, client):
        """카테고리 이름을 수정합니다."""
        created = create_test_category(client, name="업무")
        response = client.patch(
            f"/api/v1/categories/{created['id']}",
            json={"name": "회사 업무"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "회사 업무"

    def test_update_category_not_found(self, client):
        """존재하지 않는 카테고리 수정 시 404를 반환합니다."""
        response = client.patch(
            "/api/v1/categories/9999",
            json={"name": "없는 카테고리"},
        )
        assert response.status_code == 404


class TestDeleteCategory:
    """DELETE /api/v1/categories/{id} 테스트"""

    def test_delete_category(self, client):
        """카테고리를 삭제합니다."""
        created = create_test_category(client, name="삭제용")
        response = client.delete(f"/api/v1/categories/{created['id']}")
        assert response.status_code == 204

        # 삭제 확인
        response = client.get(f"/api/v1/categories/{created['id']}")
        assert response.status_code == 404

    def test_delete_category_not_found(self, client):
        """존재하지 않는 카테고리 삭제 시 404를 반환합니다."""
        response = client.delete("/api/v1/categories/9999")
        assert response.status_code == 404


# ─── Todo CRUD Tests ────────────────────────────────────


class TestCreateTodo:
    """POST /api/v1/todos 테스트"""

    def test_create_todo(self, client):
        """유효한 데이터로 TODO를 생성합니다."""
        response = client.post(
            "/api/v1/todos",
            json={
                "title": "FastAPI 학습",
                "description": "공식 문서 읽기",
                "priority": "high",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "FastAPI 학습"
        assert data["priority"] == "high"
        assert data["completed"] is False
        assert data["category_id"] is None
        assert data["category_name"] is None

    def test_create_todo_with_category(self, client):
        """카테고리를 지정하여 TODO를 생성합니다."""
        category = create_test_category(client, name="학습")
        response = client.post(
            "/api/v1/todos",
            json={
                "title": "Python 학습",
                "priority": "medium",
                "category_id": category["id"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["category_id"] == category["id"]
        assert data["category_name"] == "학습"

    def test_create_todo_with_invalid_category(self, client):
        """존재하지 않는 카테고리로 TODO 생성 시 404를 반환합니다."""
        response = client.post(
            "/api/v1/todos",
            json={
                "title": "잘못된 카테고리",
                "category_id": 9999,
            },
        )
        assert response.status_code == 404

    def test_create_todo_minimal(self, client):
        """제목만으로 TODO를 생성합니다."""
        response = client.post(
            "/api/v1/todos",
            json={"title": "간단한 할 일"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "간단한 할 일"
        assert data["priority"] == "medium"

    def test_create_todo_empty_title(self, client):
        """빈 제목으로 TODO 생성 시 422를 반환합니다."""
        response = client.post("/api/v1/todos", json={"title": ""})
        assert response.status_code == 422

    def test_create_todo_long_title(self, client):
        """200자를 초과하는 제목으로 TODO 생성 시 422를 반환합니다."""
        response = client.post(
            "/api/v1/todos",
            json={"title": "가" * 201},
        )
        assert response.status_code == 422

    def test_create_todo_with_due_date(self, client):
        """마감일을 지정하여 TODO를 생성합니다."""
        response = client.post(
            "/api/v1/todos",
            json={"title": "마감일 있는 할 일", "due_date": "2026-12-31"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["due_date"] == "2026-12-31"

    def test_create_todo_invalid_due_date(self, client):
        """잘못된 마감일 형식으로 TODO 생성 시 422를 반환합니다."""
        response = client.post(
            "/api/v1/todos",
            json={"title": "잘못된 날짜", "due_date": "2026/12/31"},
        )
        assert response.status_code == 422

    def test_create_todo_invalid_priority(self, client):
        """잘못된 우선순위로 TODO 생성 시 422를 반환합니다."""
        response = client.post(
            "/api/v1/todos",
            json={"title": "잘못된 우선순위", "priority": "urgent"},
        )
        assert response.status_code == 422


class TestGetTodo:
    """GET /api/v1/todos/{id} 테스트"""

    def test_get_todo(self, client):
        """TODO를 ID로 조회합니다."""
        created = create_test_todo(client, title="조회 테스트")
        response = client.get(f"/api/v1/todos/{created['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "조회 테스트"

    def test_get_todo_not_found(self, client):
        """존재하지 않는 TODO 조회 시 404를 반환합니다."""
        response = client.get("/api/v1/todos/9999")
        assert response.status_code == 404


class TestListTodos:
    """GET /api/v1/todos 테스트"""

    def test_list_todos_empty(self, client):
        """TODO가 없을 때 빈 목록을 반환합니다."""
        response = client.get("/api/v1/todos")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["size"] == 10

    def test_list_todos_pagination(self, client):
        """페이지네이션이 올바르게 동작합니다."""
        for i in range(15):
            create_test_todo(client, title=f"할 일 {i}")

        # 1페이지
        response = client.get("/api/v1/todos?page=1&size=10")
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15

        # 2페이지
        response = client.get("/api/v1/todos?page=2&size=10")
        data = response.json()
        assert len(data["items"]) == 5
        assert data["total"] == 15

    def test_list_todos_filter_priority(self, client):
        """우선순위로 필터링합니다."""
        create_test_todo(client, title="높은 우선순위", priority="high")
        create_test_todo(client, title="낮은 우선순위", priority="low")

        response = client.get("/api/v1/todos?priority=high")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "높은 우선순위"

    def test_list_todos_filter_completed(self, client):
        """완료 여부로 필터링합니다."""
        todo = create_test_todo(client, title="완료할 일")
        client.patch(f"/api/v1/todos/{todo['id']}", json={"completed": True})
        create_test_todo(client, title="미완료 할 일")

        response = client.get("/api/v1/todos?completed=true")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "완료할 일"

    def test_list_todos_filter_category(self, client):
        """카테고리로 필터링합니다."""
        category = create_test_category(client, name="업무")
        create_test_todo(client, title="업무 할 일", category_id=category["id"])
        create_test_todo(client, title="개인 할 일")

        response = client.get(f"/api/v1/todos?category_id={category['id']}")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "업무 할 일"


class TestUpdateTodo:
    """PATCH /api/v1/todos/{id} 테스트"""

    def test_update_todo_title(self, client):
        """TODO 제목을 수정합니다."""
        created = create_test_todo(client, title="원래 제목")
        response = client.patch(
            f"/api/v1/todos/{created['id']}",
            json={"title": "수정된 제목"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "수정된 제목"

    def test_update_todo_completed(self, client):
        """TODO 완료 상태를 변경합니다."""
        created = create_test_todo(client)
        response = client.patch(
            f"/api/v1/todos/{created['id']}",
            json={"completed": True},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_update_todo_category(self, client):
        """TODO에 카테고리를 지정합니다."""
        category = create_test_category(client, name="업무")
        created = create_test_todo(client)
        response = client.patch(
            f"/api/v1/todos/{created['id']}",
            json={"category_id": category["id"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["category_id"] == category["id"]
        assert data["category_name"] == "업무"

    def test_update_todo_invalid_category(self, client):
        """존재하지 않는 카테고리로 수정 시 404를 반환합니다."""
        created = create_test_todo(client)
        response = client.patch(
            f"/api/v1/todos/{created['id']}",
            json={"category_id": 9999},
        )
        assert response.status_code == 404

    def test_update_todo_not_found(self, client):
        """존재하지 않는 TODO 수정 시 404를 반환합니다."""
        response = client.patch(
            "/api/v1/todos/9999",
            json={"title": "없는 할 일"},
        )
        assert response.status_code == 404


class TestDeleteTodo:
    """DELETE /api/v1/todos/{id} 테스트"""

    def test_delete_todo(self, client):
        """TODO를 삭제합니다."""
        created = create_test_todo(client)
        response = client.delete(f"/api/v1/todos/{created['id']}")
        assert response.status_code == 204

        response = client.get(f"/api/v1/todos/{created['id']}")
        assert response.status_code == 404

    def test_delete_todo_not_found(self, client):
        """존재하지 않는 TODO 삭제 시 404를 반환합니다."""
        response = client.delete("/api/v1/todos/9999")
        assert response.status_code == 404


# ─── Search Tests ───────────────────────────────────────


class TestSearch:
    """GET /api/v1/todos?q= 검색 테스트"""

    def test_search_by_title(self, client):
        """제목으로 검색합니다."""
        create_test_todo(client, title="FastAPI 학습하기")
        create_test_todo(client, title="React 학습하기")
        create_test_todo(client, title="운동하기")

        response = client.get("/api/v1/todos?q=학습")
        data = response.json()
        assert data["total"] == 2

    def test_search_by_description(self, client):
        """설명으로 검색합니다."""
        create_test_todo(
            client, title="할 일 1", description="Python 공식 문서를 읽습니다"
        )
        create_test_todo(
            client, title="할 일 2", description="JavaScript 튜토리얼을 봅니다"
        )

        response = client.get("/api/v1/todos?q=Python")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "할 일 1"

    def test_search_no_results(self, client):
        """검색 결과가 없으면 빈 목록을 반환합니다."""
        create_test_todo(client, title="일반 할 일")

        response = client.get("/api/v1/todos?q=존재하지않는키워드")
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_search_with_filter(self, client):
        """검색과 필터를 동시에 사용합니다."""
        create_test_todo(client, title="FastAPI 학습", priority="high")
        create_test_todo(client, title="FastAPI 복습", priority="low")

        response = client.get("/api/v1/todos?q=FastAPI&priority=high")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["priority"] == "high"


# ─── Stats Tests ────────────────────────────────────────


class TestStats:
    """GET /api/v1/stats 테스트"""

    def test_stats_empty(self, client):
        """TODO가 없을 때 기본 통계를 반환합니다."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_todos"] == 0
        assert data["completed_todos"] == 0
        assert data["completion_rate"] == 0.0
        assert data["priority_distribution"] == {
            "low": 0,
            "medium": 0,
            "high": 0,
        }
        assert data["category_stats"] == []

    def test_stats_with_todos(self, client):
        """TODO가 있을 때 올바른 통계를 반환합니다."""
        # 카테고리 생성
        work = create_test_category(client, name="업무")
        personal = create_test_category(client, name="개인")

        # TODO 생성
        todo1 = create_test_todo(
            client, title="업무 1", priority="high", category_id=work["id"]
        )
        create_test_todo(
            client, title="업무 2", priority="medium", category_id=work["id"]
        )
        create_test_todo(
            client, title="개인 1", priority="low", category_id=personal["id"]
        )
        create_test_todo(client, title="미분류", priority="high")

        # 1개 완료 처리
        client.patch(f"/api/v1/todos/{todo1['id']}", json={"completed": True})

        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()

        assert data["total_todos"] == 4
        assert data["completed_todos"] == 1
        assert data["completion_rate"] == 0.25
        assert data["priority_distribution"]["high"] == 2
        assert data["priority_distribution"]["medium"] == 1
        assert data["priority_distribution"]["low"] == 1

        # 카테고리별 통계 확인
        cat_stats = {s["category_name"]: s for s in data["category_stats"]}
        assert "업무" in cat_stats
        assert cat_stats["업무"]["total"] == 2
        assert cat_stats["업무"]["completed"] == 1
        assert cat_stats["업무"]["completion_rate"] == 0.5
        assert "개인" in cat_stats
        assert cat_stats["개인"]["total"] == 1
        assert cat_stats["개인"]["completed"] == 0
        assert "미분류" in cat_stats
        assert cat_stats["미분류"]["total"] == 1

    def test_stats_completion_rate(self, client):
        """완료율이 올바르게 계산됩니다."""
        todo1 = create_test_todo(client, title="할 일 1")
        todo2 = create_test_todo(client, title="할 일 2")
        create_test_todo(client, title="할 일 3")

        client.patch(f"/api/v1/todos/{todo1['id']}", json={"completed": True})
        client.patch(f"/api/v1/todos/{todo2['id']}", json={"completed": True})

        response = client.get("/api/v1/stats")
        data = response.json()
        assert data["total_todos"] == 3
        assert data["completed_todos"] == 2
        assert abs(data["completion_rate"] - 0.67) < 0.01
