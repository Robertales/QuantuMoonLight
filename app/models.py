from flask_login._compat import text_type

from app import db, login_manager
from flask_login import UserMixin


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(length=255), nullable=True)
    size = db.Column(db.Integer, nullable=True)
    paths = db.Column(db.String(length=500), nullable=True)
    ps = db.Column(db.Boolean, nullable=True)
    fe = db.Column(db.Boolean, nullable=True)
    autosplit = db.Column(db.Boolean, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))


class Utente(db.Model, UserMixin):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    token = db.Column(db.Text, nullable=True, unique=True)
    isAdmin = db.Column(db.Boolean, default=False)
    nome = db.Column(db.Text, nullable=False, unique=False)
    cognome = db.Column(db.Text, nullable=False, unique=False)
    newsletter = db.Column(db.Boolean, default=0)

    def get_id(self):
        try:
            return text_type(self.id_user)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


def __repr__(self):
    return f'Item{self.name}'
