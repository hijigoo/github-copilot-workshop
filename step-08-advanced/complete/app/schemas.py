"""스키마 정의 모듈.

API 요청/응답에 사용되는 Pydantic 스키마를 정의합니다.
TODO, Category, Stats 관련 스키마를 포함합니다.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# ─── Enums ──────────────────────────────────────────────


class Priority(str, Enum):
    """우선순위 열거형.

    TODO 항목의 우선순위를 정의합니다.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ─── Category Schemas ───────────────────────────────────


class CategoryCreate(BaseModel):
    """카테고리 생성 스키마.

    Attributes:
        name: 카테고리 이름 (1-50자).
        description: 카테고리 설명 (선택).
    """

    name: str = Field(min_length=1, max_length=50, description="카테고리 이름")
    description: str | None = Field(
        default=None, max_length=200, description="카테고리 설명"
    )


class CategoryUpdate(BaseModel):
    """카테고리 수정 스키마.

    모든 필드가 선택적입니다.

    Attributes:
        name: 카테고리 이름.
        description: 카테고리 설명.
    """

    name: str | None = Field(
        default=None, min_length=1, max_length=50, description="카테고리 이름"
    )
    description: str | None = Field(
        default=None, max_length=200, description="카테고리 설명"
    )


class CategoryResponse(BaseModel):
    """카테고리 응답 스키마.

    Attributes:
        id: 카테고리 ID.
        name: 카테고리 이름.
        description: 카테고리 설명.
        created_at: 생성 시각.
    """

    id: int
    name: str
    description: str | None
    created_at: datetime


class CategoryListResponse(BaseModel):
    """카테고리 목록 응답 스키마.

    Attributes:
        items: 카테고리 목록.
        total: 전체 카테고리 수.
    """

    items: list[CategoryResponse]
    total: int


# ─── Todo Schemas ───────────────────────────────────────


class TodoCreate(BaseModel):
    """TODO 생성 스키마.

    Attributes:
        title: 할 일 제목 (1-200자, 필수).
        description: 할 일 상세 설명 (최대 1000자).
        priority: 우선순위 (low/medium/high, 기본값: medium).
        due_date: 마감일 (YYYY-MM-DD 형식).
        category_id: 카테고리 ID (선택).
    """

    title: str = Field(
        min_length=1,
        max_length=200,
        description="할 일 제목",
        examples=["FastAPI 학습하기"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="할 일 상세 설명",
        examples=["공식 문서를 읽고 실습 프로젝트를 만든다"],
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="우선순위",
    )
    due_date: str | None = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="마감일 (YYYY-MM-DD)",
        examples=["2024-12-31"],
    )
    category_id: int | None = Field(
        default=None,
        description="카테고리 ID",
    )


class TodoUpdate(BaseModel):
    """TODO 수정 스키마.

    모든 필드가 선택적입니다. 전달된 필드만 업데이트됩니다.

    Attributes:
        title: 할 일 제목.
        description: 할 일 상세 설명.
        priority: 우선순위.
        completed: 완료 여부.
        due_date: 마감일.
        category_id: 카테고리 ID.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="할 일 제목",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="할 일 상세 설명",
    )
    priority: Priority | None = Field(
        default=None,
        description="우선순위",
    )
    completed: bool | None = Field(
        default=None,
        description="완료 여부",
    )
    due_date: str | None = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="마감일 (YYYY-MM-DD)",
    )
    category_id: int | None = Field(
        default=None,
        description="카테고리 ID",
    )


class TodoResponse(BaseModel):
    """TODO 응답 스키마.

    Attributes:
        id: TODO 고유 식별자.
        title: 할 일 제목.
        description: 할 일 상세 설명.
        priority: 우선순위.
        completed: 완료 여부.
        created_at: 생성 시각.
        updated_at: 최종 수정 시각.
        due_date: 마감일.
        category_id: 카테고리 ID.
        category_name: 카테고리 이름.
    """

    id: int
    title: str
    description: str | None
    priority: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    due_date: str | None
    category_id: int | None
    category_name: str | None


class TodoListResponse(BaseModel):
    """TODO 목록 응답 스키마.

    페이지네이션을 지원하는 목록 응답입니다.

    Attributes:
        items: TODO 목록.
        total: 전체 항목 수.
        page: 현재 페이지 번호.
        size: 페이지 크기.
    """

    items: list[TodoResponse]
    total: int
    page: int
    size: int


# ─── Stats Schemas ──────────────────────────────────────


class CategoryStats(BaseModel):
    """카테고리별 통계.

    Attributes:
        category_name: 카테고리 이름.
        total: 전체 TODO 수.
        completed: 완료된 TODO 수.
        completion_rate: 완료율 (0.0 ~ 1.0).
    """

    category_name: str
    total: int
    completed: int
    completion_rate: float


class StatsResponse(BaseModel):
    """통계 응답 스키마.

    Attributes:
        total_todos: 전체 TODO 수.
        completed_todos: 완료된 TODO 수.
        completion_rate: 전체 완료율 (0.0 ~ 1.0).
        priority_distribution: 우선순위별 TODO 수.
        category_stats: 카테고리별 통계.
    """

    total_todos: int
    completed_todos: int
    completion_rate: float
    priority_distribution: dict[str, int]
    category_stats: list[CategoryStats]
