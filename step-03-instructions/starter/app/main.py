"""TODO API 메인 애플리케이션 모듈.

FastAPI를 사용한 인메모리 TODO CRUD REST API를 제공합니다.
데이터는 딕셔너리 기반 인메모리 저장소에 보관되며,
서버가 재시작되면 초기화됩니다.
"""

from fastapi import FastAPI, HTTPException
from datetime import datetime

from app.models import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI(title="TODO API")

# 인메모리 저장소
todos: dict[int, dict] = {}
next_id: int = 1


@app.get("/todos", response_model=list[TodoResponse])
def get_todos():
    """전체 TODO 목록을 조회합니다.

    인메모리 저장소에 저장된 모든 TODO 항목을 리스트로 반환합니다.

    Returns:
        list[TodoResponse]: 저장된 모든 TODO 항목의 리스트.
            저장된 항목이 없으면 빈 리스트를 반환합니다.
    """
    return list(todos.values())


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate):
    """새로운 TODO 항목을 생성합니다.

    전달받은 데이터로 새 TODO를 생성하고 인메모리 저장소에 저장합니다.
    ID는 자동 증가하며, 완료 상태는 False로 초기화됩니다.

    Args:
        todo: 생성할 TODO의 제목과 설명을 담은 요청 데이터.

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
        "created_at": now,
    }
    todos[next_id] = new_todo
    next_id += 1
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    """기존 TODO 항목을 수정합니다.

    지정된 ID의 TODO 항목에서 전달받은 필드만 부분 수정합니다.
    None이 아닌 필드만 업데이트됩니다.

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
    if todo.title is not None:
        existing["title"] = todo.title
    if todo.description is not None:
        existing["description"] = todo.description
    if todo.completed is not None:
        existing["completed"] = todo.completed

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
