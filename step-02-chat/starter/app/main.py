from fastapi import FastAPI, HTTPException
from datetime import datetime

from app.models import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI(title="TODO API")

# 인메모리 저장소
todos: dict[int, dict] = {}
next_id: int = 1


# 모든 TODO 목록을 반환하는 엔드포인트
@app.get("/todos", response_model=list[TodoResponse])
def get_todos():
    return list(todos.values())


# 새 TODO를 생성하는 엔드포인트
@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate):
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


# 특정 TODO를 수정하는 엔드포인트
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
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


# 특정 TODO를 삭제하는 엔드포인트
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")
    del todos[todo_id]
