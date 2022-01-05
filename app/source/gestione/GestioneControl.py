from app import app, db
from app.models import User, Article
from flask import request, render_template

@app.route('/gestione/', methods=['GET', 'POST'])
def getList():
    scelta = request.form.get("scelta")
    if scelta=="listUser":
        email = request.form.get('email')
        listUser = getListaUser()
    if scelta == "listArticlesData":
        fristData = request.form.get('fristData')
        secondData = request.form.get('secondData')
        listArticleData = getListaArticlesData(fristData,secondData)
    if scelta=="listArticlesUser":
        email = request.form.get('email')
        listArticleUser= getListaArticlesUser(email)

    return "sei in gestione";

@app.route('/removeUser/', methods=['GET', 'POST'])
def removeUser():
    email = request.form.get('email')

    user = User.query.get(email)
    db.session.delete(user)
    db.session.commit()
    return render_template('index.html')

@app.route('/ModifyUser/', methods=['GET', 'POST'])
def modifyUserProfile():
    email = request.form.get('email')
    user = User.query.get(email)

    newPassword = (request.form.get('password'))
    newToken = request.form.get('token')
    newUsername = request.form.get('username')
    newNome = request.form.get('nome')
    newCognome = request.form.get('cognome')

    setattr(user, 'token', newToken)
    setattr(user, 'password', newPassword)
    setattr(user, 'username', newUsername)
    setattr(user, 'nome', newNome)
    setattr(user, 'cognome', newCognome)
    db.session.commit()
    return render_template('index.html')

def getListaUser():
    return User.query.all()

def getListaArticlesData(data1, data2):
    return Article.query.filter(Article.data.between(data1,data2))

def getListaArticlesUser(email):
    return Article.query.filter_by(email_user = email).all()
