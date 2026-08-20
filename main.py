from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from database import initialize_database,get_all_tasks,get_task_by_id,create_task,update_task,delete_task
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing Database...")
    initialize_database()
    print("Database Ready!")
    yield


app = FastAPI(lifespan=lifespan)
class TaskCreate(BaseModel):
    title: str  
class TaskUpdate(BaseModel):
    title: str
    done: bool




initial_tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Learn Swagger UI", "done": True}
]


tasks = [task.copy() for task in initial_tasks]

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks(done: bool | None = None, search: str | None = None):

    result = get_all_tasks()

    if done is not None:
        result = [
            task for task in result
            if task["done"] == done
        ]

    if search is not None:
        result = [
            task for task in result
            if search.lower() in task["title"].lower()
        ]

    return result


@app.get("/tasks/{task_id}", response_model=None)
def get_task(task_id: int):

    task = get_task_by_id(task_id)

    if task:
        return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )

@app.post("/tasks", status_code=201)
def create_new_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    return create_task(task.title)

@app.put("/tasks/{task_id}")
def update_existing_task(task_id: int, updated_task: TaskUpdate):

    if not updated_task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    task = update_task(
        task_id,
        updated_task.title,
        updated_task.done
    )

    if task:
        return task

    return JSONResponse(
        status_code=404,
        content={"error": "Task not found"},
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_existing_task(task_id: int):

    deleted = delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    return None


@app.post("/reset")
def reset_tasks():

    global tasks

    tasks = [task.copy() for task in initial_tasks]

    return {
        "message": "Tasks reset successfully",
        "tasks": tasks
    }


@app.get("/stats")
def get_stats():

    total = len(tasks)

    done = sum(
        1 for task in tasks
        if task["done"]
    )

    open_tasks = total - done

    return {
        "total": total,
        "done": done,
        "open": open_tasks
    }