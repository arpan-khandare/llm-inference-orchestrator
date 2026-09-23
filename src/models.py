# SQLAlchemy ORM tables

from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Text, DateTime

from src.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# inference task = A record representing one LLM request.
# ┌──────────────────────────────────────┐
# │ InferenceTask                        │
# ├──────────────────────────────────────┤
# │ id:              8a72f1c9-...        │
# │ prompt:          "Explain quantum..."│
# │ status:          PENDING             │
# │ created_at:      10:30:00            │
# │ completed_at:    NULL                │
# │ duration_second: NULL                │
# └──────────────────────────────────────┘
class InferenceTask(Base):
   __tablename__ = "inference_tasks"

   id: Mapped[str] = mapped_column(
      String, primary_key=True, index=True, default = lambda: str(uuid.uuid4())
   )
   prompt: Mapped[str]= mapped_column(Text, nullable=False)
   status : Mapped[str]= mapped_column(String, default="PENDING")
   created_at: Mapped[datetime]= mapped_column(
      DateTime(timezone=True), default=utc_now
   )
   completed_at: Mapped[Optional[datetime]]= mapped_column(
      DateTime(timezone=True), nullable=True
   )
   duration_second: Mapped[Optional[float]]= mapped_column(Float, nullable=True)