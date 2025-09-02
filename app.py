from dotenv import load_dotenv

load_dotenv()

import os
import models.db as db
from flask import Flask
from models.user import User
from routes.public import public
from routes.events import events
from flask_login import LoginManager


app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = os.getenv("POSTGRES_PASSWORD")

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)  # type: ignore
login_manager.login_view = "public.login"  # type: ignore


@login_manager.user_loader  # type: ignore
def load_user(user_id: str):
    return User.get(int(user_id))


# Register routers (Blueprints)
app.register_blueprint(public)
app.register_blueprint(events)


db.create_tables()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
