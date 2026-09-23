from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./orchestrator.db"
engine = create_async_engine(DATABASE_URL, echo=True) #manages communication b/w db and application

#factory for database sessions
AsyncSessionLocal = async_sessionmaker( 
                        engine, 
                        expire_on_commit=False, 
                        class_=AsyncSession)

class Base(DeclarativeBase):
    pass

#opens a database session, do something(here yield), and handles its cleanup afterward.
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session