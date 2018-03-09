# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from cucumber.modules.amazon import AmazonSearch
import os
import pytest


def common_lookup_book(amazon):
    new_book = amazon.lookup_book("9784048916592")
    assert u"実践Vim" in new_book.title
    assert new_book.ean == "9784048916592"

def test_lookup_book_using_app_config(cucumber_app):
    from cucumber.extensions import amazon
    common_lookup_book(amazon)

def test_lookup_book_without_app_config():
    access_key = os.environ.get('ACCESS_KEY')
    secret_key = os.environ.get('SECRET_KEY')
    associate_id = os.environ.get('ASSOCIATE_ID')

    if not associate_id or not secret_key or not associate_id:
        pytest.skip("Not given ACCESS_KEY, SECRET_KEY, ASSOCIATE_ID")

    amazon = AmazonSearch()
    amazon.setup_from_arugument(access_key, secret_key, associate_id)
    common_lookup_book(amazon)
