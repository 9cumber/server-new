from flask import Flask
from flask_migrate import Migrate
from config import config
from app.amazon import AmazonSearch
from app.flaskconfig import MyFlaskConfig
from app.models import db
from app.login_manager import LoginManager
from flask_jwt_extended import JWTManager

amazon = AmazonSearch()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)

    # admin authenticator
    from .admin_auth import admin_auth as admin_auth_blueprint
    app.register_blueprint(admin_auth_blueprint, url_prefix='/admin/auth')

    app.config = MyFlaskConfig(app.config)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.models import db

    db.init_app(app)
    migrate.init_app(app, db)

    amazon.init_app(app)
    jwt.init_app(app)

    login_manager.init_app(app)

    return app
