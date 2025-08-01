from db.db import get_db_connection


def create_tables():
    conn = get_db_connection()
    c = conn.cursor()

    # Users table
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
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
        id TEXT PRIMARY KEY,
        creator_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        date TEXT NOT NULL, -- ISO date string
        location TEXT,
        price REAL,
        FOREIGN KEY (creator_id) REFERENCES users(id)
    )
    """
    )

    # Registrations table (users registered for events)
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        event_id TEXT NOT NULL,
        UNIQUE(user_id, event_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (event_id) REFERENCES events(id)
    )
    """
    )

    # Ticket options per event (ticket tiers)
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS ticket_options (
        id TEXT PRIMARY KEY,
        event_id TEXT NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity_available INTEGER NOT NULL,
        FOREIGN KEY (event_id) REFERENCES events(id)
    )
    """
    )

    # Tickets purchased by users
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS tickets (
        id TEXT PRIMARY KEY,
        event_id TEXT NOT NULL,
        ticket_option_id TEXT NOT NULL,
        owner_id TEXT NOT NULL,
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


if __name__ == "__main__":
    create_tables()
