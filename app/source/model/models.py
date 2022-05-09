from sqlalchemy import ForeignKey, Enum

from app import db
from app.source.utente.UserAuth import UserAuth


class User(db.Model, UserAuth):
    """
    code representation of the User table of the database
    """
    email = db.Column(db.VARCHAR(255), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String(128), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(30), nullable=False, unique=False)
    surname = db.Column(db.String(30), nullable=False, unique=False)
    newsletter = db.Column(db.Boolean, default=False)
    isResearcher = db.Column(db.Boolean, default=False)

    def has_liked_post(self, post):
        return Like.query.filter(
            Like.email_user == self.email,
            Like.id_article == post.id).count() > 0


class Dataset(db.Model):
    """
    code representation of the Dataset table of the database
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    name = db.Column(db.String(30), nullable=False)
    path = db.Column(db.String(150), nullable=True)
    upload_date = db.Column(db.DateTime, nullable=False)
    simple_split = db.Column(db.Boolean, nullable=True)
    k_fold = db.Column(db.Boolean, nullable=True)
    ps = db.Column(db.Boolean, nullable=True)
    fe = db.Column(db.Boolean, nullable=True)
    model = db.Column(db.String(30), nullable=False, default="None")
    accuracy = db.Column(db.Float, nullable=True, default=-1)
    precision = db.Column(db.Float, nullable=True, default=-1)
    recall = db.Column(db.Float, nullable=True, default=-1)
    rmse = db.Column(db.Float, nullable=True, default=-1)
    mse = db.Column(db.Float, nullable=True, default=-1)
    mae = db.Column(db.Float, nullable=True, default=-1)
    training_time = db.Column(db.Integer, nullable=True, default=-1)
    total_time = db.Column(db.Integer, nullable=True, default=-1)


class Article(db.Model):
    """
       code representation of the Article table of the database
       """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    title = db.Column(db.Text(length=200), nullable=False)
    author = db.Column(db.Text(length=200), nullable=False)
    body = db.Column(db.Text(length=1200), nullable=False)
    category = db.Column(db.String(20), nullable=True)
    data = db.Column(db.DateTime, nullable=False)
    authorized = db.Column(db.Boolean, default=False)
    label = db.Column(Enum("Article", "Experiment", name="label_enum", create_type=False))
    likes = db.relationship('Like', backref='post', lazy='dynamic')




class Comment(db.Model):
    """
       code representation of the Comment table of the database
       """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    id_article = db.Column(db.Integer, ForeignKey("article.id"))
    body = db.Column(db.Text(length=250), nullable=False)
    author = db.Column(db.Text(length=200), nullable=False)
    data = db.Column(db.Date, nullable=False)
    authorized = db.Column(db.Boolean, default=False)



class Like(db.Model):
    """
       code representation of the Like table of the database
       """
    __table_args__ = (db.PrimaryKeyConstraint("email_user", "id_article"),)
    email_user = db.Column(db.VARCHAR(255), ForeignKey("user.email"))
    id_article = db.Column(db.Integer, ForeignKey("article.id"))


def __repr__(self):
    return f"Item{self.name}"
