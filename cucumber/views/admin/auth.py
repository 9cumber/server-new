# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
# 管理者用ログインページ
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies

from cucumber.modules.login_manager import AdminUnauthorized
from cucumber.views.forms import UserForm
from cucumber.extensions import login_manager
from cucumber.entities import User

admin_auth = Blueprint('admin_auth', __name__)


@admin_auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('admin_auth.login'))


@admin_auth.route('/login', methods=['GET', 'POST'])
def login():
    # when logged in, redirect to dashboard
    if login_manager.is_logged_user:
        return redirect(url_for('admin_main.dashboard'))
    form = UserForm()
    if form.is_submitted():
        if form.validate():
            admin = User.fetch(
                email=form.email.data, password=form.password.data)
            if admin is not None and bool(
                    admin.is_admin) and admin.verify_user(
                        form.password.data) is True:
                access_token = login_manager.logged_user(admin)
                res = redirect(
                    request.args.get('next')
                    or url_for('admin_main.dashboard'))
                set_access_cookies(res, access_token)
                return res
            flash('Invalid administrator information', 'danger')
        else:
            flash('Invalid input', 'danger')
    return render_template('admin_login.html', form=form)


@admin_auth.route('/logout', methods=['GET'])
@login_manager.admin_required
def logout():
    flash('You have been logged out.', 'success')
    res = redirect(url_for('admin_auth.login'))
    unset_jwt_cookies(res)
    return res


@admin_auth.errorhandler(AdminUnauthorized)
def handle_admin_unauthorized(_):
    flash('You need to log in as an administrator.', 'warning')
    return redirect(url_for('admin_auth.login'))
