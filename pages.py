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

@pages.route('/profile')
def profile():
    # You can pass user data here
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'events': [
            {'name': 'Music Concert', 'date': 'Aug 5'},
            {'name': 'Tech Meetup', 'date': 'Aug 10'},
            {'name': 'Tech Meetup', 'date': 'Aug 10'}
        ]
    }
    return render_template('userprofile.html', user=user_data)
