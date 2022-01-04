from unittest import TestCase
from sqlalchemy_utils import database_exists, create_database
from app import app, db
from app.models import User, Article


class TestUser(TestCase):

    def setUp(self):
        super().setUp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/test_db'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        with app.app_context():
            db.create_all()
            user = User(email="mariorossi12@gmail.com", password="prosopagnosia", username="Antonio de Curtis ",
                      name="Antonio", surname="De Curtis")
            db.session.add(user)
            db.session.commit()

    def test_removeUser(self):
        tester = app.test_client(self)
        with app.app_context():
            db.create_all()
            self.assertTrue(User.query.filter_by(email='mariorossi12@gmail.com').first())
            response = tester.post(
                '/removeUser/',
                data=dict(email="mariorossi12@gmail.com"))
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertFalse(User.query.filter_by(email="mariorossi12@gmail.com").first())
            db.session.commit()


    def test_modifyUser(self):
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        self.assertTrue(User.query.filter_by(email='mariorossi12@gmail.com').first())
        response = tester.post(
            '/ModifyUser/',
            data=dict(email="mariorossi12@gmail.com", password="newPassword", username="newUsername ",
                      nome="newName", cognome="newSurname"))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(User.query.filter_by(email='mariorossi12@gmail.com', username='newUsername').first())
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all();

class TestList(TestCase):
    def setUp(self):
        super().setUp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/test_db'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        with app.app_context():
            db.create_all()
            user = User(email="mariorossi12@gmail.com", password="prosopagnosia", username="Antonio de Curtis ",
                        name="Antonio", surname="De Curtis")
            art1 = Article(email_user="mariorossi12@gmail.com", title="BuonNatale", body="primobody", category="all", data='2021-12-25')
            art2 = Article(email_user="mariorossi12@gmail.com", title="BuonCapodanno", body="secondoBody", category="all", data='2022-01-01')
            db.session.add(user)
            db.session.add(art1)
            db.session.add(art2)
            db.session.commit()

    def test_listUser(self): #TO DO
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        self.assertTrue(User.query.filter_by(email='mariorossi12@gmail.com').first())
        self.assertTrue(Article.query.filter_by(id='0').first())
        self.assertTrue(Article.query.filter_by(id='1').first())
        response = tester.post(
            '/gestione/',
            data=dict(scelta="listUser", email="mariorossi12@gmail.com"))
        #TODO

    def test_listArticlesData(self): #TODO

    def test_listArticlesUser(self): #TODO

    def tearDown(self):
        with app.app_context():
            db.drop_all();