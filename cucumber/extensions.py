# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals

from cucumber.modules.amazon import AmazonSearch
from cucumber.modules.login_manager import LoginManager
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

amazon = AmazonSearch()
jwt = JWTManager()
login_manager = LoginManager()
bcrypt = Bcrypt()
db = SQLAlchemy()


def init_extentions(app):
    from cucumber.entities import UserManager
    db.init_app(app)
    amazon.init_app(app)
    jwt.init_app(app)
    user_manager = UserManager()
    login_manager.init_app(app, user_manager)
    bcrypt.init_app(app)
