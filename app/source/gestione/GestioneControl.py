from app import app


@app.route('/gestione/', methods=['GET', 'POST'])
def valida():
    return "sei in gestione";