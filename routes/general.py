from fastapi import APIRouter,Depends
from db.session import get_session
from sqlmodel import Session

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to the Task Management API 👋",
        "endpoints": {
            "health": "/health",
            "tasks CRUD endpoints ": {
                "create": "POST /tasks",
                "list": "GET /tasks",
                "get_by_id": "GET /tasks/{task_id}",
                "update": "PUT /tasks/{task_id}",
                "delete": "DELETE /tasks/{task_id}",
                "filter_by_status": "GET /tasks/status/{status}",
                "filter_by_priority": "GET /tasks/priority/{priority}"
            }
        }
    }


@router.get("/health")
def health_check(session: Session = Depends(get_session)):
    try:
        session.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}
