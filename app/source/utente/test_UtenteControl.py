import hashlib
from unittest import TestCase
from sqlalchemy_utils import database_exists, create_database
from app import app, db
from flask_login import current_user
from app.models import User


class Test(TestCase):

    def setUp(self):
        super().setUp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/test_db'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        with app.app_context():
            db.create_all()

    def test_signup(self):
        """
test the sign-up functionality of the website, creating a dummy  account and verifying it was correctly registered as a user
        """
        tester = app.test_client(self)
        with app.app_context():
            db.create_all()
        response = tester.post(
            '/signup',
            data=dict(email="mariorossi12@gmail.com", password="prosopagnosia", username="Antonio de Curtis ",
                      nome="Antonio", cognome="De Curtis"))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(User.query.filter_by(email='mariorossi12@gmail.com').first())
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all();


class Test_Login_Logout(TestCase):
    def setUp(self):
        super().setUp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/test_db'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        with app.app_context():
            db.create_all()
            password = 'quercia'
            password = hashlib.sha512(password.encode()).hexdigest()
            utente = User(email="boscoverde27@gmail.com", password=password, username="Antonio de Curtis",
                          name="Antonio", surname="De Curtis")
            db.session.add(utente)
            db.session.commit()

    def test_login_logout(self):
        """
test the login functionality of the website,by trying to log in a predetermined and existing user account and then logging out
        """
        tester = app.test_client(self)
        self.assertFalse(current_user)
        with tester:

            response = tester.post(
                '/login',
                data=dict(email="boscoverde27@gmail.com", password='quercia'))
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            assert isinstance(current_user, User)
            self.assertTrue(current_user.is_authenticated)
            response = tester.post('/logout')
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertFalse(current_user.is_authenticated)

    def tearDown(self):
        with app.app_context():
            db.drop_all()
