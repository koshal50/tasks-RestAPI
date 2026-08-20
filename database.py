import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def initialize_database():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL
            )
        """)

    connection.commit()
    connection.close()

    seed_database()


def seed_database():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]

        if count == 0:
            sample_tasks = [
                ("Learn FastAPI", False),
                ("Study PostgreSQL", False),
                ("Complete Assignment", False)
            ]

            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                sample_tasks
            )

    connection.commit()
    connection.close()


def get_all_tasks():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, title, done
            FROM tasks
        """)

        rows = cursor.fetchall()

    connection.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "done": row[2]
        })

    return tasks


def get_task_by_id(task_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, title, done
            FROM tasks
            WHERE id = %s
        """, (task_id,))

        row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


def create_task(title):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING id
            """,
            (title, False)
        )

        task_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }
def update_task(task_id, title, done):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, done = %s
            WHERE id = %s
            RETURNING id, title, done
            """,
            (title, done, task_id)
        )

        row = cursor.fetchone()

    if row is None:
        connection.close()
        return None

    connection.commit()
    connection.close()

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }

def delete_task(task_id):
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            """,
            (task_id,)
        )

        deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted