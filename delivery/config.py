# -*- coding:utf8 -*-
# pylint: disable=R0903
"""
Flask Configuration
"""

class Config(object):
    """
    Default Config Class for abstracting
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    """
    Production Config
    """
    pass

class TestConfig(Config):
    """
    Testing Config
    """
    TESTING = True

class DevelopmentConfig(Config):
    """
    For Development Config
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rppt:dlstkrhk1q'+\
    '@localhost/abyo_delivery'