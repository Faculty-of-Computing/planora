# NOTE THESE PAGES REQUIRE THAT THE USER MUST BE AUTHENTICATED

from flask import (
    Response,
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    abort,
)
import utils
import db

pages = Blueprint("pages", __name__)


# SECTION MIDDLEWARE TO REQUIRE AUTH
@pages.before_request
def require_login():
    if utils.user_is_authenticated() == False:
        return redirect("/login")


@pages.route("/home")
def upcoming_events():
    events = db.get_upcoming_events()

    # Add image_url and attendees count for each event
    event_list = []
    for event in events:
        event_dict = dict(event)
        event_id = event_dict["id"]
        event_dict["image_url"] = (
            url_for("pages.event_image", event_id=event_id)
            if db.event_has_image(event_id)
            else "/images/planora.png"
        )
        event_dict["attendees"] = db.count_event_registrations(event_id)
        event_list.append(event_dict)  # type: ignore

    return render_template("home.html", events=event_list)


@pages.route("/events/<int:event_id>/image")
def event_image(event_id: int):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT image, image_mime FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()

    if row and row["image"]:
        return Response(row["image"], mimetype=row["image_mime"])
    return None


@pages.route("/events/create", methods=["POST", "GET"])
def create_event():
    if request.method == "GET":
        return render_template("create-event.html", error=None)

    if request.method == "POST":
        user_id: str = request.cookies.get("user_id")  # type: ignore

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        date = request.form.get("date", "").strip()
        location = request.form.get("location", "").strip()
        price = request.form.get("price", "").strip()
        image_file = request.files.get("image")

        if not (title and description and date and price and image_file):
            return render_template(
                "create-event.html", error="Please fill in all required fields."
            )

        try:
            creator_id = int(user_id)
            price_val = float(price)
            if price_val < 0:
                return render_template(
                    "create-event.html", error="Price must be zero or positive."
                )
        except ValueError:
            return render_template(
                "create-event.html", error="Invalid user ID or price."
            )

        event_id = db.insert_event(
            creator_id=creator_id,
            title=title,
            description=description,
            date=date,
            location=location,
            price=price_val,
            image_file=image_file,
        )

        return redirect(f"/events/{event_id}")


@pages.route("/events/<int:event_id>", methods=["GET", "POST"])
def event_details(event_id: int):
    # Assume user_id is always set (from cookies or session)
    user_id = int(request.cookies.get("user_id"))  # type: ignore

    if request.method == "POST":
        if db.is_user_registered_for_event(user_id, event_id):
            db.unregister_user_from_event(user_id, event_id)
        else:
            db.register_user_for_event(user_id, event_id)
        return redirect(url_for("pages.event_details", event_id=event_id))

    event = db.get_event_by_id(event_id)
    if not event:
        abort(404, description="Event not found")

    event["attendees"] = db.count_event_registrations(event_id)

    # Provide image URL or default image path
    event["image_url"] = (
        url_for("pages.event_image", event_id=event_id)
        if db.event_has_image(event_id)
        else "/images/planora.png"
    )

    user_registered = db.is_user_registered_for_event(user_id, event_id)

    return render_template(
        "event-details.html", event=event, user_registered=user_registered
    )


@pages.route("/profile")
def profile():

    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "events": [
            {"name": "Music Concert", "date": "Aug 5"},
            {"name": "Tech Meetup", "date": "Aug 10"},
            {"name": "Tech Meetup", "date": "Aug 10"},
        ],
    }
    return render_template("userprofile.html", user=user_data)


@pages.route("/events/<int:event_id>/attendees")
def attendees(event_id: int):
    # Sample data - replace with actual database query
    sample_attendees = [
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "ticket_type": "General Admission",
        },
        {"name": "Bob Smith", "email": "bob@example.com", "ticket_type": "VIP Ticket"},
        {
            "name": "Cynthia Lee",
            "email": "cynthia@example.com",
            "ticket_type": "General Admission",
        },
        {
            "name": "Morpheus Endless",
            "email": "dreamking@example.com",
            "ticket_type": "General Admission",
        },
        {
            "name": "Okarun Momochan",
            "email": "okarun@example.com",
            "ticket_type": "General Admission",
        },
        {
            "name": "Cole Palmer",
            "email": "palmer@example.com",
            "ticket_type": "VVIP Ticket",
        },
    ]

    # Get event details - replace with actual database query
    event = {"id": event_id, "name": "Music Concert"}

    return render_template("attendees.html", attendees=sample_attendees, event=event)


@pages.route("/ticket/<int:ticket_id>")
def ticket():
    return render_template("ticket.html")


@pages.route("/event/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id: int):
    # Sample event data - replace with database query
    event = {
        "id": event_id,
        "name": "Music Concert",
        "date": "2025-08-05",
        "location": "Main Hall",
        "description": "This music concert brings together...",
        "image_url": "path/to/image.jpg",
    }

    if request.method == "POST":
        # Handle form submission
        # Update event in database
        return redirect(url_for("pages.details", event_id=event_id))

    return render_template("edit-event.html", event=event)
