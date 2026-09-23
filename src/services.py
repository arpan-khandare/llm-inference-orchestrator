from datetime import datetime, timezone
from typing import AsyncGenerator
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import InferenceTask


async def mock_llm_streamer_with_logging(
    task_id: str, prompt: str, db: AsyncSession
    ) -> AsyncGenerator[str, None]:
   start_time = datetime.now(timezone.utc)

   task = await db.get(InferenceTask, task_id) #task_id = primary key
   if task:
      task.status = "PROCESSING"
      await db.commit()

   dummy_response = f"Processing task [{task_id[:8]}] for prompt: '{prompt}'... "
   words = dummy_response.split() + [
        "Streaming", 
        "tokens", 
        "persistently", 
        "from", 
        "FastAPI", 
        "with", 
        "Async", 
        "SQLAlchemy", 
        "tracking!"
   ]

   # creating the "LLM typing" effect.
   for word in words:
      yield f"data: {word}\n\n"
      await asyncio.sleep(0.15)

   end_time = datetime.now(timezone.utc)
   duration = (end_time-start_time).total_seconds()

   if task:
      task.status = "COMPLETED"
      task.completed_at = end_time
      task.duration_second = duration
      await db.commit()