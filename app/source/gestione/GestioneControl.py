from app import app, db
from app.models import User, Article
from flask import request, render_template


@app.route("/gestione/", methods=["GET", "POST"])
def getList():
    """
    what function do

    :return: tbd
    """
    scelta = request.form.get("scelta")
    if scelta == "listUser":
        list = getListaUser()
    if scelta == "listArticlesData":
        firstData = request.form.get("firstData")
        secondData = request.form.get("secondData")
        list = getListaArticlesData(firstData, secondData)
    if scelta == "listArticlesUser":
        email = request.form.get("email")
        list = getListaArticlesUser(email)

    return "sei in gestione"


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

    newPassword = request.form.get("password")
    newToken = request.form.get("token")
    newUsername = request.form.get("username")
    newNome = request.form.get("nome")
    newCognome = request.form.get("cognome")

    setattr(user, "token", newToken)
    setattr(user, "password", newPassword)
    setattr(user, "username", newUsername)
    setattr(user, "nome", newNome)
    setattr(user, "cognome", newCognome)
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
