import hashlib
import pathlib
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from flask import request, render_template

from app import app, db
from app.models import User, Article


class GestioneControl:
    @app.route("/gestione/", methods=["GET", "POST"])
    def getList():
        """
        The function returns a list of users or administrators requested by an admin

        :return: redirect to index page
        """
        
        scelta = request.form.get("scelta")
        if scelta == "listUser":
            list = GestioneControl.getListaUser()
        if scelta == "listArticlesData":
            first_data = request.form.get("firstData")
            second_data = request.form.get("secondData")
            list = GestioneControl.getListaArticlesData(first_data, second_data)
        if scelta == "listArticlesUser":
            email = request.form.get("email")
            list = GestioneControl.getListaArticlesUser(email)

        return "List of User or article"

    @app.route("/removeUser/", methods=["GET", "POST"])
    def removeUser():
        """
        the function allows an administrator to delete a user from the database

        :return: redirect to index page
        """
        email = request.form.get("email")

        user = User.query.get(email)
        db.session.delete(user)
        db.session.commit()
        return render_template("index.html")

    @app.route("/ModifyUser/", methods=["GET", "POST"])
    def modifyUserProfile():
        """
        the function allows an administrator to modify user information

        :return: tbd
        """
        email = request.form.get("email")
        user = User.query.get(email)

        new_password = request.form.get("password")
        hashed_password = hashlib.sha512(new_password.encode()).hexdigest()
        new_token = request.form.get("token")
        new_username = request.form.get("username")
        new_nome = request.form.get("nome")
        new_cognome = request.form.get("cognome")

        setattr(user, "token", new_token)
        setattr(user, "password", hashed_password)
        setattr(user, "username", new_username)
        setattr(user, "nome", new_nome)
        setattr(user, "cognome", new_cognome)
        db.session.commit()
        return render_template("adminPage.html")

    def getListaUser():
        """
        the function returns the list of registered users

        :return: user list
        :rtype: dict
        """
        return User.query.all()

    def getListaArticlesData(data1, data2):
        """
        the function returns the list of Article

        :return: article list filter by date
        :rtype: dict
        """
        return Article.query.filter(Article.data.between(data1, data2))

    def getListaArticlesUser(email):
        """
        the function returns the list of Article

        :return: article list filter by user
        :rtype: dict
        """
        return Article.query.filter_by(email_user=email).all()

    @app.route("/sendEmailNewsletter/", methods=["GET", "POST"])
    def sendEmailNewsletter():
        """
          the function allows an administrator to send an email to users registered for the newsletter

           :return: state
           :rtype: int
           """
        title = request.form.get("title")
        body = request.form.get("body")
        listautenti = User.query.filter_by(newsletter=True)
        for utente in listautenti:
            try:
                email = MIMEMultipart()
                email["From"] = "quantumoonlight@gmail.com"
                email["Date"] = formatdate(localtime=True)
                email["To"] = utente.email
                email["Subject"] = title

                email.attach(MIMEText('<tr><center><img style="width:15%;" src="cid:image"></center></tr>', 'html'))
                img_path = open(
                    pathlib.Path(__file__).parents[2] / "static" / "images" / "logos" / "Logo_SenzaScritta.png",
                    "rb")
                img = MIMEImage(img_path.read())
                img.add_header('Content-ID', '<image>')
                email.attach(img)
                email.attach(MIMEText("Hi " + utente.username + ","))
                email.attach(MIMEText('<br>', 'html'))
                email.attach(MIMEText(body))
                email.attach(MIMEText('<h6><center>You received this email because you signed up to receive '
                                      'communications from QML. This message was sent from QML, Italy.</center></h6>',
                                      'html'))
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.ehlo()
                server.login("quantumoonlight@gmail.com", "Quantum123?")
                server.send_message(email)
                server.close()
            except BaseException:
                return 0
        return render_template("adminPage.html")
