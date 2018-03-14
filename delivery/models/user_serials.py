# -*- coding:utf8 -*-
# pylint: disable=E1101
import hashlib

from delivery import db

class UserSerials(db.Model):
    __tablename__ = 'user_serials'

    id = db.Column(db.Integer, primary_key=True)

    uid = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    serial = db.Column(db.String(32), unique=True, nullable=False)

    def create_serial(self):
        return hashlib.md5(self.users.user_id.encode('utf8')).hexdigest()