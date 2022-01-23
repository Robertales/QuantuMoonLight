import datetime
from datetime import datetime
from unittest import TestCase

from sqlalchemy_utils import database_exists, create_database

from app import app, db
from app.source.model.models import User, Article


class TestUser(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            user = User(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis ",
                name="Antonio",
                surname="De Curtis",
            )
            db.session.add(user)
            db.session.commit()

    def test_removeUser(self):
        """
        test the removeUser functionality, checking first that the account exists,
        then delete it and verify that it was deleted correctly
        """
        tester = app.test_client(self)
        with app.app_context():
            db.create_all()
            self.assertTrue(
                User.query.filter_by(email="mariorossi12@gmail.com").first()
            )
            response = tester.post(
                "/removeUser/",
                data=dict(email="mariorossi12@gmail.com"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertFalse(
                User.query.filter_by(email="mariorossi12@gmail.com").first()
            )
            db.session.commit()

    def test_modifyUser(self):
        """
        test the modifyUser functionality, checking first that the account exists,
        then modify it and verify that it has been modified correctly
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        self.assertTrue(
            User.query.filter_by(email="mariorossi12@gmail.com").first()
        )
        response = tester.post(
            "/ModifyUser/",
            data=dict(
                email="mariorossi12@gmail.com",
                password="newPassword",
                username="newUsername ",
                nome="newName",
                cognome="newSurname",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            User.query.filter_by(
                email="mariorossi12@gmail.com", username="newUsername"
            ).first()
        )
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()


class TestList(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            user1 = User(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis ",
                name="Antonio",
                surname="De Curtis",
            )
            user2 = User(
                email="giuseppeverdi@gmail.com",
                password="asperger",
                username="giuVerdiProXX",
                name="Giuseppe",
                surname="Verdi",
            )
            art1 = Article(
                email_user="mariorossi12@gmail.com",
                title="BuonNatale",
                body="primobody",
                category="primaCat",
                data=datetime(2021, 12, 25),
            )
            art2 = Article(
                email_user="mariorossi12@gmail.com",
                title="BuonCapodanno",
                body="secondoBody",
                category="secondaCat",
                data=datetime(2022, 1, 1),
            )
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            db.session.add(art1)
            db.session.add(art2)
            db.session.commit()

    def test_listUser(self):
        """
        test the functionality of getting all registered users to the site
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(scelta="listUser"),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(User.query.filter_by(email="mariorossi12@gmail.com").first())
        self.assertTrue(User.query.filter_by(email="giuseppeverdi@gmail.com").first())
        db.session.commit()

    def test_listArticlesUser(self):
        """
        test the functionality of getting articles written by a user
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(
                scelta="listArticlesUser",
                email="mariorossi12@gmail.com",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            Article.query.filter_by(
                email_user="mariorossi12@gmail.com"
            ).limit(2)
        )
        db.session.commit()

    def test_listArticlesData(self):
        """
        tests the functionality of getting articles written between two dates
        """
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(
                scelta="listArticlesData",
                firstData="2021-12-20",
                secondData="2021-12-30",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            Article.query.filter(
                Article.data.between("2021-12-20", "2021-12-30")
            ).first()
        )
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()
