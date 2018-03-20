# -*- coding:utf8 -*-
# pylint: disable=E1101
import datetime

from delivery import db

class CanceledOrders(db.Model):
    """배달 취소 담는 테이블"""
    __tablename__ = 'canceled_orders'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('order_contracts.id'), nullable=False)
    reasons = db.Column(db.Enum('1', '2', '3', '4'), nullable=False)

    canceled_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    reasons_info = [
        '거리가 먼 배달주소',
        '배송하기 싫은 식당',
        '수락 오류',
        '다른 호출 받기'
    ]

    def map_reason(self, reason=None):
        if reason is None:
            reason = self.reasons
        return self.reasons_info[int(reason) - 1]

    def get_canceled_order_object(self):
        return {
            'contract_id': self.contract_id,
            'reasons': self.map_reason(),
            'canceled_at': str(self.canceled_at)
        }