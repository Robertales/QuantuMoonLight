import os
from flask import render_template, request
import subprocess as sp
from app import app, db


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
    ROOT_DIR = os.path.abspath(os.curdir)
    sp.run("python "+ROOT_DIR+"\\app\\source\\utils\\getlog.py" )
    file = request.files.get('userfile')
    ext_ok = ['txt', 'csv', 'data']
    temp = file.filename
    extension = temp.split('.')[-1]
    print(extension)
    if not ext_ok.__contains__(extension):
        return 'Il file ha un estensione non ammessa!'

    if file is None:
        return 'No Train set uploaded'

    uploaddir = ROOT_DIR + '\\uploads\\'
    userfile_name = file.filename
    userpath = uploaddir + userfile_name

    if file.content_length > 80000000:
        return 'Il file è troppo grande!'
    ps = request.args.get('reduce1')
    fe = request.args.get('reduce')

    file.save(userpath)

    if (fe == 'reduceFeatureExtraction') and (ps == 'reduceProtypeSelection'):
        sql = 'INSERT INTO files (paths,ps,fe) VALUES (\'%s\',TRUE,TRUE)' % userpath
    elif (fe != 'reduceFeatureExtraction') and (ps == 'reduceProtypeSelection'):
        sql = 'INSERT INTO files (paths,ps,fe) VALUES (\'%s\',FALSE,TRUE)' % userpath
    elif (fe == 'reduceFeatureExtraction') and (ps != 'reduceProtypeSelection'):
        sql = 'INSERT INTO files (paths,ps,fe) VALUES (\'%s\',TRUE,FALSE)' % userpath
    elif (fe != 'reduceFeatureExtraction') and (ps != 'reduceProtypeSelection'):
        sql = 'INSERT INTO files (paths,ps,fe) VALUES (\'%s\',FALSE,FALSE)' % userpath

    result = db.engine.execute(sql)

    if result:
        return ("<br><p>Connection with database: Done!</p>")

    else:
        return ("<br>ATTENZIONE! Inserimento non eseguito")

#Effettua il caricamento dei file, va colelgato al modulo che esegue effettivamente la ps
