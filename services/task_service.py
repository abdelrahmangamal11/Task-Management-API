from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import Session, select
from sqlalchemy import func

from models.Task import Task
from schemas.TaskSchema import TaskCreate, TaskUpdate, TaskResponse, PaginatedResponse
from models.enums.TaskStatus import TaskStatus
from models.enums.TaskPriority import TaskPriority
from utils.exceptions import validation_exception, not_found_exception


def create_new_task(task_in: TaskCreate, session: Session) -> Task:
    task_in.title = task_in.title.strip()
    if not task_in.title:
        raise validation_exception("Title cannot be empty or only whitespace.")
    if task_in.due_date and task_in.due_date <= datetime.now(timezone.utc):
        raise validation_exception("Due date must be in the future.")

    task = Task(**task_in.model_dump())
    task.created_at = datetime.now(timezone.utc)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_paginated_tasks(
    session: Session,
    status: Optional[TaskStatus],
    priority: Optional[TaskPriority],
    assigned_to: Optional[str],
    skip: int,
    limit: int,
    sort_by: Optional[str],
    sort_order: Optional[str],
) -> PaginatedResponse[TaskResponse]:
    base_query = select(Task)
    count_query = select(func.count(Task.id))

    if status:
        base_query = base_query.where(Task.status == status)
        count_query = count_query.where(Task.status == status)
    if priority:
        base_query = base_query.where(Task.priority == priority)
        count_query = count_query.where(Task.priority == priority)
    if assigned_to:
        base_query = base_query.where(Task.assigned_to == assigned_to)
        count_query = count_query.where(Task.assigned_to == assigned_to)

    if sort_by:
        sort_attr = getattr(Task, sort_by, None)
        if sort_attr is not None:
            if sort_order == "desc":
                base_query = base_query.order_by(sort_attr.desc())
            else:
                base_query = base_query.order_by(sort_attr.asc())

    total = session.exec(count_query).first() or 0
    tasks = session.exec(base_query.offset(skip).limit(limit)).all()

    return PaginatedResponse(
        data=[TaskResponse.model_validate(task) for task in tasks],
        total=total,
        limit=limit,
        offset=skip,
        pages=(total + limit - 1) // limit
    )


def get_task_by_id(task_id: int, session: Session) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise not_found_exception("Task not found")
    return task


def update_existing_task(task_id: int, task_in: TaskUpdate, session: Session) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise not_found_exception("Task not found")

    task_data = task_in.model_dump(exclude_unset=True)

    if "title" in task_data:
        task_data["title"] = task_data["title"].strip()
        if not task_data["title"]:
            raise validation_exception("Title cannot be empty or only whitespace.")
    if "due_date" in task_data and task_data["due_date"] is not None:
        if task_data["due_date"] <= datetime.now(timezone.utc):
            raise validation_exception("Due date must be in the future.")

    for key, value in task_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task_by_id(task_id: int, session: Session):
    task = session.get(Task, task_id)
    if not task:
        raise not_found_exception("Task not found")
    session.delete(task)
    session.commit()
