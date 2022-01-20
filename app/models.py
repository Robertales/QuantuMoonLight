from sqlalchemy import ForeignKey

from app import db
from app.source.utente.UserAuth import UserAuth


class User(db.Model, UserAuth):
    email = db.Column(db.VARCHAR(255), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String(128), nullable=False, unique=True)
    isAdmin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(30), nullable=False, unique=False)
    surname = db.Column(db.String(30), nullable=False, unique=False)
    newsletter = db.Column(db.Boolean, default=False)
    isResearcher = db.Column(db.Boolean, default=False)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    name = db.Column(db.String(30), nullable=False)
    path = db.Column(db.String(150), nullable=True)
    upload_date = db.Column(db.DateTime, nullable=False)
    simple_split = db.Column(db.Boolean, nullable=True)
    k_fold = db.Column(db.Boolean, nullable=True)
    ps = db.Column(db.Boolean, nullable=True)
    fe = db.Column(db.Boolean, nullable=True)
    doQSVM = db.Column(db.Boolean, nullable=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    title = db.Column(db.Text(length=200), nullable=False)
    body = db.Column(db.Text(length=1200), nullable=False)
    category = db.Column(db.String(20), nullable=True)
    data = db.Column(db.DateTime, nullable=False)


class Comment(db.Model):
    __table_args__ = (db.PrimaryKeyConstraint("email_user", "id_article"),)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    id_article = db.Column(db.Integer, ForeignKey("article.id"))
    body = db.Column(db.Text(length=250), nullable=False)
    data = db.Column(db.Date, nullable=False)


class Like(db.Model):
    __table_args__ = (db.PrimaryKeyConstraint("email_user", "id_article"),)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    id_article = db.Column(db.Integer, ForeignKey("article.id"))


def __repr__(self):
    return f"Item{self.name}"
