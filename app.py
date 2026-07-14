import sqlite3
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "change-this-secret-key-in-production"

DATABASE = Path(__file__).parent / "passwords.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT,
            password TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()
    db.close()


@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    db = get_db()

    if search:
        query = """
            SELECT * FROM passwords
            WHERE service LIKE ? OR username LIKE ? OR notes LIKE ?
            ORDER BY service ASC
        """
        pattern = f"%{search}%"
        passwords = db.execute(query, (pattern, pattern, pattern)).fetchall()
    else:
        passwords = db.execute(
            "SELECT * FROM passwords ORDER BY service ASC"
        ).fetchall()

    return render_template("index.html", passwords=passwords, search=search)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        service = request.form.get("service", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        notes = request.form.get("notes", "").strip()

        if not service or not password:
            flash("Service name and password are required.", "error")
            return render_template("add.html")

        db = get_db()
        db.execute(
            """
            INSERT INTO passwords (service, username, password, notes)
            VALUES (?, ?, ?, ?)
            """,
            (service, username, password, notes),
        )
        db.commit()
        flash("Password saved successfully.", "success")
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:password_id>", methods=["GET", "POST"])
def edit(password_id):
    db = get_db()
    entry = db.execute(
        "SELECT * FROM passwords WHERE id = ?", (password_id,)
    ).fetchone()

    if entry is None:
        flash("Password entry not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        service = request.form.get("service", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        notes = request.form.get("notes", "").strip()

        if not service or not password:
            flash("Service name and password are required.", "error")
            return render_template("edit.html", entry=entry)

        db.execute(
            """
            UPDATE passwords
            SET service = ?, username = ?, password = ?, notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (service, username, password, notes, password_id),
        )
        db.commit()
        flash("Password updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", entry=entry)


@app.route("/delete/<int:password_id>", methods=["POST"])
def delete(password_id):
    db = get_db()
    entry = db.execute(
        "SELECT * FROM passwords WHERE id = ?", (password_id,)
    ).fetchone()

    if entry is None:
        flash("Password entry not found.", "error")
        return redirect(url_for("index"))

    db.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
    db.commit()
    flash(f"Deleted entry for {entry['service']}.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
