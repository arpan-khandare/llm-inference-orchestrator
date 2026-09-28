from datetime import datetime, timezone
import json
from typing import AsyncGenerator
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import InferenceTask

OLLMA_URL = "http://localhost:11434/api/generate"
      
async def stream_llm_from_ollama(
    task_id: str, prompt: str, db: AsyncSession, model_name: str = "llama3"
    ) -> AsyncGenerator[str, None]:
   start_time = datetime.now(timezone.utc)

   # 1. Update task status to PROCESSING in DB
   task = await db.get(InferenceTask, task_id) #task_id = primary key
   if task:
      task.status = "PROCESSING"
      await db.commit()

   # 2. Open an Async HTTP Stream to local Ollama server
   async with httpx.AsyncClient(timeout=60.0) as client:
      try:
         async with client.stream(
            "POST",
            OLLMA_URL,
            json={
               "model": model_name,
               "prompt": prompt,
               "stream": True
            },
         ) as response:
            print("This is the log I'm trying to print", response)
            if response.status_code!=200:
               yield f"data: [Error: Ollama returned status {response.status_code}\n\n]"
               return
         
            async for line in response.aiter_lines():
               if line:
                  data = json.loads(line)
                  token = data.get("response", "")
                  
                  #yield token formatted as SSE
                  yield f"data: {token}\n\n"
                  
                  #check if model reached end-of-generation
                  if data.get("done", False):
                     break
      
      except Exception as e:
         yield f"data: [Error communicating with LLM Engine: {str(e)}\n\n]"
         if task:
            task.status="FAILED"
            await db.commit()
         return     
            
   # 3. Update task status to COMPLETED
   end_time = datetime.now(timezone.utc)
   duration = (end_time-start_time).total_seconds()

   if task:
      task.status = "COMPLETED"
      task.completed_at = end_time
      task.duration_second = duration
      await db.commit()