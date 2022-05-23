import hashlib
import itertools
import re
from os.path import exists
from pathlib import Path
from zipfile import ZipFile

from flask import request, render_template, flash, send_from_directory
from flask_login import login_user, logout_user, current_user

from app import app, db
from app.source.model.models import User


class UtenteControl:
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        """
                Reads the user credentials from a http request and adds him to the project database
                    :return: redirect to index page
                """
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("confirmPassword")
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        token = request.form.get("token")
        print(token)
        isResearcher = request.form.get("isResearcher")
        if token == "":
            token = None
        username = request.form.get("username")
        utente = User.query.filter_by(username=username).first()
        if utente:
            flash("Username is invalid or already taken", "error")
            return render_template("registration.html")
        Name = request.form.get("nome")
        cognome = request.form.get("cognome")
        if not 0 < username.__len__() < 30:
            flash(
                "Invalid username (length mus be between 1 and 30 characters)",
                "error")
            return render_template("registration.html")
        if not re.fullmatch(
                '^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,10}$',
                email):
            flash("Invalid email", "error")
            return render_template("registration.html")
        if not password.__len__() >= 8:
            flash("Password length has to be at least 8 characters", "error")
            return render_template("registration.html")
        if not password.__eq__(cpassword):
            flash("Password and confirm password do not match", "error")
            return render_template("registration.html")
        if not re.fullmatch('^[A-zÀ-ù ‘-]{2,30}$', Name):
            flash("Invalid name, ,name must contain only alphabetical characters", "error")
            return render_template("registration.html")
        if not re.fullmatch('^[A-zÀ-ù ‘-]{2,30}$', cognome):
            flash("Invalid surname, ,surname must contain only alphabetical characters", "error")
            return render_template("registration.html")
        if not ((token is None) or token.__len__() == 128):
            flash("Invalid ibmq token", "error")
            return render_template("registration.html")

        utente=User.query.filter_by(email=email).first()
        if utente:
            flash("Email is invalid or already taken","error")
            return render_template("registration.html")

        utente = User(
            email=email,
            password=hashed_password,
            token=token,
            username=username,
            name=Name,
            surname=cognome,
            isResearcher=bool(isResearcher)
        )

        db.session.add(utente)
        db.session.commit()

        path = Path(__file__).parents[3] / "upload_dataset" / email
        print(path.__str__())
        if not path.is_dir():
            path.mkdir()
        login_user(utente)
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """
        reads a user login credentials from a http request and if they are valid logs the user in with those same
        credentials,changing his state from anonymous  user to logged user
        :return: redirect to index page
        """
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        attempted_user: User = User.query.filter_by(email=email).first()
        if not attempted_user:
            print(attempted_user.__class__)
            flash("Utente non registrato", "error")
            return render_template("login.html")

        if attempted_user.password == hashed_password:
            login_user(attempted_user)
        else:
            flash("password errata", "error")
            return render_template("login.html")
        return render_template("index.html")

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        """
        logs a user out, changing his state from logged user to anonymous user
            :return:redirect to index page
        """
        logout_user()
        return render_template("index.html")

    @app.route("/newsletter", methods=["GET", "POST"])
    def signup_newsletter():
        """
        changes the User ,whose email was passed as a http request parameter ,newsletter flag to true
            :return: redirect to index page
        """
        email = request.form.get("email")
        if re.fullmatch('^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,10}$', email):
            utente: User = User.query.filter_by(email=email).first()
            utente.newsletter = True
            db.session.commit()
            flash("Subscribed", "notifica")
            return render_template("index.html")
        else:
            flash("Invalid email format", "notifica")
            return render_template("index.html")

    @app.route("/download", methods=["GET", "POST"])
    def download():
        ID = request.form.get("id")
        filename = request.form.get("filename")
        filepath = Path(__file__).parents[3] / \
                   "upload_dataset" / current_user.email / ID
        print(filename)

        if filename:
            # Quando l'applicazione sarà hostata su un web server sostituire
            # con un metodo di download fornito dal web server
            zip_name = ''
            if (filename == "Validation"):
                zip_path = filepath / 'ValidationResult.zip'
                zip_name = 'ValidationResult.zip'
                zip = ZipFile(zip_path, 'w')
                if exists(
                        filepath /
                        "Data_training.csv") and exists(
                    filepath /
                    "Data_testing.csv"):
                    zip.write(
                        filepath / "Data_training.csv",
                        "data_training.csv")
                    zip.write(
                        filepath / 'Data_testing.csv',
                        "data_testing.csv")

                for count in itertools.count(start=1):
                    str_test = "testing_fold_" + count.__str__() + ".csv"
                    str_train = "training_fold_" + count.__str__() + ".csv"
                    if exists(filepath / str_test):
                        zip.write(filepath / str_test,
                                  str_test)
                        zip.write(filepath / str_train,
                                  str_train)
                    else:
                        break
                zip.close()
            else:
                zip_path = filepath / 'PreprocessingResult.zip'
                zip_name = 'PreprocessingResult.zip'
                zip = ZipFile(zip_path, 'w')
                if exists(
                        filepath /
                        "DataSetTestPreprocessato.csv") and exists(
                    filepath /
                    "DataSetTrainPreprocessato.csv"):
                    zip.write(
                        filepath / 'DataSetTestPreprocessato.csv',
                        'DataSetTestPreprocessato.csv')
                    zip.write(
                        filepath / 'DataSetTrainPreprocessato.csv',
                        'DataSetTrainPreprocessato.csv')
                if exists(filepath / "doPredictionFE.csv"):
                    zip.write(
                        filepath / 'doPredictionFE.csv',
                        'doPredictionFE.csv')
                if exists(filepath / "reducedTrainingPS.csv"):
                    zip.write(
                        filepath / 'reducedTrainingPS.csv',
                        'reducedTrainingPS.csv')
                if exists(
                        filepath /
                        "Test_Feature_Extraction.csv") and exists(
                    filepath /
                    "Train_Feature_Extraction.csv"):
                    zip.write(
                        filepath / 'Test_Feature_Extraction.csv',
                        'Test_Feature_Extraction.csv')
                    zip.write(
                        filepath / 'Train_Feature_Extraction.csv',
                        'Train_Feature_Extraction.csv')
                if exists(filepath / "Train_Feature_Selection.csv"):
                    zip.write(filepath / "Train_Feature_Selection.csv", "Train_Feature_Selection.csv")
                if exists(filepath / "Test_Feature_Selection.csv"):
                    zip.write(filepath / "Test_Feature_Selection.csv", "Test_Feature_Selection.csv")

                if exists(filepath / "TrainImputation.csv"):
                    zip.write(filepath / "TrainImputation.csv", "TrainImputation.csv")
                if exists(filepath / "TestImputation.csv"):
                    zip.write(filepath / "TestImputation.csv", "TestImputation.csv")
                if exists(filepath / "PredictImputation.csv"):
                    zip.write(filepath / "PredictImputation.csv", "PredictImputation.csv")
                if exists(filepath / "TrainScaled.csv"):
                    zip.write(filepath / "TrainScaled.csv", "TrainScaled.csv")
                if exists(filepath / "TestScaled.csv"):
                    zip.write(filepath / "TestScaled.csv", "TestScaled.csv")
                if exists(filepath / "PredictScaled.csv"):
                    zip.write(filepath / "PredictScaled.csv", "PredictScaled.csv")
                zip.close()

            return send_from_directory(
                directory=filepath,
                path=zip_name
            )
        else:
            flash(
                "Unable to download the file, try again",
                "error")
            return render_template("downloadPage.html")

