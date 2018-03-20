# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from delivery import db

class OrderContracts(db.Model):
    """배달원 계약건 담는 테이블"""
    __tablename__ = 'order_contracts'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    orders = db.relationship('Orders', back_populates='contracts', lazy=True)

    #accepted_image = db.relationship('ContractImages', backref='contracts', lazy=True)
    #images = db.relationship('OrderImages', backref='contracts', lazy=True)
    completed = db.relationship('CompletedOrders', backref='contracts', lazy=True)
    canceled = db.relationship('CanceledOrders', backref='contracts', lazy=True)
    #reviews = db.relationship('OrderReviews', back_populates='contracts', uselist=False, lazy=True)

    def get_contract_object(self, include_image_info=False, include_order_info=False):
        contract = {
            'id': self.id,
            'order_id': self.order_id,
            'uid': self.uid,
            'created_at': str(self.created_at)
        }

        '''if include_image_info:
            result['images'] = []
            for image in self.images:
                result['images'].append(image.get_image_object())

            result['contract_image'] = []
            for image in self.accepted_image:
                result['contract_image'].append(image.get_image_object())
        '''

        if include_order_info:
            contract['order'] = self.orders.get_order_object(include_user_info=True)

        return contract
