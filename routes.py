from init import app
from flask import render_template, jsonify
from db import get_db_connection


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/events")
def events():
    conn = get_db_connection()
    events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return jsonify([dict(event) for event in events])
