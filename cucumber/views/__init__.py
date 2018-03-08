# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals

from cucumber.views.admin import init_views as init_admin_views


def init_views(app):
    init_admin_views(app)
