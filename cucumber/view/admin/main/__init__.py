# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint

admin_main = Blueprint('admin_main', __name__)

from . import views, errors
