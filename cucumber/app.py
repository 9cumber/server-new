# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals


def create_app(config_name):
    from cucumber.extentions import init_extentions
    from flask import Flask

    app = Flask(__name__)

    # admin authenticator
    from cucumber.views.admin.auth import admin_auth as admin_auth_blueprint
    app.register_blueprint(admin_auth_blueprint, url_prefix='/admin/auth')

    init_extentions(app)

    # config loader
    #app.config = MyFlaskConfig(app.config)
    #app.config.from_object(config[config_name])
    #config[config_name].init_app(app)

    return app
