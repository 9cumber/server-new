# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import six
from flask_env import MetaFlaskEnv

import os
import binascii

@six.add_metaclass(MetaFlaskEnv)
class Configuration(object):
    ENV_PREFIX = 'CUCUMBER_'
    SECRET_KEY = binascii.hexlify(os.urandom(32))
