# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals


def create_app():
    from cucumber.extentions import init_extentions
    from cucumber.views import init_views
    from flask import Flask

    app = Flask(__name__)

    # admin authenticator
    init_views(app)
    init_extentions(app)

    # config loader
    #app.config = MyFlaskConfig(app.config)
    #app.config.from_object(config[config_name])
    #config[config_name].init_app(app)

    return app
