from cs50 import SQL
from flask import render_template, request, redirect, session

db = SQL("sqlite:///syncpro.db")


from flask import request, redirect, session

def contact_list(list_id):
    list_id = int(list_id)
    profiles = db.execute("SELECT * FROM profiles JOIN lists_profiles AS lp ON lp.profile_id = profiles.id JOIN lists ON lp.list_id = lists.id WHERE lists.id = ? ORDER BY last_name", list_id)
    lists = db.execute("SELECT * FROM lists WHERE id = ?", list_id)
    list_name = lists[0]["list_name"]
    if profiles:
        avatar = profiles[0]["image"]
    else:
        avatar = '/static/user-avatar.png'
    return render_template("contact-list.html", list_id=list_id, profiles=profiles, list_name=list_name, avatar=avatar)

def add_contact(profile_id):
    user_id = session["id"]
    if request.method == "POST":
        selected_list = request.form.getlist("selected_list")
        for list_id in selected_list:
            exist_contact = db.execute("SELECT * FROM lists JOIN lists_profiles ON lists.id = lists_profiles.list_id WHERE lists.id = ? AND lists_profiles.profile_id = ?", list_id, profile_id)
            if exist_contact:
                return redirect('/')
            else:
                db.execute("INSERT INTO lists_profiles (list_id, profile_id) VALUES (?, ?)", list_id, profile_id)
        return redirect('/')
    else:
        lists = db.execute("SELECT * FROM lists WHERE user_id = ?", user_id)
        if not lists:
            db.execute("INSERT INTO lists (user_id, list_name) VALUES (?, ?)", user_id, 'My contacts')
            lists = db.execute("SELECT * FROM lists WHERE user_id = ?", user_id)
        return render_template("add-contact.html", lists=lists, profile_id=profile_id)

def edit_contact(profile_id):
    user_id = session["id"]
    profile = db.execute("SELECT * FROM profiles WHERE id = ?", profile_id)
    current_list = db.execute("SELECT list_id FROM lists_profiles WHERE profile_id = ?", profile_id)
    current_list_ids = {item['list_id'] for item in current_list}
    if request.method == "POST":
        selected_lists = set(map(int, request.form.getlist("selected_lists")))

        for list_id in selected_lists - current_list_ids:
            db.execute("INSERT INTO lists_profiles (list_id, profile_id) VALUES (?, ?)", list_id, profile_id)

        for list_id in current_list_ids - selected_lists:
            db.execute("DELETE FROM lists_profiles WHERE list_id = ? AND profile_id = ?", list_id, profile_id)
        return redirect(f"/profile-detail/{profile_id}")
    else:
        lists = db.execute("SELECT * FROM lists WHERE user_id = ?", user_id)
        return render_template("edit-contact.html", profile=profile, lists=lists, current_list=current_list, current_list_ids=current_list_ids)


def delete_contact(profile_id):
    user_id = session["id"]
    list_id = db.execute("SELECT id FROM lists JOIN lists_profiles AS lp ON lp.list_id = lists.id WHERE lp.profile_id = ? AND lists.user_id = ?", profile_id, user_id)
    if list_id:
        list_id = list_id[0]["id"]
        db.execute("DELETE FROM lists_profiles WHERE list_id = ? AND profile_id = ?", list_id, profile_id)
        return redirect(f"/contact-list/{list_id}")
    else:
        return render_template("error.html", error_message="Couldn't delete the contact")
