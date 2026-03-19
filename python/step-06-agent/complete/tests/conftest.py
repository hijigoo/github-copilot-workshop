"""테스트 픽스처 설정 모듈.

테스트용 인메모리 SQLite 데이터베이스를 설정하고,
FastAPI의 의존성 주입을 오버라이드하여 테스트 격리를 보장합니다.
각 테스트마다 새로운 테이블이 생성되고 정리됩니다.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session


@pytest.fixture(name="session", autouse=True)
def session_fixture():
    """테스트용 인메모리 SQLite 데이터베이스 세션을 생성합니다.

    각 테스트마다 새로운 인메모리 데이터베이스를 생성하여
    테스트 간 데이터 격리를 보장합니다.

    Yields:
        Session: 테스트용 SQLModel 데이터베이스 세션.
    """
    # 테스트용 인메모리 SQLite 엔진 생성
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # 테이블 생성
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # get_session 의존성을 테스트용 세션으로 오버라이드
        def get_session_override():
            yield session

        app.dependency_overrides[get_session] = get_session_override

        yield session

    # 테스트 후 오버라이드 해제
    app.dependency_overrides.clear()


@pytest.fixture(name="client")
def client_fixture():
    """테스트용 FastAPI TestClient를 생성합니다.

    Returns:
        TestClient: 테스트용 HTTP 클라이언트.
    """
    return TestClient(app)
