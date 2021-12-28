from app import app


@app.route('/Gestione/', methods=['GET', 'POST'])
def valida():
    return "sei in Gestione";