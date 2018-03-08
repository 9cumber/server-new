# coding: utf-8
# Copyright © 2015-2018 9cumber Ltd. All Rights Reserved.
from __future__ import absolute_import, division, print_function, unicode_literals
from functools import wraps

from flask_jwt_extended.view_decorators import _decode_jwt_from_request
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_jwt_extended import create_access_token, get_jwt_identity

try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:
    from flask import _request_ctx_stack as ctx_stack


class UserUnauthorized(Exception):
    pass


class AdminUnauthorized(Exception):
    pass


# reffred to concept of https://github.com/mattupstate/flask-jwt/issues/106
def _jwt_optional(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            jwt_data = _decode_jwt_from_request(request_type='access')
            if jwt_data:
                ctx_stack.top.jwt = jwt_data
        except JWTExtendedException:
            pass
        return fn(*args, **kwargs)

    return decorator


class DefaultUserManager(object):
    @staticmethod
    def get_id_in_user(user):
        return user.id

    @staticmethod
    def resolve_user_by_id(user_id):
        # pylint: disable=unused-argument
        # FIXME
        # return db.session.query(User).filter_by(id=user_id).first()
        return None


class LoginManager(object):

    user_manager = DefaultUserManager()

    def __init__(self, app=None):
        self.app = app

    def init_app(self, app):
        self.app = app

    def logged_user(self, user):
        # typed: (User, bool) -> str
        user_id = self.user_manager.get_id_in_user(user)
        return create_access_token(identity=user_id)

    @_jwt_optional
    def get_logged_user(self):
        # typed: () -> Union[None, User]
        user_id = get_jwt_identity()
        if user_id:
            return self.user_manager.resolve_user_by_id(user_id)

    def _fresh_token(self):
        user = self.get_logged_user()
        if user is not None:
            user_id = self.user_manager.get_id_in_user(user)
            create_access_token(identity=user_id, fresh=True)

    @property
    def is_logged_user(self):
        return self.get_logged_user() is not None

    @property
    def is_logged_admin(self):
        may_user = self.get_logged_user()  # Union[User, None]
        if may_user is None:
            return False
        if may_user.is_admin is not True:
            return False
        return True

    def user_optional(self, f):
        @wraps(f)
        def func(*args, **kwargs):
            if self.is_logged_user is True:
                self._fresh_token()
            return f(*args, **kwargs)

        return func

    def user_required(self, f):
        @wraps(f)
        def func(*args, **kwargs):
            if self.is_logged_user is False:
                raise UserUnauthorized
            else:
                self._fresh_token()
            return f(*args, **kwargs)

        return func

    def admin_required(self, f):
        @wraps(f)
        def func(*args, **kwargs):
            if self.is_logged_admin is False:
                raise AdminUnauthorized
            else:
                self._fresh_token()
            return f(*args, **kwargs)

        return func
