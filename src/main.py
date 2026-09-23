from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import engine, Base
from src.router import router


@asynccontextmanager
async def lifespan(ap: FastAPI):
   async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)
   yield
   await engine.dispose()
   
app = FastAPI(title="LLM Inference Orchestrator", lifespan=lifespan)
app.include_router(router)