# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from cucumber.view.admin import main


@admin_main.app_errorhandler(404)
def not_found(e):
    print(e)
    return '404'


@admin_main.app_errorhandler(500)
def server_error(e):
    print(e)
    return '500'
