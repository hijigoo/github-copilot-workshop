"""헬스 체크 엔드포인트 테스트."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """헬스 체크가 정상 응답을 반환하는지 확인합니다."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
