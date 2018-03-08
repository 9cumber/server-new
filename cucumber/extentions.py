# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals

from cucumber.modules.amazon import AmazonSearch
from cucumber.modules.login_manager import LoginManager
from flask_jwt_extended import JWTManager

amazon = AmazonSearch()
jwt = JWTManager()
login_manager = LoginManager()


def init_extentions(app):
    amazon.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
