# -*- coding:utf8 -*-
from flask_restful_swagger_2 import Schema

class EmailModel(Schema):
    type = 'string'
    format = 'email'

class ResponseModel(Schema):
    type = 'object'
    properties = {
        'code': {
            'type': 'integer',
            'format': 'int64'
        },
        'message': {
            'type': 'string'
        },
        'data': {
            'type': 'object'
        },
    }
    required = ['code', 'message']