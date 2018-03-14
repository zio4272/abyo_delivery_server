# -*- coding:utf8 -*-
import jwt

from flask import current_app
from delivery.models import Users

def encode_token(user):
    if not isinstance(user, Users):
        raise ValueError('arg1 is not instance of Users')

    return jwt.encode({'id': user.id, 'user_id': user.user_id,\
        'password': user.password_hashed}, current_app.config['JWT_SECRET'], algorithm=current_app.config['JWT_ALGORITHM']).decode("utf-8")

def decode_token(token):
    if token:
        decoded = jwt.decode(token, current_app.config['JWT_SECRET'],\
            algorithms=[current_app.config['JWT_ALGORITHM']])

        user = Users.query.filter_by(id=decoded['id'], user_id=decoded['user_id'],\
            password_hashed=decoded['password']).first()
        if user is None:
            raise ValueError('token is not valid')

        return user

    raise ValueError('token is not valid')