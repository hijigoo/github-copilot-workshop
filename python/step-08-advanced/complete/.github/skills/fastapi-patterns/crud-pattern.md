# FastAPI CRUD Pattern Skill

This skill teaches the standard CRUD pattern used in our FastAPI + SQLModel project.

## Standard Endpoint Pattern

### Create (POST)
```python
@app.post("/api/v1/{resource}", response_model=ResourceResponse, status_code=201)
def create_resource(data: ResourceCreate, session: Session = Depends(get_session)):
    """리소스를 생성합니다."""
    db_resource = ResourceModel(**data.model_dump())
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return _resource_to_response(db_resource)
```

### Read Single (GET)
```python
@app.get("/api/v1/{resource}/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, session: Session = Depends(get_session)):
    """리소스를 조회합니다."""
    resource = session.get(ResourceModel, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return _resource_to_response(resource)
```

### Read List with Pagination (GET)
```python
@app.get("/api/v1/{resource}", response_model=ResourceListResponse)
def list_resources(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """리소스 목록을 조회합니다."""
    offset = (page - 1) * size
    statement = select(ResourceModel).offset(offset).limit(size)
    resources = session.exec(statement).all()
    total = session.exec(select(func.count(ResourceModel.id))).one()
    return ResourceListResponse(
        items=[_resource_to_response(r) for r in resources],
        total=total,
        page=page,
        size=size,
    )
```

### Update (PATCH)
```python
@app.patch("/api/v1/{resource}/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int, data: ResourceUpdate, session: Session = Depends(get_session)
):
    """리소스를 수정합니다."""
    resource = session.get(ResourceModel, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resource, key, value)
    resource.updated_at = datetime.now()
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return _resource_to_response(resource)
```

### Delete (DELETE)
```python
@app.delete("/api/v1/{resource}/{resource_id}", status_code=204)
def delete_resource(resource_id: int, session: Session = Depends(get_session)):
    """리소스를 삭제합니다."""
    resource = session.get(ResourceModel, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    session.delete(resource)
    session.commit()
```

## Key Principles

1. **Dependency Injection**: Always use `Session = Depends(get_session)`
2. **Response Conversion**: Never return raw DB models; use `_resource_to_response()`
3. **Error Handling**: Use `HTTPException` with appropriate status codes
4. **Validation**: Use Pydantic `Field()` with constraints in schemas
5. **Pagination**: Always support `page` and `size` for list endpoints
