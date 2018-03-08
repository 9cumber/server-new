# encoding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from . import amazon
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = declarative_base()
metadata = Base.metadata


class BaseModel():
    @staticmethod
    def generate_token():
        from uuid import uuid4
        return uuid4().hex

    @staticmethod
    def hash(email, password):
        import hashlib
        one = hashlib.sha256("9cumber" + email + password).hexdigest()

        for _ in range(current_app.config['HASH_ROUND']):
            one = hashlib.sha256(one).hexdigest()

        return one


class StdFetchMixin(object):
    @classmethod
    def fetch(cls, primary_key):
        # pylint: disable=no-member
        return db.session.query(cls).filter_by(id=primary_key).first()

    @classmethod
    def fetch_all(cls):
        # pylint: disable=no-member
        return db.session.query(cls).all()


class User(db.Model, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    is_uaizu = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def verify_user(self, email, password):
        given = User.hash(email, password)
        return True if self.password == given else False

    @staticmethod
    def new(email, password, is_admin=False):
        if email is None or password is None:
            raise Exception("Empty email or password")
        is_uaizu = 'u-aizu.ac.jp' in email.split('@')[-1]
        password = User.hash(email, password)
        new_user = User(
            email=email,
            password=password,
            is_uaizu=is_uaizu,
            is_admin=is_admin)
        return new_user

    def update(self, email=None, password=None):
        self.email = email if email is not None else self.email
        self.password = User.hash(password) if password is not None else self.password

    @staticmethod
    def create_non_admin(email, password):
        return User.new(email, password)

    @staticmethod
    def create_admin(email, password):
        return User.new(email, password, 1)

    @classmethod
    def fetch(cls, email, password):
        password = User.hash(email, password)
        # pylint: disable=no-member
        return db.session.query(User).filter_by(
            email=email, password=password).first()


class Book(db.Model, StdFetchMixin):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), server_default=text("NULL"))
    publisher = Column(String(255), server_default=text("NULL"))
    isbn13 = Column(String(13))
    language = Column(String(128))
    price = Column(Integer)
    reldate = Column(Date)
    shelf = Column(String(255))
    classify = Column(String(255))
    description = Column(String(256))
    picture = Column(String(512))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def new(title,
            price=None,
            author=None,
            publisher=None,
            isbn13=None,
            language=None,
            reldate=None,
            shelf=None,
            classify=None,
            description=None,
            picture=None):
        # TODO default picture URL should be relpaced.
        if title is None:
            raise Exception("Empty title")
        new_book = Book(
            title=title,
            author=author,
            publisher=publisher,
            isbn13=isbn13,
            language=language,
            price=price,
            reldate=reldate,
            shelf=shelf,
            classify=classify,
            description=description,
            picture=picture)
        return new_book

    @staticmethod
    def new_from_isbn(isbn):
        b = amazon.lookup_book(isbn)
        if b is None or b.ean is None:
            return None

        if b.price_and_currency[0] is None or b.price_and_currency[1] != "JPY":
            price = None
        else:
            price = int(b.price_and_currency[0])

        # FIXME: UNF
        language = ", ".join(b.languages)

        picture_urls_nullable = [
            b.tiny_image_url, b.small_image_url, b.medium_image_url,
            b.large_image_url
        ]
        picture_url = next((i for i in picture_urls_nullable
                            if i is not None), None)

        new_book = Book.new(b.title, price, b.author, b.publisher, b.ean,
                            language, b.release_date, None, None, picture_url)
        return new_book

    @staticmethod
    def fetch_by_isbn(isbn13):
        # pylint: disable=no-member
        return db.session.query(Book).filter_by(isbn13=isbn13).first()

    #@staticmethod
    #def search_by(arg):
    #TODO フロントの検索画面レイアウトができてから実装
    #    return db.session.query(Book).all()

    def update(self,
                    isbn13,
                    title=None,
                    price=None,
                    author=None,
                    publisher=None,
                    language=None,
                    reldate=None,
                    shelf=None,
                    classify=None,
                    description=None,
                    picture=None):
        self.title = title if title is not None else self.title
        self.price = price if price is not None else self.price
        self.author = author if author is not None else self.author
        self.publisher = publisher if publisher is not None else self.publisher
        self.isbn13 = isbn13 if isbn13 is not None else self.isbn13
        self.language = language if language is not None else self.language
        self.reldate = reldate if reldate is not None else self.reldate
        self.shelf = shelf if shelf is not None else self.shelf
        self.classify = classify if classify is not None else self.classify
        self.description = description if description is not None else self.description
        self.picture = picture if picture is not None else self.picture


class Stock(db.Model, StdFetchMixin):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey(u'books.id'))
    saleprice = Column(Integer, nullable=False)
    type = Column("type", String(16))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    book = relationship(u'Book')

    __mapper_args__ = {'polymorphic_on': type, 'polymorphic_identity': 'stock'}

    @staticmethod
    def new(book_id, saleprice):
        if book_id is None or saleprice is None:
            raise Exception("Empty book_id or saleprice")
        new_stock = Stock(book_id=book_id, saleprice=saleprice)
        return new_stock

    def update_price(self, saleprice):
        self.saleprice = saleprice

    @staticmethod
    def fetch_by_book_id(book_id):
        # pylint: disable=no-member
        return db.session.query(Stock).filter_by(book_id=book_id).all()

    @staticmethod
    def fetch_available_by_book_id(book_id):
        # pylint: disable=no-member
        return db.session.query(Stock).\
                outerjoin(ReservedInfo, Stock.id == ReservedInfo.stock_id).\
                filter(Stock.type == 'stock').\
                filter(ReservedInfo.stock_id.is_(None)).filter(Stock.book_id == book_id).first()

    @staticmethod
    def update_type(stock_id, stock_type):
        db.session.execute("UPDATE stocks SET type=:type WHERE id=:id",
                           {"type": stock_type,
                            "id": stock_id})


class ReturnedStock(Stock):
    __tablename__ = 'returned_stocks'
    __mapper_args__ = {'polymorphic_identity': 'returned'}

    stock = relationship(u'Stock')

    id = Column(Integer, ForeignKey(u'stocks.id'), primary_key=True)
    returned_at = Column(DateTime, nullable=False)
    remarks = Column(String(256), server_default=text("NULL"))

    @staticmethod
    def register(stock_id, remarks=None):
        if stock_id is None:
            raise Exception("Empty stock_id")
        elif Stock.fetch(stock_id) is None:
            raise Exception("Stock id not found")
        new_ret = ReturnedStock(id=stock_id, remarks=remarks)
        db.session.execute(
            "INSERT INTO returned_stocks (id, returned_at, remarks) VALUES (:id, :returned_at, :remarks)",
            {
                "id": new_ret.id,
                "returned_at": datetime.now(),
                "remarks": new_ret.remarks
            })
        Stock.update_type(new_ret.id, "returned")
        db.session.commit()
        #db.session.expunge_all()
        return new_ret

    @staticmethod
    def create_from(returned_stock):
        if returned_stock.id is None or returned_stock.remarks is None:
            raise Exception(
                "Database operation error: failed to record return")
        # pylint: disable=no-member
        db.session.execute(
            "INSERT INTO returned_stocks (id, returned_at, remarks) VALUES (:id, :returned_at, :remarks)",
            {
                "id": returned_stock.id,
                "returned_at": datetime.now(),
                "remarks": returned_stock.remarks
            })
        Stock.update_type(returned_stock.id, "returned")

    @staticmethod
    def fetch_by_book_id(book_id):
        # pylint: disable=no-member
        return db.session.query(ReturnedStock).filter_by(book_id=book_id).all()


class SoldStock(Stock):
    __tablename__ = 'sold_stocks'
    __mapper_args__ = {'polymorphic_identity': 'sold'}

    id = Column(Integer, ForeignKey(u'stocks.id'), primary_key=True)
    sold_at = Column(DateTime, nullable=False)
    remarks = Column(String(256), server_default=text("NULL"))

    @staticmethod
    def new(stock_id, book_id, saleprice, remarks=None):
        if stock_id is None or book_id is None or saleprice is None:
            raise Exception("Empty stock_id or book_id or saleprice")
        new_sold = SoldStock(
            id=stock_id, remarks=remarks, sold_at=datetime.now())
        new_sold.book_id = book_id
        new_sold.saleprice = saleprice
        return new_sold

    @staticmethod
    def add(sold_stock):
        if sold_stock.id is None or sold_stock.remarks is None:
            raise Exception("Database operation error: failed to record sold")
        # pylint: disable=no-member
        db.session.execute(
            "INSERT INTO sold_stocks (id, sold_at, remarks) VALUES (:id, :sold_at, :remarks)",
            {
                "id": sold_stock.id,
                "sold_at": datetime.now(),
                "remarks": sold_stock.remarks
            })

        Stock.update_type(sold_stock.id, "sold")

    @staticmethod
    def fetch_by_book_id(book_id):
        # pylint: disable=no-member
        return db.session.query(SoldStock).filter_by(book_id=book_id).all()


class ReservedInfo(db.Model, StdFetchMixin):
    __tablename__ = 'reserved_info'

    id = Column(Integer, primary_key=True)
    reserved_at = Column(DateTime, nullable=False)
    reserved_due = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey(u'users.id'))
    stock_id = Column(
        Integer, ForeignKey(u'stocks.id'), unique=True, nullable=True)
    remarks = Column(String(256), server_default=text("NULL"))

    user = relationship(u'User', foreign_keys=[user_id])
    stock = relationship(u'Stock', foreign_keys=[stock_id])

    def set_stock_id(self, stock_id):
        if self.stock_id is None:
            self.stock_id = stock_id
        else:
            print("reservation %s was already received by %s" % (self.stock_id,
                                                                 self.user_id))

    @staticmethod
    def new(user_id, stock_id=None, remarks=None, reserved_due=None):
        if user_id is None:
            raise Exception("Empty user_id or stock_id")
        new_reserved = ReservedInfo(
            remarks=remarks,
            reserved_at=datetime.now(),
            reserved_due=reserved_due,
            user_id=user_id,
            stock_id=stock_id)
        return new_reserved

    @staticmethod
    def add(reserved_info):
        if reserved_info.user_id is None:
            raise Exception(
                "Database operation error: failed to record reserved")
        # pylint: disable=no-member
        db.session.execute(
            "INSERT INTO reserved_info (reserved_at, reserved_due, user_id, stock_id, remarks) VALUES (:reserved_at, :reserved_due, :user_id, :stock_id, :remarks)",
            {
                "reserved_at": datetime.now(),
                "reserved_due": reserved_info.reserved_due,
                "user_id": reserved_info.user_id,
                "stock_id": reserved_info.stock_id,
                "remarks": reserved_info.remarks
            })

    @staticmethod
    def fetch_by_book_id(book_id):
        # pylint: disable=no-member
        return db.session.query(ReservedInfo).\
                join(Stock, ReservedInfo.id == Stock.id).\
                filter_by(book_id=book_id).all()

    @staticmethod
    def fetch_by_stock_id(stock_id):
        # pylint: disable=no-member
        return db.session.query(ReservedInfo).filter_by(
            stock_id=stock_id).first()

    @staticmethod
    def fetch_by_uid(user_id):
        # pylint: disable=no-member
        return db.session.query(ReservedInfo).filter_by(user_id=user_id).all()

    @staticmethod
    def fetch_exceeded(days):
        # fetch all reservations which were made by N days ago
        limit_date = datetime.now() - timedelta(days=days)
        # pylint: disable=no-member
        return db.session.query(ReservedInfo).filter(
            ReservedInfo.reserved_at < limit_date).all()
