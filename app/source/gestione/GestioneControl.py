from app import app, db
from app.models import User, Article
from flask import request, render_template


@app.route("/gestione/", methods=["GET", "POST"])
def getList():
    """
    The function returns a list of users or administrators requested by an admin

    :return: tbd
    """
    scelta = request.form.get("scelta")
    if scelta == "listUser":
        list = getListaUser()
    if scelta == "listArticlesData":
        first_data = request.form.get("firstData")
        second_data = request.form.get("secondData")
        list = getListaArticlesData(first_data, second_data)
    if scelta == "listArticlesUser":
        email = request.form.get("email")
        list = getListaArticlesUser(email)

    return "List of User or article"


@app.route("/removeUser/", methods=["GET", "POST"])
def removeUser():
    """
    the function allows an administrator to delete a user from the database

    :return: tbd
    """
    email = request.form.get("email")

    user = User.query.get(email)
    db.session.delete(user)
    db.session.commit()
    return render_template("index.html")


@app.route("/ModifyUser/", methods=["GET", "POST"])
def modifyUserProfile():
    """
    the function allows an administrator to modify user information

    :return: tbd
    """
    email = request.form.get("email")
    user = User.query.get(email)

    new_password = request.form.get("password")
    new_token = request.form.get("token")
    new_username = request.form.get("username")
    new_nome = request.form.get("nome")
    new_cognome = request.form.get("cognome")

    setattr(user, "token", new_token)
    setattr(user, "password", new_password)
    setattr(user, "username", new_username)
    setattr(user, "nome", new_nome)
    setattr(user, "cognome", new_cognome)
    db.session.commit()
    return render_template("index.html")


def getListaUser():
    """
    the function returns the list of registered users

    :return: user list
    :rtype: dict
    """
    return User.query.all()


def getListaArticlesData(data1, data2):
    """
    the function returns the list of Article

    :return: article list filter by date
    :rtype: dict
    """
    return Article.query.filter(Article.data.between(data1, data2))


def getListaArticlesUser(email):
    """
    the function returns the list of Article

    :return: article list filter by user
    :rtype: dict
    """
    return Article.query.filter_by(email_user=email).all()
