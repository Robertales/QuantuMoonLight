from app import app


@app.route('/Preprocessing/', methods=['GET', 'POST'])
def preprocessing():
    return "sei in Preprocessing";