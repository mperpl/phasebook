from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.models.base import Base

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:ZAQ!2wsx@localhost:5432/blog_app'
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(
    expire_on_commit=False, bind=engine, class_=AsyncSession
)



async def get_db():
    async with SessionLocal() as session:
        yield session

async def create_db_tables():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

DB_SESSION = Annotated[AsyncSession, Depends(get_db)]