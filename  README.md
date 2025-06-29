# FastAPI Task Management API

A comprehensive task management API built with FastAPI, SQLModel, and Pydantic.

## Features

- Full CRUD operations for tasks
- Data validation with Pydantic
- SQLite database with SQLModel ORM
- Pagination support
- Filtering by status, priority, and assignee
- Proper error handling
- Automatic API documentation (OpenAPI/Swagger)
- Health check endpoint

## Installation

1. Create virtual environment:
   ```bash
   python -m venv env
   ```

2. Activate virtual environment:
   ```bash
   # Windows
   env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

Access the API:
- API Base URL: `http://localhost:8000`
- Interactive Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

## API Endpoints

### Root and Health
- `GET /` - API information and available endpoints
- `GET /health` - Health check with database status

### Task Management
- `POST /tasks` - Create a new task
- `GET /tasks` - List all tasks with pagination and filtering
- `GET /tasks/{task_id}` - Get a specific task by ID
- `PUT /tasks/{task_id}` - Update an existing task
- `DELETE /tasks/{task_id}` - Delete a task

### Filtering
- `GET /tasks/status/{status}` - Get tasks by status
- `GET /tasks/priority/{priority}` - Get tasks by priority

## Data Models

### Task Status
- `pending` - Task is waiting to be started
- `in_progress` - Task is currently being worked on
- `completed` - Task has been finished
- `cancelled` - Task has been cancelled

### Task Priority
- `low` - Low priority task
- `medium` - Medium priority task (default)
- `high` - High priority task
- `urgent` - Urgent task requiring immediate attention

## Example API Calls

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Complete API Documentation",
       "description": "Write comprehensive API documentation",
       "priority": "high",
       "assigned_to": "John Doe"
     }'
```

### Get All Tasks
```bash
curl "http://localhost:8000/tasks"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "in_progress",
       "priority": "urgent"
     }'
```

## Validation Rules

1. **Title Validation:**
   - Cannot be empty or whitespace only
   - Maximum 200 characters

2. **Description Validation:**
   - Optional field
   - Maximum 1000 characters

3. **Due Date Validation:**
   - Must be in the future (if provided)

4. **Assignee Validation:**
   - Optional field
   - Maximum 100 characters

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Successful retrieval/update
- `201` - Successful creation
- `204` - Successful deletion
- `400` - Bad request
- `404` - Resource not found
- `422` - Validation error

## Project Structure

task-management/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── database.db             # SQLite database file
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose setup
├── .dockerignore           # Files to exclude from Docker context
├── db/
│   └── session.py          # Database session management
├── models/
│   ├── Task.py             # Task database model
│   └── enums/
│       ├── TaskStatus.py   # Task status enumeration
│       └── TaskPriority.py # Task priority enumeration
├── schemas/
│   └── TaskSchema.py       # Pydantic models for validation
├── routes/
│   ├── general.py          # Root and health endpoints
│   ├── task_routes.py      # Task CRUD operations
│   └── filter_routes.py    # Task filtering endpoints
├── services/
│   └── task_service.py     # Business logic and DB interaction
└── utils/
    └── exceptions.py       # Custom exception handlers


## Testing

1. Start the server as described above
2. Open the Swagger UI at `http://localhost:8000/docs`
3. Test endpoints using the interactive interface

## Docker Support

### Prerequisites

- Make sure you have Docker and Docker Compose installed.

### Build and Run the Application

```bash
docker-compose up --build
