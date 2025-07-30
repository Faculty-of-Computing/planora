from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__, static_folder="static", static_url_path="")
DATABASE = "planora.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/events")
def events():
    conn = get_db_connection()
    events = conn.execute("SELECT id, name, date FROM events").fetchall()
    conn.close()
    return jsonify([dict(event) for event in events])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
