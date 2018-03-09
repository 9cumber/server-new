# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
# 管理者用ページ
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import url_for, render_template, redirect, flash, Blueprint
from cucumber.views.forms import UserForm

from mock import MagicMock
from cucumber.entities import Book

Stock = MagicMock()
ReturnedStock = MagicMock()
SoldStock = MagicMock()
ReservedInfo = MagicMock()

from cucumber.modules.login_manager import AdminUnauthorized
from cucumber.extensions import login_manager

admin_main = Blueprint('admin_main', __name__)


@admin_main.route('/', methods=['GET'])
@login_manager.admin_required
def index():
    # ダッシュボードにリダイレクト
    return redirect(url_for('admin_main.dashboard'))


@admin_main.route('/dashboard', methods=['GET'])
@login_manager.admin_required
def dashboard():
    admonition_users_over_3_days = [
        User.new('over 3days man', 'over_3days_man_1@u-aizu.ac.jp',
                 'password'),
        User.new('over_3days_man_2', 'over_3days_man_2@u-aizu.ac.jp',
                 'password')
    ]
    admonition_users_over_7_days = [
        User.new('over 7days man', 'over_7days_man_1@u-aizu.ac.jp',
                 'password'),
        User.new('over_7days_man_2', 'over_7days_man_2@u-aizu.ac.jp',
                 'password')
    ]
    return render_template(
        'admin_dashboard.html',
        user=login_manager.get_logged_user(),
        admonition_users_over_3_days=admonition_users_over_3_days,
        admonition_users_over_7_days=admonition_users_over_7_days)


@admin_main.route('/book/list', methods=['GET'])
@login_manager.admin_required
def book_list():
    books = Book.fetch_all()
    from datetime import datetime
    books = [
        Book(
            id=1,
            title=
            'The Practice of Programming (Addison-Wesley Professional Computing Series) ',
            author='Brian W. Pike, Rob Kernighan',
            publisher='Addison-Wesley Professional',
            isbn13='9780201615869',
            language='us',
            price='5948',
            reldate=datetime.utcnow(),
            shelf='shelf-1',
            classify='classify-2',
            description=
            'With the same insight and authority that made their book The Unix Programming Environment a classic, Brian Kernighan and Rob Pike have written The Practice of Programming to help make individual programmers more effective and productive.',
            picture=
            'https://images-fe.ssl-images-amazon.com/images/I/41SUHlT7ovL._AC_SY200_.jpg'
        ),
        Book(
            id=2,
            title='title',
            author='author',
            publisher='publisher',
            isbn13='1234567890123',
            language='jp',
            price='1000',
            reldate=datetime.utcnow(),
            shelf='1',
            classify='2',
            description='description',
            picture=
            'https://images-fe.ssl-images-amazon.com/images/I/41SUHlT7ovL._AC_SY200_.jpg'
        )
    ]

    return render_template(
        'list_book.html', lists=books, user=login_manager.get_logged_user())


@admin_main.route('/book/<int:book_id>/detail', methods=['GET'])
@login_manager.admin_required
def book_detail(book_id):
    book = Book.fetch(book_id)
    return render_template(
        'detail_book.html', book=book, user=login_manager.get_logged_user())


def base_list_view_function(stock, model):
    def func():
        lists = model.fetch_all()
        return render_template(
            'list_%s.html' % stock,
            lists=lists,
            user=login_manager.get_logged_user())

    func.__name__ = str('list_' + stock)
    return login_manager.admin_required(func)


stock_list_view_function = base_list_view_function('stock', Stock)
returned_list_view_function = base_list_view_function('returned',
                                                      ReturnedStock)
sold_list_view_function = base_list_view_function('sold', SoldStock)
reserved_list_view_function = base_list_view_function('reserved', ReservedInfo)

admin_main.add_url_rule('/stock/list', view_func=stock_list_view_function)
admin_main.add_url_rule(
    '/returned/list', view_func=returned_list_view_function)
admin_main.add_url_rule('/sold/list', view_func=sold_list_view_function)
admin_main.add_url_rule(
    '/reserved/list', view_func=reserved_list_view_function)


def base_registration_view_function(stock):
    def func():
        form = UserForm()
        return render_template(
            'registration_%s.html' % stock,
            form=form,
            user=login_manager.get_logged_user())

    func.__name__ = str('register_' + stock)
    return login_manager.admin_required(func)


stock_registration_view_function = base_registration_view_function('stock')
returned_registration_view_function = base_registration_view_function(
    'returned')
sold_registration_view_function = base_registration_view_function('sold')
reserved_registration_view_function = base_registration_view_function(
    'reserved')

admin_main.add_url_rule(
    '/stock/registration', view_func=stock_registration_view_function)
admin_main.add_url_rule(
    '/returned/registration', view_func=returned_registration_view_function)
admin_main.add_url_rule(
    '/sold/registration', view_func=sold_registration_view_function)
admin_main.add_url_rule(
    '/reserved/registration', view_func=reserved_registration_view_function)


@admin_main.errorhandler(AdminUnauthorized)
def handle_admin_unauthorized(_):
    flash('You need to log in as an administrator.', 'warning')
    return redirect(url_for('admin_auth.login'))
