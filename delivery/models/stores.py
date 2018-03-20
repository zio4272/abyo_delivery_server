from delivery import db

import datetime

class Stores(db.Model):
    """가게 정보 테이블"""
    __tablename__ = 'stores'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    call = db.Column(db.String(13), nullable=False)
    
    
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Numeric(15, 10), nullable=False)
    longitude = db.Column(db.Numeric(15, 10), nullable=False)

    # 사업자 등록번호
    regist_num = (db.String(112), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    owners = db.relationship('Owners', back_populates='stores', lazy=True, uselist=False)

    def get_store_object(self, include_owner_info=False):
        store = {
            'store_id': self.id,
            'name': self.name,
            'phone': self.phone,
            'call': self.call,
            'address': self.address,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.latitude else None,
            'regist_num': self.regist_num,
            'created_at': str(self.created_at)
        }

        if include_owner_info:
            store['owner'] = self.owners.get_owner_object()

        return store
