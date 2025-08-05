from flask import Blueprint, request, jsonify, make_response
from db import get_user_by_id, get_db_connection

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/")
def events():
    return jsonify({"hello": "World"})


@api.route("/events", methods=["POST", "GET"])
def addevent():
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
            return jsonify({"error": "Event not found"}), 404

    user_id = request.cookies.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "PUT":
        cursor.execute("SELECT * FROM events WHERE id = ?", (eventid,))
        event = cursor.fetchone()

        if not event:
            conn.close()
            return jsonify({"error": "Event not found"}), 404

        if event["creator_id"] != int(user_id):
            conn.close()
            return (
                jsonify({"error": "You do not have permission to edit this event"}),
                403,
            )

        name = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        price = request.form.get("price")

        cursor.execute(
            """
            UPDATE events 
            SET title = ?, description = ?, date = ?, location = ?, price = ? 
            WHERE id = ?
            """,
            (name, description, date, location, price, eventid),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Event updated successfully"})

    if request.method == "DELETE":
        cursor.execute("SELECT * FROM events WHERE id = ?", (eventid,))
        event = cursor.fetchone()
        if not event:
            conn.close()
            return jsonify({"error": "Event not found"}), 404

        if event["creator_id"] != int(user_id):
            conn.close()
            return (
                jsonify({"error": "You do not have permission to delete this event"}),
                403,
            )

        cursor.execute("DELETE FROM events WHERE id = ?", (eventid,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Event deleted successfully"}), 204


@api.route("/auth/logout", methods=["POST"])
def logout():
    response = make_response(
        jsonify(
            {"success": True, "message": "Logout successful, session cookie cleared."}
        )
    )

    response.set_cookie("user_id", "", expires=0, httponly=True)

    return response, 200


@api.route("/auth/me", methods=["GET"])
def current_user():
    user_id = request.cookies.get("user_id")

    if not user_id:
        return (
            jsonify(
                {"success": False, "message": "Unauthorized. No session cookie found."}
            ),
            401,
        )

    user = get_user_by_id(user_id)

    if not user:
        return (
            jsonify({"success": False, "message": "Invalid session. User not found."}),
            401,
        )

    user_data = {"id": user[0], "username": user[1], "email": user[2]}

    return jsonify({"success": True, "user": user_data}), 200


@api.route("/attendees", methods=["GET"])
def view_attendees():
    # TODO check_auth()
    conn = get_db_connection()
    attendees = conn.execute("SELECT * FROM attendees").fetchall()
    conn.close()
    return jsonify([dict(row) for row in attendees])


@api.route("/tickets", methods=["GET"])
def view_tickets():
    # TODO check_auth()
    conn = get_db_connection()
    tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()
    return jsonify([dict(row) for row in tickets])


@api.route("/tickets/purchased", methods=["GET"])
def view_purchased_tickets():
    # TODO check_auth()
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
