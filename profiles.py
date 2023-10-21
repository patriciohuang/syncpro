from cs50 import SQL
from flask import render_template, request, redirect, session
import requests
from bs4 import BeautifulSoup
from helpers import get_favicon_url

db = SQL("sqlite:///syncpro.db")

def profile_lists():
    user_id = session["id"]
    profiles = db.execute("SELECT * FROM profiles WHERE user_id = ?", user_id)

    return render_template("profile-lists.html", profiles=profiles)

def profile_detail(profile_id):
    user_id = session.get("id")
    user_id = user_id
    profile = db.execute("SELECT * FROM profiles WHERE id = ?", profile_id)
    profile_id = profile[0]["id"]
    exist_contact = 0
    links = db.execute("SELECT * FROM profile_links WHERE profile_id = ?", profile_id)
    exist_contact = db.execute("SELECT * FROM profiles JOIN lists_profiles AS lp ON lp.profile_id = profiles.id JOIN lists ON lp.list_id = lists.id WHERE profiles.id = ? AND lists.user_id = ?", profile_id, user_id)
    print(exist_contact)

    return render_template("profile-detail.html", links=links, profile=profile, profile_id=profile_id, user_id=user_id, exist_contact=exist_contact)

def add_profile():
    user_id = session["id"]
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

        for key, value in request.form.items():
            if key.startswith("url"):
                link_url = value
                if link_url:
                    try:
                        user_favicon = get_favicon_url(link_url)
                        response = requests.get(link_url)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title_tag = soup.find('title')
                        if title_tag:
                            title = title_tag.text
                        else:
                            title = "Title not found on the page."
                        profile_id = db.execute("SELECT id FROM profiles ORDER BY id DESC LIMIT 1")
                        profile_id = profile_id[0]["id"]
                        db.execute("INSERT INTO profile_links (profile_id, link_title, link_url, icon) VALUES (?, ?, ?, ?)", profile_id, title, link_url, user_favicon)
                    except requests.exceptions.RequestException as e:
                        return render_template("error.html", error_message="Invalid URL, please try again")
                else:
                    render_template("error.html", error_message="URL not provided, please insert a valid URL")
        return redirect("/")
    else:
        return render_template("add-profile.html")

def edit_profile(profile_id):
    profile = db.execute("SELECT * FROM profiles WHERE id = ?", profile_id)
    links = db.execute("SELECT * FROM profile_links WHERE profile_id = ?", profile_id)
    if not profile:
        return render_template("error.html", error_message="Profile dosen't exist, please try again")

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
                if link_url:
                    try:
                        user_favicon = get_favicon_url(link_url)
                        response = requests.get(link_url)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title_tag = soup.find('title')
                        if title_tag:
                            title = title_tag.text
                        else:
                            title = "Title not found on the page."
                        if link_id:
                            db.execute("UPDATE profile_links SET link_title = ?, link_url = ?, icon = ? WHERE id = ?", title, link_url, user_favicon,link_id)
                        else:
                            db.execute("INSERT INTO profile_links (profile_id, link_title, link_url, icon) VALUES (?, ?, ?, ?)", profile_id, title, link_url, user_favicon)
                    except requests.exceptions.RequestException as e:
                        return render_template("error.html", error_message='Invalid URL please try again')
                else:
                    render_template("error.html", error_message="URL not provided, please insert a valid URL")

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
        return render_template("error.html", error_message="Couldn't delete the profile")

