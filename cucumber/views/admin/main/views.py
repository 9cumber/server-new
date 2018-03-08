# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from cucumber.modules import login_manager
from view.admin import main
from flask import url_for, render_template, redirect, request, flash
from cucumber.modules.login_manager import AdminUnauthorized
from cucumber.models import Book, Stock, ReturnedStock, SoldStock, ReservedInfo
from cucumber.view.forms import UserForm
"""
管理者用ページ
"""


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
def book_detail():
    book = Book.fetch(id=book_id)
    return render_template(
        'detail_book.html', book=book, user=login_manager.get_logged_user())


def base_list_view_function(stock, model):
    def func():
        lists = model.fetch_all()
        return render_template(
            'list_%s.html' % stock,
            lists=lists,
            user=login_manager.get_logged_user())

    func.__name__ = 'list_' + stock
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


def base_registration_view_function(stock, model):
    def func():
        form = UserForm()
        return render_template(
            'registration_%s.html' % stock,
            form=form,
            user=login_manager.get_logged_user())

    func.__name__ = 'register_' + stock
    return login_manager.admin_required(func)


stock_registration_view_function = base_registration_view_function(
    'stock', Stock)
returned_registration_view_function = base_registration_view_function(
    'returned', ReturnedStock)
sold_registration_view_function = base_registration_view_function(
    'sold', SoldStock)
reserved_registration_view_function = base_registration_view_function(
    'reserved', ReservedInfo)

admin_main.add_url_rule(
    '/stock/registration', view_func=stock_registration_view_function)
admin_main.add_url_rule(
    '/returned/registration', view_func=returned_registration_view_function)
admin_main.add_url_rule(
    '/sold/registration', view_func=sold_registration_view_function)
admin_main.add_url_rule(
    '/reserved/registration', view_func=reserved_registration_view_function)


@admin_main.errorhandler(AdminUnauthorized)
def handle_admin_unauthorized(error):
    flash('You need to log in as an administrator.', 'warning')
    return redirect(url_for('admin_auth.login'))