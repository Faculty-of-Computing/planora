from flask import (
    Blueprint,
    abort,
    Response,
    request,
    render_template,
    redirect,
    url_for,
    flash,
)
import models.db as db
from flask_login import login_required, current_user  # type: ignore


events = Blueprint("events", __name__, url_prefix="/events")


@events.route("/<int:event_id>/image")
def image(event_id: int):
    image_data = db.get_event_image(event_id)
    if image_data:
        return Response(image_data["image"], mimetype=image_data["image_mime"])
    abort(404)


@events.route("/create", methods=["POST", "GET"])
@login_required  # type: ignore
def create():
    if request.method == "GET":
        return render_template("create-event.html")

    user_id: str = current_user.id  # type: ignore

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    date = request.form.get("date", "").strip()
    location = request.form.get("location", "").strip()
    price = request.form.get("price", "").strip()
    tickets_available = request.form.get("tickets_available", "").strip()
    image_file = request.files.get("image")

    if not (
        title and description and date and price and tickets_available and image_file
    ):
        flash("Please fill in all required fields.")
        return render_template("create-event.html")

    try:
        creator_id = int(user_id)
        price_val = float(price)
        tickets_available_val = int(tickets_available)
        if price_val < 0:
            flash("Price must be zero or positive.")
            return render_template("create-event.html")
        if tickets_available_val < 0:
            flash("Tickets available must be zero or positive.")
            return render_template(
                "create-event.html",
            )
    except ValueError:
        flash("Invalid user ID, price, or tickets available.")
        return render_template(
            "create-event.html",
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

    return redirect(url_for("events.details", event_id=event_id))


@events.route("/<int:event_id>", methods=["GET"])
def details(event_id: int):
    event = db.get_event_by_id(event_id)
    if not event:
        abort(404, description="Event not found")

    event["attendees"] = db.count_event_registrations(event_id)  # type: ignore

    event["image_url"] = (  # type: ignore
        url_for("events.image", event_id=event_id)
        if db.event_has_image(event_id)
        else "/images/planora.png"
    )

    user_id = int(current_user.id) if current_user.is_authenticated else -1

    user_registered = db.is_user_registered_for_event(user_id, event_id)
    attendees = db.get_attendees_for_event(event_id)

    is_creator = event["creator_id"] == user_id

    return render_template(
        "event-details.html",
        event=event,
        user_registered=user_registered,
        is_creator=is_creator,
        attendees=attendees,
    )


@events.route("/<int:event_id>", methods=["POST"])
@login_required  # type: ignore
def rsvp(event_id: int):
    user_id = int(current_user.id)
    if db.is_user_registered_for_event(user_id, event_id):
        db.unregister_user_from_event(user_id, event_id)
    else:
        db.register_user_for_event(user_id, event_id)
    return redirect(url_for("events.details", event_id=event_id))


@events.route("/<int:event_id>/edit", methods=["GET", "POST"])
@login_required  # type: ignore
def edit_event(event_id: int):
    event = db.get_event_by_id(event_id)
    user_id = int(current_user.id)  # type: ignore

    if not event:
        abort(404)

    if event["creator_id"] != user_id:
        return redirect(url_for("events.details", event_id=event_id))

    if db.event_has_image(event_id):
        event["image_url"] = url_for("events.image", event_id=event_id)  # type: ignore

    def render_with_error(error: str):
        flash(error)
        return render_template("edit-event.html", event=event)

    if request.method == "POST":
        title: str = request.form.get("title", "").strip()
        date: str = request.form.get("date", "").strip()
        location: str = request.form.get("location", "").strip()
        description: str = request.form.get("description", "").strip()
        price_str = request.form.get("price", "0.0").strip()
        tickets_available_str = request.form.get("tickets_available", "0").strip()
        image_file = request.files.get("image")

        if not (title and date and location and description):
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
                image_file,
            )
            return redirect(url_for("events.details", event_id=event_id))
        except Exception as e:
            return render_with_error(
                f"An error occurred while updating the event: {str(e)}"
            )

    return render_template("edit-event.html", event=event)


@events.route("/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id: int):
    event = db.get_event_by_id(event_id)
    user_id = int(current_user.id)  # type: ignore

    if not event:
        return redirect(url_for("public.index"))

    if event["creator_id"] != user_id:
        return redirect(url_for("events.details", event_id=event_id))

    success = db.delete_event(event_id)

    if success:
        return redirect(url_for("public.index"))
    else:
        return redirect(url_for("events.details", event_id=event_id))
