"""TODO API 애플리케이션."""
from fastapi import FastAPI

app = FastAPI(title="TODO API")


@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트."""
    return {"status": "ok"}
