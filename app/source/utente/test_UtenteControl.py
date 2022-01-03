from unittest import TestCase
from sqlalchemy_utils import database_exists, create_database
from app import app, db
from flask_login import current_user
from app.models import Utente


class Test(TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/test_db'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Create database if it does not exist.
        from app import models
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            with app.app_context():
                db.create_all()

    def test_signup(self):
        tester = app.test_client(self)
        with app.app_context():
            db.drop_all()
            db.create_all()

        data = dict(email="mariorossi12@gmail.com", password="prosopagnosia", username="Antonio de Curtis ",
                    nome="Antonio", cognome="De Curtis")
        response = tester.post(
            '/signup',
            data=dict(email="mariorossi12@gmail.com", password="prosopagnosia", username="Antonio de Curtis ",
                      nome="Antonio", cognome="De Curtis"))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_login(self):
            tester = app.test_client(self)
            self.assertFalse(current_user)
            with tester:
                response = tester.post(
                    '/login',
                    data=dict(email="mariorossi12@gmail.com", password="prosopagnosia"))
                statuscode = response.status_code
                print(current_user)
                self.assertEqual(statuscode, 200)
                assert isinstance(current_user, Utente)
                self.assertTrue(current_user.is_authenticated)


