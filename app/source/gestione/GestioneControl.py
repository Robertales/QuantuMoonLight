from app import app, db
from app.models import User, Article
from flask import request, render_template

@app.route('/gestione/', methods=['GET', 'POST'])
def valida():
    return "sei in gestione";

def removeUser():
    id = request.form.get('id')

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return render_template('index.html')

def modifyUserProfile():
    id = request.form.get('id')
    user = User.query.get(id)

    newEmail = request.form.get('email')
    newToken = request.form.get('token')
    newUsername = request.form.get('username')
    newNome = request.form.get('nome')
    newCognome = request.form.get('cognome')

    setattr(user, 'email', newEmail)
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
    return  Article.query.filter_by(Article.data == datetime)

def getListaArticlesUser():
    id = request.form.get("id")
    return Article.query.filter_by(Article.id_user == id)
