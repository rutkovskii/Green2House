# from config import Config

from flask import Flask
from flask_bootstrap import Bootstrap
import os

from app.admin.config import ServerConfig

from app.user.env_page import env_page_bp
from app.user.current_env_data_page import current_env_data_page_bp

from app.user.datasample_page import datasample_page_bp
from app.user.get_data import get_data_bp
from app.user.home_page import home_page_bp
from app.admin.views import admin_bp
from app.auth.auth import auth_bp, login_manager
from app.index import index_bp


# Secret Key
bootstrap = Bootstrap()


def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(datasample_page_bp)
    app.register_blueprint(get_data_bp)
    app.register_blueprint(home_page_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(env_page_bp)
    app.register_blueprint(current_env_data_page_bp)


def add_configs(app):
    app.config["SECRET_KEY"] = ServerConfig.SECRET_KEY
    return app


def create_app():
    FlaskApp = Flask(
        __name__,
        template_folder=os.path.abspath(ServerConfig.FLASK_HTML_DIR),
        static_folder=os.path.abspath(ServerConfig.FLASK_STATIC_DIR),
    )
    FlaskApp = add_configs(FlaskApp)
    bootstrap.init_app(FlaskApp)
    login_manager.init_app(FlaskApp)
    login_manager.login_view = "auth_bp.signin"
    return FlaskApp


if ServerConfig.ENVIRONMENT == "development":
    FlaskApp = create_app()
    register_blueprints(FlaskApp)
