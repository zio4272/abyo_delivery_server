# -*- coding:utf8 -*-
# pylint: disable=E1101
import hashlib
import re
import datetime

from delivery import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(32), nullable=False, unique=True)
    password_hashed = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(320), nullable=False)

    latitude = db.Column(db.Numeric(15, 10), nullable=False, default=0)
    longitude = db.Column(db.Numeric(15, 10), nullable=False, default=0)
    address = db.Column(db.String(255))

    bank_code = db.Column(db.Integer, db.ForeignKey('bank_code.id'))
    bank_account = db.Column(db.String(64))

    type = db.Column(db.Enum('WORKER', 'OWNER'), nullable=False)

    profile_image_key = db.Column(db.String(320), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    
    banned = db.relationship('BannedUsers', backref='users', lazy=True)
    serial = db.relationship('UserSerials', backref='users', lazy=True)
    bank_code = db.relationship('BankCode', backref='users', lazy=True)
   
    @staticmethod
    def generate_password_hash(password):
        pre_hashed = hashlib.sha512(('x3FpknhFyR' + password + 'a6E8kInyyW')\
            .encode('utf8')).hexdigest()
        return hashlib.md5(pre_hashed.encode('utf8')).hexdigest()

    @staticmethod
    def check_password_hash(password_hashed, password):
        return password_hashed == Users.generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hashed = self.generate_password_hash(password)

    def verify_password(self, password):
        return self.check_password_hash(self.password_hashed, password)

    def get_user_object(self, simpler_format=False, include_crimes=False, complex_format=False):
        user = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'bank_code': self.bank_code,
            'bank_account': self.bank_account,
            'type': self.type,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'address': self.address,
            'profile_image': 'https://s3.ap-northeast-2.amazonaws.com/delivery-resource/{}'.format(self.profile_image_key)\
                if self.profile_image_key else None
        }

        if simpler_format:
            user.pop('latitude', None)
            user.pop('longitude', None)
            user.pop('address', None)
            user.pop('type', None)

        if complex_format:
            user['banned'] = str(self.banned.banned_at) if self.banned else None

        if include_crimes:
            user['crimes'] = [
                {
                    'id': crime.id,
                    'name': crime.name,
                    'sentence': crime.sentence,
                    'date': str(crime.date)
                } for crime in self.crimes
            ]

        return user
    
    @staticmethod
    def verify_phone_number(phone_number):
        phone_pattern = re.compile(r'^[\d]{3}-[\d]{3,4}-[\d]{4}$')
        return phone_pattern.match(phone_number)

    @staticmethod
    def verify_email(email):
        email_pattern = re.compile(r'^[A-Z0-9a-z._%+-]{1,64}@[A-Za-z0-9.-]{2,}\.[A-Za-z0-9.-]{2,}$')
        return email_pattern.match(email)

    @staticmethod
    def verify_name(name): 
        name_pattern = re.compile(r'^[가-힣]{2,5}$')
        return name_pattern.match(name)
