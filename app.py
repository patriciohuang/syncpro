from flask import Flask, render_template
from flask_session import Session

from helpers import login_required
from auth import login, logout, register
from contact import contact_list, add_contact, delete_contact, edit_contact
from list import index, add_list, delete_list, edit_list
from profiles import profile_detail, edit_profile, add_profile, delete_profile, profile_lists

# Configure application
app = Flask(__name__, static_folder="static")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# HOME
"LISTS"
@app.route("/")
@login_required
def index_route():
    return index()

"ADD LISTS"
@app.route("/add-list", methods=["GET", "POST"])
@login_required
def add_list_route():
    return add_list()

"EDIT LISTS"
@app.route("/edit-list/<int:list_id>", methods=["GET", "POST"])
@login_required
def edit_list_route(list_id):
    return edit_list(list_id)

"DELETE LIST"
@app.route("/delete-list/<int:list_id>")
@login_required
def delete_list_route(list_id):
    return delete_list(list_id)


# PROFILE
"PROFILE LISTS"
@app.route("/profile-lists")
@login_required
def profile_lists_route():
    return profile_lists()

"PROFILE DETAIL"
@app.route("/profile-detail/<int:profile_id>")
def profile_detail_route(profile_id):
    return profile_detail(profile_id)

"EDIT PROFILE"
@app.route("/profile-detail/edit-profile/<int:profile_id>", methods=["GET", "POST"])
@login_required
def edit_profile_route(profile_id):
    return edit_profile(profile_id)

"ADD PROFILE"
@app.route("/add-profile", methods=["GET", "POST"])
@login_required
def add_profile_route():
    return add_profile()

"DELETE PROFILE"
@app.route("/delete-profile/<int:profile_id>")
@login_required
def delete_profile_route(profile_id):
    return delete_profile(profile_id)

# CONTACT LIST
"CONTACTS LISTS"
@app.route("/contact-list/<int:list_id>", methods=["GET", "POST"])
@login_required
def contact_list_route(list_id):
    return contact_list(list_id)

"ADD CONTACT"
@app.route("/add-contact/<int:profile_id>", methods=["GET", "POST"])
@login_required
def add_contact_route(profile_id):
    return add_contact(profile_id)

"EDIT CONTACT"
@app.route("/profile-detail/edit-contact/<int:profile_id>", methods=["GET", "POST"])
@login_required
def contact_edit_route(profile_id):
    return edit_contact(profile_id)

"DELETE CONTACT"
@app.route("/delete-contact/<int:profile_id>")
@login_required
def delete_contact_route(profile_id):
    return delete_contact(profile_id)

# "CONTACT DETAIL"
# @app.route("/contact-list/contact-detail/<int:contact_id>")
# @login_required
# def contact_detail_route(contact_id):
#     return contact_detail(contact_id)

# "CONTACT EDIT"
# @app.route("/contact-list/contact-detail/contact-edit/<int:contact_id>", methods=["GET", "POST"])
# @login_required
# def contact_edit_route(contact_id):
#     return contact_edit(contact_id)


# "CONTACT DELETE"
# @app.route("/delete-contact/<int:contact_id>")
# @login_required
# def delete_contact_route(contact_id):
#     return delete_contact(contact_id)

# AUTH
"LOGIN"
@app.route("/login", methods=["GET", "POST"])
def login_route():
    return login()

"LOGOUT"
@app.route("/logout")
def logout_route():
    return logout()

"REGISTER"
@app.route("/register", methods=["GET", "POST"])
def register_route():
    return register()

@app.route("/error")
def error():
    return render_template("error.html")
