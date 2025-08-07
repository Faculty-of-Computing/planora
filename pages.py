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
        tickets_available = request.form.get("tickets_available", "").strip()
        image_file = request.files.get("image")

        if not (
            title
            and description
            and date
            and price
            and tickets_available
            and image_file
        ):
            return render_template(
                "create-event.html", error="Please fill in all required fields."
            )

        try:
            creator_id = int(user_id)
            price_val = float(price)
            tickets_available_val = int(tickets_available)
            if price_val < 0:
                return render_template(
                    "create-event.html", error="Price must be zero or positive."
                )
            if tickets_available_val < 0:
                return render_template(
                    "create-event.html",
                    error="Tickets available must be zero or positive.",
                )
        except ValueError:
            return render_template(
                "create-event.html",
                error="Invalid user ID, price, or tickets available.",
            )

        event_id = db.insert_event(
            creator_id=creator_id,
            title=title,
            description=description,
            date=date,
            location=location,
            price=price_val,
            tickets_available=tickets_available_val,
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
    attendees = db.get_attendees_for_event(event_id)  # type: ignore

    is_creator = True if event["creator_id"] == user_id else False

    return render_template(
        "event-details.html",
        event=event,
        user_registered=user_registered,
        is_creator=is_creator,
        attendees=attendees,
    )


# @pages.route("/profile")
# def profile():
#     user_data = {
#         "name": "John Doe",
#         "email": "john@example.com",
#         "events": [
#             {"name": "Music Concert", "date": "Aug 5"},
#             {"name": "Tech Meetup", "date": "Aug 10"},
#             {"name": "Tech Meetup", "date": "Aug 10"},
#         ],
#     }
#     return render_template("userprofile.html", user=user_data)


@pages.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id: int):
    event = db.get_event_by_id(event_id)
    user_id = int(request.cookies.get("user_id"))  # type: ignore

    if not event:
        abort(404)

    if event["creator_id"] != user_id:
        return redirect(url_for("pages.event_details", event_id=event_id))

    if db.event_has_image(event_id):
        event["image_url"] = url_for("pages.event_image", event_id=event_id)

    def render_with_error(error: str):
        return render_template("edit-event.html", event=event, error=error)

    if request.method == "POST":
        # Data Validation
        title: str = request.form.get("title")  # type: ignore
        date: str = request.form.get("date")  # type: ignore
        location: str = request.form.get("location")  # type: ignore
        description: str = request.form.get("description")  # type: ignore
        price_str = request.form.get("price", "0.0")
        tickets_available_str = request.form.get("tickets_available", "0")
        image_file = request.files.get("image")

        if title == "" or date == "" or location == "" or description == "":
            return render_with_error("Please fill all required fields")

        try:
            price = float(price_str)
            if price < 0:
                return render_with_error("Price cannot be negative.")
        except ValueError:
            return render_with_error(
                "Invalid price format. Please enter a valid number."
            )

        try:
            tickets_available = int(tickets_available_str)
            if tickets_available < 0:
                return render_with_error("Tickets available cannot be negative.")
        except ValueError:
            return render_with_error(
                "Invalid number of tickets. Please enter a whole number."
            )

        try:
            db.update_event(
                event_id,
                title,
                description,
                date,
                location,
                price,
                tickets_available,
                image_file,  # type: ignore
            )
            return redirect(url_for("pages.event_details", event_id=event_id))
        except Exception as e:
            return render_with_error(
                f"An error occurred while updating the event: {str(e)}"
            )

    return render_template("edit-event.html", event=event)


@pages.route("/home")
def home():
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
