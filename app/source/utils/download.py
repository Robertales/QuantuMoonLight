import os

from flask import request, send_from_directory

from app import app

cartella_download = os.pardir + "\\uploads\\"


@app.route("/download")
def download():
    filename = request.form.get("filename")

    if filename:
        filepath = "/uploads/" + filename
        return send_from_directory(
            filepath,
            filename="Classification_results.csv",
            as_attachment=True,
        )
