from flask import Blueprint, request, jsonify
import sqlite3

api = Blueprint("api", __name__, url_prefix="/api")


def get_db_connection():
    conn = sqlite3.connect("planora.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@api.route("/")
def events():
    return jsonify({"hello": "World"})


@api.route("/events/<int:event_id>/register", methods=["POST"])
def register_for_event(event_id):
    """Register a user for an event."""
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = data["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    if not event:
        conn.close()
        return jsonify({"error": "Event not found"}), 404

    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    try:
        cursor.execute(
            "INSERT INTO registrations (user_id, event_id) VALUES (?, ?)",
            (user_id, event_id),
        )
        conn.commit()
        return jsonify({"message": "Successfully registered for event"}), 201
    except sqlite3.IntegrityError as e:
        if (
            "UNIQUE constraint failed: registrations.user_id, registrations.event_id"
            in str(e)
        ):
            return jsonify({"error": "User already registered for this event"}), 409
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()
