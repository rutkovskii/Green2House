# from config import Config

from flask import Flask
from flask_bootstrap import Bootstrap
import os

from app.user.datasample_page import datasample_page_bp
from app.user.get_data import get_data_bp
from app.user.home_page import home_page_bp
from app.admin.admin_page import admin_page_bp
from app.admin.config import SERVER_CONFIG

app = Flask(__name__, template_folder=os.path.abspath(
    SERVER_CONFIG.FLASK_HTML_DIR))
app.register_blueprint(admin_page_bp)
app.register_blueprint(datasample_page_bp)
app.register_blueprint(get_data_bp)
app.register_blueprint(home_page_bp)
bootstrap = Bootstrap(app)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80, debug=True) # host='0.0.0.0', port=80, debug=False, threaded=True
    # app.run(host="0.0.0.0", port=80
    app.run(port=80, debug=True)

    # To run with ngrok
    # `ngrok http 80` and then start `sudo python3 flaskMain.py`
    # app.run(port=80)  # host='0.0.0.0', port=80, debug=False, threaded=True
