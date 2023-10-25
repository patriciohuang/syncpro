from cs50 import SQL
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

db = SQL("sqlite:///syncpro.db")

def user_detail():
    user_id = session.get("id")
    print(user_id)
    user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    return render_template("user-detail.html", user_data=user_data, user_id=user_id)

def edit_user():
    user_id = session.get("id")
    user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if request.method == "POST":
        currentpassword = request.form.get("currentpassword")
        newpassword = request.form.get("newpassword")

        stored_hashed_password = user_data[0]["password_hash"]

        if not check_password_hash(stored_hashed_password, currentpassword):
            return render_template("edit-user.html", current_password_error=True)

        hashed_new_password = generate_password_hash(newpassword)
        db.execute("UPDATE users SET password_hash = ? WHERE id = ?", hashed_new_password, user_id)
        return redirect("/")
    else:
        return render_template("edit-user.html", user_data=user_data, current_password_error=False)

def login():
    session.clear()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        redirect_url = request.args.get("redirect", "/")
        if not email:
            return render_template("login.html")
        elif not password:
            return render_template("login.html")
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
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
        return render_template("login.html", redirect_param=redirect_param, invalid=False)

def logout():
    session.clear()
    return redirect("/")

def register():
    existing_user = False
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        redirect_url = request.args.get("redirect")

        existing_user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if existing_user:
            return render_template("register.html", existing_user=True)

        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", email, hashed_password)

        row = db.execute("SELECT * FROM users WHERE email = ?", email)
        session["id"] = row[0]["id"]
        db.execute("INSERT INTO lists (user_id, list_name) VALUES (?, ?)", session["id"], 'My contacts')
        image = "static/user-avatar.png"
        db.execute("INSERT INTO profiles (profile_name, first_name, last_name, number, address, email, image, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 'My profile', '', '', '', '', '', image, session["id"])
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