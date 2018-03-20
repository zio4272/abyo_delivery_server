import datetime

from delivery import db

class Owners(db.Model):
    """가게를 가지고있는(오너) 사용자 테이블"""
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    users = db.relationship('Users', backref='owners', uselist=False, lazy=True)
    stores = db.relationship('Stores', back_populates='owners', uselist=False, lazy=True)

    accepted_image = db.relationship('ContractImages', backref='contracts', lazy=True)
    images = db.relationship('OrderImages', backref='contracts', lazy=True)
    completed = db.relationship('CompletedOrders', backref='contracts', lazy=True)
    canceled = db.relationship('CanceledOrders', backref='contracts', lazy=True)
    reviews = db.relationship('OrderReviews', back_populates='contracts', uselist=False, lazy=True)

    def get_contract_object(self, include_image_info=False, include_order_info=False):
        result = {
            'id': self.id,
            'order_id': self.order_id,
            'uid': self.uid,
            'created_at': str(self.created_at)
        }

        if include_image_info:
            result['images'] = []
            for image in self.images:
                result['images'].append(image.get_image_object())

            result['contract_image'] = []
            for image in self.accepted_image:
                result['contract_image'].append(image.get_image_object())

        if include_order_info:
            result['order'] = self.orders.get_order_object(include_user_info=True)

        return result
