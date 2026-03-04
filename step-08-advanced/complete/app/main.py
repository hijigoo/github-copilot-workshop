"""TODO 앱 메인 모듈.

FastAPI 애플리케이션과 모든 API 엔드포인트를 정의합니다.
카테고리 시스템, 검색, 통계, production-ready 기능을 포함합니다.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, func, select

from app.database import create_db_and_tables, get_session
from app.models import Category, Todo
from app.schemas import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryStats,
    CategoryUpdate,
    StatsResponse,
    TodoCreate,
    TodoListResponse,
    TodoResponse,
    TodoUpdate,
)

# ─── Logging ────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("todo_app")


# ─── Lifespan ───────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 라이프사이클 관리자.

    시작 시 데이터베이스 테이블을 생성합니다.
    """
    logger.info("애플리케이션 시작 - 데이터베이스 초기화")
    create_db_and_tables()
    yield
    logger.info("애플리케이션 종료")


# ─── App ────────────────────────────────────────────────

app = FastAPI(
    title="TODO API",
    description="GitHub Copilot 워크숍용 TODO API — Step 08 Advanced",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 미들웨어 — 프론트엔드(localhost:5173) 연동 지원
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request Logging Middleware ─────────────────────────


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """요청/응답을 로깅하는 미들웨어."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} → {response.status_code}")
    return response


# ─── Health Check ───────────────────────────────────────


@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트.

    Returns:
        dict: 애플리케이션 상태.
    """
    return {"status": "healthy", "version": "1.0.0"}


# ─── Helpers ────────────────────────────────────────────


def _todo_to_response(todo: Todo, session: Session) -> TodoResponse:
    """Todo 모델을 TodoResponse 스키마로 변환합니다.

    카테고리가 지정된 경우 카테고리 이름도 포함합니다.

    Args:
        todo: 데이터베이스 Todo 모델.
        session: 데이터베이스 세션.

    Returns:
        TodoResponse: API 응답용 스키마.
    """
    category_name = None
    if todo.category_id:
        category = session.get(Category, todo.category_id)
        if category:
            category_name = category.name

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=todo.completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        due_date=todo.due_date,
        category_id=todo.category_id,
        category_name=category_name,
    )


def _category_to_response(category: Category) -> CategoryResponse:
    """Category 모델을 CategoryResponse 스키마로 변환합니다.

    Args:
        category: 데이터베이스 Category 모델.

    Returns:
        CategoryResponse: API 응답용 스키마.
    """
    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        created_at=category.created_at,
    )


# ─── Category CRUD ──────────────────────────────────────


@app.post(
    "/api/v1/categories",
    response_model=CategoryResponse,
    status_code=201,
)
def create_category(
    data: CategoryCreate,
    session: Session = Depends(get_session),
):
    """카테고리를 생성합니다.

    Args:
        data: 카테고리 생성 데이터.
        session: 데이터베이스 세션.

    Returns:
        CategoryResponse: 생성된 카테고리.
    """
    logger.info(f"카테고리 생성: {data.name}")
    category = Category(**data.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return _category_to_response(category)


@app.get(
    "/api/v1/categories",
    response_model=CategoryListResponse,
)
def list_categories(
    session: Session = Depends(get_session),
):
    """카테고리 목록을 조회합니다.

    Args:
        session: 데이터베이스 세션.

    Returns:
        CategoryListResponse: 카테고리 목록과 전체 수.
    """
    categories = session.exec(select(Category)).all()
    total = session.exec(select(func.count(Category.id))).one()
    return CategoryListResponse(
        items=[_category_to_response(c) for c in categories],
        total=total,
    )


@app.get(
    "/api/v1/categories/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    """카테고리를 조회합니다.

    Args:
        category_id: 카테고리 ID.
        session: 데이터베이스 세션.

    Returns:
        CategoryResponse: 카테고리 정보.

    Raises:
        HTTPException: 카테고리를 찾을 수 없는 경우 (404).
    """
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return _category_to_response(category)


@app.patch(
    "/api/v1/categories/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    session: Session = Depends(get_session),
):
    """카테고리를 수정합니다.

    Args:
        category_id: 카테고리 ID.
        data: 수정할 데이터.
        session: 데이터베이스 세션.

    Returns:
        CategoryResponse: 수정된 카테고리.

    Raises:
        HTTPException: 카테고리를 찾을 수 없는 경우 (404).
    """
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    logger.info(f"카테고리 수정: {category_id}")
    return _category_to_response(category)


@app.delete("/api/v1/categories/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    """카테고리를 삭제합니다.

    Args:
        category_id: 카테고리 ID.
        session: 데이터베이스 세션.

    Raises:
        HTTPException: 카테고리를 찾을 수 없는 경우 (404).
    """
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    logger.info(f"카테고리 삭제: {category_id}")


# ─── Todo CRUD ──────────────────────────────────────────


@app.post(
    "/api/v1/todos",
    response_model=TodoResponse,
    status_code=201,
)
def create_todo(
    data: TodoCreate,
    session: Session = Depends(get_session),
):
    """TODO 항목을 생성합니다.

    Args:
        data: TODO 생성 데이터.
        session: 데이터베이스 세션.

    Returns:
        TodoResponse: 생성된 TODO 항목.

    Raises:
        HTTPException: 카테고리가 존재하지 않는 경우 (404).
    """
    # 카테고리 존재 여부 확인
    if data.category_id is not None:
        category = session.get(Category, data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    logger.info(f"TODO 생성: {data.title}")
    todo = Todo(**data.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return _todo_to_response(todo, session)


@app.get(
    "/api/v1/todos",
    response_model=TodoListResponse,
)
def list_todos(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    priority: str | None = Query(None, description="우선순위 필터"),
    completed: bool | None = Query(None, description="완료 여부 필터"),
    category_id: int | None = Query(None, description="카테고리 ID 필터"),
    q: str | None = Query(None, description="검색 키워드 (제목, 설명)"),
    session: Session = Depends(get_session),
):
    """TODO 목록을 조회합니다.

    페이지네이션, 필터링, 검색을 지원합니다.

    Args:
        page: 페이지 번호 (1부터 시작).
        size: 페이지 크기 (최대 100).
        priority: 우선순위 필터.
        completed: 완료 여부 필터.
        category_id: 카테고리 ID 필터.
        q: 검색 키워드 (제목과 설명에서 검색).
        session: 데이터베이스 세션.

    Returns:
        TodoListResponse: TODO 목록과 페이지네이션 정보.
    """
    offset = (page - 1) * size

    # 기본 쿼리
    statement = select(Todo)
    count_statement = select(func.count(Todo.id))

    # 필터 적용
    if priority is not None:
        statement = statement.where(Todo.priority == priority)
        count_statement = count_statement.where(Todo.priority == priority)

    if completed is not None:
        statement = statement.where(Todo.completed == completed)
        count_statement = count_statement.where(Todo.completed == completed)

    if category_id is not None:
        statement = statement.where(Todo.category_id == category_id)
        count_statement = count_statement.where(Todo.category_id == category_id)

    # 검색 적용
    if q is not None:
        search_filter = Todo.title.contains(q) | Todo.description.contains(q)
        statement = statement.where(search_filter)
        count_statement = count_statement.where(search_filter)

    # 페이지네이션
    statement = statement.offset(offset).limit(size)

    todos = session.exec(statement).all()
    total = session.exec(count_statement).one()

    return TodoListResponse(
        items=[_todo_to_response(todo, session) for todo in todos],
        total=total,
        page=page,
        size=size,
    )


@app.get(
    "/api/v1/todos/{todo_id}",
    response_model=TodoResponse,
)
def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
):
    """TODO 항목을 조회합니다.

    Args:
        todo_id: TODO 항목 ID.
        session: 데이터베이스 세션.

    Returns:
        TodoResponse: TODO 항목 정보.

    Raises:
        HTTPException: TODO를 찾을 수 없는 경우 (404).
    """
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return _todo_to_response(todo, session)


@app.patch(
    "/api/v1/todos/{todo_id}",
    response_model=TodoResponse,
)
def update_todo(
    todo_id: int,
    data: TodoUpdate,
    session: Session = Depends(get_session),
):
    """TODO 항목을 수정합니다.

    전달된 필드만 업데이트합니다 (Partial Update).

    Args:
        todo_id: TODO 항목 ID.
        data: 수정할 데이터.
        session: 데이터베이스 세션.

    Returns:
        TodoResponse: 수정된 TODO 항목.

    Raises:
        HTTPException: TODO를 찾을 수 없는 경우 (404).
        HTTPException: 카테고리가 존재하지 않는 경우 (404).
    """
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = data.model_dump(exclude_unset=True)

    # 카테고리 존재 여부 확인
    if "category_id" in update_data and update_data["category_id"] is not None:
        category = session.get(Category, update_data["category_id"])
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    for key, value in update_data.items():
        setattr(todo, key, value)
    todo.updated_at = datetime.now()

    session.add(todo)
    session.commit()
    session.refresh(todo)
    logger.info(f"TODO 수정: {todo_id}")
    return _todo_to_response(todo, session)


@app.delete("/api/v1/todos/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
):
    """TODO 항목을 삭제합니다.

    Args:
        todo_id: TODO 항목 ID.
        session: 데이터베이스 세션.

    Raises:
        HTTPException: TODO를 찾을 수 없는 경우 (404).
    """
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    logger.info(f"TODO 삭제: {todo_id}")


# ─── Stats ──────────────────────────────────────────────


@app.get(
    "/api/v1/stats",
    response_model=StatsResponse,
)
def get_stats(
    session: Session = Depends(get_session),
):
    """통계 정보를 반환합니다.

    전체 TODO 수, 완료율, 우선순위 분포, 카테고리별 통계를 제공합니다.

    Args:
        session: 데이터베이스 세션.

    Returns:
        StatsResponse: 통계 정보.
    """
    # 전체 통계
    total_todos = session.exec(select(func.count(Todo.id))).one()
    completed_todos = session.exec(
        select(func.count(Todo.id)).where(Todo.completed == True)  # noqa: E712
    ).one()
    completion_rate = completed_todos / total_todos if total_todos > 0 else 0.0

    # 우선순위 분포
    priority_distribution = {}
    for priority in ["low", "medium", "high"]:
        count = session.exec(
            select(func.count(Todo.id)).where(Todo.priority == priority)
        ).one()
        priority_distribution[priority] = count

    # 카테고리별 통계
    category_stats = []
    categories = session.exec(select(Category)).all()
    for category in categories:
        cat_total = session.exec(
            select(func.count(Todo.id)).where(Todo.category_id == category.id)
        ).one()
        cat_completed = session.exec(
            select(func.count(Todo.id)).where(
                Todo.category_id == category.id,
                Todo.completed == True,  # noqa: E712
            )
        ).one()
        cat_rate = cat_completed / cat_total if cat_total > 0 else 0.0
        category_stats.append(
            CategoryStats(
                category_name=category.name,
                total=cat_total,
                completed=cat_completed,
                completion_rate=round(cat_rate, 2),
            )
        )

    # 카테고리 없는 TODO 통계
    uncategorized_total = session.exec(
        select(func.count(Todo.id)).where(Todo.category_id == None)  # noqa: E711
    ).one()
    if uncategorized_total > 0:
        uncategorized_completed = session.exec(
            select(func.count(Todo.id)).where(
                Todo.category_id == None,  # noqa: E711
                Todo.completed == True,  # noqa: E712
            )
        ).one()
        uncategorized_rate = (
            uncategorized_completed / uncategorized_total
            if uncategorized_total > 0
            else 0.0
        )
        category_stats.append(
            CategoryStats(
                category_name="미분류",
                total=uncategorized_total,
                completed=uncategorized_completed,
                completion_rate=round(uncategorized_rate, 2),
            )
        )

    return StatsResponse(
        total_todos=total_todos,
        completed_todos=completed_todos,
        completion_rate=round(completion_rate, 2),
        priority_distribution=priority_distribution,
        category_stats=category_stats,
    )
