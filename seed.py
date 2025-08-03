import random
from datetime import datetime, timedelta
from db import get_db_connection, create_tables, reset_database

reset_database()
create_tables()


def populate_users(conn):
    users = [(f"user{i}@example.com", f"user{i}", f"hash{i}") for i in range(1, 11)]
    conn.executemany(
        "INSERT OR IGNORE INTO users (email, username, password_hash) VALUES (?, ?, ?)",
        users,
    )


def populate_events(conn):
    events = []
    for i in range(1, 11):
        creator_id = random.randint(1, 10)
        title = f"Event {i}"
        description = f"Description for event {i}"
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        location = f"Location {i}"
        price = round(random.uniform(10, 100), 2)
        events.append((creator_id, title, description, date, location, price))
    conn.executemany(
        """
        INSERT OR IGNORE INTO events (creator_id, title, description, date, location, price)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        events,
    )


def populate_registrations(conn):
    registrations = []
    for i in range(1, 11):
        user_id = random.randint(1, 10)
        event_id = random.randint(1, 10)
        registrations.append((user_id, event_id))
    conn.executemany(
        "INSERT OR IGNORE INTO registrations (user_id, event_id) VALUES (?, ?)",
        registrations,
    )


def populate_ticket_options(conn):
    options = []
    for i in range(1, 11):
        event_id = random.randint(1, 10)
        name = f"Option {i}"
        price = round(random.uniform(5, 50), 2)
        quantity = random.randint(50, 200)
        options.append((event_id, name, price, quantity))
    conn.executemany(
        """
        INSERT OR IGNORE INTO ticket_options (event_id, name, price, quantity_available)
        VALUES (?, ?, ?, ?)
    """,
        options,
    )


def populate_tickets(conn):
    tickets = []
    for i in range(1, 11):
        event_id = random.randint(1, 10)
        ticket_option_id = random.randint(1, 10)
        owner_id = random.randint(1, 10)
        purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        qr_code_url = f"https://example.com/qr/{i}.png"
        tickets.append(
            (event_id, ticket_option_id, owner_id, purchase_date, qr_code_url)
        )
    conn.executemany(
        """
        INSERT OR IGNORE INTO tickets (event_id, ticket_option_id, owner_id, purchase_date, qr_code_url)
        VALUES (?, ?, ?, ?, ?)
    """,
        tickets,
    )


def main():
    conn = get_db_connection()
    populate_users(conn)
    populate_events(conn)
    populate_registrations(conn)
    populate_ticket_options(conn)
    populate_tickets(conn)
    conn.commit()
    conn.close()
    print("Database populated successfully with sample data.")


if __name__ == "__main__":
    main()
