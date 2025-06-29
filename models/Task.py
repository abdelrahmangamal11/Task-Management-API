from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from models.enums.TaskStatus import TaskStatus
from models.enums.TaskPriority import TaskPriority


# Task Model
class Task(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    title: str = Field(max_length=200)

    description: Optional[str] = Field(default=None, max_length=1000)

    status: TaskStatus = Field(default=TaskStatus.pending)

    priority: TaskPriority = Field(default=TaskPriority.medium)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: Optional[datetime] = None

    due_date: Optional[datetime] = None

    assigned_to: Optional[str] = Field(default=None, max_length=100)