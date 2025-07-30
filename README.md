# Planora – Backend

![School Project](https://img.shields.io/badge/School%20Project-✔️-blue)

This is the **backend** of **Planora**, a simple event management system built with **Flask** and **SQLite**.
It provides API endpoints to retrieve and manage events stored in a lightweight SQLite database.

---

## 🚀 Features

- Minimal Flask server with basic API routes
- Uses SQLite for lightweight storage
- Simple setup for school demonstration of client-server relationship

---

## 🛠️ Tech Stack

- Python 3.x
- Flask
- SQLite (no ORM or migrations)

---

## 🧩 Recommended VS Code Extensions

This project is preconfigured with code formatting and helpful extensions:

- Python development (`ms-python.black-formatter`, `ms-python.vscode-pylance`, `ms-python.debugpy`, etc.)
- API testing with [Thunder Client](https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client)
- SQLite database browsing with [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)

When you open this folder in VS Code, you'll automatically see a prompt  
to install these recommended extensions

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/planora-backend.git
cd planora-backend
```

### 2. Install dependencies

```bash
pip install Flask
```

---

### 3. Install SQLite CLI (Optional)

You can download the SQLite command-line tool from:
[SQLite Downloads](https://www.sqlite.org/download.html)

---

### 4. Create the SQLite Database

If you don’t have an existing database, you can create an empty one using:

```bash
sqlite3 planora.db ""
```

This will generate a new `planora.db` file in your project folder.

---

### 5. Initialize the database schema

Create a simple table manually using the SQLite CLI:

```bash
sqlite3 planora.db

sqlite> CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL
);
sqlite> .exit
```

---

### 6. Run the Flask Server

```bash
python app.py
```

Your backend API will now be available at:

```text
http://localhost:5000
```

---

## 📌 Notes

- This is a **school project**, not intended for production use.
- For database inspection, you can use:
  - SQLite CLI (`sqlite3 planora.db`)
  - [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer) for VS Code

---

Would you like me to also add **instructions for testing POST requests** to add new events (e.g., using `curl`)?
