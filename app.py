import db
from pages import pages
from api import api
from flask import Flask, request
from public import public

app = Flask(__name__, static_folder="static", static_url_path="")

# Register routers (Blueprints)
app.register_blueprint(public)
app.register_blueprint(pages)
app.register_blueprint(api)


@app.context_processor
def inject_user():
    user_id = request.cookies.get("user_id")
    current_user = None
    if user_id:
        current_user = db.get_user_by_id(int(user_id))
    return dict(user=current_user)


db.create_tables()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
