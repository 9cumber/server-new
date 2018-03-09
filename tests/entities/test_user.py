# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from tests.conftest import DBCreatorFromSession
from cucumber.entities import User

def test_is_uaizu():
    assert User(email='s99999999@u-aizu.ac.jp').is_uaizu 
    assert User(email='foo@u-aizu.ac.jp').is_uaizu 
    assert not User(email='@u-aizu.ac.jp').is_uaizu 
    assert not User(email='@@u-aizu.ac.jp').is_uaizu 
    assert not User(email='u-aizu.ac.jp@').is_uaizu 
    assert not User(email='u-aizu.ac.jp').is_uaizu 
    assert not User(email='foo@u-aizu.com').is_uaizu 
    assert not User(email='').is_uaizu 
    assert not User(email=None).is_uaizu 
    assert not User(email='@').is_uaizu 
