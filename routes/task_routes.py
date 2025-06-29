from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from typing import List, Optional

from schemas.TaskSchema import TaskCreate, TaskResponse, TaskUpdate, PaginatedResponse
from db.session import get_session
from services.task_service import (
    create_new_task,
    get_paginated_tasks,
    get_task_by_id,
    update_existing_task,
    delete_task_by_id
)
from models.enums.TaskStatus import TaskStatus
from models.enums.TaskPriority import TaskPriority

router = APIRouter(prefix="/tasks", tags=["Task Management"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    return create_new_task(task_in, session)


@router.get("/", response_model=PaginatedResponse[TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks(
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    assigned_to: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    session: Session = Depends(get_session)
):
    return get_paginated_tasks(session, status, priority, assigned_to, skip, limit, sort_by, sort_order)



@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, session: Session = Depends(get_session)):
    return get_task_by_id(task_id, session)


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_in: TaskUpdate, session: Session = Depends(get_session)):
    return update_existing_task(task_id, task_in, session)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    delete_task_by_id(task_id, session)
    return None
