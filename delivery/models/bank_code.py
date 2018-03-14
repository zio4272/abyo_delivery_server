# -*- coding:utf8 -*-
# pylint: disable=E1102
from delivery import db

class BankCode(db.Model):
    """은행코드 테이블"""
    __tablename__ = 'bank_code'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(12), nullable=False)
    logo = db.Column(db.String(320), nullable=False)

    def get_bank_object(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'logo': self.logo
            # 'logo': "https://s3.ap-northeast-2.amazonaws.com/delivery-logofile/{}".format(self.logo)
        }
