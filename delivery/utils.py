# -*- coding: utf8 -*-

class RestfulType:
    @staticmethod
    def user_type(value, name):
        if value in ['WORKER', 'OWNER']:
            return value

        raise ValueError("The parameter '{}' is not valid.".format(name))

    @staticmethod
    def alphanumeric(value, name):
        if str.isalnum(value):
            return value

        raise ValueError("The parameter '{}' is not valid.".format(name))