from config import database_settings, IS_DEBUG
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    url=database_settings.DATABASE_URL,
    echo=IS_DEBUG
)

session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with session_factory() as session:
        yield session
