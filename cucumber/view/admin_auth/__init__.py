from flask import Blueprint

admin_auth = Blueprint('admin_auth', __name__)

from . import views
