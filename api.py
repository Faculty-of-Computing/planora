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



@api.route("/events", methods=["POST", "GET"])
def addevent():
    if request.method == "POST":

        conn = get_db_connection()
        cursor = conn.cursor()

        user_id = request.cookies.get("user_id")
        name = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        price = request.form.get("price")        

        cursor.execute("INSERT INTO events (creator_id, title, description, date, location, price) VALUES(?, ?, ?, ?, ?, ?)", (user_id, name, description, date, location, price))

        conn.commit()
        conn.close()

        return jsonify({"message":"Event added successfully"}), 201
    
    if request.method == "GET":
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        conn.close()

        # Convert rows to dicts for JSON response
        event_list = [dict(event) for event in events]
        
        return jsonify(event_list), 200
    

@api.route("/events/<int:eventid>", methods=["GET", "PUT", "DELETE"])
def edit_event(eventid):
    if request.method == "GET":
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM events WHERE id = ?", (eventid,))

        event = cursor.fetchone()
        conn.close()

        if event:
            return jsonify(dict(event))
        else:
            return jsonify({"error":"Event not found"})

    if request.method == "PUT":
        conn = get_db_connection()
        cursor = conn.cursor()
        id = request.cookies.get("user_id")


        #Get the events created by the user, so other users can't edit another user's event's
        cursor.execute("SELECT * FROM events WHERE id = ? AND creator_id = ?", (eventid, id))
        event = cursor.fetchone()
    

        if not event:
            conn.close()
            return jsonify({"error":"Event not found"})
        
        name = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        price = request.form.get("price")

        cursor.execute("UPDATE events SET title = ?, description = ?, date = ?, location = ?, price = ? WHERE id = ?", (name, description, date, location, price, eventid))
        conn.commit()
        conn.close()

        return jsonify({"message":"Events updated successfully"})
    
    if request.method == "DELETE":
        conn = get_db_connection()
        cursor = conn.cursor()
        id = request.cookies.get("user_id")


        cursor.execute("SELECT * FROM events WHERE id = ? AND creator_id = ?", (eventid, id,))
        event = cursor.fetchone()
    

        if not event:
            conn.close()
            return jsonify({"error":"Event not found"})
        
        cursor.execute("DELETE FROM events WHERE id = ?", (eventid,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Event deleted successfully"}), 200