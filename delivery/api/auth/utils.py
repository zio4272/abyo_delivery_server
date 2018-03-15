# -*- coding:utf8 -*-
import jwt

from functools import wraps

from flask import current_app, g
from flask_restful import reqparse

from delivery.models import Users

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-Http-Token', type=str, location='headers', dest='token', required=True)

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
        return user

    return None

def token_required(func):
    @wraps(func)
    def decorator(*args, **kargs):
        args = token_parser.parse_args()
        user = decode_token(args['token'])
        if user:
            if user.banned:
                return {
                    'code': 403,
                    'message': '정지된 유저입니다.'
                }

            g.user = user
            return func(*args, **kargs)
        
        return {
            'code': 404,
            'message': '올바르지 않은 토큰입니다.'
        }, 404

    return decorator