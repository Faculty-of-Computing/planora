from db import create_tables
from db.db import get_db_connection
from flask import Flask, jsonify, render_template


create_tables()

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/events")
def events():
    conn = get_db_connection()
    events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return jsonify([dict(event) for event in events])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
