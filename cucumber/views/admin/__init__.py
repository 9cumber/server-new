# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals

from cucumber.views.admin.auth import admin_auth
from cucumber.views.admin.main import admin_main


def init_views(app):
    app.register_blueprint(admin_auth, url_prefix='/admin/auth')
    app.register_blueprint(admin_main, url_prefix='/admin')
