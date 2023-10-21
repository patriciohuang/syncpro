from cs50 import SQL
from flask import redirect, session, request
from functools import wraps
import requests
from bs4 import BeautifulSoup

db = SQL("sqlite:///syncpro.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            url_path = request.path
            login_url = f"/login?redirect={url_path}"
            register_url = f"/register?redirect={url_path}"
            if login_url:
                return redirect(login_url)
            if register_url:
                return redirect(register_url)
        return f(*args, **kwargs)
    return decorated_function

def get_favicon_url(user_url):
    try:
        response = requests.get(user_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_link = soup.find("link", rel="icon")
        if favicon_link:
            favicon_url = favicon_link.get("href")
            if not favicon_url.startswith("http"):
                # Relative URL, so convert it to an absolute URL
                url_parts = user_url.split("/")
                base_url = url_parts[0] + "//" + url_parts[2]
                favicon_url = base_url + "/" + favicon_url.lstrip("/")
            return favicon_url
        return None  # No favicon found
    except (requests.exceptions.RequestException, Exception):
        return None
