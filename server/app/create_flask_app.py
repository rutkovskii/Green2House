# from config import Config

from flask import Flask
from flask_bootstrap import Bootstrap
import os

from app.admin.config import AdminConfig

from app.user.env_page import env_page_bp
from app.user.current_env_data_page import current_env_data_page_bp

from app.user.datasample_page import datasample_page_bp
from app.user.get_data import get_data_bp
from app.user.home_page import home_page_bp
from app.admin.views import admin_bp
from app.auth.auth import auth_bp, login_manager
from app.index import index_bp
from app.user.charts import charts_page_bp
from app.admin.charts import admin_charts_page_bp

from app.server_logger import setup_logger
from config import Config

logger = setup_logger(__name__, "server.log")
logger.info("Logger Created")


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
    app.register_blueprint(charts_page_bp)
    app.register_blueprint(admin_charts_page_bp)


def add_configs(app):
    app.config["SECRET_KEY"] = AdminConfig.SECRET_KEY
    return app


def create_app():
    logger.info(AdminConfig.FLASK_HTML_DIR)
    FlaskApp = Flask(
        __name__,
        template_folder=os.path.abspath(AdminConfig.FLASK_HTML_DIR),
        static_folder=os.path.abspath(AdminConfig.FLASK_STATIC_DIR),
    )
    FlaskApp = add_configs(FlaskApp)
    bootstrap.init_app(FlaskApp)
    login_manager.init_app(FlaskApp)
    login_manager.login_view = "auth_bp.signin"
    logger.info("Flask App Created")
    return FlaskApp


if Config.ENVIRONMENT == "development":
    FlaskApp = create_app()
    register_blueprints(FlaskApp)
    logger.info("Flask App Created in Development Mode")
