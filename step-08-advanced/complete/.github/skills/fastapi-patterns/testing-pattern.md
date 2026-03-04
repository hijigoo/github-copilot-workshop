# FastAPI Testing Pattern Skill

This skill teaches the standard testing patterns used in our FastAPI + SQLModel project.

## Test Setup

### conftest.py Pattern
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    """테스트용 인메모리 SQLite 세션을 생성합니다."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """테스트용 FastAPI 클라이언트를 생성합니다."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

## Test Structure

### Class-Based Test Organization
```python
class TestCreateResource:
    """POST /api/v1/resources 테스트"""

    def test_create_success(self, client):
        """유효한 데이터로 리소스 생성"""
        response = client.post("/api/v1/resources", json={
            "title": "Test Resource",
            "description": "Test description",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Resource"
        assert "id" in data

    def test_create_missing_required_field(self, client):
        """필수 필드 누락 시 422 반환"""
        response = client.post("/api/v1/resources", json={})
        assert response.status_code == 422

    def test_create_validation_error(self, client):
        """유효성 검사 실패 시 422 반환"""
        response = client.post("/api/v1/resources", json={
            "title": "",  # min_length=1 violation
        })
        assert response.status_code == 422
```

### Helper Functions
```python
def create_test_resource(client, **overrides):
    """테스트용 리소스를 생성하는 헬퍼 함수"""
    data = {
        "title": "Test Resource",
        "description": "Test description",
        "priority": "medium",
    }
    data.update(overrides)
    response = client.post("/api/v1/resources", json=data)
    assert response.status_code == 201
    return response.json()
```

## Test Categories

### 1. Happy Path Tests
- Create with valid data → 201
- Get existing resource → 200
- List resources → 200 with pagination
- Update with valid data → 200
- Delete existing resource → 204

### 2. Validation Error Tests
- Missing required field → 422
- Invalid field value → 422
- Field constraint violation → 422

### 3. Not Found Tests
- Get non-existent resource → 404
- Update non-existent resource → 404
- Delete non-existent resource → 404

### 4. Edge Case Tests
- Boundary values (min/max length)
- Empty string vs None
- Pagination edge cases (page=0, size=0)
- Partial update (only some fields)

### 5. Filter/Search Tests
- Filter by specific field
- Multiple filters combined
- Invalid filter values

## Key Principles

1. **Isolation**: Each test uses a fresh in-memory database
2. **AAA Pattern**: Arrange → Act → Assert
3. **Descriptive Names**: `test_create_todo_with_high_priority`
4. **Korean Docstrings**: Describe what each test verifies
5. **Helper Functions**: Reduce boilerplate with `create_test_*` helpers
6. **Assert Specifics**: Check status codes AND response body fields
