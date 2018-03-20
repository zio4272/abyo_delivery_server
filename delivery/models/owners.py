import datetime

from delivery import db

class Owners(db.Model):
    """가게를 가지고있는(오너) 사용자 테이블"""
    #다대다 연관 테이블?
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    users = db.relationship('Users', back_populates='owners', lazy=True)
    stores = db.relationship('Stores', back_populates='owners', lazy=True)
    orders = db.relationship('Orders', backref='orders', lazy=True)

    def get_owner_object(self, include_users_info=False, include_stores_info=False, include_orders_info=False):
        owner = {
            'id': self.id,
            'uid': self.uid,
            'store_id': self.store_id,
            'created_at': str(self.created_at)
        }
        if include_users_info:
            owner['users'] = [user.get_order_object() for user in self.users]

        if include_stores_info:
            owner['stores'] = [store.get_order_object() for store in self.stores]

        if include_orders_info:
            owner['orders'] = [order.get_order_object() for order in self.orders]

        return owner
