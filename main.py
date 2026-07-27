from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
tasks = [ 
    { "id": 1, "title": "Learn FastAPI", "done": False }, 
    { "id": 2, "title": "Build CRUD API", "done": False }, 
    { "id": 3, "title": "Learn Swagger UI", "done": True } 
]


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
def get_tasks(): 
    return tasks

@app.get("/tasks")
def list_tasks() -> list[dict[str, int | str | bool]]:
    return tasks


@app.get("/tasks/{task_id}", response_model=None)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )