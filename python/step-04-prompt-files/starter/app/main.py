"""TODO API 메인 애플리케이션 모듈.

FastAPI를 사용한 인메모리 TODO CRUD REST API를 제공합니다.
Priority(우선순위) 지원, 페이지네이션, 필터링 기능이 포함됩니다.
데이터는 딕셔너리 기반 인메모리 저장소에 보관되며,
서버가 재시작되면 초기화됩니다.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from datetime import datetime

from app.schemas import (
    Priority,
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
)

app = FastAPI(title="TODO API")

# 인메모리 저장소
todos: dict[int, dict] = {}
next_id: int = 1


@app.get("/todos", response_model=TodoListResponse)
def get_todos(
    priority: Optional[Priority] = Query(
        default=None, description="우선순위로 필터링"
    ),
    page: int = Query(default=1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(default=10, ge=1, le=100, description="페이지당 항목 수"),
):
    """TODO 목록을 조회합니다 (필터링 + 페이지네이션).

    인메모리 저장소에 저장된 TODO 항목을 조회합니다.
    우선순위 필터와 페이지네이션을 지원합니다.

    Args:
        priority: 필터링할 우선순위. None이면 전체 조회합니다.
        page: 조회할 페이지 번호. 1부터 시작하며 기본값은 1입니다.
        size: 페이지당 항목 수. 기본값은 10이며 최대 100입니다.

    Returns:
        TodoListResponse: 페이지네이션이 적용된 TODO 목록 응답.
    """
    # 전체 목록에서 필터링
    items = list(todos.values())
    if priority is not None:
        items = [item for item in items if item["priority"] == priority.value]

    # 전체 개수 (필터 적용 후)
    total = len(items)

    # 페이지네이션 적용
    start = (page - 1) * size
    end = start + size
    paginated_items = items[start:end]

    return TodoListResponse(
        items=paginated_items,
        total=total,
        page=page,
        size=size,
    )


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate):
    """새로운 TODO 항목을 생성합니다.

    전달받은 데이터로 새 TODO를 생성하고 인메모리 저장소에 저장합니다.
    ID는 자동 증가하며, 완료 상태는 False로 초기화됩니다.

    Args:
        todo: 생성할 TODO의 제목, 설명, 우선순위를 담은 요청 데이터.

    Returns:
        TodoResponse: 생성된 TODO 항목의 전체 정보.
    """
    global next_id
    now = datetime.now()
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "priority": todo.priority.value,
        "created_at": now,
        "updated_at": None,
    }
    todos[next_id] = new_todo
    next_id += 1
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    """기존 TODO 항목을 전체 수정합니다.

    지정된 ID의 TODO 항목에서 전달받은 필드만 업데이트합니다.
    None이 아닌 필드만 업데이트되며, 수정 시 updated_at이 갱신됩니다.

    Args:
        todo_id: 수정할 TODO 항목의 고유 ID.
        todo: 수정할 필드를 담은 요청 데이터.

    Returns:
        TodoResponse: 수정된 TODO 항목의 전체 정보.

    Raises:
        HTTPException: 해당 ID의 TODO가 존재하지 않을 때 404 에러를 발생시킵니다.
    """
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")

    existing = todos[todo_id]
    updated = False

    if todo.title is not None:
        existing["title"] = todo.title
        updated = True
    if todo.description is not None:
        existing["description"] = todo.description
        updated = True
    if todo.completed is not None:
        existing["completed"] = todo.completed
        updated = True
    if todo.priority is not None:
        existing["priority"] = todo.priority.value
        updated = True

    if updated:
        existing["updated_at"] = datetime.now()

    return existing


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def patch_todo(todo_id: int, todo: TodoUpdate):
    """TODO 항목을 부분 수정합니다.

    지정된 ID의 TODO 항목에서 전달받은 필드만 부분 수정합니다.
    PUT과 달리 PATCH는 변경이 필요한 필드만 전송하면 됩니다.
    model_dump(exclude_unset=True)를 사용하여 명시적으로 전달된 필드만 업데이트합니다.
    수정된 필드가 있으면 updated_at이 갱신됩니다.

    Args:
        todo_id: 수정할 TODO 항목의 고유 ID.
        todo: 수정할 필드를 담은 요청 데이터.

    Returns:
        TodoResponse: 수정된 TODO 항목의 전체 정보.

    Raises:
        HTTPException: 해당 ID의 TODO가 존재하지 않을 때 404 에러를 발생시킵니다.
    """
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")

    existing = todos[todo_id]
    update_data = todo.model_dump(exclude_unset=True)

    # priority는 Enum 값을 문자열로 변환하여 저장
    if "priority" in update_data and update_data["priority"] is not None:
        update_data["priority"] = update_data["priority"].value

    if update_data:
        for key, value in update_data.items():
            existing[key] = value
        existing["updated_at"] = datetime.now()

    return existing


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    """특정 TODO 항목을 삭제합니다.

    지정된 ID의 TODO 항목을 인메모리 저장소에서 제거합니다.

    Args:
        todo_id: 삭제할 TODO 항목의 고유 ID.

    Raises:
        HTTPException: 해당 ID의 TODO가 존재하지 않을 때 404 에러를 발생시킵니다.
    """
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")
    del todos[todo_id]
