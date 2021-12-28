from app import app


@app.route('/Utente/', methods=['GET', 'POST'])
def utente():
    return "sei in Utente";