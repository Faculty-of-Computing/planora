import sqlite3
from werkzeug.datastructures import FileStorage
from typing import List


def get_db_connection():
    conn = sqlite3.connect("planora.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def reset_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF")
    cursor.execute(
        """
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' 
        AND name NOT LIKE 'sqlite_%';
        """
    )
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    conn.commit()
    conn.close()
    print("Database reset: all tables and data deleted.")


def create_tables():
    conn = get_db_connection()
    c = conn.cursor()

    # Users table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )

    # Events table with tickets_available column added
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL, -- ISO date string
            location TEXT,
            price REAL,
            tickets_available INTEGER NOT NULL DEFAULT 0, -- new column for tickets
            image BLOB, -- Store binary image data
            image_mime TEXT, -- Store MIME type (e.g., image/png)
            FOREIGN KEY (creator_id) REFERENCES users(id)
        )
        """
    )

    # Registrations table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            UNIQUE(user_id, event_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
        """
    )

    conn.commit()
    conn.close()


def insert_user(email: str, username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
            (email, username, password),
        )
        user_id = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError("Email or username already exists") from e
    finally:
        conn.close()
    return user_id


def get_user_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash FROM users WHERE email = ?", (email,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def insert_event(
    creator_id: int,
    title: str,
    description: str,
    date: str,
    location: str,
    price: float,
    tickets_available: int,
    image_file: FileStorage,
):
    """
    image_file: FileStorage object from Flask (request.files['image'])
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    image_bytes = image_file.read()
    image_mime = image_file.mimetype

    cursor.execute(
        """
        INSERT INTO events (creator_id, title, description, date, location, price, tickets_available, image, image_mime)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    event_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return event_id


def get_event_by_id(event_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, description, date, location, price, tickets_available
        FROM events 
        WHERE id = ?
        """,
        (event_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def count_event_registrations(event_id: int) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) AS count FROM registrations WHERE event_id = ?", (event_id,)
    )
    count = cursor.fetchone()["count"]
    conn.close()
    return count


def event_has_image(event_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT image FROM events WHERE id = ? AND image IS NOT NULL AND LENGTH(image) > 0",
        (event_id,),
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def is_user_registered_for_event(user_id: int, event_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM registrations WHERE user_id = ? AND event_id = ?",
        (user_id, event_id),
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def register_user_for_event(user_id: int, event_id: int) -> bool:
    """
    Attempt to register user for event.
    Return True if registered, False if no tickets available or already registered.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already registered
    cursor.execute(
        "SELECT 1 FROM registrations WHERE user_id = ? AND event_id = ?",
        (user_id, event_id),
    )
    if cursor.fetchone():
        conn.close()
        return False  # Already registered

    # Check tickets availability
    cursor.execute("SELECT tickets_available FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    if not row or row["tickets_available"] <= 0:
        conn.close()
        return False  # No tickets available

    # Proceed to register user
    try:
        cursor.execute(
            "INSERT INTO registrations (user_id, event_id) VALUES (?, ?)",
            (user_id, event_id),
        )
        # Decrement tickets_available by 1
        cursor.execute(
            "UPDATE events SET tickets_available = tickets_available - 1 WHERE id = ?",
            (event_id,),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def unregister_user_from_event(user_id: int, event_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete registration
    cursor.execute(
        "DELETE FROM registrations WHERE user_id = ? AND event_id = ?",
        (user_id, event_id),
    )
    if cursor.rowcount > 0:
        # Increase tickets_available by 1 only if a registration was deleted
        cursor.execute(
            "UPDATE events SET tickets_available = tickets_available + 1 WHERE id = ?",
            (event_id,),
        )
    conn.commit()
    conn.close()


def get_upcoming_events() -> List[sqlite3.Row]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, description, date, location, price, tickets_available
        FROM events
        WHERE date >= date('now')
        ORDER BY date ASC
        """
    )
    events = cursor.fetchall()
    conn.close()
    return events
