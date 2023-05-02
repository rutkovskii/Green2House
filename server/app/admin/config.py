import os
from dotenv import load_dotenv

load_dotenv()


class AdminConfig:
    ADMIN_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.dirname(ADMIN_DIR)
    FLASK_CONTENT_DIR = os.path.join(ROOT_DIR, "flask_content")
    FLASK_HTML_DIR = os.path.join(FLASK_CONTENT_DIR, "html")
    FLASK_STATIC_DIR = os.path.join(FLASK_CONTENT_DIR, "static")
    FLASK_CSS_DIR = os.path.join(FLASK_STATIC_DIR, "css")

    # Routes
    HOME_PAGE_ROUTE = "/"
    ADMIN_PAGE_ROUTE = "/admin"
    ADMIN_PAGE_USERS_ROUTE = "/admin/all-users"
    ADMIN_PAGE_SERVE_USERS_ROUTE = "/api/serve-users"
    GET_DATA_ROUTE = "/get-data"
    ADMIN_DATA_SAMPLES_ROUTE = "/admin/all-data-records"

    # Secrets
    ADMINS = [os.getenv("ADMIN1"), os.getenv("ADMIN2")]
    SECRET_KEY = os.getenv("SECRET_KEY")
