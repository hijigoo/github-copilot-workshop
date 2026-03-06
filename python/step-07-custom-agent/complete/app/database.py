"""데이터베이스 설정 모듈.

SQLite 데이터베이스 연결과 세션 관리를 담당합니다.
SQLModel을 사용하여 ORM 기반 데이터 접근을 제공합니다.
"""

from sqlmodel import SQLModel, Session, create_engine

# SQLite 데이터베이스 URL
DATABASE_URL = "sqlite:///./todo.db"

# SQLite는 단일 스레드가 아닌 환경에서 사용할 때 check_same_thread=False 필요
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    """데이터베이스와 테이블을 생성합니다.

    SQLModel 메타데이터를 기반으로 정의된 모든 테이블을 생성합니다.
    이미 존재하는 테이블은 무시됩니다.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """데이터베이스 세션을 생성하는 제너레이터.

    FastAPI의 Depends()와 함께 사용하여 요청마다 세션을 제공합니다.
    요청이 완료되면 세션이 자동으로 닫힙니다.

    Yields:
        Session: SQLModel 데이터베이스 세션.
    """
    with Session(engine) as session:
        yield session
