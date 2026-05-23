from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Base class for models
Base = declarative_base()

# Connection String (Ideally from env vars)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/neuralops")

engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory
async_session = async_sessionmaker(
    engine, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session