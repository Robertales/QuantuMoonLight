from app import app


@app.route('/Blog/', methods=['GET', 'POST'])
def Blog():
    return "sei in Blog";