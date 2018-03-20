from delivery import db

import datetime

class Orders(db.Model):
    """배달 주문 담는 테이블"""
    __tablename__ = 'orders'


    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    price = db.Column(db.Integer, nullable=False)
    # 1 : CASH
    # 2 : CARD
    # 3 : PREPAID
    paid_type = db.Column(db.Enum('1', '2', '3'), nullable=False)
    waiting_time = db.Column(db.Integer, nullabe=False, default=0)
    delivery_amount = db.Column(db.Integer, nullable=False, default=1) 

    # 1 : CAR
    # 2 : BIKE
    # 3 : PREPAID
    transport_type = db.Column(db.Enum('1', '2', '3'), nullable=False)
    
    address = db.Column(db.String(255), nullable=False)
    address_detail = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Numeric(15, 10), nullable=False)
    longitude = db.Column(db.Numeric(15, 10), nullable=False)
    customer_call = db.Column(db.String(13), nullable=False)


    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    contracts = db.relationship('OrderContracts', back_populates='orders', lazy=True, uselist=False)

    def get_order_object(self, include_owner_info=False):
        order = {
            'order_id': self.id,
            'own'
            'destination': self.address,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.latitude else None,
            'amount': self.amount,
            'unit_price': self.unit_price,
            'weight': self.weight,
            'COD_amount': self.COD_amount,
            'expected_arrival_time': str(self.expected_arrival_time),
            'requirements': self.requirements,
            'created_at': str(self.created_at)
        }

        if include_owner_info:
            order['owner'] = self.owners.get_user_object(simpler_format=True)

        return order
