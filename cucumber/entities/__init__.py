# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals

from sqlalchemy import BINARY, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Book(Base):
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


class OrderEvent(Base):
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


class Order(Base):
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


class Returned(Base):
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


class Sold(Base):
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


class Stock(Base):
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


class UserType(Base):
    __tablename__ = 'user_types'

    type = Column(String(63), primary_key=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(BINARY(64), nullable=False)
    type = Column(ForeignKey(u'user_types.type'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user_type = relationship(
        u'UserType',
        primaryjoin='User.type == UserType.type',
        backref=u'users')
