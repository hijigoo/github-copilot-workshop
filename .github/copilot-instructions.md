# Copilot Instructions — GitHub Copilot Workshop

## Project Overview

This is a **progressive tutorial workshop** that teaches GitHub Copilot features by building a TODO API. The workshop is available in two language tracks:

- **`python/`** — Python + FastAPI + VS Code
- **`java/`** — Java + Spring Boot + IntelliJ IDEA

Each `step-XX-*` folder is a self-contained lesson with `starter/` (starting code) and `complete/` (reference answer). Steps 00–10 are the main track; 11–12 are bonus tracks (README-only self-paced guides).

**This is educational content, not a production application.** When modifying code, preserve the progressive learning design — each step must only use Copilot features introduced up to that point.

## Language & Locale

- All comments, docstrings/Javadoc, commit messages, error messages must be in **Korean**.
- Python docstrings follow **Google style** in Korean.
- Java Javadoc follows standard Javadoc style in Korean.

## Tech Stack

### Python Track
- Python 3.11+, FastAPI, Pydantic v2 (`BaseModel`), SQLModel (ORM), SQLite (local file DB)
- Testing: pytest + `FastAPI.testclient.TestClient` + httpx

### Java Track
- Java 17+, Spring Boot 3.x, Spring Data JPA, H2 Database
- Build: Gradle (Kotlin DSL)
- Testing: JUnit 5 + MockMvc + @SpringBootTest

## Architecture Patterns

### File Organization (steps 07–10)

```
app/database.py   — Engine, create_db_and_tables(), get_session() generator
app/models.py     — SQLModel table classes (DB schema)
app/schemas.py    — Pydantic BaseModel classes (API request/response)
app/main.py       — FastAPI app, lifespan, all route handlers
tests/conftest.py — In-memory SQLite session fixture + TestClient fixture
tests/test_*.py   — Class-based test organization by endpoint
```

**Key separation**: ORM models (`SQLModel, table=True`) live in `models.py`; API schemas (`BaseModel`) live in `schemas.py`. Never mix them.

### CRUD Endpoint Pattern

```python
@app.post("/api/v1/{resource}", response_model=ResourceResponse, status_code=201)
def create_resource(data: ResourceCreate, session: Session = Depends(get_session)):
    db_item = ResourceModel(**data.model_dump())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return _to_response(db_item)
```

- Always use `Depends(get_session)` for DB access
- `response_model` required on every endpoint
- Status codes: 201 create, 204 delete, 404 not found
- Partial updates via `PATCH` with `model_dump(exclude_unset=True)`
- Pagination: `page`/`size` query params with `Query(ge=1)` validation

### Testing Pattern

- Tests use **in-memory SQLite** via `conftest.py` dependency override (see `step-06-agent/complete/tests/conftest.py`)
- Group tests by endpoint in classes: `TestCreateTodo`, `TestListTodos`, etc.
- Use helper functions (`create_test_todo()`, `create_test_category()`) for test data setup
- Cover: happy path, validation errors, edge cases, 404 scenarios

## Step Progression & Constraints

| Steps | Code style | DB | Key constraint |
|-------|-----------|-----|----------------|
| 01–05 | In-memory `list[dict]` + `schemas.py` | None | No database, no SQLModel (`schemas.py` introduced at step-04) |
| 06–10 | SQLModel + Session | SQLite | Full ORM with `Depends(get_session)` |

When editing a specific step's code, use only patterns available at that step level. For example, step-03 code should not use `schemas.py` (introduced in step-04 prompt-files). Steps 08–10 start from a blank/minimal starter and build from scratch using Agent/Sub-Agent.

## Developer Commands

```bash
# Run the API server (from any step's starter/ or complete/ directory)
pip install -r requirements.txt
uvicorn app.main:app --reload

# Run tests
pytest -v

# Run tests from workspace root for a specific step
cd python/step-06-agent/complete && pytest -v
```

## Copilot Config Files Inside Steps

Steps contain `.github/` directories as **tutorial artifacts** (copilot-instructions.md, instructions/, prompts/, agents/, skills/). These demonstrate Copilot configuration to workshop participants — treat them as lesson content, not as active project config.
