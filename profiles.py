from cs50 import SQL
from flask import render_template, request, redirect, session
from urllib.parse import urlsplit

db = SQL("sqlite:///syncpro.db")

def profile_lists():
    user_id = session["user_id"]
    profiles = db.execute("SELECT * FROM profiles WHERE user_id = ?", user_id)

    return render_template("profile-lists.html", profiles=profiles)

def profile_detail(profile_id):
    profile = db.execute("SELECT * FROM profiles WHERE id = ?", profile_id)
    profile_id = profile[0]["id"]
    links = db.execute("SELECT * FROM profile_links WHERE profile_id = ?", profile_id)

    return render_template("profile-detail.html", links=links, profile=profile, profile_id=profile_id)

def add_profile():
    user_id = session["user_id"]
    if request.method == "POST":
        profilename = request.form.get("profilename").title()
        firstname = request.form.get("firstname").title()
        lastname = request.form.get("lastname").title()
        number = request.form.get("number")
        address = request.form.get("address")
        email = request.form.get("email")
        image = 'static/user-avatar.png'

        db.execute(
            "INSERT INTO profiles (profile_name, first_name, last_name, number, address, email, image, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            profilename,
            firstname,
            lastname,
            number,
            address,
            email,
            image,
            user_id,
        )

        profile_id = db.execute("SELECT id FROM profiles ORDER BY id DESC LIMIT 1")
        profile_id = profile_id[0]["id"]
        for key, value in request.form.items():
            if key.startswith("url"):
                link_url = value
                parsed_url = urlsplit(link_url)
                link_type = parsed_url.netloc
                db.execute("INSERT INTO profile_links (profile_id, link_type, link_url) VALUES (?, ?, ?)", profile_id, link_type, link_url)
        return redirect(f"/")
    else:
        return render_template("add-profile.html")

def edit_profile(profile_id):
    profile = db.execute("SELECT * FROM profiles WHERE id = ?", profile_id)
    links = db.execute("SELECT * FROM profile_links WHERE profile_id = ?", profile_id)
    if not profile:
        return redirect("/error")

    if request.method == "POST":
        profilename = request.form.get("profilename").title()
        firstname = request.form.get("firstname").title()
        lastname = request.form.get("lastname").title()
        number = request.form.get("number")
        address = request.form.get("address")
        email = request.form.get("email")
        db.execute(
            "UPDATE profiles SET profile_name = ?, first_name = ?, last_name = ?, number = ?, address = ?, email = ? WHERE id = ?",
            profilename,
            firstname,
            lastname,
            number,
            address,
            email,
            profile_id
        )
        for key, value in request.form.items():
            if key.startswith("url"):
                link_id = request.form.get("link_id" + key[3:])
                link_url = value
                parsed_url = urlsplit(link_url)
                link_type = parsed_url.netloc
                if link_id:
                    db.execute("UPDATE profile_links SET link_type = ?, link_url = ? WHERE id = ?", link_type, link_url, link_id)
                else:
                    db.execute("INSERT INTO profile_links (profile_id, link_type, link_url) VALUES (?, ?, ?)", profile_id, link_type, link_url)

        return redirect(f"/profile-detail/{profile_id}")
    else:
        return render_template("edit-profile.html", profile=profile[0], profile_id=profile_id, links=links)

def delete_profile(profile_id):
    if profile_id:
        db.execute("DELETE FROM profile_links WHERE profile_id = ?", profile_id)
        db.execute("DELETE FROM lists_profiles WHERE profile_id = ?", profile_id)
        db.execute("DELETE FROM profiles WHERE id = ?", profile_id)
        return redirect(f"/")
    else:
        return redirect("/error")

