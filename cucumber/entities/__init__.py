# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals

from sqlalchemy import BINARY, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from cucumber.extensions import bcrypt, db
from cucumber.modules.login_manager import BaseUserManager
from cucumber.exceptions import UserNotFound

Base = declarative_base()
metadata = Base.metadata


class FetchQueryMixin(object):
    @classmethod
    def _make_query(cls):
        # pylint: disable=no-member
        return db.session.query(cls)

    @classmethod
    def fetch(cls, primary_key):
        return cls._make_query().filter_by(id=primary_key).first()

    @classmethod
    def fetch_all(cls):
        return cls._make_query().order_by("id").all()


class Book(Base, FetchQueryMixin):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    publisher = Column(String(255))
    isbn13 = Column(String(13), nullable=False)
    language = Column(String(63))
    price = Column(Numeric(10, 0), nullable=False)
    reldate = Column(DateTime)
    shelf = Column(String(63))
    classify = Column(String(63))
    description = Column(Text)
    picture = Column(String(512))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @property
    def stocks_quantity(self):
        import random
        return random.randint(1, 10000)

    @property
    def returns_quantity(self):
        import random
        return random.randint(1, 10000)

    @property
    def sales_quantity(self):
        import random
        return random.randint(1, 10000)


class OrderEvent(Base, FetchQueryMixin):
    __tablename__ = 'order_events'

    id = Column(Integer, primary_key=True)
    order_id = Column(
        ForeignKey(u'orders.id', ondelete=u'CASCADE', onupdate=u'CASCADE'),
        nullable=False,
        index=True)
    status = Column(
        ForeignKey(u'order_statuses.status'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    remarks = Column(Text)

    @property
    def is_finished(self):
        return self.order_status.status_group == 1

    @property
    def is_rejected(self):
        return self.order_status.status_group == 4

    @property
    def is_inprogress(self):
        return self.order_status.status_group == 2 or self.order_status.status_group == 3

    order = relationship(
        u'Order',
        primaryjoin='OrderEvent.order_id == Order.id',
        backref=u'order_events')
    order_status = relationship(
        u'OrderStatus',
        primaryjoin='OrderEvent.status == OrderStatus.status',
        backref=u'order_events')


class OrderStatus(Base):
    __tablename__ = 'order_statuses'

    status = Column(String(45), primary_key=True, nullable=False)
    status_group = Column(Integer, primary_key=True, nullable=False)


class Order(Base, FetchQueryMixin):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey(u'books.id'), nullable=False, index=True)
    stock_id = Column(
        ForeignKey(u'stocks.id', ondelete=u'CASCADE', onupdate=u'CASCADE'),
        index=True)
    user_id = Column(ForeignKey(u'users.id'), nullable=False, index=True)
    latest_status = Column(
        ForeignKey(u'order_statuses.status'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    book = relationship(
        u'Book', primaryjoin='Order.book_id == Book.id', backref=u'orders')
    order_status = relationship(
        u'OrderStatus',
        primaryjoin='Order.latest_status == OrderStatus.status',
        backref=u'orders')
    stock = relationship(
        u'Stock', primaryjoin='Order.stock_id == Stock.id', backref=u'orders')
    user = relationship(
        u'User', primaryjoin='Order.user_id == User.id', backref=u'orders')


class Returned(Base, FetchQueryMixin):
    __tablename__ = 'returned'

    id = Column(Integer, primary_key=True)
    stock_id = Column(
        ForeignKey(u'stocks.id', ondelete=u'CASCADE', onupdate=u'CASCADE'),
        nullable=False,
        unique=True)
    remarks = Column(Text)
    created_at = Column(DateTime, nullable=False)

    stock = relationship(
        u'Stock',
        primaryjoin='Returned.stock_id == Stock.id',
        backref=u'returneds')


class Sold(Base, FetchQueryMixin):
    __tablename__ = 'sold'

    id = Column(Integer, primary_key=True)
    stock_id = Column(
        ForeignKey(u'stocks.id', ondelete=u'CASCADE', onupdate=u'CASCADE'),
        nullable=False,
        unique=True)
    remarks = Column(Text)
    created_at = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 0), nullable=False)

    stock = relationship(
        u'Stock', primaryjoin='Sold.stock_id == Stock.id', backref=u'solds')


class StockType(Base):
    __tablename__ = 'stock_types'

    type = Column(String(63), primary_key=True)


class Stock(Base, FetchQueryMixin):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey(u'books.id'), nullable=False, index=True)
    type = Column(ForeignKey(u'stock_types.type'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 0), nullable=False)

    book = relationship(
        u'Book', primaryjoin='Stock.book_id == Book.id', backref=u'stocks')
    stock_type = relationship(
        u'StockType',
        primaryjoin='Stock.type == StockType.type',
        backref=u'stocks')


class UserManager(BaseUserManager):
    @staticmethod
    def get_id_in_user(user):
        return user.id

    @staticmethod
    def check_admin(user):
        return bool(user.is_admin)

    @staticmethod
    def resolve_user_by_id(user_id):
        # pylint: disable=no-member
        return db.session.query(User).filter_by(id=user_id).first()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(BINARY(60), nullable=False)
    is_admin = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @property
    def is_uaizu(self):
        try:
            splitted_email = self.email.split('@')
            return (len(splitted_email[0]) >= 1) and (len(
                splitted_email) == 2) and ('u-aizu.ac.jp' in splitted_email[1])
        except AttributeError:
            return False

    def verify_user(self, password):
        try:
            return bcrypt.check_password_hash(self.password, password)
        except (ValueError, TypeError):
            return False

    @classmethod
    def new(cls, name, email, password, is_admin=0):
        from datetime import datetime
        now_datetime = datetime.utcnow()
        password = bcrypt.generate_password_hash(password)
        new_user = cls(
            name=name,
            email=email,
            password=password,
            is_admin=int(is_admin),
            created_at=now_datetime,
            updated_at=now_datetime)
        return new_user

    @classmethod
    def fetch(cls, email, password):
        # pylint: disable=no-member
        user = db.session.query(User).filter_by(email=email).first()
        if not user or not user.verify_user(password):
            raise UserNotFound
        return user
