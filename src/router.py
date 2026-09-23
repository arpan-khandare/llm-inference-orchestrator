
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import mock_llm_streamer_with_logging
from src.schemas import TaskResponse, PromptRequest
from src.models import InferenceTask
from src.database import get_db


router = APIRouter(prefix="/api/v1", tags=["Inference Orchestrator"])

# Creates a persistent task record in DB and streams LLM output.
@router.post("/chat/stream")
async def stream_llm_response(payload: PromptRequest, db: AsyncSession = Depends(get_db)):
   new_task = InferenceTask(prompt= payload.prompt, status= "PENDING")
   db.add(new_task)
   await db.commit()
   await db.refresh(new_task)
   
   return StreamingResponse(
       mock_llm_streamer_with_logging(new_task.id, payload.prompt, db),
       media_type="text/event-stream",
   )

# Check the execution status and duration of an inference task.
@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str, db: AsyncSession = Depends(get_db)):
   task = await db.get(InferenceTask, task_id) #look up InferenceTask object by primary key
   if not task:
      raise HTTPException(status_code=404, detail="Task not found")
   return{
      "task_id": task.id,
      "prompt": task.prompt,
      "status": task.status,
      "created_at": task.created_at,
      "completed_at": task.completed_at,
      "duration_seconds": task.duration_second
   }
   