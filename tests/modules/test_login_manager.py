# encoding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Flask, request, current_app
from flask_jwt_extended import JWTManager, set_access_cookies, unset_jwt_cookies
from cucumber.modules.login_manager import LoginManager,UserUnauthorized, AdminUnauthorized, BaseUserManager

class User(object):
    is_admin = False
    id = 1

class Admin(object):
    is_admin = True
    id = 2

USERS = {1: User, 2: Admin}

class UserManager(BaseUserManager):
    @staticmethod
    def get_user_id(user):
        return int(user.id)

    @staticmethod
    def check_admin(user):
        return user.is_admin

    @staticmethod
    def resolve_user_by_id(user_id):
        return USERS[int(user_id)]


def setup():
    app = Flask('login_manager')
    app.config['SECRET_KEY'] = '1234'
    app.config['JWT_TOKEN_LOCATION'] = 'cookies'

    jwt = JWTManager(app)
    login_manager = LoginManager(app, UserManager)
    app_context = app.app_context()
    app_context.push()


    @app.route('/public')
    def public():
        return 'public', 200

    @app.route('/login', methods=['POST'])
    def login():
        user_id = request.form.get('user_id', type=int)
        try:
            user = login_manager.user_manager.resolve_user_by_id(
                user_id)
        except KeyError:
            return 'error', 401

        access_token = login_manager.logged_user(user)
        resp = current_app.make_response('login')
        set_access_cookies(resp, access_token)
        return resp, 200

    @app.route('/logout', methods=['POST'])
    def logout():
        resp = current_app.make_response('logout')
        unset_jwt_cookies(resp)
        return resp, 200

    @app.route('/user_optional')
    @login_manager.user_optional
    def user_optional():
        if login_manager.is_logged_admin:
            admin = login_manager.get_logged_user()
            return 'user_optional_admin_{id}'.format(id=admin.id), 200
        elif login_manager.is_logged_user:
            user = login_manager.get_logged_user()
            return 'user_optional_user_{id}'.format(id=user.id), 200
        else:
            return 'user_optional_non_user', 200

    @app.route('/user_required')
    @login_manager.user_required
    def user_required():
        return 'user_required', 200

    @app.route('/admin_required')
    @login_manager.admin_required
    def admin_required():
        return 'admin_required', 200

    @app.errorhandler(UserUnauthorized)
    def user_unauthorized(_):
        return 'not user', 401

    @app.errorhandler(AdminUnauthorized)
    def admin_unauthorized(_):
        return 'not admin', 403


def test_non_user(app):
    with app.test_client() as client:
        assert client.get('/public').data == 'public'
        assert client.get(
            '/user_optional').data == 'user_optional_non_user'
        assert client.get('/user_required').data == 'not user'
        assert client.get('/admin_required').data == 'not admin'
        assert client.post('/logout').data == 'logout'

def test_user(app):
    with app.test_client() as client:
        assert client.post(
            '/login', data={'user_id': User.id}).data == 'login'
        assert client.get('/public').data == 'public'
        assert client.get(
            '/user_optional').data == 'user_optional_user_{id}'.format(
                id=User.id)
        assert client.get('/user_required').data == 'user_required'
        assert client.get('/admin_required').data == 'not admin'
        assert client.post('/logout').data == 'logout'

def test_admin(app):
    with app.test_client() as client:
        assert client.post(
            '/login', data={'user_id': Admin.id}).data == 'login'
        assert client.get('/public').data == 'public'
        assert client.get(
            '/user_optional').data == 'user_optional_admin_{id}'.format(
                id=Admin.id)
        assert client.get('/user_required').data == 'user_required'
        assert client.get('/admin_required').data == 'admin_required'
        assert client.post('/logout').data == 'logout'
