import os
import urllib.request
from os.path import exists

from app import app
from flask import request, send_file, send_from_directory

cartella_download = os.pardir + "\\uploads\\"


@app.route('/download')
def download():
    filename = request.form.get('filename')

    if filename:
        filepath = '/uploads/' + filename
        return send_from_directory(filepath, filename="Classification_results.csv",
                                   as_attachment=True)


