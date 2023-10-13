from cs50 import SQL
from flask import render_template, request, redirect, session
from urllib.parse import urlsplit

db = SQL("sqlite:///syncpro.db")


def add_contact(list_id):
    user_id = session["user_id"]
    list_id = int(list_id)

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        number = request.form.get("number")
        note = request.form.get("note")

        db.execute(
            "INSERT INTO contacts (list_id, user_id, first_name, last_name, email, phone_number, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            list_id,
            user_id,
            firstname,
            lastname,
            email,
            number,
            note
        )

        contact_id = db.execute("SELECT id FROM contacts ORDER BY id DESC LIMIT 1")
        contact_id = contact_id[0]["id"]
        for key, value in request.form.items():
            if key.startswith("url"):
                link_url = value
                parsed_url = urlsplit(link_url)
                link_type = parsed_url.netloc
                db.execute("INSERT INTO user_links (user_id, contact_id, link_type, link_url) VALUES (?, ?, ?, ?)", user_id, contact_id, link_type, link_url)
        return redirect(f"/contact-list/{list_id}")
    else:
        list_info = db.execute("SELECT * FROM lists WHERE id = ? AND user_id = ?", list_id, user_id)
        if not list_info:
            return redirect("/error")
        return render_template("add-contact.html", list_id=list_id)

def contact_list(list_id):
    list_id = int(list_id)
    user_id = session["user_id"]
    q = request.args.get("q")
    list_info = db.execute("SELECT * FROM lists WHERE id = ? AND user_id = ?", list_id, user_id)
    list_name = list_info[0]["list_name"]
    contact_list = db.execute("SELECT * FROM contacts WHERE list_id = ? AND user_id = ?", list_id, user_id)

    if not list_info:
        return redirect("/error")

    return render_template("contact-list.html", list_id=list_id, contact_list=contact_list, list_name=list_name)


def contact_detail(contact_id):
    user_id = session["user_id"]
    contacts = db.execute("SELECT * FROM contacts WHERE id = ? AND user_id = ?", contact_id, user_id)
    links = db.execute("SELECT * FROM user_links WHERE contact_id = ? AND user_id = ?", contact_id, user_id)
    list_id = contacts[0]["list_id"]
    if not contacts:
        return redirect("/error")

    return render_template("contact-detail.html", contacts=contacts, links=links, list_id=list_id, contact_id=contact_id)

def contact_edit(contact_id):
    user_id = session["user_id"]
    contacts = db.execute("SELECT * FROM contacts WHERE id = ? AND user_id = ?", contact_id, user_id)
    links = db.execute("SELECT * FROM user_links WHERE contact_id = ? AND user_id = ?", contact_id, user_id)
    if not contacts:
        return redirect("/error")

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        number = request.form.get("number")
        note = request.form.get("note")
        db.execute(
            "UPDATE contacts SET first_name = ?, last_name = ?, email = ?, phone_number = ?, note = ? WHERE id = ?",
            firstname,
            lastname,
            email,
            number,
            note,
            contact_id
        )
        for key, value in request.form.items():
            if key.startswith("url"):
                link_id = request.form.get("link_id" + key[3:])
                link_url = value
                parsed_url = urlsplit(link_url)
                link_type = parsed_url.netloc
                if link_id:
                    db.execute("UPDATE user_links SET link_type = ?, link_url = ? WHERE id = ?", link_type, link_url, link_id)
                else:
                    db.execute("INSERT INTO user_links (user_id, contact_id, link_type, link_url) VALUES (?, ?, ?, ?)", user_id, contact_id, link_type, link_url)

        return redirect(f"/contact-list/contact-detail/{contact_id}")
    else:
        return render_template("contact-edit.html", contact=contacts[0], contact_id=contact_id, links=links)

def delete_contact(contact_id):
    list_id = db.execute("SELECT list_id FROM contacts WHERE id = ?", contact_id)
    if list_id:
        list_id = list_id[0]["list_id"]
        db.execute("DELETE FROM user_links WHERE contact_id = ?", contact_id)
        db.execute("DELETE FROM contacts WHERE id = ?", contact_id)
        return redirect(f"/contact-list/{list_id}")
    else:
        return redirect("/error")