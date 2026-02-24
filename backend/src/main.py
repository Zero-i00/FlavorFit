from fastapi import (
    status,
    FastAPI
)

from config.settings import settings

from database.orm import Base
from database.session import engine

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from modules.schema import graphql_schema
from strawberry.fastapi import GraphQLRouter
from config.graphql import get_graphql_context


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
)

graphql_router = GraphQLRouter(graphql_schema, context_getter=get_graphql_context)
app.include_router(graphql_router, prefix='/graphql')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],  # Список разрешенных источников
    allow_credentials=True,  # Разрешить отправку куки и авторизационных заголовков
    allow_methods=["*"],  # Разрешить все HTTP методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
    expose_headers=["*"],  # Заголовки, которые будут доступны клиенту
    max_age=600,  # Время кэширования preflight запросов в секундах (10 минут)
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
