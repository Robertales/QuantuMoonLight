from app import app


@app.route('/utente/', methods=['GET', 'POST'])
def utente():
    return "sei in utente";