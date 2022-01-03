import os

from flask import request
import hashlib, uuid
from app import app, db
from app.models import Utente
import secrets



@app.route('/signup', methods=['GET', 'POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    token = request.form.get('token')
    username = request.form.get('username')
    nome = request.form.get('nome')
    cognome = request.form.get('cognome')
    utente = Utente(email=email, password=hashed_password, token=token,username=username,nome=nome,cognome=cognome)
    db.session.add(utente)
    db.session.commit()
    return "sei in utente";
