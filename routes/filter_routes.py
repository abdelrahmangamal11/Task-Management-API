from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select

from models.Task import Task
from models.enums.TaskPriority import  TaskPriority
from models.enums.TaskStatus import TaskStatus

from db.session import get_session
from schemas.TaskSchema import TaskResponse
from utils.exceptions import validation_exception,not_found_exception,bad_request_exception


router = APIRouter(prefix="/tasks", tags=["Task Filters"])

@router.get("/status/{status}", response_model=List[TaskResponse])
def filter_by_status(status: TaskStatus, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.status == status)).all()
    if not tasks:
        raise not_found_exception("No tasks found with that status")
    return tasks


@router.get("/priority/{priority}", response_model=List[TaskResponse])
def filter_by_priority(priority: TaskPriority, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.priority == priority)).all()
    if not tasks:
        raise not_found_exception("No tasks found with that priority")
    return tasks
