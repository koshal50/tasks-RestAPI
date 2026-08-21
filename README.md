# Task API

A **CRUD REST API built with Python, FastAPI, and PostgreSQL**.

This project is part of the Backend Track assignment and demonstrates how to build a RESTful API using FastAPI with persistent data storage in PostgreSQL. The API supports creating, reading, updating, and deleting tasks, along with filtering and searching.

The complete application stack is containerized using **Docker and Docker Compose**, allowing the API and PostgreSQL database to be started together with a single command.

---

# Features

* Create tasks
* Read all tasks
* Read a single task
* Update tasks
* Delete tasks
* Input validation
* Filter tasks by completion status
* Search tasks by title
* Interactive Swagger UI documentation
* Persistent storage using PostgreSQL
* Automatic database initialization
* Sample task seeding
* Dockerized FastAPI application
* Dockerized PostgreSQL database
* One-command application startup

---

# Tech Stack

* Python
* FastAPI
* PostgreSQL
* Pydantic
* Uvicorn
* psycopg
* Docker
* Docker Compose
* Swagger UI / OpenAPI

---

# Database

The application uses **PostgreSQL** as its persistent database.

Unlike the previous SQLite implementation, PostgreSQL runs as a separate Docker container managed by Docker Compose.

The database configuration is provided through the `DATABASE_URL` environment variable.

Example:

```env
DATABASE_URL=postgres://postgres:dev@db:5432/tasks
```

The important parts are:

```text
Database: tasks
User:     postgres
Host:     db
Port:     5432
```

The hostname `db` refers to the PostgreSQL service defined in `compose.yaml`.

No manual PostgreSQL installation or database creation is required.

---

# Environment Variables

The repository contains a `.env.example` file showing the variables required to run the application.

Create your local `.env` file from the example.

### Linux / macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Required Variables

| Variable       | Description                        | Example                                 |
| -------------- | ---------------------------------- | --------------------------------------- |
| `DATABASE_URL` | PostgreSQL database connection URL | `postgres://postgres:dev@db:5432/tasks` |

> The real `.env` file must not be committed to GitHub. It contains environment-specific configuration and potentially sensitive credentials.

---

# Installation and Running

You do **not** need to install PostgreSQL locally.

You also do not need to manually start Uvicorn or configure the database.

The only requirement is **Docker Desktop**.

## Start the Complete Application

From the project directory, run:

```bash
docker compose up
```

Docker Compose starts both:

```text
FastAPI API
     │
     │
     ▼
PostgreSQL
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## Run in the Background

To run the stack in detached mode:

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

Stop the application:

```bash
docker compose down
```

---

# Docker Architecture

The application consists of two Docker services:

```text
                    Docker Compose
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
      FastAPI Container       PostgreSQL Container
          API :8000                 DB :5432
             │                       │
             └──────────┬────────────┘
                        │
                  DATABASE_URL
                        │
                        ▼
                  tasks database
```

The FastAPI container communicates with PostgreSQL through the Docker Compose service name:

```text
db
```

Therefore, the database connection uses:

```text
postgres://postgres:dev@db:5432/tasks
```

rather than:

```text
localhost
```

because `localhost` inside the API container refers to the API container itself.

---

# Project Structure

```text
task-api/
│
├── main.py
├── database.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> Update this structure if your repository contains additional files or directories.

---

# API Endpoints

| Method | Endpoint             | Description            |
| ------ | -------------------- | ---------------------- |
| GET    | `/`                  | API Information        |
| GET    | `/health`            | Health Check           |
| GET    | `/tasks`             | Get all tasks          |
| GET    | `/tasks/{task_id}`   | Get task by ID         |
| POST   | `/tasks`             | Create a task          |
| PUT    | `/tasks/{task_id}`   | Update a task          |
| DELETE | `/tasks/{task_id}`   | Delete a task          |
| GET    | `/tasks?done=true`   | Filter completed tasks |
| GET    | `/tasks?search=text` | Search tasks           |

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

## Get All Tasks

```bash
curl -i http://localhost:8000/tasks
```

Example response:

```text
HTTP/1.1 200 OK
content-type: application/json

[
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": false
    }
]
```

> Replace the example response with the actual response returned by your current API if the structure differs.

---

## Get Task by ID

```bash
curl -i http://localhost:8000/tasks/1
```

---

## Create Task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Learn PostgreSQL\"}"
```

---

## Update Task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
-H "Content-Type: application/json" \
-d "{\"title\":\"Master FastAPI\"}"
```

---

## Delete Task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

---

## Filter Completed Tasks

```bash
curl -i "http://localhost:8000/tasks?done=true"
```

---

## Search Tasks

```bash
curl -i "http://localhost:8000/tasks?search=FastAPI"
```

---

# HTTP Status Codes

| Status | Meaning                   |
| ------ | ------------------------- |
| 200    | Request Successful        |
| 201    | Task Created Successfully |
| 204    | Task Deleted Successfully |
| 400    | Invalid Request           |
| 404    | Task Not Found            |

---

# Database Verification

PostgreSQL can be accessed directly through the running Docker container.

First start the application:

```bash
docker compose up
```

Then, in another terminal:

```bash
docker compose exec db psql -U postgres -d tasks
```

Once inside PostgreSQL, list the tables:

```sql
\dt
```

Then query the task data:

```sql
SELECT * FROM tasks;
```

The seeded tasks should be visible in the result.

Exit PostgreSQL with:

```sql
\q
```

---

# Database Screenshot

The database was verified directly using PostgreSQL.

The screenshot below should show:

1. The `\dt` command displaying the database tables.
2. The `SELECT * FROM tasks;` query.
3. The seeded task records.

### Screenshot

**Add your database screenshot here:**

```text
[ INSERT DATABASE SCREENSHOT HERE ]
```

For example, save the screenshot in a `screenshots/` directory and reference it here:

```markdown
![PostgreSQL Database](screenshots/postgresql_database.png)
```

---

# Environment & Security

The repository contains:

```text
.env.example
```

which documents the required environment variables.

The real:

```text
.env
```

file is ignored by Git.

The `.gitignore` should contain:

```gitignore
.env
```

This prevents database credentials and other environment-specific secrets from being committed to the public GitHub repository.

**Never commit real passwords or secrets to GitHub.**

---

# Clean Clone Verification

The project is designed so that a stranger can clone the repository and run the complete stack without manually installing PostgreSQL or creating the database.

## 1. Clone the Repository

```bash
git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

## 2. Create `.env`

### Linux / macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

## 3. Start the Complete Stack

```bash
docker compose up
```

Docker Compose starts both the FastAPI API and PostgreSQL database.

## 4. Test the API

Open:

```text
http://localhost:8000/docs
```

Or run:

```bash
curl -i http://localhost:8000/tasks
```

The endpoint should return the seeded tasks.

No manual PostgreSQL installation, database creation, or database configuration is required.

---

# Conclusion

This project demonstrates the implementation of a RESTful CRUD API using **FastAPI and PostgreSQL**.

The application provides persistent task storage, input validation, filtering, searching, and interactive Swagger documentation.

The complete application is containerized using **Docker and Docker Compose**, allowing the API and PostgreSQL database to run together without manual database setup.

The project can be reproduced from a clean clone using:

```bash
cp .env.example .env
docker compose up
```

and verified using:

```bash
curl -i http://localhost:8000/tasks
```

This provides a reproducible, one-command development environment suitable for running the API from a fresh clone.
