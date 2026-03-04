"""TODO API의 Pydantic 데이터 모델 정의 모듈.

이 모듈은 TODO API에서 사용하는 요청/응답 데이터 모델을 정의합니다.
Pydantic BaseModel을 상속하여 자동 유효성 검사를 제공합니다.

참고: Step 04에서는 schemas.py가 새로 추가되어 Priority, 페이지네이션 등
확장된 스키마를 제공합니다. 이 파일은 하위 호환성을 위해 유지됩니다.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    """TODO 생성 요청 모델.

    새로운 TODO 항목을 생성할 때 클라이언트가 전송하는 데이터 구조입니다.

    Attributes:
        title: TODO 항목의 제목. 필수 입력값입니다.
        description: TODO 항목의 상세 설명. 선택 입력값이며 기본값은 None입니다.
    """

    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    """TODO 수정 요청 모델.

    기존 TODO 항목을 부분 수정할 때 클라이언트가 전송하는 데이터 구조입니다.
    모든 필드가 선택적이므로 변경하고 싶은 필드만 전송하면 됩니다.

    Attributes:
        title: 수정할 제목. None이면 변경하지 않습니다.
        description: 수정할 설명. None이면 변경하지 않습니다.
        completed: 수정할 완료 상태. None이면 변경하지 않습니다.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    """TODO 응답 모델.

    API가 클라이언트에게 반환하는 TODO 항목의 전체 데이터 구조입니다.

    Attributes:
        id: TODO 항목의 고유 식별자.
        title: TODO 항목의 제목.
        description: TODO 항목의 상세 설명. 없을 경우 None입니다.
        completed: TODO 항목의 완료 여부. 기본값은 False입니다.
        created_at: TODO 항목이 생성된 일시.
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
