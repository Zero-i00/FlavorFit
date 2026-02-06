from fastapi import (
    status,
    FastAPI
)

from config.settings import settings

from database.orm import Base
from database.session import engine

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
)

@app.get('/')
async def health_check():
    return {
        "status": status.HTTP_200_OK,
        "message": f"Hello from {settings.app_name}",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        reload=True,
        host=settings.app_host,
        port=settings.app_port,
    )
