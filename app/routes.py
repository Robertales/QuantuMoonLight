import os
import pathlib
from pathlib import Path
from app import models
from flask import render_template, request
import subprocess as sp
from app import app, db
from app.models import Files


@app.route('/')
@app.route('/home')
def homepage():  # put application's code here
    return render_template('index.html')


@app.route('/classificazione/', methods=['GET', 'POST'])
def classifica():
    try:
        email = request.args.get('email', str)
        token = request.args.get('token', str)
        return str(email + "   " + token)
    except ValueError:
        return "invalid input"


@app.route('/upload_dataset/', methods=['GET', 'POST'])
def upload():
    print('Request send on ')
    ROOT_DIR = pathlib.Path(__file__).cwd()
    logpath = Path(ROOT_DIR / "app/source/utils/getlog.py")
    sp.run("python " + logpath.__str__())
    file = request.files.get('userfile')
    ext_ok = ['txt', 'csv', 'data']
    temp = file.filename
    extension = temp.split('.')[-1]
    print(extension)
    if not ext_ok.__contains__(extension):
        return 'Il file ha un estensione non ammessa!'

    if file is None:
        return 'No Train set uploaded'

    uploaddir = ROOT_DIR / 'uploads/'
    userfile_name = file.filename
    userpath = uploaddir / userfile_name

    if file.content_length > 80000000:
        return 'Il file è troppo grande!'
    ps = request.form.get('reduce1')
    fe = request.form.get('reduce')

    print(ps)
    print(fe)
    print(userpath)

    file.save(userpath)

    salvataggiodatabase = Files(paths=userpath,fe= bool(fe),ps= bool(ps))

    db.session.add(salvataggiodatabase)
    db.session.commit()

    if salvataggiodatabase:
        return ("<br><p>Connection with database: Done!</p>")

    else:
        return ("<br>ATTENZIONE! Inserimento non eseguito")

# Effettua il caricamento dei file, va colelgato al modulo che esegue effettivamente la ps
