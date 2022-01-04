from app import app, db
from app.models import User, Article
from flask import request, render_template

@app.route('/gestione/', methods=['GET', 'POST'])
def valida():
    return "sei in gestione";

def removeUser():
    email = request.form.get('email')

    user = User.query.get(email)
    db.session.delete(user)
    db.session.commit()
    return render_template('index.html')

def modifyUserProfile():
    email = request.form.get('email')
    user = User.query.get(email)

    newToken = request.form.get('token')
    newUsername = request.form.get('username')
    newNome = request.form.get('nome')
    newCognome = request.form.get('cognome')

    setattr(user, 'token', newToken)
    setattr(user, 'username', newUsername)
    setattr(user, 'nome', newNome)
    setattr(user, 'cognome', newCognome)
    db.session.commit()
    return render_template('index.html')

def getListaUser():
    return User.query.all()

def getListaArticlesData():
    datetime = request.form.get("date")
    return Article.query.filter_by(Article.data == datetime)

def getListaArticlesUser():
    email = request.form.get('email')
    return Article.query.filter_by(Article.email_user == email)
