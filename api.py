from flask import Blueprint, request, jsonify
import sqlite3
from db import get_db_connection

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/")
def events():
    return jsonify({"hello": "World"})


@api.route("/events/<int:event_id>/register", methods=["POST"])
def register_for_event(event_id):
    """Register a user for an event."""

    user_id = request.cookies.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

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
