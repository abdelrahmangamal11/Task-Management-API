from pydantic import BaseModel, Field, validator, field_validator
from datetime import datetime, timezone
from models.enums.TaskPriority import TaskPriority
from models.enums.TaskStatus import TaskStatus
from typing import Generic, List, TypeVar ,Optional
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")
class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(default=None, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Title cannot be empty or whitespace only.")
        return trimmed

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v):
        if v:
            if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
                v = v.replace(tzinfo=timezone.utc)
            if v < datetime.now(timezone.utc):
                raise ValueError("Due date must be in the future.")
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(None, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is not None:
            trimmed = v.strip()
            if not trimmed:
                raise ValueError("Title cannot be empty or whitespace only.")
            return trimmed
        return v

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v):
        if v:
            if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
                v = v.replace(tzinfo=timezone.utc)
            if v < datetime.now(timezone.utc):
                raise ValueError("Due date must be in the future.")
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    limit: int
    offset: int
    pages: int

