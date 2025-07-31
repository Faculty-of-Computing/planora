# Planora

![School Project](https://img.shields.io/badge/School%20Project-✔️-blue)

🎓 **School Project** – Event Management System built with **Flask (Python)** and **SQLite**, featuring a **frontend built with HTML, CSS, and JavaScript** served via Flask templates.  
📖 **Course:** UUY-CSC222
🏫 **Department:** Computer Science
👥 **Group:** 9
🎓 **Series:** 022/023

Provides a backend API for managing events, users, and bookings with a simple, lightweight architecture.

---

## 🚀 Features

- Flask backend with SQLite database
- Frontend served from Flask templates with static assets
- API endpoints for events, users, and bookings

---

## 🛠️ Tech Stack

- Python 3.x, Flask
- SQLite database
- HTML, CSS, JavaScript served via Flask `templates` and `static` folders

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/planora.git
cd planora
```

### 2. (Optional) Create and activate a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install SQLite CLI (optional)

Download from [SQLite Downloads](https://www.sqlite.org/download.html).

### 5. Create the SQLite database (if not exists)

```bash
sqlite3 planora.db ""
```

### 6. Initialize the database schema

```bash
sqlite3 planora.db

sqlite> CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL
);
sqlite> .exit
```

### 7. Run the Flask application

```bash
python app.py
```

The app will be available at:

```text
http://localhost:5000
```

---

## 🧩 Recommended VS Code Extensions

- Python, Pylance, Black Formatter
- Thunder Client (for API testing)
- SQLite Viewer ([qwtel.sqlite-viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer))
- Live Server (optional, for frontend prototyping)

> Extensions and settings are preconfigured in `.vscode/extensions.json` and `.vscode/settings.json`.
