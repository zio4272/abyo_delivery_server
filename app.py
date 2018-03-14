# -*- coding:utf8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object('delivery.config.{0}'.format(config_name))

    db.init_app(app)

    return app