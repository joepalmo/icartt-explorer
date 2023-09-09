from os import environ, path
import pandas as pd
from flask import Flask, request, jsonify, redirect
from requests import get
from werkzeug.utils import secure_filename

from .utils import read_data_ict

IS_DEV = environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER_HOST = "http://127.0.0.1:3000"
UPLOAD_FOLDER = path.abspath(path.dirname(__file__)) + '/Downloads/'
ALLOWED_EXTENSIONS = set(['ict'])

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)


def proxy(host, path):
    response = get(f"{host}{path}")
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return (response.content, response.status_code, headers)


@app.route("/")
def getRoot():
    return "Welcome!"

@app.route("/app/", defaults={"path": "index.html"})

@app.route("/app/<path:path>")
def getApp(path):
    if IS_DEV:
        return proxy(WEBPACK_DEV_SERVER_HOST, request.path)
    return app.send_static_file(path)

@app.route("/app/upload", methods=["GET", "POST"])
def fileUpload():
    if request.method == 'POST':
        file = request.files.getlist('file')
        for f in file:
            filename = secure_filename(f.filename)
            if allowedFile(filename):
                csv_filename = 'data.csv'
                df = read_data_ict(f, delim_whitespace=True)
                # f.save(path.join(UPLOAD_FOLDER, csv_filename))
                df.to_csv(path.join(UPLOAD_FOLDER, csv_filename))
                return redirect('/app/')
            else:
                return jsonify({'message': 'File type not allowed'}), 400
        return jsonify({"name": filename, "status": "success"})
    else:
        return jsonify({"status": "failed"})