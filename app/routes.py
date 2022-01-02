import os
import pathlib
from pathlib import Path
from app import models
from flask import render_template, request
import subprocess as sp
from app import app, db
from app.models import Files
from app.source.utils import getlog as log


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


