from cs50 import SQL
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///syncpro.db")

def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return render_template("login.html")
        elif not password:
            return render_template("login.html")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            return render_template("login.html", invalid=True)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

def logout():
    session.clear()
    return redirect("/")

def register():
    existing_user = False
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return render_template("register.html", existing_user=True)

        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hashed_password)

        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = row[0]["id"]
        db.execute("INSERT INTO lists (user_id, list_name) VALUES (?, ?)", session["user_id"], 'My contact')
        return redirect("/")
    return render_template("register.html")