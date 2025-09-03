from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required  # type: ignore
import models.db as db
from models.user import User

public = Blueprint("public", __name__)


@public.route("/")
def index():
    events = db.get_upcoming_events()
    event_list = []
    for event in events:
        event_dict: db.Event = dict(event)  # type: ignore
        event_id = event_dict["id"]
        event_dict["image_url"] = (  # type: ignore
            url_for("events.image", event_id=event_id)
            if db.event_has_image(event_id)  # type: ignore
            else "/images/planora.png"
        )
        event_dict["attendees"] = db.count_event_registrations(event_id)  # type: ignore
        event_list.append(event_dict)  # type: ignore
    return render_template("home.html", events=event_list)


@public.route("/login", methods=["GET", "POST"])
def login():
    redirect_to = request.args.get("next") or request.form.get("next")

    if request.method == "GET":
        return render_template("login.html", redirect_to=redirect_to)

    # POST
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email and Password are required!")
        return render_template("login.html", redirect_to=redirect_to)

    user_row = db.get_user_by_email(email)
    if not user_row:
        flash("User not found!")
        return render_template("login.html", redirect_to=redirect_to)

    if password != user_row["password_hash"]:  # replace with proper hash check
        flash("Incorrect Password!")
        return render_template("login.html", redirect_to=redirect_to)

    # Wrap db row into User class
    user = User(
        id=user_row["id"],
        email=user_row["email"],
        username=user_row["username"],
        password_hash=user_row["password_hash"],
    )

    # This creates the session
    login_user(user, remember=True)

    # Redirect appropriately
    if redirect_to:
        return redirect(redirect_to)
    return redirect(url_for("public.index"))


@public.route("/register", methods=["GET", "POST"])
def register():
    redirect_to = request.args.get("next") or request.form.get("next")

    if request.method == "GET":
        return render_template("register.html", redirect_to=redirect_to)

    # POST
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    if not email or not username or not password:
        flash("Please fill out all fields")
        return render_template("register.html", redirect_to=redirect_to)

    try:
        user_id = db.insert_user(
            email=email.strip().lower(),
            username=username.strip().lower(),
            password=password.strip(),  # hash this in real code
        )
        if user_id is None:  # type: ignore
            raise ValueError("Email or username already exists")

        # Create a User instance
        user = User(
            id=user_id,
            email=email.strip().lower(),
            username=username.strip().lower(),
            password_hash=password.strip().lower(),
        )

        # Log the user in immediately after registering
        login_user(user, remember=True)

        if redirect_to:
            return redirect(redirect_to)
        return redirect(url_for("public.index"))

    except ValueError as e:
        flash(str(e))
        return render_template("register.html", redirect_to=redirect_to)


@public.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
