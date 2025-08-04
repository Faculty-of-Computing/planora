from db import create_tables
from pages import pages
from api import api
from flask import Flask

app = Flask(__name__, static_folder="static", static_url_path="")

# Register routers (Blueprints)
app.register_blueprint(pages)
app.register_blueprint(api)

create_tables()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
