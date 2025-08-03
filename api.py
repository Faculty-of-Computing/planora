from flask import Flask, Blueprint, request, jsonify, make_response
from db import insert_user, get_user_by_email, get_user_by_id, get_db_connection
import sqlite3

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

@api.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    username = data.get("username")
    password = data.get("password")

    if email is None or username is None or password is None:
        return jsonify({
            "error": "Please fill out all fields!"
        }), 400
    

    user_id = insert_user(email, username, password)
    
    response = make_response(jsonify({
        "success": True,
        "user_id": user_id,
        "message": f"User {username} registered Successfully!"
    }))

    response.set_cookie("user_id", str(user_id), httponly=True)

    return response, 201


@api.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password")

    if email is None or password is None:
        return jsonify({
            "error": "Email and Password are required!"
        }), 400
    
    print(f"Looking for email: {email}")

    user = get_user_by_email(email)

    print("User found:", user)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found!"
        }), 404
    
    user_id, username, password_hash = user

    if password != password_hash:
        return jsonify({
            "success": False,
            "message": "Incorrect Password!"
        }), 401
    
    response = make_response(jsonify({
        "success": True,
        "message": f"Welcome back, {username}!",
        "user_id": user_id
    }))
    response.set_cookie("user_id", str(user_id), httponly=True)

    return response, 200

@api.route("/auth/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({
        "success": True,
        "message": "Logout successful, session cookie cleared."
    }))

    response.set_cookie("user_id", "", expires=0, httponly=True)

    return response, 200

@api.route("/auth/me", methods=["GET"])
def current_user():
    user_id = request.cookies.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized. No session cookie found."
        }), 401

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid session. User not found."
        }), 401

    user_data = {
        "id": user[0],
        "username": user[1],
        "email": user[2]
    }

    return jsonify({
        "success": True,
        "user": user_data
    }), 200