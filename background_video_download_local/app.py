# -*- coding: UTF-8 -*-
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7881, debug=True, ssl_context=(
        "./rtc-video-room-cert.pem",
        "./rtc-video-room-key.pem"
    ))
