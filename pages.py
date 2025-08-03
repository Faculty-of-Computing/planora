from flask import render_template, Blueprint

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


@pages.route("/create")
def create():
    return render_template("create.html")
