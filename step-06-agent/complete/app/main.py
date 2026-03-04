"""TODO API 메인 애플리케이션 모듈.

FastAPI를 사용한 SQLite 기반 TODO CRUD REST API를 제공합니다.
Priority(우선순위) 지원, 마감일(due_date), 페이지네이션, 필터링 기능이 포함됩니다.
데이터는 SQLite 데이터베이스에 영구 저장되며, SQLModel ORM을 통해 접근합니다.
"""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import Session, select, func
from datetime import datetime

from app.schemas import (
    Priority,
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
)
from app.models import Todo
from app.database import create_db_and_tables, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작 시 데이터베이스와 테이블을 생성합니다."""
    create_db_and_tables()
    yield


app = FastAPI(title="TODO API", lifespan=lifespan)


def _todo_to_response(todo: Todo) -> TodoResponse:
    """Todo ORM 모델을 TodoResponse Pydantic 모델로 변환합니다.

    Args:
        todo: 데이터베이스에서 조회한 Todo ORM 인스턴스.

    Returns:
        TodoResponse: API 응답용 Pydantic 모델.
    """
    return TodoResponse(
        id=todo.id,  # type: ignore
        title=todo.title,
        description=todo.description,
        priority=Priority(todo.priority),
        completed=todo.completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        due_date=todo.due_date,
    )


@app.get("/todos", response_model=TodoListResponse)
def get_todos(
    session: Session = Depends(get_session),
    priority: Optional[Priority] = Query(
        default=None, description="우선순위로 필터링"
    ),
    page: int = Query(default=1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(default=10, ge=1, le=100, description="페이지당 항목 수"),
):
    """TODO 목록을 조회합니다 (필터링 + 페이지네이션).

    SQLite 데이터베이스에서 TODO 항목을 조회합니다.
    우선순위 필터와 페이지네이션을 지원합니다.

    Args:
        session: SQLModel 데이터베이스 세션 (의존성 주입).
        priority: 필터링할 우선순위. None이면 전체 조회합니다.
        page: 조회할 페이지 번호. 1부터 시작하며 기본값은 1입니다.
        size: 페이지당 항목 수. 기본값은 10이며 최대 100입니다.

    Returns:
        TodoListResponse: 페이지네이션이 적용된 TODO 목록 응답.
    """
    # 기본 쿼리 구성
    statement = select(Todo)
    count_statement = select(func.count()).select_from(Todo)

    # 우선순위 필터 적용
    if priority is not None:
        statement = statement.where(Todo.priority == priority.value)
        count_statement = count_statement.where(Todo.priority == priority.value)

    # 전체 개수 조회 (필터 적용 후)
    total = session.exec(count_statement).one()

    # 페이지네이션 적용
    offset = (page - 1) * size
    statement = statement.offset(offset).limit(size)
    todos = session.exec(statement).all()

    # ORM 모델을 응답 모델로 변환
    items = [_todo_to_response(todo) for todo in todos]

    return TodoListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
    )


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
):
    """새로운 TODO 항목을 생성합니다.

    전달받은 데이터로 새 TODO를 생성하고 SQLite 데이터베이스에 저장합니다.
    ID는 자동 생성되며, 완료 상태는 False로 초기화됩니다.

    Args:
        todo: 생성할 TODO의 제목, 설명, 우선순위, 마감일을 담은 요청 데이터.
        session: SQLModel 데이터베이스 세션 (의존성 주입).

    Returns:
        TodoResponse: 생성된 TODO 항목의 전체 정보.
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority.value,
        completed=False,
        created_at=datetime.now(),
        due_date=todo.due_date,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return _todo_to_response(db_todo)


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    session: Session = Depends(get_session),
):
    """기존 TODO 항목을 전체 수정합니다.

    지정된 ID의 TODO 항목에서 전달받은 필드만 업데이트합니다.
    None이 아닌 필드만 업데이트되며, 수정 시 updated_at이 갱신됩니다.

    Args:
        todo_id: 수정할 TODO 항목의 고유 ID.
        todo: 수정할 필드를 담은 요청 데이터.
        session: SQLModel 데이터베이스 세션 (의존성 주입).

    Returns:
        TodoResponse: 수정된 TODO 항목의 전체 정보.

    Raises:
        HTTPException: 해당 ID의 TODO가 존재하지 않을 때 404 에러를 발생시킵니다.
    """
    db_todo = session.get(Todo, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")

    updated = False

    if todo.title is not None:
        db_todo.title = todo.title
        updated = True
    if todo.description is not None:
        db_todo.description = todo.description
        updated = True
    if todo.completed is not None:
        db_todo.completed = todo.completed
        updated = True
    if todo.priority is not None:
        db_todo.priority = todo.priority.value
        updated = True
    if todo.due_date is not None:
        db_todo.due_date = todo.due_date
        updated = True

    if updated:
        db_todo.updated_at = datetime.now()

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return _todo_to_response(db_todo)


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def patch_todo(
    todo_id: int,
    todo: TodoUpdate,
    session: Session = Depends(get_session),
):
    """TODO 항목을 부분 수정합니다.

    지정된 ID의 TODO 항목에서 전달받은 필드만 부분 수정합니다.
    PUT과 달리 PATCH는 변경이 필요한 필드만 전송하면 됩니다.
    model_dump(exclude_unset=True)를 사용하여 명시적으로 전달된 필드만 업데이트합니다.
    수정된 필드가 있으면 updated_at이 갱신됩니다.

    Args:
        todo_id: 수정할 TODO 항목의 고유 ID.
        todo: 수정할 필드를 담은 요청 데이터.
        session: SQLModel 데이터베이스 세션 (의존성 주입).

    Returns:
        TodoResponse: 수정된 TODO 항목의 전체 정보.

    Raises:
        HTTPException: 해당 ID의 TODO가 존재하지 않을 때 404 에러를 발생시킵니다.
    """
    db_todo = session.get(Todo, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")

    update_data = todo.model_dump(exclude_unset=True)

    # priority는 Enum 값을 문자열로 변환하여 저장
    if "priority" in update_data and update_data["priority"] is not None:
        update_data["priority"] = update_data["priority"].value

    if update_data:
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db_todo.updated_at = datetime.now()

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return _todo_to_response(db_todo)


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
):
    """특정 TODO 항목을 삭제합니다.

    지정된 ID의 TODO 항목을 데이터베이스에서 제거합니다.

    Args:
        todo_id: 삭제할 TODO 항목의 고유 ID.
        session: SQLModel 데이터베이스 세션 (의존성 주입).

    Raises:
        HTTPException: 해당 ID의 TODO가 존재하지 않을 때 404 에러를 발생시킵니다.
    """
    db_todo = session.get(Todo, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")

    session.delete(db_todo)
    session.commit()
