# Pydantic Data Models

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PromptRequest(BaseModel):
   prompt: str

class TaskResponse(BaseModel):
   task_id: str
   status: str
   created_at: datetime
   completed_at: Optional[datetime] = None
   duration_seconds: Optional[datetime]= None
   
   model_config = ConfigDict(from_attributes=True)
   