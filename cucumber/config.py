# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import six
from flask_env import MetaFlaskEnv
from datetime import timedelta


@six.add_metaclass(MetaFlaskEnv)
class Configuration(object):
    ENV_PREFIX = 'CUCUMBER_'
    SECRET_KEY = 'MJ*dz-?bl4-B?Bg7e&DZv+x9F'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_ALGORITHM = "HS256"
