# encoding: utf-8
from flask import render_template, redirect, request, url_for, flash
from . import admin_auth
from ..login_manager import AdminUnauthorized
from ..models import User
from ..forms import UserForm
from .. import login_manager, jwt
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
"""
ログインセッション失効時の処理
"""


@jwt.expired_token_loader
def waste_token():
    res = redirect(url_for('admin_auth.login'))
    unset_jwt_cookies(res)
    return res


"""
管理者用ログインページ
"""


@admin_auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('admin_auth.login'))


@admin_auth.route('/login', methods=['GET', 'POST'])
def login():
    # when logged in, redirect to dashboard
    if login_manager.is_logged_user:
        return redirect(url_for('admin_auth.logout'))
    form = UserForm()
    if form.validate_on_submit():
        admin = User.fetch(email=form.email.data, password=form.password.data)
        if admin is not None and admin.is_admin is True and admin.verify_user(
                form.email.data, form.password.data) is True:
            access_token = login_manager.logged_user(admin)
            res = redirect(
                request.args.get('next') or url_for('admin_auth.logout'))
            set_access_cookies(res, access_token)
            return res
        flash('Invalid administrator information', 'danger')
    return render_template('admin_login.html', form=form)


@admin_auth.route('/logout', methods=['GET'])
@login_manager.admin_required
def logout():
    flash('You have been logged out.', 'success')
    res = redirect(url_for('admin_auth.login'))
    unset_jwt_cookies(res)
    return res


@admin_auth.errorhandler(AdminUnauthorized)
def handle_admin_unauthorized(error):
    flash('You need to log in as an administrator.', 'warning')
    return redirect(url_for('admin_auth.login'))
