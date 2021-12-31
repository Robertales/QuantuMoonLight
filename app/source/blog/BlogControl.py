from app import app


@app.route('/blog/', methods=['GET', 'POST'])
def Blog():
    return "sei in blog";