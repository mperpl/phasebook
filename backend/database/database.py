from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings
from database.models.base import Base


engine = create_async_engine(settings.DB_URL)
SessionLocal = async_sessionmaker(expire_on_commit=False, bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


# async def create_db_tables():
#     async with engine.begin() as con:
#         await con.run_sync(Base.metadata.create_all)


DB_SESSION = Annotated[AsyncSession, Depends(get_db)]