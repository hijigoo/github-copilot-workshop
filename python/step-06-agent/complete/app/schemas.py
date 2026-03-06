"""TODO API의 스키마 정의 모듈.

이 모듈은 TODO API의 요청/응답 스키마를 정의합니다.
Priority 열거형, Field 유효성 검사, 페이지네이션 응답 모델을 포함합니다.
due_date(마감일) 필드가 추가되어 TODO 항목에 마감 기한을 설정할 수 있습니다.

Note:
    이 모듈의 스키마는 순수 Pydantic 모델로, API 요청/응답 직렬화에 사용됩니다.
    데이터베이스 ORM 모델은 models.py에 별도로 정의되어 있습니다.
"""

from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """TODO 항목의 우선순위를 나타내는 열거형.

    Attributes:
        LOW: 낮은 우선순위.
        MEDIUM: 보통 우선순위.
        HIGH: 높은 우선순위.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoCreate(BaseModel):
    """TODO 생성 요청 스키마.

    새로운 TODO 항목을 생성할 때 클라이언트가 전송하는 데이터 구조입니다.
    제목은 1~200자 제한이 있으며, 우선순위와 마감일을 선택적으로 지정할 수 있습니다.

    Attributes:
        title: TODO 항목의 제목. 1자 이상 200자 이하 필수 입력값입니다.
        description: TODO 항목의 상세 설명. 선택 입력값이며 기본값은 None입니다.
        priority: TODO 항목의 우선순위. 기본값은 MEDIUM입니다.
        due_date: TODO 항목의 마감일. 선택 입력값이며 기본값은 None입니다.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="TODO 항목의 제목 (1~200자)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="TODO 항목의 상세 설명 (최대 1000자)",
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="TODO 항목의 우선순위",
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="TODO 항목의 마감일",
    )


class TodoUpdate(BaseModel):
    """TODO 수정 요청 스키마.

    기존 TODO 항목을 부분 수정할 때 클라이언트가 전송하는 데이터 구조입니다.
    모든 필드가 선택적이므로 변경하고 싶은 필드만 전송하면 됩니다.

    Attributes:
        title: 수정할 제목. None이면 변경하지 않습니다. 1~200자 제한.
        description: 수정할 설명. None이면 변경하지 않습니다.
        completed: 수정할 완료 상태. None이면 변경하지 않습니다.
        priority: 수정할 우선순위. None이면 변경하지 않습니다.
        due_date: 수정할 마감일. None이면 변경하지 않습니다.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="수정할 제목 (1~200자)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="수정할 설명 (최대 1000자)",
    )
    completed: Optional[bool] = Field(
        default=None,
        description="수정할 완료 상태",
    )
    priority: Optional[Priority] = Field(
        default=None,
        description="수정할 우선순위",
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="수정할 마감일",
    )


class TodoResponse(BaseModel):
    """TODO 응답 스키마.

    API가 클라이언트에게 반환하는 TODO 항목의 전체 데이터 구조입니다.

    Attributes:
        id: TODO 항목의 고유 식별자.
        title: TODO 항목의 제목.
        description: TODO 항목의 상세 설명. 없을 경우 None입니다.
        completed: TODO 항목의 완료 여부. 기본값은 False입니다.
        priority: TODO 항목의 우선순위. 기본값은 MEDIUM입니다.
        due_date: TODO 항목의 마감일. 설정하지 않은 경우 None입니다.
        created_at: TODO 항목이 생성된 일시.
        updated_at: TODO 항목이 마지막으로 수정된 일시. 수정 전에는 None입니다.
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class TodoListResponse(BaseModel):
    """TODO 목록 페이지네이션 응답 스키마.

    페이지네이션이 적용된 TODO 목록 조회 결과를 반환하는 데이터 구조입니다.

    Attributes:
        items: 현재 페이지의 TODO 항목 리스트.
        total: 필터 조건에 맞는 전체 TODO 항목 수.
        page: 현재 페이지 번호 (1부터 시작).
        size: 페이지당 항목 수.
    """

    items: list[TodoResponse]
    total: int
    page: int
    size: int
