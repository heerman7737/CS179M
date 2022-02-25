from flask import Flask, request, make_response, jsonify, redirect, url_for

app = Flask(__name__)


@app.after_request
def after(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return resp


@app.route('/')
def index():
    return make_response()


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        return redirect(url_for('uploadManifest'))


# return "hello"


@app.route('/uploadManifest', methods=["GET", "POST"])
def uploadManifest():
    return "hello"


# @app.route('/operate', methods=["GET", "POST"])
# def operateCrane():


if __name__ == '__main__':
    app.run()
