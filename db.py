import sqlite3


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

    # Events table
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

    # Ticket options table
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS ticket_options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity_available INTEGER NOT NULL,
        FOREIGN KEY (event_id) REFERENCES events(id)
    )
    """
    )

    # Tickets table
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        ticket_option_id INTEGER NOT NULL,
        owner_id INTEGER NOT NULL,
        purchase_date TEXT NOT NULL, -- ISO datetime string
        qr_code_url TEXT,
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (ticket_option_id) REFERENCES ticket_options(id),
        FOREIGN KEY (owner_id) REFERENCES users(id)
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
