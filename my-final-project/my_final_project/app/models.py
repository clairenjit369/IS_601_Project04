"""Database models."""
from flask_login import UserMixin


class User(UserMixin):

    __tablename__ = 'flasklogin-users'

    def __init__(self, my_id, name, email, password):
        self.id = my_id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)