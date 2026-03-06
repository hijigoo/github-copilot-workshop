"""데이터베이스 모델 정의.

SQLModel을 사용하여 데이터베이스 테이블을 정의합니다.
Todo와 Category 모델을 포함합니다.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    """카테고리 테이블.

    TODO 항목을 분류하기 위한 카테고리를 관리합니다.

    Attributes:
        id: 카테고리 고유 식별자 (자동 생성).
        name: 카테고리 이름 (고유).
        description: 카테고리 설명.
        created_at: 생성 시각.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class Todo(SQLModel, table=True):
    """TODO 항목 테이블.

    할 일 항목의 모든 정보를 저장합니다.

    Attributes:
        id: TODO 고유 식별자 (자동 생성).
        title: 할 일 제목.
        description: 할 일 상세 설명.
        priority: 우선순위 (low, medium, high).
        completed: 완료 여부.
        created_at: 생성 시각.
        updated_at: 최종 수정 시각.
        due_date: 마감일.
        category_id: 카테고리 외래키.
    """

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = None
    priority: str = Field(default="medium")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    due_date: str | None = None
    category_id: int | None = Field(default=None, foreign_key="category.id")
