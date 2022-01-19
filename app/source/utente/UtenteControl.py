from pathlib import Path

from flask import request, render_template, flash
import hashlib
from flask_login import login_user, current_user, logout_user
from app import app, db
from app.models import User
import re


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Reads the user credentials from a http request and adds him to the project database
        :return: redirect to index page
    """
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    token = request.form.get("token")
    if token.__eq__(""):
        token = None
    username = request.form.get("username")
    Name = request.form.get("nome")
    cognome = request.form.get("cognome")
    if 0 < username.__len__() < 30 and re.fullmatch('^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,10}$',email) \
            and password.__len__() >= 8 and re.fullmatch('^[A-zÀ-ù ‘-]{0,30}$' ,Name)\
            and re.fullmatch('^[A-zÀ-ù ‘-]{0,30}$',cognome):
        utente = User(
            email=email,
            password=hashed_password,
            token=token,
            username=username,
            name=Name,
            surname=cognome,
        )
        db.session.add(utente)
        db.session.commit()
        path = Path(__file__).parents[3] / "upload_dataset" / email
        print(path.__str__())
        if not path.is_dir():
            path.mkdir()
        login_user(utente)
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    reads a user login credentials from a http request and if they are valid logs the user in with those same
    credentials,changing his state from anonymous  user to logged user
    :return: redirect to index page
    """
    email = request.form.get("email")
    password = request.form.get("password")
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    attempted_user: User = User.query.filter_by(email=email).first()
    if not attempted_user:
        print(attempted_user.__class__)
        flash("Utente non registrato")
        return render_template("login.html")

    if attempted_user.password == hashed_password:
        login_user(attempted_user)
    else:
        flash("password errata")
        return render_template("login.html")
    return render_template("index.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
    logs a user out, changing his state from logged user to anonymous user
        :return:redirect to index page
    """
    logout_user()
    return render_template("index.html")


@app.route("/newsletter", methods=["GET", "POST"])
def signup_newsletter():
    """
    changes the User ,whose email was passed as a http request parameter ,newsletter flag to true
        :return: redirect to index page
    """
    email = request.form.get("email")
    utente: User = User.query.filter_by(email=email).first()
    utente.newsletter = True
    db.session.commit()

    return render_template("index.html")
