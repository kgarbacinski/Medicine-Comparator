import os

from .main import db, LOGIN_MANAGER
from sqlalchemy.orm import relationship


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_super_user = db.Column(db.Integer, nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('token.token_id'))

    def __init__(self, username, password, email, is_super_user, token_id):
        self.username = username
        self.password = password
        self.email = email
        self.is_super_user = is_super_user
        self.token_id = token_id

    @property
    def id(self):
        return self._id


class Token(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    user = relationship("User", backref="token")

    def __init__(self, token, is_used):
        self.token = token
        self.is_used = is_used


def register_user(new_user: User):
    db.session.add(new_user)
    db.session.commit()


def update_token_status(token_id):
    token_to_update = Token.query.get(token_id)
    token_to_update.is_used = True
    db.session.commit()


def add_tokens(tokens):
    db.session.add_all(tokens)
    db.session.commit()


def token_generator():
    tokens_used = Token.query(Token.is_used).count()
    token_list = []
    if tokens_used % 10 == 0:
        for x in range(10):
            token = Token(os.urandom(2), False)
            token_list.append(token)
        add_tokens(token_list)


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
