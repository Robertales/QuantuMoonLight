import hashlib
from unittest import TestCase

from flask_login import current_user, UserMixin, AnonymousUserMixin
from sqlalchemy_utils import database_exists, create_database

from src import app, db
from src.source.model.models import User


class Test_signup(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()

    def test_signup(self):
        """
        test the sign-up functionality of the website, creating a dummy  account and verifying it was correctly
        registered as a user
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis ",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            User.query.filter_by(email="mariorossi12@gmail.com").first()
        )
        db.session.commit()

    def test_signupEmptyToken(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty token and verifying it
        was correctly registered as a user and the token was correctly parsed to Null
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis ",
                token="",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertTrue(user)
        self.assertIsNone(user.token)
        db.session.commit()

    def test_signupInvalidUsername(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty username and verifying
        it wasn't correctly registered as a user
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def test_signupInvalidEmail(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty email and verifying it
        wasn't correctly registered as a user.
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                password="prosopagnosia",
                username="Antonio de Curtis ",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()


class Test_Login_Logout(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            password = "quercia"
            password = hashlib.sha512(password.encode()).hexdigest()
            utente = User(
                email="boscoverde27@gmail.com",
                password=password,
                username="Antonio de Curtis",
                name="Antonio",
                surname="De Curtis",
            )
            db.session.add(utente)
            db.session.commit()

    def test_LoginLogout(self):
        """
        test the login functionality of the website,by trying to log in a predetermined and existing user account and
        then logging out
        """
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            response = tester.post(
                "/login",
                data=dict(email="boscoverde27@gmail.com", password="quercia"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            assert isinstance(current_user, User)
            self.assertTrue(current_user.is_authenticated)
            response = tester.post("/logout")
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertFalse(current_user.is_authenticated)

    def test_loginUnregistered(self):
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            response = tester.post(
                "/login",
                data=dict(
                    email="emailsbagliata1234d@gmail.com",
                    password="quercia",
                ),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertNotIsInstance(current_user, UserMixin)
            self.assertIsInstance(current_user, AnonymousUserMixin)
            self.assertFalse(current_user.is_authenticated)

    def test_loginWrongPassword(self):
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            response = tester.post(
                "/login",
                data=dict(
                    email="boscoverde27@gmail.com",
                    password="passwordsbagliata",
                ),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertNotIsInstance(current_user, UserMixin)
            self.assertIsInstance(current_user, AnonymousUserMixin)
            self.assertFalse(current_user.is_authenticated)

    def test_Newsletter(self):
        tester = app.test_client()
        with tester:
            tester.post(
                "/login",
                data=dict(email="boscoverde27@gmail.com", password="quercia"),
            )
            assert isinstance(current_user, User)
            self.assertFalse(current_user.newsletter)
            response = tester.post(
                "/newsletter",
                data=dict(email="boscoverde27@gmail.com"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertTrue(current_user.newsletter)

    def tearDown(self):
        with app.app_context():
            db.drop_all()
