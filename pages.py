from flask import render_template, Blueprint, request, redirect, url_for

pages = Blueprint("pages", __name__)


@pages.route("/")
def index():
    return render_template("index.html")


@pages.route("/test")
def test():
    return render_template("test.html")


@pages.route("/home")
def home():
    return render_template("home.html")


@pages.route("/events/create")
def create():
    return render_template("create.html")


@pages.route("/events/<int:event_id>/details")
def details(event_id):
    return render_template("details.html")


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
def attendees(event_id):
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


@pages.route("/login")
def login():
    return render_template("login-page.html")


@pages.route("/ticket/<int:ticket_id>")
def ticket():
    return render_template("ticket.html")


@pages.route("/event/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id):
    # Sample event data - replace with database query
    event = {
        "id": event_id,
        "name": "Music Concert",
        "date": "2025-08-05",
        "location": "Main Hall",
        "description": "This music concert brings together...",
        "image_url": "path/to/image.jpg"
    }

    if request.method == "POST":
        # Handle form submission
        # Update event in database
        return redirect(url_for("pages.details", event_id=event_id))

    return render_template("edit-event.html", event=event)

@pages.route("/register")
def register():
    return render_template("sign-up.html")