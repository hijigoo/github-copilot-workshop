"""TODO 데이터베이스 모델 모듈.

SQLModel을 사용한 TODO 테이블 모델을 정의합니다.
SQLite 데이터베이스에 저장되는 TODO 항목의 스키마입니다.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    """TODO 데이터베이스 테이블 모델.

    SQLite 데이터베이스의 todo 테이블에 매핑되는 ORM 모델입니다.

    Attributes:
        id: TODO 항목의 고유 식별자. 자동 생성되는 기본 키입니다.
        title: TODO 항목의 제목. 필수 입력값입니다.
        description: TODO 항목의 상세 설명. 선택 입력값입니다.
        priority: TODO 항목의 우선순위. 기본값은 "medium"입니다.
        completed: TODO 항목의 완료 여부. 기본값은 False입니다.
        created_at: TODO 항목이 생성된 일시. 자동으로 현재 시간이 설정됩니다.
        updated_at: TODO 항목이 마지막으로 수정된 일시. 수정 전에는 None입니다.
        due_date: TODO 항목의 마감일. 선택 입력값입니다.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    priority: str = Field(default="medium")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
