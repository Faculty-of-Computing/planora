from dotenv import load_dotenv

load_dotenv()

from flask import Flask
import db
from private import private
from public import public


app = Flask(__name__, static_folder="static", static_url_path="/static")

# Register routers (Blueprints)
app.register_blueprint(public)
app.register_blueprint(private)


db.create_tables()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
