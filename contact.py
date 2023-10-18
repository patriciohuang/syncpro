from cs50 import SQL
from flask import render_template, request, redirect, session
from urllib.parse import urlsplit

db = SQL("sqlite:///syncpro.db")


from flask import request, redirect, session, url_for

# ... your other imports and code ...

def add_contact(profile_id):
    user_id = session["id"]
    if request.method == "POST":
        selected_list = request.form.get("selected_list")
        exist_contact = db.execute("SELECT * FROM lists JOIN lists_profiles ON lists.id = lists_profiles.list_id WHERE lists.id = ? AND lists_profiles.profile_id = ?", selected_list, profile_id)
        if exist_contact:
            return redirect('/')
        else:
            db.execute("INSERT INTO lists_profiles (list_id, profile_id) VALUES (?, ?)", selected_list, profile_id)
            return redirect('/')
    else:
        lists = db.execute("SELECT * FROM lists WHERE user_id = ?", user_id)
        if not lists:
            db.execute("INSERT INTO lists (user_id, list_name) VALUES (?, ?)", user_id, 'My contacts')
            lists = db.execute("SELECT * FROM lists WHERE user_id = ?", user_id)
        return render_template("add-contact.html", lists=lists, profile_id=profile_id)


### DONE
def contact_list(list_id):
    list_id = int(list_id)
    profiles = db.execute("SELECT * FROM profiles JOIN lists_profiles AS lp ON lp.profile_id = profiles.id JOIN lists ON lp.list_id = lists.id WHERE lists.id = ?", list_id)
    lists = db.execute("SELECT * FROM lists WHERE id = ?", list_id)
    list_name = lists[0]["list_name"]
    return render_template("contact-list.html", list_id=list_id, profiles=profiles, list_name=list_name)


# def contact_detail(contact_id):
#     user_id = session["user_id"]
#     contacts = db.execute("SELECT * FROM contacts WHERE id = ? AND user_id = ?", contact_id, user_id)
#     links = db.execute("SELECT * FROM user_links WHERE contact_id = ? AND user_id = ?", contact_id, user_id)
#     list_id = contacts[0]["list_id"]
#     if not contacts:
#         return redirect("/error")

#     return render_template("contact-detail.html", contacts=contacts, links=links, list_id=list_id, contact_id=contact_id)

# def contact_edit(contact_id):
#     user_id = session["user_id"]
#     contacts = db.execute("SELECT * FROM contacts WHERE id = ? AND user_id = ?", contact_id, user_id)
#     links = db.execute("SELECT * FROM user_links WHERE contact_id = ? AND user_id = ?", contact_id, user_id)
#     if not contacts:
#         return redirect("/error")

#     if request.method == "POST":
#         firstname = request.form.get("firstname")
#         lastname = request.form.get("lastname")
#         email = request.form.get("email")
#         number = request.form.get("number")
#         note = request.form.get("note")
#         db.execute(
#             "UPDATE contacts SET first_name = ?, last_name = ?, email = ?, phone_number = ?, note = ? WHERE id = ?",
#             firstname,
#             lastname,
#             email,
#             number,
#             note,
#             contact_id
#         )
#         for key, value in request.form.items():
#             if key.startswith("url"):
#                 link_id = request.form.get("link_id" + key[3:])
#                 link_url = value
#                 parsed_url = urlsplit(link_url)
#                 link_type = parsed_url.netloc
#                 if link_id:
#                     db.execute("UPDATE user_links SET link_type = ?, link_url = ? WHERE id = ?", link_type, link_url, link_id)
#                 else:
#                     db.execute("INSERT INTO user_links (user_id, contact_id, link_type, link_url) VALUES (?, ?, ?, ?)", user_id, contact_id, link_type, link_url)

#         return redirect(f"/contact-list/contact-detail/{contact_id}")
#     else:
#         return render_template("contact-edit.html", contact=contacts[0], contact_id=contact_id, links=links)

# def delete_contact(contact_id):
#     list_id = db.execute("SELECT list_id FROM contacts WHERE id = ?", contact_id)
#     if list_id:
#         list_id = list_id[0]["list_id"]
#         db.execute("DELETE FROM user_links WHERE contact_id = ?", contact_id)
#         db.execute("DELETE FROM contacts WHERE id = ?", contact_id)
#         return redirect(f"/contact-list/{list_id}")
#     else:
#         return redirect("/error")