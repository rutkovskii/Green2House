#from config import Config

from flask import Flask
from flask_bootstrap import Bootstrap
import os

from app.admin.admin_page import admin_page_bp
from app.datasample_page import datasample_page_bp
from app.get_data import get_data_bp
from app.admin.config import FLASK_HTML_DIR

app = Flask(__name__, template_folder=os.path.abspath(FLASK_HTML_DIR))
app.register_blueprint(admin_page_bp)
app.register_blueprint(datasample_page_bp)
app.register_blueprint(get_data_bp)
bootstrap = Bootstrap(app)


@app.route('/')
def hello():
    mes = """
        <a href="/all_data_samples">All Data Samples</a>\n
        <a href="/admin/all_users">All Users</a>
    """
    return mes

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

    # To run with ngrok
    #  `ngrok http 80` and then start `sudo python3 flaskMain.py`
    # app.run(port=80)  # host='0.0.0.0', port=80, debug=False, threaded=True








