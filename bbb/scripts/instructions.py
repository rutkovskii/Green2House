from flask import Flask, request
import json


app = Flask(__name__)


@app.route('/instructions', methods=['POST'])
def instructions():
    if request.method == 'POST':
        body = json.loads(request.get_json())
        print(body)

        return {"message": "JSON received"}, 200

    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
