# -*- coding:utf8 -*-
#pylint: disable=E1101,C0103
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from delivery import db
from delivery.swagger import ResponseModel
from delivery.utils import RestfulType
from delivery.models import Users

from .utils import encode_token, decode_token

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-http-token', type=str, location='headers', dest='token')

signin_parser = reqparse.RequestParser()
signin_parser.add_argument('user_id', type=RestfulType.alphanumeric,\
    required=True, location='form')
signin_parser.add_argument('password', type=RestfulType.alphanumeric,\
    required=True, location='form')

signup_parser = signin_parser.copy()
signup_parser.add_argument('name', type=str, required=True, location='form')
signup_parser.add_argument('phone', type=str, required=True, location='form')
signup_parser.add_argument('email', type=str, required=True, location='form')

signup_parser.add_argument('address', type=str, location='form')
signup_parser.add_argument('longitude', type=float, location='form')
signup_parser.add_argument('latitude', type=float, location='form')

signup_parser.add_argument('type', type=RestfulType.user_type,\
    required=True, location='form')

class Auth(Resource):
    @swagger.doc({
        'tags': ['user'],
        'description': '토큰으로 유저 조회',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '유저 토큰',
                'in': 'header',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '토큰으로 조회 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '토큰 조회 성공',
                        'data': {
                            'user': {
                                'id': 123,
                                'user_id': 'some value',
                                'name': 'some value',
                                'email': 'some value',
                                'phone': 'some value',
                                'type': 'some value',
                                'latitude': 'some value',
                                'longitude': 'some value',
                                'address': 'some value'
                            }
                        }
                    }
                }
            },
            '404': {
                'description': '올바르지 않은 조회',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 404,
                        'message': '올바르지 않은 토큰입니다.'
                    }
                }
            }
        }  
    })
    def get(self):
        args = token_parser.parse_args()
        user = decode_token(args['token'])
        if user:
            return {
                'code': 200,
                'message': '토큰 조회 성공',
                'data': {
                    'user': {
                        'id': user.id,
                        'user_id': user.user_id,
                        'name': user.name,
                        'email': user.email,
                        'phone': user.phone,
                        'type': user.type,
                        'latitude': float(user.latitude),
                        'longitude': float(user.longitude),
                        'address': user.address
                    }
                }
            }, 200
        return {
            'code': 404,
            'message': '올바르지 않은 토큰입니다.'
        }, 404

    @swagger.doc({
        'tags': ['user'],
        'description': '로그인',
        'parameters': [
            {
                'name': 'user_id',
                'description': '유저 아이디',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'password',
                'description': '유저 비밀번호',
                'in': 'formData',
                'type': 'string',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': '로그인 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 200,
                        'message': '로그인 성공',
                        'data': {
                            'user': {
                                'id': 123,
                                'user_id': 'some value',
                                'name': 'some value',
                                'email': 'some value',
                                'phone': 'some value',
                                'type': 'some value',
                                'latitude': 'some value',
                                'longitude': 'some value',
                                'address': 'some value'
                            },
                            'token': 'jwt value'
                        }
                    }
                }
            }
        }  
    })
    def post(self):
        args = signin_parser.parse_args()
        user = Users.query.filter_by(user_id=args['user_id']).first()
        if user is not None:
            if user.verify_password(args['password']):
                return {
                    'code': 200,
                    'message': '로그인 성공',
                    'data': {
                        'user': {
                            'id': user.id,
                            'user_id': user.user_id,
                            'name': user.name,
                            'email': user.email,
                            'phone': user.phone,
                            'type': user.type,
                            'latitude': float(user.latitude),
                            'longitude': float(user.longitude),
                            'address': user.address
                        },
                        'token': encode_token(user)
                    }
                }, 200           
            return {
                'code': 400,
                'message': '비밀번호가 옳바르지 않습니다.'
            }, 400
        return {
              'code': 400,
              'message': '아이디가 존재하지 않습니다.'
        },400

    @swagger.doc({
        'tags': ['user'],
        'description': '회원가입',
        'parameters': [
            {
                'name': 'user_id',
                'description': '유저 아이디',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'password',
                'description': '유저 비밀번호',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'name',
                'description': '유저 이름',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'phone',
                'description': '유저 휴대폰 번호. 정규식은 `^[\d]{3}-[\d]{3,4}-[\d]{4}$` 사용',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'email',
                'description': '유저 이메일',
                'in': 'formData',
                'type': 'string',
                'required': True
            }, {
                'name': 'address',
                'description': '유저 주소, 일반 string 값으로만 처리함.',
                'in': 'formData',
                'type': 'string'
            }, {
                'name': 'longitude',
                'description': '유저의 주소 경도',
                'in': 'formData',
                'type': 'float'
            }, {
                'name': 'latitude',
                'description': '유저의 주소 위도',
                'in': 'formData',
                'type': 'float'
            }, {
                'name': 'type',
                'description': '유저 타입. WORKER, OWNER 둘 중 하나의 값을 가짐',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
        ],
        'responses': {
            '201': {
                'description': '회원가입 성공',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 201,
                        'message': '회원가입 성공',
                        'data': {
                            'user': {
                                'id': 123,
                                'user_id': 'some value',
                                'name': 'some value',
                                'email': 'some value',
                                'phone': 'some value',
                                'type': 'some value',
                                'latitude': 'some value',
                                'longitude': 'some value',
                                'address': 'some value'
                            },
                            'token': 'jwt value'
                        }
                    }
                }
            },
            '400': {
                'description': '파라미터 값 이상',
                'schema': ResponseModel,
                'examples': {
                    'application/json': {
                        'code': 400,
                        'message': '특정 파라미터 값이 올바르지 않습니다.'
                    }
                }
            }
        }
    })
    def put(self):
        args = signup_parser.parse_args()

        if not (len(args['user_id']) >= 8 and len(args['user_id']) <= 16):
            return {
                'code': 400,
                'message': '유저 아이디 값이 올바르지 않습니다.'
            }, 400
        elif not (len(args['password']) >= 8 and len(args['password']) <= 16):
            return {
                'code': 400,
                'message': '유저 비밀번호 값이 올바르지 않습니다.'
            }, 400
        elif not Users.verify_name(args['name']):
            return {
                'code': 400,
                'message': '사용자 이름 값이 올바르지 않습니다.'
            }, 400
        elif not Users.verify_phone_number(args['phone']):
            return {
                'code': 400,
                'message': '휴대전화 값이 올바르지 않습니다.'
            }, 400
        elif not Users.verify_email(args['email']):
            return {
                'code': 400,
                'message': '이메일 값이 올바르지 않습니다.'
            }

        user = Users.query.filter_by(user_id=args['user_id']).first()
        if user is not None:
            return {
                'code': 400,
                'message': '중복된 유저 아이디가 존재합니다.'
            }, 400

        user = Users.query.filter_by(email=args['email']).first()
        if user is not None:
            return {
                'code': 400,
                'message': '중복된 유저 이메일이 존재합니다.'
            }, 400

        user = Users.query.filter_by(phone=args['phone']).first()
        if user is not None:
            return {
                'code': 400,
                'message': '중복된 유저 전화번호가 존재합니다.'
            }, 400

        new_user = Users()
        new_user.user_id = args['user_id']
        new_user.password = args['password']
        new_user.name = args['name']
        new_user.email = args['email']
        new_user.phone = args['phone']
        new_user.type = args['type']

        if args['latitude']:
            new_user.latitude = args['latitude']
        if args['longitude']:
            new_user.longitude = args['longitude']
        if args['address']:
            new_user.address = args['address']

        db.session.add(new_user)
        db.session.commit()

        return {
            'code': 201,
            'message': '회원가입 성공입니다.',
            'data': {
                'user': { 
                    'id': new_user.id,
                    'user_id': new_user.user_id,
                    'name': new_user.name,
                    'email': new_user.email,
                    'phone': new_user.phone,
                    'type': new_user.type,
                    'latitude': float(new_user.latitude),
                    'longitude': float(new_user.longitude),
                    'address': new_user.address
                },
                'token': encode_token(new_user)
            }
        }, 201