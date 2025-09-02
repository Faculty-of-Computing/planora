import os
from typing import List, Optional, TypedDict
from psycopg import connect, Connection
from psycopg.rows import dict_row
from psycopg.errors import UniqueViolation, Error
from werkzeug.datastructures import FileStorage


class EventImage(TypedDict):
    image: bytes
    image_mime: str


class User(TypedDict):
    id: int
    username: str
    email: str
    password_hash: str


class Event(TypedDict):
    id: int
    title: str
    description: str
    date: str
    location: str
    price: float
    tickets_available: int
    creator_id: int


class Registration(TypedDict):
    registration_id: int
    user_id: int
    name: str
    email: str


env = {
    "name": os.getenv("POSTGRES_DATABASE"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
}


def get_db_connection() -> Connection:
    if not all(env.values()):
        raise EnvironmentError("Missing PostgreSQL environment variables")
    return connect(
        f"dbname={env['name']} user={env['user']} password={env['password']} host={env['host']}",
        row_factory=dict_row,  # type: ignore
    )


def create_tables() -> None:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        );
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            creator_id INTEGER NOT NULL REFERENCES users(id),
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date DATE NOT NULL,
            location TEXT,
            price DOUBLE PRECISION,
            tickets_available INTEGER NOT NULL DEFAULT 0,
            image BYTEA,
            image_mime TEXT
        );
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            event_id INTEGER NOT NULL REFERENCES events(id),
            UNIQUE(user_id, event_id)
        );
    """
    )
    conn.commit()
    conn.close()


def insert_user(email: str, username: str, password: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (email, username, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id
        """,
            (email, username, password),
        )
        user_id = cursor.fetchone()["id"]  # type: ignore
        conn.commit()
        return user_id  # type: ignore
    except UniqueViolation:
        raise ValueError("Email or username already exists")
    finally:
        conn.close()


def get_user_by_email(email: str) -> Optional[User]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, email FROM users WHERE email = %s",
        (email,),
    )
    user = cursor.fetchone()
    conn.close()
    return user  # type: ignore


def get_user_by_id(user_id: int) -> Optional[User]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, email FROM users WHERE id = %s", (user_id,)
    )
    user = cursor.fetchone()
    conn.close()
    return user  # type: ignore


def get_user_by_username(username: str) -> Optional[User]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, email FROM users WHERE username = %s",
        (username,),
    )
    user = cursor.fetchone()
    conn.close()
    return user  # type: ignore


def insert_event(
    creator_id: int,
    title: str,
    description: str,
    date: str,
    location: str,
    price: float,
    tickets_available: int,
    image_file: FileStorage,
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    image_bytes = image_file.read()
    image_mime = image_file.mimetype
    cursor.execute(
        """
        INSERT INTO events (creator_id, title, description, date, location, price, tickets_available, image, image_mime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """,
        (
            creator_id,
            title,
            description,
            date,
            location,
            price,
            tickets_available,
            image_bytes,
            image_mime,
        ),
    )
    event_id = cursor.fetchone()["id"]  # type: ignore
    conn.commit()
    conn.close()
    return event_id  # type: ignore


def get_event_by_id(event_id: int) -> Optional[Event]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, description, date, location, price, tickets_available, creator_id
        FROM events WHERE id = %s
    """,
        (event_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None  # type: ignore


def count_event_registrations(event_id: int) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) AS count FROM registrations WHERE event_id = %s", (event_id,)
    )
    count = cursor.fetchone()["count"]  # type: ignore
    conn.close()
    return count  # type: ignore


def event_has_image(event_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM events WHERE id = %s AND image IS NOT NULL AND LENGTH(image) > 0",
        (event_id,),
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def is_user_registered_for_event(user_id: int, event_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM registrations WHERE user_id = %s AND event_id = %s",
        (user_id, event_id),
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def register_user_for_event(user_id: int, event_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM registrations WHERE user_id = %s AND event_id = %s",
        (user_id, event_id),
    )
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute("SELECT tickets_available FROM events WHERE id = %s", (event_id,))
    row = cursor.fetchone()
    if not row or row["tickets_available"] <= 0:  # type: ignore
        conn.close()
        return False
    try:
        cursor.execute(
            "INSERT INTO registrations (user_id, event_id) VALUES (%s, %s)",
            (user_id, event_id),
        )
        cursor.execute(
            "UPDATE events SET tickets_available = tickets_available - 1 WHERE id = %s",
            (event_id,),
        )
        conn.commit()
        return True
    except UniqueViolation:
        return False
    finally:
        conn.close()


def unregister_user_from_event(user_id: int, event_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM registrations WHERE user_id = %s AND event_id = %s",
        (user_id, event_id),
    )
    if cursor.rowcount > 0:
        cursor.execute(
            "UPDATE events SET tickets_available = tickets_available + 1 WHERE id = %s",
            (event_id,),
        )
    conn.commit()
    conn.close()


def get_upcoming_events() -> List[Event]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, description, date, location, price, tickets_available
        FROM events WHERE date >= CURRENT_DATE ORDER BY date ASC
    """
    )
    events = cursor.fetchall()
    conn.close()
    return events  # type: ignore


def get_attendees_for_event(event_id: int) -> List[Registration]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.id AS registration_id, u.id AS user_id, u.username AS name, u.email
        FROM registrations AS r
        JOIN users AS u ON r.user_id = u.id
        WHERE r.event_id = %s
        ORDER BY u.username ASC
    """,
        (event_id,),
    )
    attendees = cursor.fetchall()
    conn.close()
    return [dict(row) for row in attendees]  # type: ignore


def delete_registration_by_id(registration_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT event_id FROM registrations WHERE id = %s", (registration_id,)
    )
    registration = cursor.fetchone()
    if not registration:
        conn.close()
        return False
    event_id = registration["event_id"]  # type: ignore
    cursor.execute("DELETE FROM registrations WHERE id = %s", (registration_id,))
    if cursor.rowcount > 0:
        cursor.execute(
            "UPDATE events SET tickets_available = tickets_available + 1 WHERE id = %s",
            (event_id,),  # type: ignore
        )
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def update_event(
    event_id: int,
    title: str,
    description: str,
    date: str,
    location: str,
    price: float,
    tickets_available: int,
    image_file: Optional[FileStorage],
) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    if image_file and image_file.filename != "":
        image_bytes = image_file.read()
        image_mime = image_file.mimetype
        cursor.execute(
            """
            UPDATE events
            SET title = %s, description = %s, date = %s, location = %s, price = %s,
                tickets_available = %s, image = %s, image_mime = %s
            WHERE id = %s
        """,
            (
                title,
                description,
                date,
                location,
                price,
                tickets_available,
                image_bytes,
                image_mime,
                event_id,
            ),
        )
    else:
        cursor.execute(
            """
            UPDATE events
            SET title = %s, description = %s, date = %s, location = %s, price = %s,
                tickets_available = %s
            WHERE id = %s
        """,
            (title, description, date, location, price, tickets_available, event_id),
        )
    conn.commit()
    conn.close()


def delete_event(event_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM registrations WHERE event_id = %s", (event_id,))
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Database error during event deletion: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_event_image(event_id: int) -> Optional[EventImage]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT image, image_mime FROM events WHERE id = %s", (event_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row["image"]:  # type: ignore
        return EventImage(image=row["image"], image_mime=row["image_mime"])  # type: ignore
    return None
