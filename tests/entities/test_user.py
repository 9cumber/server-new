# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from mock import patch
from tests.conftest import DBCreatorFromSession
from cucumber.entities import User, Base, Order
from cucumber.exceptions import UserNotFound
from datetime import datetime, timedelta

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

def test_verify_user():
    new_user = User.new('poe', 's999@u-aizu.ac.jp', 'password')
    assert new_user.verify_user('password')
    assert new_user.verify_user(str('password'))
    assert new_user.verify_user(unicode('password'))
    assert not new_user.verify_user(None)
    assert not new_user.verify_user('')
    assert not new_user.verify_user('password\0')

def test_new():
    new_user = User.new('poe', 's999@u-aizu.ac.jp', 'password')
    assert new_user.name == 'poe'
    assert new_user.email == 's999@u-aizu.ac.jp'
    assert len(new_user.password) == 60 # the hash length of bcrypt is always 60
    assert new_user.is_admin == 0
    assert type(new_user.is_admin) == int
    assert type(new_user.created_at) is datetime
    assert type(new_user.updated_at) is datetime
    assert new_user.created_at == new_user.updated_at

    new_admin = User.new('poe2', 's9999@u-aizu.ac.jp', 'password', is_admin=1)
    assert new_admin.name == 'poe2'
    assert new_admin.email == 's9999@u-aizu.ac.jp'
    assert len(new_admin.password) == 60 # the hash length of bcrypt is always 60
    assert new_admin.is_admin == 1
    assert type(new_admin.is_admin) == int
    assert type(new_admin.created_at) is datetime
    assert type(new_admin.updated_at) is datetime
    assert new_admin.created_at == new_admin.updated_at

def test_fetch(Session):
    session = Session()
    Base.metadata.create_all(session.get_bind())
    new_user = User.new('poe', 's999@u-aizu.ac.jp', 'password')
    session.add(new_user)
    session.commit()

    with patch('cucumber.entities.db', new_callable=DBCreatorFromSession(Session)):
        user = User.fetch('s999@u-aizu.ac.jp', 'password')
        assert user.id == new_user.id

        with pytest.raises(UserNotFound):
            User.fetch('s999@u-aizu.ac.jp', 'invalid_password')

        with pytest.raises(UserNotFound):
            User.fetch('s9999@u-aizu.ac.jp', '')

        with pytest.raises(UserNotFound):
            User.fetch('', 'invalid_password')

        with pytest.raises(UserNotFound):
            User.fetch('s9999@u-aizu.ac.jp', None)

        with pytest.raises(UserNotFound):
            User.fetch(None, 'poe')

def test_latest_order():
    now = datetime.utcnow()
    now2 = datetime.utcnow() + timedelta(hours=3)
    user = User.new('over 3days man', 'over_3days_man_1@u-aizu.ac.jp', 'password')
    assert user.latest_order is None
    user_order_1 = Order(latest_status="引き取り待機", created_at=now, updated_at=now)
    user.orders.append(user_order_1)
    assert user.latest_order is user_order_1
    user_order_2 = Order(latest_status="引き取り待機", created_at=now2, updated_at=now2)
    user.orders.append(user_order_2)
    assert user.latest_order is user_order_2
