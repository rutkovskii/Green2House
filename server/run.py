from app.create_flask_app import FlaskApp
from flask import url_for

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80, debug=True) # host='0.0.0.0', port=80, debug=False, threaded=True
    # app.run(host="0.0.0.0", port=80
    FlaskApp.run(host="0.0.0.0", port=80, debug=True)

    # To run with ngrok
    # `ngrok http 80` and then start `sudo python3 flaskMain.py`
    # app.run(port=80)  # host='0.0.0.0', port=80, debug=False, threaded=True
