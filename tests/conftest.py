# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import pathlib
import sys
import pytest

TEST_FOLDER = pathlib.Path(__file__).parent


@pytest.fixture(autouse=True, scope='session')
def _register_sys_path():
    sys.path.append(str(TEST_FOLDER))

@pytest.fixture(scope="function")
def Session():
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    engine = create_engine('sqlite://')

    return sessionmaker(bind=engine)

class SessionBag(object):
    def __init__(self, session):
        self.session = session

class DBCreatorFromSession(object):
    def __init__(self, session_cls):
        self.session_cls = session_cls

    def __call__(self):
        return SessionBag(self.session_cls())
