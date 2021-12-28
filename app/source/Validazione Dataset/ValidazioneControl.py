from app import app


@app.route('/Validazione/', methods=['GET', 'POST'])
def valida():
    return "sei in Validazione";