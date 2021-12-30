from app import db


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, nullable=True)
    name = db.Column(db.VARCHAR(255), nullable=True)
    size = db.Column(db.Integer, nullable=True)
    paths = db.Column(db.VARCHAR(50), nullable=True)
    ps = db.Column(db.Boolean, nullable=True)
    fe = db.Column(db.Boolean, nullable=True)
    autosplit = db.Column(db.Boolean, nullable=True)

    def __init__(self, paths, ps, fe):
        self.paths = paths
        self.ps = ps
        self.fe = fe


class Utente(db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=True)
    token = db.Column(db.Text, nullable=True)
    newsletter = db.Column(db.Boolean, default=0)


def __repr__(self):
    return f'Item{self.name}'
