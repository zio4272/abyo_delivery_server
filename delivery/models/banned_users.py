# -*- coding:utf8 -*-
# pylint: disable=E1101
from delivery import db

class BannedUsers(db.Model):
    __tablename__ = 'banned_users'

    id = db.Column(db.Integer, primary_key=True)

    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text)