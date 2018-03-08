# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from amaboko import AmazonBook, normalize_isbn_format


class AmazonSearch(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def setup_from_app(self, app):
        self.setup_from_arugument(app.config['API_ACCESS_KEY'],
                                  app.config['API_SECRET_KEY'],
                                  app.config['ASSOCIATE_ID'])

    def setup_from_arugument(self, access_key, secret_key, associate_id):
        self._amazon = AmazonBook(access_key, secret_key, associate_id)  # pylint: disable=attribute-defined-outside-init

    def init_app(self, app):
        self.setup_from_app(app)

    @property
    def amazon(self):
        return self._amazon

    def lookup_book(self, isbn13, **kwargs):
        """
            ISBN13(EAN)コードをAmazon Advertise APIのItemLookを用いて問い合わせ，
            最初にEANコードが存在した本の情報(amazon.api.AmazonProduct)を1つ返却する

            見つからなかった場合，Noneが返却される
        """
        isbn13 = normalize_isbn_format(isbn13)
        kwargs.update({"IdType": "ISBN", "SearchIndex": "Books"})
        books_include_kindle = self.amazon.lookup(isbn13, **kwargs)

        if type(books_include_kindle) is not list:
            books_include_kindle = [books_include_kindle]

        for book in books_include_kindle:
            if book is None:
                continue

            elif book.ean is not None and normalize_isbn_format(
                    book.ean) == isbn13:
                return book
