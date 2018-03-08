# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from flask.config import Config


class MyFlaskConfig(Config):
    def __init__(self, flask_config):
        # type: (Config) -> None
        super(MyFlaskConfig, self).__init__(flask_config.root_path,
                                            flask_config)
        self.__dict__.update(flask_config.__dict__)

    @property
    def is_changed_amazon_config(self):
        # type: () -> bool
        return "dummy" not in [
            self["SECRET_KEY"], self["API_ACCESS_KEY"], self["API_SECRET_KEY"],
            self["ASSOCIATE_ID"]
        ]
