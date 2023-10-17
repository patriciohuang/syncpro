from cs50 import SQL
from flask import render_template, request, redirect, session

db = SQL("sqlite:///syncpro.db")

def index():
    user_id = session["user_id"]
    lists = db.execute("SELECT id, list_name FROM lists WHERE user_id = ?", user_id)
    profiles = db.execute("SELECT * FROM profiles WHERE user_id = ? ORDER BY id DESC", user_id)
    if profiles:
        avatar = profiles[0]["image"]
    else:
        avatar = 'static/user-avatar.png'
    return render_template("index.html", lists=lists, profiles=profiles, avatar=avatar)

def add_list():
    if request.method == "POST":
        user_id = session["user_id"]
        listname = request.form.get("listname")

        db.execute("INSERT INTO lists (user_id, list_name) VALUES (?, ?)", user_id, listname)
        return redirect("/")
    else:
        return render_template("add-list.html")

def edit_list(list_id):
    if request.method == "POST":
        listname = request.form.get("listname")
        db.execute("UPDATE lists SET list_name = ? WHERE id = ?", listname, list_id)
        return redirect("/")
    else:
        current_list_name = db.execute("SELECT list_name FROM lists WHERE id = ?", list_id)

        if current_list_name:
            current_list_name = current_list_name[0]["list_name"]
            return render_template("edit-list.html", list_id=list_id, current_list_name=current_list_name)
        else:
            return redirect("/error")


def delete_list(list_id):
    if list_id:
        db.execute("DELETE FROM lists_profiles WHERE list_id = ?", list_id)
        db.execute("DELETE FROM lists WHERE id = ?", list_id)

        return redirect("/")
    else:
        return redirect("/error")
