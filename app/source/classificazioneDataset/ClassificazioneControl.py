from app import app


@app.route('/Classificazione/', methods=['GET', 'POST'])
def valida():
    return "sei in Classificazione";