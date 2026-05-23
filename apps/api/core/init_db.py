import asyncio
from .database import engine, Base
from ..models.core_models import User, Agent, TaskLog

async def init_models():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
        print("Database schemas initialized.")

if __name__ == "__main__":
    asyncio.run(init_models())
