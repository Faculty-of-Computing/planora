from flask import Blueprint, render_template, request
import db
import sqlite3
import utils


public = Blueprint("public", __name__)


@public.route("/")
def index():
    return render_template("index.html")


@public.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email is None or password is None:
            return render_template(
                "login.html", error="Email and Password are required!"
            )

        user: sqlite3.Row = db.get_user_by_email(email)

        if not user:
            return render_template("login.html", error="User not found!")

        if password != user["password_hash"]:
            return render_template("login.html", error="Incorrect Password!")

        return utils.set_user_cookie_and_recirect(user["id"])


@public.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        if email is None or username is None or password is None:
            return render_template("register.html", error="Please fill out all fields")

        try:
            user_id = db.insert_user(
                email=email.strip().lower(),
                username=username.strip().lower(),
                password=password.strip(),
            )
            if user_id is None:
                raise ValueError("Email or username already exists")
            return utils.set_user_cookie_and_recirect(int(user_id))
        except ValueError as e:
            return render_template("register.html", error=str(e))
