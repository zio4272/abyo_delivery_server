# -*- coding:utf8 -*-
import hashlib

from delivery import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(32), nullable=False, unique=True)
    password_hashed = db.Column(db.String(32), nullable=False)

    name = db.Column(db.String(32), nullable=False)

    @staticmethod
    def generate_password_hash(password):
        pre_hashed = hashlib.sha512(('x3FpknhFyR' + password + 'a6E8kInyyW')\
            .encode('utf8')).hexdigest()
        return hashlib.md5(pre_hashed.encode('utf8')).hexdigest()

    @staticmethod
    def check_password_hash(password_hashed, password):
        return password_hashed == Users.generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hashed = self.generate_password_hash(password)

    def verify_password(self, password):
        return self.check_password_hash(self.password_hashed, password)