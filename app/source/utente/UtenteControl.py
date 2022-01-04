from flask import request, render_template
import hashlib
from flask_login import login_user, current_user, logout_user
from app import app, db
from app.models import User


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    token = request.form.get('token')
    username = request.form.get('username')
    nome = request.form.get('nome')
    cognome = request.form.get('cognome')
    utente = User(email=email, password=hashed_password, token=token, username=username, nome=nome, cognome=cognome)
    db.session.add(utente)
    db.session.commit()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    attempted_user: User = User.query.filter_by(email=email).first()
    if attempted_user.password == hashed_password:
        login_user(attempted_user)
    return render_template('index.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return render_template('index.html')
