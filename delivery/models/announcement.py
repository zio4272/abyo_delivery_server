# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from delivery import db

class Announcement(db.Model):
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)