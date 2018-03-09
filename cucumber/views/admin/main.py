# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
# 管理者用ページ
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import url_for, render_template, redirect, flash, Blueprint
from cucumber.views.forms import UserForm
from cucumber.entities import Order, User, Book, Stock, Returned, Sold

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
    return render_template(
        'admin_dashboard.html', user=login_manager.get_logged_user())


@admin_main.route('/book/list', methods=['GET'])
@login_manager.admin_required
def book_list():
    return render_template(
        'list_book.html',
        lists=Book.fetch_all(),
        user=login_manager.get_logged_user())


@admin_main.route('/book/detail/<int:book_id>', methods=['GET'])
@login_manager.admin_required
def book_detail(book_id):
    book = Book.fetch(id=book_id)
    return render_template(
        'detail_book.html', book=book, user=login_manager.get_logged_user())


@admin_main.route('/orders/list', methods=['GET'])
@login_manager.admin_required
def orders_list():
    from datetime import datetime
    orders = [
        Order(
            id='1',
            book_id='id123456',
            stock_id=None,
            user_id='uid123456',
            latest_status='引き取り済み',
            created_at=datetime.now(),
            user=User(email='hoge@gmail.com'),
            book=Book(title='Bible'))
    ]
    return render_template(
        'list_orders.html',
        orders=orders,
        user=login_manager.get_logged_user())


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
returned_list_view_function = base_list_view_function('returned', Returned)
sold_list_view_function = base_list_view_function('sold', Sold)
#reserved_list_view_function = base_list_view_function('reserved', ReservedInfo)

admin_main.add_url_rule('/stock/list', view_func=stock_list_view_function)
admin_main.add_url_rule(
    '/returned/list', view_func=returned_list_view_function)
admin_main.add_url_rule('/sold/list', view_func=sold_list_view_function)

#admin_main.add_url_rul(e'/reserved/list', view_func=reserved_list_view_function)


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
