# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from delivery import db

class CompletedOrders(db.Model):
    """완료된 배달건 테이블"""
    __tablename__ = 'completed_orders'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('order_contracts.id'), nullable=False)

    completed_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)