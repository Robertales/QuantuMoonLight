from app import app, db
from app.models import User, Article
from flask import request, render_template

@app.route('/gestione/', methods=['GET', 'POST'])
def getList():
    email = request.form.get('email')
    fristData = request.form.get('fristData')
    secondData = request.form.get('secondData')

    scelta = request.form.get("scelta")
    if scelta=="listUser":
        listUser = getListaUser()
    if scelta == "listArticlesData":
        listArticleData = getListaArticlesData(fristData,secondData)
    if scelta=="listArticlesUser":
        listArticleUser= getListaArticlesUser(email)
    return "sei in gestione";

@app.route('/removeUser/', methods=['GET', 'POST'])
def removeUser():
    email = request.form.get('email')
    print(email)

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
    listArticles = Article.query.filter(Article.data.between(data1,data2).all())
    return listArticles

def getListaArticlesUser(email):
    list = Article.query.filter_by(Article.email_user == email).all()
    return list
