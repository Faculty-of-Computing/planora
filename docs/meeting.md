# 🕒 1-Hour Meeting Plan — Planora Project

## 0 – 5 min | Introduction and Goals

- Welcome and set expectations:

  > "Today, we’ll set up our environment, understand the project structure, learn how to contribute through forks and pull requests, and review theming and task assignments."

- Links to share:

  - [Repo](https://github.com/Faculty-of-Computing/planora)
  - [Python](https://www.python.org/downloads/)
  - [Git](https://git-scm.com/downloads)
  - [VS Code](https://code.visualstudio.com/download)
  - [PyCharm](https://www.jetbrains.com/pycharm/download/)
  - [GitHub (Android)](https://play.google.com/store/apps/details?id=com.github.android&hl=en&pli=1)
  - [GitHub (iOS)](https://apps.apple.com/us/app/github/id1477376905)
  - [Git & GitHub Tutorial](https://www.youtube.com/playlist?list=PL4cUxeGkcC9goXbgTDQ0n_4TBzOO0ocPR)

---

## 5 – 20 min | Environment Setup

- **Desktop contributors:**

  - Install Python, Git, and IDE (VS Code or PyCharm).
  - Fork the repo on GitHub.
  - Clone their fork:

    ```bash
    git clone https://github.com/<username>/planora.git
    ```

  - Open the folder in VS Code.
  - Install recommended extensions (auto-suggested by VS Code).
  - Start the app:

    ```bash
    python app.py
    ```

  - Verify app runs in browser.

- **Mobile contributors:**

  - Install [GitHub Mobile](https://play.google.com/store/apps/details?id=com.github.android&hl=en&pli=1) or [iOS version](https://apps.apple.com/us/app/github/id1477376905).
  - Fork the repo.
  - Download code to phone (Termux or other git client).
  - Make edits, commit, and push from phone.
  - Open PR using GitHub Mobile.

---

## 20 – 25 min | Recommended VS Code Extensions

- Show `.vscode/extensions.json` and explain:

  - **Black Formatter** → Formats Python automatically.
  - **Prettier** → Formats HTML, CSS, JS.
  - **Pylance & Python Envs** → Python IntelliSense and environment support.
  - **SQLite Viewer** → See database contents inside VS Code.
  - **Thunder Client** → Test API endpoints.
  - **Debugpy** → Debug Python code.
  - **Swagger Viewer** → OpenAPI docs preview.
  - **GitLens** → See Git history and authorship.
  - **Markdown Preview + Checkbox** → View and interact with markdown task lists.

---

## 25 – 40 min | Project Structure Walkthrough

- Explain main files:

  - `app.py` — Runs Flask app.
  - `pages.py` — Frontend routes (HTML pages).
  - `api.py` — API endpoints.
  - `db.py` — Database logic.

- `/templates`:

  - `base.html` → Main HTML structure with blocks for content.

- `/static`: CSS and images.
- `/docs`:

  - `tasks.md` → Task assignments.
  - `openapi.yaml` → API spec.
  - `styles.md` → **Theming guide** (colors, fonts, UI rules).

- `/previews`: SVG mockups for frontend pages.
- Show `openapi.yaml` using Swagger Viewer and explain endpoint documentation.

---

## 40 – 50 min | Contributing Workflow

- **Step-by-step:**

  1. Fork repo → clone fork.
  2. Create a branch:

     ```bash
     git checkout -b feature-name
     ```

  3. Make changes → commit → push:

     ```bash
     git add .
     git commit -m "Description"
     git push origin feature-name
     ```

  4. Open a Pull Request (PR) from fork to main repo.

- **Mobile:**

  - Fork → download → edit → commit → push → PR via GitHub Mobile.

- ✅ **Reminder:** Share [Git & GitHub Tutorial](https://www.youtube.com/playlist?list=PL4cUxeGkcC9goXbgTDQ0n_4TBzOO0ocPR).

- Live demo: make a small change → commit → push → PR.

- Allow 1–2 participants to practice.

---

## 50 – 55 min | Task Assignments and Theming

- Open `/docs/tasks.md` → assign responsibilities.
- Open `/docs/styles.md`:

  - Explain color palette, typography, and UI rules.

- Show `/previews` SVGs as references for building pages.
- ✅ **Reminder:** Share links to `tasks.md`, `styles.md`, and `/previews`.

---

## 55 – 60 min | Wrap-up and Next Steps

- Recap:

  - Environment setup ✅
  - Extensions ✅
  - Project structure ✅
  - Git + PR workflow ✅
  - Mobile workflow ✅
  - Theming and tasks ✅

- Goal: first commit and PR within 24 hrs.
- Schedule a follow-up session to review contributions.
- Final Q\&A.
