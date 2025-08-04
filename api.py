from flask import Flask, jsonify, request, abort
import sqlite3
import os

app = Flask(__name__)
DATABASE = "planora.db"
API_KEY = "tightkeychain001"  # Only organizers should know this


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = sqlite3.connect(DATABASE)
    with conn:

        # For Attendees
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attendees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                email TEXT NOT NULL UNIQUE
            )
        """
        )

        #  For Tickets
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        """
        )

        # For Tickets Bought
        conn.execute(
            """"
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT
                attendee_id INTEGER,
                ticket_id INTEGER,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (attendee_id) REFERENCES atrendees(id),
                FOREIGN KEY (ticket_id) REFERENCES tickets(id)         
            );             
        """
        )
        conn.commit()


def check_auth():
    key = request.args.get("key")
    if key != API_KEY:
        abort(403)


@app.route("/attendees", methods=["GET"])
def view_attendees():
    check_auth()
    conn = get_db_connection()
    attendees = conn.execute("SELECT * FROM attendees").fetchall()
    conn.close()
    return jsonify([dict(row) for row in attendees])


@app.route("/tickets", methods=["GET"])
def view_tickets():
    check_auth()
    conn = get_db_connection()
    tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()
    return jsonify([dict(row) for row in tickets])


@app.route("/tickets/purchased", methods=["GET"])
def view_purchased_tickets():
    check_auth()
    conn = get_db_connection()
    results = conn.execute(
        """
        SELECT attendees.name AS attendee_name, tickets,type AS tickets.price, purchases AS purchases.quantity
        FROM purchases
        JOIN attendees ON purchases.attendee_id = attendees.id
        JOIN tickets ON purchases.ticket_id = tickets.id
    """
    ).fetchall()
    conn.close()
    return jsonify([dict(row)] for row in results)


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
