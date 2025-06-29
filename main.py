from fastapi import FastAPI
from db.session import create_db_and_tables
from routes import task_routes,filter_routes,general

app= FastAPI();

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(general.router)
app.include_router(task_routes.router)
app.include_router(filter_routes.router)