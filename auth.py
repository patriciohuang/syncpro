from cs50 import SQL
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///syncpro.db")

def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username").title()
        password = request.form.get("password")
        redirect_url = request.args.get("redirect", "/")
        if not username:
            return render_template("login.html")
        elif not password:
            return render_template("login.html")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            return render_template("login.html", invalid=True)
        session["id"] = rows[0]["id"]

        if redirect_url:
            return redirect(redirect_url)
        else:
            return redirect("/")
    else:
        redirect_url = request.args.get("redirect", "/")
        if redirect_url:
            redirect_param = f"?redirect={redirect_url}"
        else:
            redirect_param = ""
        return render_template("login.html", redirect_param=redirect_param)

def logout():
    session.clear()
    return redirect("/")

def register():
    existing_user = False
    if request.method == "POST":
        username = request.form.get("username").title()
        password = request.form.get("password")
        redirect_url = request.args.get("redirect")

        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return render_template("register.html", existing_user=True)

        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hashed_password)

        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["id"] = row[0]["id"]
        db.execute("INSERT INTO lists (user_id, list_name) VALUES (?, ?)", session["id"], 'My contacts')
        image = "static/user-avatar.png"
        db.execute("INSERT INTO profiles (profile_name, first_name, last_name, number, address, email, image, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 'My profile', username, '', '', '', '', image, session["id"])
        if redirect_url:
            return redirect(redirect_url)
        else:
            return redirect("/")
    else:
        redirect_url = request.args.get("redirect", "/")
        if redirect_url:
            redirect_param = f"?redirect={redirect_url}"
        else:
            redirect_param = ""
        return render_template("register.html", redirect_param=redirect_param)