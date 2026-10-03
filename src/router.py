
import os

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import stream_llm_from_ollama
from src.schemas import TaskResponse, PromptRequest
from src.models import InferenceTask
from src.database import get_db

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Set expected key
EXPECTED_API_KEY= os.getenv("ORCHESTRATOR_API_KEY")

async def verify_api_key(api_key: str = Security(api_key_header)):
   if api_key != EXPECTED_API_KEY:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Invalid/missing api key"
      )

router = APIRouter(
      prefix="/api/v1", 
      tags=["Inference Orchestrator"],
      dependencies=[Depends(verify_api_key)]
      )

# Creates a persistent task record in DB and streams LLM output from Ollama via SSE
@router.post("/chat/stream")
async def stream_llm_response(payload: PromptRequest, db: AsyncSession = Depends(get_db)):
   new_task = InferenceTask(prompt= payload.prompt, status= "PENDING")
   db.add(new_task)
   await db.commit()
   await db.refresh(new_task)
   
   return StreamingResponse(
         stream_llm_from_ollama(new_task.id, payload.prompt, db, "llama3"),
         media_type="text/event-stream",
         headers={"X-Task-ID": new_task.id}
   )

# Check the execution status and duration of an inference task.
@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str, db: AsyncSession = Depends(get_db)):
   task = await db.get(InferenceTask, task_id) #look up InferenceTask object by primary key
   if not task:
      raise HTTPException(status_code=404, detail="Task not found")
   return TaskResponse(
         task_id=task.id,
         prompt=task.prompt,
         status=task.status,
         created_at=task.created_at,
         completed_at=task.completed_at,
         duration_seconds=float(task.duration_second) if task.duration_second is not None else None,
   )
   