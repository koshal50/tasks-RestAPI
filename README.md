# Task API

A simple **CRUD REST API built with Python, FastAPI, and SQLite**.

This project is part of the Backend Track assignment and demonstrates how to build a RESTful API using FastAPI with persistent data storage in SQLite. The API supports creating, reading, updating, and deleting tasks while automatically storing data in a SQLite database.

Unlike the previous in-memory implementation, all task data persists even after the server is restarted.

---

# Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Input validation
- Filter tasks by completion status
- Search tasks by title
- Interactive Swagger UI documentation
- Persistent storage using SQLite
- Automatic database initialization and sample data seeding

---

# Tech Stack

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- Swagger UI / OpenAPI

---

# Why SQLite?

SQLite was chosen for this project because:

- It is a **single-file database**, making it lightweight and easy to manage.
- It requires **zero installation or server setup**.
- Python provides built-in support through the `sqlite3` module.
- Data survives application restarts because it is stored on disk.
- It is ideal for learning backend development and small applications.

---

# Database

The application stores all data in:

```text
tasks.db
```

The database file:

- Is created automatically when the FastAPI application starts.
- Automatically creates the required `tasks` table if it does not already exist.
- Seeds the database with three sample tasks only when the table is empty.
- Is usually added to `.gitignore` so every cloned repository creates its own fresh database automatically.

---

# Installation

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment (Windows)

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

Start the API using:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

# Project Structure

```text
task-api/
│
├── main.py
├── database.py
├── tasks.db              # Automatically generated
├── requirements.txt
├── README.md
├── screenshots/
│   ├── swagger_ui.png
│   └── sqlite_database.png
└── .gitignore
```

---

# API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API Information |
| GET | `/health` | Health Check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get task by ID |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/tasks?done=true` | Filter completed tasks |
| GET | `/tasks?search=text` | Search tasks |

---

# Task Structure

```json
{
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
}
```

---

# Example Requests

### Get All Tasks

```bash
curl http://localhost:8000/tasks
```

### Get Task by ID

```bash
curl http://localhost:8000/tasks/1
```

### Create Task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Learn SQLite\"}"
```

### Update Task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
-H "Content-Type: application/json" \
-d "{\"title\":\"Master FastAPI\"}"
```

### Delete Task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

---

# HTTP Status Codes

| Status | Meaning |
|---------|---------|
| 200 | Request Successful |
| 201 | Task Created Successfully |
| 204 | Task Deleted Successfully |
| 400 | Invalid Request |
| 404 | Task Not Found |

---

# SQLite Exploration (Stage 4)

The database was explored using **DB Browser for SQLite** to understand how SQL queries interact directly with the application's database.

### Example SQL Query

```sql
SELECT COUNT(*) FROM tasks;
```

### Observation

This query returned the total number of rows currently stored in the `tasks` table, allowing verification of how many tasks were present in the SQLite database.

### Other Queries Executed

```sql
SELECT * FROM tasks;
```

```sql
SELECT * FROM tasks WHERE done = 1;
```

```sql
UPDATE tasks SET done = 1;
```

```sql
DELETE FROM tasks WHERE done = 1;
```

After executing each query and clicking **Write Changes** in DB Browser, the FastAPI application immediately reflected those changes without restarting the server because both DB Browser and the API accessed the same `tasks.db` file.


# Conclusion

This project demonstrates the implementation of a RESTful CRUD API using **FastAPI** and **SQLite**. The application automatically creates and initializes the SQLite database, supports persistent storage across server restarts, and provides interactive API documentation through Swagger UI. Manual exploration using DB Browser for SQLite helped verify that the API and the database operate on the same data source, reinforcing the concepts of persistent storage and SQL-based data management.