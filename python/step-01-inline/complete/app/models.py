from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    """TODO 생성 요청 모델"""

    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    """TODO 수정 요청 모델"""

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    """TODO 응답 모델"""

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
