import os
from datetime import datetime
from flask import Flask, request, abort, jsonify
from werkzeug.contrib.fixers import ProxyFix

from training.results import Results
from test_cases import TestCases

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)

flask_debug = os.environ.get("FLASK_DEBUG", False)

app.config.update({"DEBUG": bool(flask_debug)})

mongo_ip = os.getenv('MONGO_IP', 'localhost')
mongo_port = os.getenv('MONGO_PORT', '27017')
mongo_user = os.getenv('MONGO_USER', 'root')
mongo_password = os.getenv('MONGO_PASSWORD', 'example')

t = TestCases(
    ip=mongo_ip,
    port=mongo_port,
    user=mongo_user,
    password=mongo_password
)
r = Results(
    ip=mongo_ip,
    port=mongo_port,
    user=mongo_user,
    password=mongo_password
)
t.load()
r.load()


@app.route("/")
def index():
    a = datetime.now()
    return "Hello, World from PyPy 3, Gunicorn and Gevent! {}".format(a.strftime("%Y-%m-%d %H:%M:%S.%f"))


@app.route("/test_cases", methods=['POST', 'GET'])
def test_cases():
    if request.method == 'POST':
        if request.json is not None:
            t.add(request.json)
            return jsonify({'status': 'added'}), 401
        else:
            return jsonify({'status': 'empty json'}), 200
    elif request.method == 'GET':
        return jsonify({'test_cases': t.get_all()}), 200
    else:
        abort(400)


@app.route("/results", methods=['GET'])
def results():
    if request.method == 'GET':
        return jsonify({'results': r.get_all()}), 200
    else:
        abort(400)


@app.route("/last_result", methods=['GET'])
def last_result():
    if request.method == 'GET':
        return jsonify({'result': r.get_last()}), 200
    else:
        abort(400)


# Following code is executed when running the server directly, for development
if __name__ == "__main__":
    # NB: for the server port, read an environmental variable called "SERVER_PORT", or use a default value
    SERVER_PORT = os.environ.get("SERVER_PORT", "8000")
    app.run(host="", port=int(SERVER_PORT))
